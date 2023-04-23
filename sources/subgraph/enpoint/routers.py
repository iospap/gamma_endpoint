import asyncio
from fastapi import Response, APIRouter
from endpoint.routers.template import (
    endpoint_builder_template,
    endpoint_builder_baseTemplate,
)
from sources.subgraph.bins.common import hypervisor, analytics, aggregate_stats
from sources.subgraph.bins.simulator import SimulatorInfo
from sources.subgraph.bins.config import DEPLOYMENTS, RUN_FIRST_QUERY_TYPE
from sources.subgraph.bins.enums import Chain, Protocol, QueryType


RUN_FIRST = RUN_FIRST_QUERY_TYPE


def build_routes() -> list:
    routes = []

    # setup dex + chain endpoints
    routes.append(
        subgraph_endpoint(
            dex=Protocol.UNISWAP,
            chain=Chain.MAINNET,
            tags=["Uniswap - Ethereum"],
            prefix=f"/{Protocol.UNISWAP.value}/{Chain.MAINNET.value}",
        )
    )
    routes.append(
        subgraph_endpoint(
            dex=Protocol.UNISWAP,
            chain=Chain.POLYGON,
            tags=["Uniswap - Polygon"],
            prefix=f"/{Protocol.UNISWAP.value}/{Chain.POLYGON.value}",
        )
    )
    routes.append(
        subgraph_endpoint(
            dex=Protocol.UNISWAP,
            chain=Chain.ARBITRUM,
            tags=["Uniswap - Arbitrum"],
            prefix=f"/{Protocol.UNISWAP.value}/{Chain.ARBITRUM.value}",
        )
    )
    routes.append(
        subgraph_endpoint(
            dex=Protocol.UNISWAP,
            chain=Chain.OPTIMISM,
            tags=["Uniswap - Optimism"],
            prefix=f"/{Protocol.UNISWAP.value}/{Chain.OPTIMISM.value}",
        )
    )
    routes.append(
        subgraph_endpoint(
            dex=Protocol.UNISWAP,
            chain=Chain.CELO,
            tags=["Uniswap - Celo"],
            prefix=f"/{Protocol.UNISWAP.value}/{Chain.CELO.value}",
        )
    )
    routes.append(
        subgraph_endpoint(
            dex=Protocol.UNISWAP,
            chain=Chain.BSC,
            tags=["Uniswap - Binance"],
            prefix=f"/{Protocol.UNISWAP.value}/{Chain.BSC.value}",
        )
    )
    routes.append(
        subgraph_endpoint(
            dex=Protocol.QUICKSWAP,
            chain=Chain.POLYGON,
            tags=["Quickswap - Polygon"],
            prefix=f"/{Protocol.QUICKSWAP.value}/{Chain.POLYGON.value}",
        )
    )
    routes.append(
        subgraph_endpoint(
            dex=Protocol.ZYBERSWAP,
            chain=Chain.ARBITRUM,
            tags=["Zyberswap - Arbitrum"],
            prefix=f"/{Protocol.ZYBERSWAP.value}/{Chain.ARBITRUM.value}",
        )
    )
    routes.append(
        subgraph_endpoint(
            dex=Protocol.THENA,
            chain=Chain.BSC,
            tags=["Thena - BSC"],
            prefix=f"/{Protocol.THENA.value}/{Chain.BSC.value}",
        )
    )

    return routes


