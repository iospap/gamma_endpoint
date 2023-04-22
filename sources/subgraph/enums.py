from enum import Enum

from common import enums as common_enums


class Chain(common_enums.Chain):
    ARBITRUM = "arbitrum"
    CELO = "celo"
    ETHEREUM = "mainnet"
    MAINNET = "mainnet"
    OPTIMISM = "optimism"
    POLYGON = "polygon"
    BSC = "bsc"


class PositionType(str, Enum):
    BASE = "base"
    LIMIT = "limit"


class Protocol(common_enums.Dex):
    QUICKSWAP = "quickswap"
    UNISWAP = "uniswap"
    ZYBERSWAP = "zyberswap"
    THENA = "thena"


class QueryType(str, Enum):
    DATABASE = "database"
    SUBGRAPH = "subgraph"
