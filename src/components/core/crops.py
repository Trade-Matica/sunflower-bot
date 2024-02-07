class Crops:
    def __init__(
        self,
        name: str,
        sellPrice: float,
        bumpkinLevel: int,
        harvestSeconds: int,
    ):
        self.name = name
        self.sellPrice = sellPrice
        self.bumpkinLevel = bumpkinLevel
        self.harvestSeconds = harvestSeconds


class CropsSeed:
    def __init__(
        self,
        name: str,
        tokenAmount: float,
        bumpkinLevel: int,
    ):
        self.name = name
        self.tokenAmount = tokenAmount
        self.bumpkinLevel = bumpkinLevel


__crops__: dict[Crops] = {
    "Sunflower": Crops(
        name="Sunflower",
        sellPrice=0.02,
        bumpkinLevel=1,
        harvestSeconds=1 * 60,
    ),
    "Potato": Crops(
        name="Potato",
        sellPrice=0.14,
        bumpkinLevel=1,
        harvestSeconds=5 * 60,
    ),
    "Pumpkin": Crops(
        name="Pumpkin",
        sellPrice=0.4,
        bumpkinLevel=3,
        harvestSeconds=30 * 60,
    ),
    "Carrot": Crops(
        name="Carrot",
        sellPrice=0.8,
        bumpkinLevel=3,
        harvestSeconds=60 * 60,
    ),
    "Cabbage": Crops(
        name="Cabbage",
        sellPrice=1.5,
        bumpkinLevel=3,
        harvestSeconds=2 * 60 * 60,
    ),
    "Beetroot": Crops(
        name="Beetroot",
        sellPrice=2.8,
        bumpkinLevel=3,
        harvestSeconds=4 * 60 * 60,
    ),
    "Cauliflower": Crops(
        name="Cauliflower",
        sellPrice=4.25,
        bumpkinLevel=4,
        harvestSeconds=8 * 60 * 60,
    ),
    "Parsnip": Crops(
        name="Parsnip",
        sellPrice=6.5,
        bumpkinLevel=4,
        harvestSeconds=12 * 60 * 60,
    ),
    "Eggplant": Crops(
        name="Eggplant",
        sellPrice=8,
        bumpkinLevel=5,
        harvestSeconds=16 * 60 * 60,
    ),
    "Corn": Crops(
        name="Corn",
        sellPrice=9,
        bumpkinLevel=5,
        harvestSeconds=20 * 60 * 60,
    ),
    "Radish": Crops(
        name="Radish",
        sellPrice=9.5,
        bumpkinLevel=5,
        harvestSeconds=24 * 60 * 60,
    ),
    "Wheat": Crops(
        name="Wheat",
        sellPrice=7,
        bumpkinLevel=5,
        harvestSeconds=24 * 60 * 60,
    ),
    "Kale": Crops(
        name="Kale",
        sellPrice=10,
        bumpkinLevel=7,
        harvestSeconds=36 * 60 * 60,
    ),
}

__crops_seed__: dict[CropsSeed] = {
    "Sunflower Seed": CropsSeed(
        name="Sunflower Seed",
        tokenAmount=0.01,
        bumpkinLevel=1,
    ),
    "Potato Seed": CropsSeed(
        name="Potato Seed",
        tokenAmount=0.1,
        bumpkinLevel=1,
    ),
    "Pumpkin Seed": CropsSeed(
        name="Pumpkin Seed",
        tokenAmount=0.2,
        bumpkinLevel=2,
    ),
    "Carrot Seed": CropsSeed(
        name="Carrot Seed",
        tokenAmount=0.5,
        bumpkinLevel=2,
    ),
    "Cabbage Seed": CropsSeed(
        name="Cabbage Seed",
        tokenAmount=1,
        bumpkinLevel=3,
    ),
    "Beetroot Seed": CropsSeed(
        name="Beetroot Seed",
        tokenAmount=2,
        bumpkinLevel=3,
    ),
    "Cauliflower Seed": CropsSeed(
        name="Cauliflower Seed",
        tokenAmount=3,
        bumpkinLevel=4,
    ),
    "Parsnip Seed": CropsSeed(
        name="Parsnip Seed",
        tokenAmount=5,
        bumpkinLevel=4,
    ),
    "Eggplant Seed": CropsSeed(
        name="Eggplant Seed",
        tokenAmount=6,
        bumpkinLevel=5,
    ),
    "Corn Seed": CropsSeed(
        name="Corn Seed",
        tokenAmount=7,
        bumpkinLevel=5,
    ),
    "Radish Seed": CropsSeed(
        name="Radish Seed",
        tokenAmount=7,
        bumpkinLevel=5,
    ),
    "Wheat Seed": CropsSeed(
        name="Wheat Seed",
        tokenAmount=5,
        bumpkinLevel=5,
    ),
    "Kale Seed": CropsSeed(
        name="Kale Seed",
        tokenAmount=7,
        bumpkinLevel=7,
    ),
}