def build_routes_compatible() -> list:
    """Build backwards compatible routes for the old endpoint

    Returns:
        list: _description_
    """
    routes = []

    # setup dex + chain endpoints
    routes.append(
        subgraph_endpoint(
            dex=Protocol.UNISWAP,
            chain=Chain.MAINNET,
            tags=["Mainnet"],
        )
    )
    routes.append(
        subgraph_endpoint(
            dex=Protocol.UNISWAP,
            chain=Chain.POLYGON,
            tags=["Polygon"],
            prefix=f"/{Chain.POLYGON.value}",
        )
    )
    routes.append(
        subgraph_endpoint(
            dex=Protocol.UNISWAP,
            chain=Chain.ARBITRUM,
            tags=["Arbitrum"],
            prefix=f"/{Chain.ARBITRUM.value}",
        )
    )
    routes.append(
        subgraph_endpoint(
            dex=Protocol.UNISWAP,
            chain=Chain.OPTIMISM,
            tags=["Optimism"],
            prefix=f"/{Chain.OPTIMISM.value}",
        )
    )
    routes.append(
        subgraph_endpoint(
            dex=Protocol.UNISWAP,
            chain=Chain.CELO,
            tags=["Celo"],
            prefix=f"/{Chain.CELO.value}",
        )
    )
    routes.append(
        subgraph_endpoint(
            dex=Protocol.UNISWAP,
            chain=Chain.BSC,
            tags=["BSC"],
            prefix=f"/{Chain.BSC.value}",
        )
    )
    routes.append(
        subgraph_endpoint(
            dex=Protocol.QUICKSWAP,
            chain=Chain.POLYGON,
            tags=["Quickswap - Polygon"],
            prefix=f"/{Protocol.QUICKSWAP.value}/{Chain.POLYGON.value}",
        )
    )
    routes.append(
        subgraph_endpoint(
            dex=Protocol.ZYBERSWAP,
            chain=Chain.ARBITRUM,
            tags=["Zyberswap - Arbitrum"],
            prefix=f"/{Protocol.ZYBERSWAP.value}/{Chain.ARBITRUM.value}",
        )
    )
    routes.append(
        subgraph_endpoint(
            dex=Protocol.THENA,
            chain=Chain.BSC,
            tags=["Thena - BSC"],
            prefix=f"/{Protocol.THENA.value}/{Chain.BSC.value}",
        )
    )

    return routes


class subgraph_endpoint(endpoint_builder_template):
    # EXECUTION FUNCTIONS

    async def hypervisor_basic_stats(self, hypervisor_address: str, response: Response):
        return await hypervisor.hypervisor_basic_stats(
            self.dex, self.chain, hypervisor_address, response
        )

    async def hypervisor_returns(self, hypervisor_address: str, response: Response):
        hypervisor_returns = hypervisor.HypervisorsReturnsAllPeriods(
            protocol=self.dex,
            chain=self.chain,
            hypervisors=[hypervisor_address],
            response=response,
        )
        return await hypervisor_returns.run(RUN_FIRST)

    async def hypervisor_average_returns(
        self, hypervisor_address: str, response: Response
    ):
        return await hypervisor.hypervisor_average_return(
            protocol=self.dex,
            chain=self.chain,
            hypervisor_address=hypervisor_address,
            response=response,
        )

    async def hypervisor_uncollected_fees(
        self, hypervisor_address: str, response: Response
    ):
        return await hypervisor.uncollected_fees(
            protocol=self.dex,
            chain=self.chain,
            hypervisor_address=hypervisor_address,
            response=response,
        )

    #    hypervisor analytics
    async def hypervisor_analytics_basic_daily(
        self, hypervisor_address: str, response: Response
    ):
        return await analytics.get_hype_data(
            chain=self.chain, hypervisor_address=hypervisor_address, period=1
        )

    async def hypervisor_analytics_basic_monthly(
        self, hypervisor_address: str, response: Response
    ):
        return await analytics.get_hype_data(
            chain=self.chain, hypervisor_address=hypervisor_address, period=30
        )

    async def hypervisors_returns(self, response: Response):
        hypervisor_returns = hypervisor.HypervisorsReturnsAllPeriods(
            protocol=self.dex, chain=self.chain, hypervisors=None, response=response
        )
        return await hypervisor_returns.run(RUN_FIRST)

    async def hypervisors_average_returns(self, response: Response):
        return await hypervisor.hypervisors_average_return(
            protocol=self.dex, chain=self.chain, response=response
        )

    async def hypervisors_all_data(self, response: Response):
        all_data = hypervisor.AllData(
            protocol=self.dex, chain=self.chain, response=response
        )
        return await all_data.run(RUN_FIRST)

    async def hypervisors_uncollected_fees(
        self,
        response: Response,
    ):
        return await hypervisor.uncollected_fees_all(
            protocol=self.dex,
            chain=self.chain,
        )

    async def hypervisors_collected_fees(
        self,
        response: Response,
        start_timestamp: int | None = None,
        end_timestamp: int | None = None,
        start_block: int | None = None,
        end_block: int | None = None,
    ):
        return await hypervisor.collected_fees(
            protocol=self.dex,
            chain=self.chain,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            start_block=start_block,
            end_block=end_block,
        )

    async def hypervisors_feeReturns_daily(self, response: Response):
        fee_returns = hypervisor.FeeReturns(
            protocol=self.dex, chain=self.chain, days=1, response=response
        )
        return await fee_returns.run(RUN_FIRST)

    async def hypervisors_feeReturns_weekly(self, response: Response):
        fee_returns = hypervisor.FeeReturns(
            protocol=self.dex, chain=self.chain, days=7, response=response
        )
        return await fee_returns.run(RUN_FIRST)

    async def hypervisors_feeReturns_monthly(self, response: Response):
        fee_returns = hypervisor.FeeReturns(
            protocol=self.dex, chain=self.chain, days=30, response=response
        )
        return await fee_returns.run(RUN_FIRST)

    async def hypervisors_impermanentDivergence_daily(self, response: Response):
        impermanent = hypervisor.ImpermanentDivergence(
            protocol=self.dex, chain=self.chain, days=1, response=response
        )
        return await impermanent.run(first=RUN_FIRST)

    async def hypervisors_impermanentDivergence_weekly(self, response: Response):
        impermanent = hypervisor.ImpermanentDivergence(
            protocol=self.dex, chain=self.chain, days=7, response=response
        )
        return await impermanent.run(first=RUN_FIRST)

    async def hypervisors_impermanentDivergence_monthly(self, response: Response):
        impermanent = hypervisor.ImpermanentDivergence(
            protocol=self.dex, chain=self.chain, days=30, response=response
        )
        return await impermanent.run(first=RUN_FIRST)


