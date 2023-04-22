from enum import Enum


class Chain(str, Enum):
    ARBITRUM = "arbitrum"
    CELO = "celo"
    ETHEREUM = "ethereum"
    OPTIMISM = "optimism"
    POLYGON = "polygon"
    BSC = "binance"


class Dex(str, Enum):
    QUICKSWAP = "quickswap"
    UNISWAP = "uniswap"
    ZYBERSWAP = "zyberswap"
    THENA = "thena"
