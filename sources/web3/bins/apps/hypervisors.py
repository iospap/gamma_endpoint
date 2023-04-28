from sources.common.general.enums import Chain, Dex, ChainId
import asyncio

# from sources.web3.bins.w3.objects.protocols import gamma_hypervisor_registry
from sources.web3.bins.w3.helpers import (
    build_hypervisor,
    build_hypervisor_anyRpc,
    build_hypervisor_registry,
    build_hypervisor_registry_anyRpc,
)

from sources.web3.bins.w3.objects.protocols import gamma_hypervisor
from sources.web3.bins.w3.objects.exchanges import univ3_pool, algebrav3_pool
from sources.web3.bins.configuration import RPC_URLS, CONFIGURATION
from sources.web3.bins.mixed.price_utilities import price_scraper


def hypervisors_list(network: Chain, dex: Dex):
    # get network registry address
    registry = build_hypervisor_registry_anyRpc(
        network=network, dex=dex, block=0, rpcUrls=RPC_URLS[network.value]
    )

    return registry.get_hypervisors_addresses()


async def hypervisor_uncollected_fees(
    network: Chain, dex: Dex, hypervisor_address: str, block: int = None
):
    hypervisor = await build_hypervisor_anyRpc(
        network=network,
        dex=dex,
        hypervisor_address=hypervisor_address,
        block=block if block else 0,
        rpcUrls=RPC_URLS[network.value],
        test=True,
    )

    # define what to initialize
    await hypervisor.init(
        methods_list=[
            "block",
            "symbol",
            "baseUpper",
            "baseLower",
            "limitUpper",
            "limitLower",
            (
                "pool",
                [
                    "slot0",
                    "globalState",
                    ("token0", ["decimals"]),
                    ("token1", ["decimals"]),
                    "feeGrowthGlobal0X128",
                    "feeGrowthGlobal1X128",
                ],
            ),
        ]
    )

    base, limit = await asyncio.gather(
        hypervisor.pool.get_fees_uncollected(
            ownerAddress=hypervisor.address,
            tickUpper=hypervisor.baseUpper,
            tickLower=hypervisor.baseLower,
            inDecimal=True,
        ),
        hypervisor.pool.get_fees_uncollected(
            ownerAddress=hypervisor.address,
            tickUpper=hypervisor.limitUpper,
            tickLower=hypervisor.limitLower,
            inDecimal=True,
        ),
    )

    totalFees0 = (
        float(base["qtty_token0"])
        + float(base["qtty_token0_owed"])
        + float(limit["qtty_token0"])
        + float(limit["qtty_token0_owed"])
    )
    totalFees1 = (
        float(base["qtty_token1"])
        + float(base["qtty_token1_owed"])
        + float(limit["qtty_token1"])
        + float(limit["qtty_token1_owed"])
    )

    return {
        "block": hypervisor.block,
        "timestamp": hypervisor.timestamp,
        "symbol": hypervisor.symbol,
        "baseFees0": float(base["qtty_token0"]),
        "baseFees1": float(base["qtty_token1"]),
        "baseTokensOwed0": float(base["qtty_token0_owed"]),
        "baseTokensOwed1": float(base["qtty_token1_owed"]),
        "limitFees0": float(limit["qtty_token0"]),
        "limitFees1": float(limit["qtty_token1"]),
        "limitTokensOwed0": float(limit["qtty_token0_owed"]),
        "limitTokensOwed1": float(limit["qtty_token1_owed"]),
        # "baseFees0USD": float(base[0]) * hypervisor.baseTokenPrice,
        # "baseFees1USD": float(base[1]) * hypervisor.quoteTokenPrice,
        # "baseTokensOwed0USD": float(base[2]) * hypervisor.baseTokenPrice,
        # "baseTokensOwed1USD": float(base[3]) * hypervisor.quoteTokenPrice,
        # "limitFees0USD": float(limit[0]) * hypervisor.baseTokenPrice,
        # "limitFees1USD": float(limit[1]) * hypervisor.quoteTokenPrice,
        # "limitTokensOwed0USD": float(limit[2]) * hypervisor.baseTokenPrice,
        # "limitTokensOwed1USD": float(limit[3]) * hypervisor.quoteTokenPrice,
        "totalFees0": totalFees0,
        "totalFees1": totalFees1,
        # "totalFeesUSD": (float(base[0]) + float(limit[0])) * hypervisor.baseTokenPrice + (float(base[1]) + float(limit[1])) * hypervisor.quoteTokenPrice,
    }
