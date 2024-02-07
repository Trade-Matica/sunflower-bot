import threading, time
from loguru import logger

from components.utils.config import BotConfig
from components.core.api_wrapper import Rest
from components.core.exceptions import GatherSessionError
from components.core.crops import Crops, CropsSeed, __crops__, __crops_seed__


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

            growSeconds = __crops__.get(body['crop'].get('name')).harvestSeconds
            createdTime = body.get('crop').get('plantedAt') / 1000

            if int(time.time()) >= (growSeconds + createdTime):
                seeds_to_harvest.append(crop)

        if len(seeds_to_plant) != 0:
            (code, plantData) = self.api.plantCrops(seeds_to_plant)

            if code != 200:
                logger.error(f"cannot plant seeds, code: {code} {plantData}")
            else:
                logger.info(
                    f"successfully planted {len(seeds_to_plant)} seeds ({', '.join(x['seedName'] for x in seeds_to_plant)})"
                )
                doneAction = True
        
        if len(seeds_to_harvest) != 0:
            (code, harvestData) = self.api.harvestCrops(seeds_to_harvest)

            if code != 200:
                logger.error(f"cannot harvest seeds, code: {code} {harvestData}")
            else:
                logger.info(
                    f"successfully harvested {len(seeds_to_harvest)} seeds"
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

    @logger.catch
    def run(self):
        while True:
            time.sleep(1)

            try:
                self.clock()
            except Exception as e:
                logger.error(e)
                break