class subgraph_allDeployments(endpoint_builder_baseTemplate):
    # ROUTEs BUILD FUNCTIONS
    def router(self) -> APIRouter:
        router = APIRouter(prefix=self.prefix)

        # ROOT
        router.add_api_route(
            path="/hypervisors/aggregateStats",
            endpoint=self.aggregate_stats,
            methods=["GET"],
        )

        return router

    async def aggregate_stats(
        self,
        response: Response,
    ) -> aggregate_stats.AggregateStatsDeploymentInfoOutput:
        results = await asyncio.gather(
            *[
                aggregate_stats.AggregateStats(
                    deployment[0], deployment[1], response
                ).run(RUN_FIRST)
                for deployment in DEPLOYMENTS
            ],
            return_exceptions=True,
        )

        valid_results = []
        included_deployments = []
        for index, result in enumerate(results):
            if not isinstance(result, Exception):
                valid_results.append(result)
                included_deployments.append(
                    f"{DEPLOYMENTS[index][0]}-{DEPLOYMENTS[index][1]}"
                )

        aggregated_results = sum(valid_results[1:], valid_results[0])

        return aggregate_stats.AggregateStatsDeploymentInfoOutput(
            totalValueLockedUSD=aggregated_results.totalValueLockedUSD,
            pairCount=aggregated_results.pairCount,
            totalFeesClaimedUSD=aggregated_results.totalFeesClaimedUSD,
            deployments=included_deployments,
        )


class router_builder_Simulator(endpoint_builder_baseTemplate):
    # ROUTEs BUILD FUNCTIONS
    def router(self) -> APIRouter:
        router = APIRouter(prefix=self.prefix)

        #
        router.add_api_route(
            path="/tokenList",
            endpoint=self.token_list,
            methods=["GET"],
        )
        router.add_api_route(
            path="/poolTicks",
            endpoint=self.pool_ticks,
            methods=["GET"],
        )
        router.add_api_route(
            path="/poolFromTokens",
            endpoint=self.pool_from_tokens,
            methods=["GET"],
        )
        router.add_api_route(
            path="/pool24HrVolume",
            endpoint=self.pool_24hr_volume,
            methods=["GET"],
        )
        return router

    async def token_list(self):
        tokens = await SimulatorInfo(Protocol.UNISWAP, Chain.MAINNET).token_list()

        return tokens

    async def pool_ticks(self, poolAddress: str):
        ticks = await SimulatorInfo(Protocol.UNISWAP, Chain.MAINNET).pool_ticks(
            poolAddress
        )

        return ticks

    async def pool_from_tokens(self, token0: str, token1: str):
        pools = await SimulatorInfo(Protocol.UNISWAP, Chain.MAINNET).pools_from_tokens(
            token0, token1
        )

        return pools

    async def pool_24hr_volume(self, poolAddress: str):
        volume = await SimulatorInfo(Protocol.UNISWAP, Chain.MAINNET).pool_volume(
            poolAddress
        )

        return volume
