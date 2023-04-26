from sources.common.general.enums import Chain, Dex, ChainId
import asyncio

# from sources.web3.bins.w3.objects.protocols import gamma_hypervisor_registry
from sources.web3.bins.w3.helpers import (
    build_hypervisor,
    build_hypervisor_anyRpc,
    build_hypervisor_registry,
    build_hypervisor_registry_anyRpc,
)

from sources.web3.bins.configuration import RPC_URLS, CONFIGURATION
from sources.web3.bins.mixed.price_utilities import price_scraper


def hypervisors_list(network: Chain, dex: Dex):
    # get network registry address
    registry = build_hypervisor_registry_anyRpc(
        network=network, dex=dex, block=0, rpcUrls=RPC_URLS[network.value]
    )

    return registry.get_hypervisors_addresses()


def hypervisor_uncollected_fees(network: Chain, dex: Dex, hypervisor_address: str):
    hypervisor = build_hypervisor_anyRpc(
        network=network,
        dex=dex,
        hypervisor_address=hypervisor_address,
        block=0,
        rpcUrls=RPC_URLS[network.value],
    )

    base = hypervisor.pool.get_fees_uncollected(
        ownerAddress=hypervisor.address,
        tickUpper=hypervisor.baseUpper,
        tickLower=hypervisor.baseLower,
        inDecimal=True,
    )
    limit = hypervisor.pool.get_fees_uncollected(
        ownerAddress=hypervisor.address,
        tickUpper=hypervisor.limitUpper,
        tickLower=hypervisor.limitLower,
        inDecimal=True,
    )

    return {
        "symbol": hypervisor.symbol,
        "baseFees0": float(base[0]),
        "baseFees1": float(base[1]),
        "baseTokensOwed0": float(base[2]),
        "baseTokensOwed1": float(base[3]),
        "limitFees0": float(limit[0]),
        "limitFees1": float(limit[1]),
        "limitTokensOwed0": float(limit[2]),
        "limitTokensOwed1": float(limit[3]),
        # "baseFees0USD": float(base[0]) * hypervisor.baseTokenPrice,
        # "baseFees1USD": float(base[1]) * hypervisor.quoteTokenPrice,
        # "baseTokensOwed0USD": float(base[2]) * hypervisor.baseTokenPrice,
        # "baseTokensOwed1USD": float(base[3]) * hypervisor.quoteTokenPrice,
        # "limitFees0USD": float(limit[0]) * hypervisor.baseTokenPrice,
        # "limitFees1USD": float(limit[1]) * hypervisor.quoteTokenPrice,
        # "limitTokensOwed0USD": float(limit[2]) * hypervisor.baseTokenPrice,
        # "limitTokensOwed1USD": float(limit[3]) * hypervisor.quoteTokenPrice,
        "totalFees0": float(base[0]) + float(limit[0]),
        "totalFees1": float(base[1]) + limit[1],
        # "totalFeesUSD": (float(base[0]) + float(limit[0])) * hypervisor.baseTokenPrice + (float(base[1]) + float(limit[1])) * hypervisor.quoteTokenPrice,
    }


async def hypervisor_uncollected_fees(
    network: Chain, dex: Dex, hypervisor_address: str
):
    hypervisor = build_hypervisor_anyRpc(
        network=network,
        dex=dex,
        hypervisor_address=hypervisor_address,
        block=0,
        rpcUrls=RPC_URLS[network.value],
    )

    base, limit = asyncio.gather(
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

    return {
        "symbol": hypervisor.symbol,
        "baseFees0": float(base[0]),
        "baseFees1": float(base[1]),
        "baseTokensOwed0": float(base[2]),
        "baseTokensOwed1": float(base[3]),
        "limitFees0": float(limit[0]),
        "limitFees1": float(limit[1]),
        "limitTokensOwed0": float(limit[2]),
        "limitTokensOwed1": float(limit[3]),
        # "baseFees0USD": float(base[0]) * hypervisor.baseTokenPrice,
        # "baseFees1USD": float(base[1]) * hypervisor.quoteTokenPrice,
        # "baseTokensOwed0USD": float(base[2]) * hypervisor.baseTokenPrice,
        # "baseTokensOwed1USD": float(base[3]) * hypervisor.quoteTokenPrice,
        # "limitFees0USD": float(limit[0]) * hypervisor.baseTokenPrice,
        # "limitFees1USD": float(limit[1]) * hypervisor.quoteTokenPrice,
        # "limitTokensOwed0USD": float(limit[2]) * hypervisor.baseTokenPrice,
        # "limitTokensOwed1USD": float(limit[3]) * hypervisor.quoteTokenPrice,
        "totalFees0": float(base[0]) + float(limit[0]),
        "totalFees1": float(base[1]) + limit[1],
        # "totalFeesUSD": (float(base[0]) + float(limit[0])) * hypervisor.baseTokenPrice + (float(base[1]) + float(limit[1])) * hypervisor.quoteTokenPrice,
    }
