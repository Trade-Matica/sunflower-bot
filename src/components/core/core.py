import threading, time
from loguru import logger

from components.utils.config import BotConfig
from components.core.api_wrapper import Rest
from components.core.exceptions import GatherSessionError
from components.core.crops import (
    Crops,
    CropsSeed,
    __crops__,
    __crops_seed__,
)
from components.core.chop import (
    TREE_RECOVERY_TIME,
    STONE_RECOVERY_TIME,
)


class Utils:
    @staticmethod
    def gatherFastestSeed(inventory: dict) -> Crops:
        fastest = None

        for name, _ in inventory.items():
            if name.endswith("Seed"):
                crop = __crops__.get(name.split(" ")[0])

                if crop and (
                    fastest is None or crop.harvestSeconds <= fastest.harvestSeconds
                ):
                    fastest = crop

        return fastest


class Bot(threading.Thread):
    def __init__(self, config: BotConfig) -> None:
        self.api = Rest(
            authorization=config.authorization,
            clientVersion=config.clientVersion,
        )

        threading.Thread.__init__(self)
        logger.info(
            f"Account loaded: {config.clientName}, version: {config.clientVersion}"
        )

        self.madeAction = True

        # warnning messages
        self.noAxeShow = False
        self.noPickaxeShow = False

    @logger.catch
    def farmCrops(self, data: dict) -> bool:
        """Collect and plant seeds

        Returns:
            bool: return True if any action was taken.
        """
        doneAction = False

        crops = data["crops"]
        inventory = data["inventory"]

        # check if crops are planted.
        # if not, put the seeds that grow the faster we have in inventory.
        # if yes, harvest if seeds is grown

        seeds_to_plant = []
        seeds_to_harvest = []
        for crop in crops:
            body = crops[crop]

            if body.get("crop") == None:
                to_plant: Crops = Utils.gatherFastestSeed(inventory)

                if to_plant == None:
                    logger.warning("You don't have any seeds to plant")
                    continue

                seeds_to_plant.append(
                    {
                        "seedName": f"{to_plant.name} Seed",
                        "index": crop,
                    }
                )
                continue

            growSeconds = __crops__.get(body["crop"].get("name")).harvestSeconds
            createdTime = body.get("crop").get("plantedAt") / 1000

            if int(time.time()) >= (growSeconds + createdTime):
                seeds_to_harvest.append(crop)

        if len(seeds_to_plant) != 0:
            (code, plantData) = self.api.plantCrops(seeds_to_plant)

            if code != 200:
                logger.error(f"cannot plant seeds, code: {code} {plantData}")
            else:
                seed_counts = {}
                for seed in seeds_to_plant:
                    seed_name = seed["seedName"]
                    seed_counts[seed_name] = seed_counts.get(seed_name, 0) + 1

                logger.info(
                    f"successfully planted {len(seeds_to_plant)} seeds ({', '.join(f'{count} {seed}' for seed, count in seed_counts.items())})"
                )
                doneAction = True

        if len(seeds_to_harvest) != 0:
            (code, harvestData) = self.api.harvestCrops(seeds_to_harvest)

            if code != 200:
                logger.error(f"cannot harvest seeds, code: {code} {harvestData}")
            else:
                logger.info(f"successfully harvested {len(seeds_to_harvest)} seeds")
                doneAction = True

        return doneAction

    @logger.catch
    def chopTimber(self, data: dict) -> bool:
        """Cut trees & collect wood

        Returns:
            bool: return True if any action was taken.
        """
        doneAction = False

        trees = data["trees"]
        inventory = data["inventory"]
        skills = data["bumpkin"]["skills"]

        if "Axe" not in inventory:
            if not self.noAxeShow:
                logger.warning(f"no axes left, skiping")
                self.noAxeShow = True
            return doneAction

        self.noAxeShow = False

        AxeCount = int(inventory["Axe"])
        BaseAxeCount = AxeCount

        # https://github.com/sunflower-land/sunflower-land/blob/e446fe488091ce40fe9dc731c5b30e86644a0673/src/features/game/events/landExpansion/chop.ts#L44
        """
        buff = TREE_RECOVERY_TIME

        if "Tree Hugger" in skills:
            buff -= buff * 0.8

        if "Time Warp Totem" in data["collectibles"]:
            buff -= buff * 0.5

        growSeconds = TREE_RECOVERY_TIME - buff
        """

        growSeconds = TREE_RECOVERY_TIME

        trees_to_cut = []
        for tree in trees:
            if AxeCount <= 0:
                logger.warning(f"no axes left, cutting {len(trees_to_cut)} trees")
                break

            body = trees[tree]
            choppedAt = body.get("wood").get("choppedAt") / 1000

            if int(time.time()) >= (growSeconds + choppedAt):
                trees_to_cut.append(tree)
                AxeCount -= 1

        if len(trees_to_cut) != 0:
            (code, chopData) = self.api.chopTimber(trees_to_cut)

            if code != 200:
                logger.error(f"cannot chop timbers, code: {code} {chopData}")
            else:
                logger.info(
                    f"successfully chopped {len(trees_to_cut)} timbers, {BaseAxeCount-len(trees_to_cut)} Axe(x) left"
                )
                doneAction = True

        return doneAction

    @logger.catch
    def mineStones(self, data: dict) -> bool:
        """Mine stones

        Returns:
            bool: return True if any action was taken.
        """
        doneAction = False

        stones = data["stones"]
        inventory = data["inventory"]
        skills = data["bumpkin"]["skills"]

        if "Pickaxe" not in inventory:
            if not self.noPickaxeShow:
                logger.warning(f"no pickaxe left, skiping")
                self.noPickaxeShow = True
            return doneAction

        self.noPickaxeShow = False

        PickaxeCount = int(inventory["Pickaxe"])
        BasePickaxeCount = PickaxeCount

        # https://github.com/sunflower-land/sunflower-land/blob/e446fe488091ce40fe9dc731c5b30e86644a0673/src/features/game/events/landExpansion/chop.ts#L44
        """
        buff = STONE_RECOVERY_TIME

        if "Coal Face" in skills:
            buff = buff * 0.2 * 1000

        if "Time Warp Totem" in data["collectibles"]:
            buff = buff * 0.5 * 1000

        growSeconds = STONE_RECOVERY_TIME - buff
        """
        
        growSeconds = STONE_RECOVERY_TIME

        stones_to_mine = []
        for stone in stones:
            if PickaxeCount <= 0:
                logger.warning(f"no pickaxe left, mining {len(stones_to_mine)} stones")
                break

            body = stones[stone]
            minedAt = body.get("stone").get("minedAt") / 1000

            if int(time.time()) >= (growSeconds + minedAt):
                stones_to_mine.append(stone)
                PickaxeCount -= 1

        if len(stones_to_mine) != 0:
            (code, mineData) = self.api.mineStone(stones_to_mine)

            if code != 200:
                logger.error(f"cannot mine stones, code: {code} {mineData}")
            else:
                logger.info(
                    f"successfully mined {len(stones_to_mine)} stones, {BasePickaxeCount-len(stones_to_mine)} Pickaxe(x) left"
                )
                doneAction = True

        return doneAction

    def clock(self):
        (status, farm) = self.api.getSession()
        if status != 200:
            raise GatherSessionError

        if self.madeAction:
            activity = farm["bumpkin"]["activity"]
            logger.info(
                f"SFL Earned: {activity['SFL Earned']}, SFL Spent: {activity['SFL Spent']}"
            )

        self.madeAction = False

        if self.farmCrops(data=farm):
            self.madeAction = True

        if self.chopTimber(data=farm):
            self.madeAction = True

        if self.mineStones(data=farm):
            self.madeAction = True

    @logger.catch
    def run(self):
        while True:
            time.sleep(1)

            try:
                self.clock()
            except Exception as e:
                logger.error(e)
                break
