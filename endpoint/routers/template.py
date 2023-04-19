from fastapi import APIRouter, Response, status
from fastapi_cache.decorator import cache


from endpoint.config.cache import (
    ALLDATA_CACHE_TIMEOUT,
    APY_CACHE_TIMEOUT,
    DASHBOARD_CACHE_TIMEOUT,
    DB_CACHE_TIMEOUT,
)


class endpoint_builder_template:
    def __init__(
        self, dex: str, chain: str, tags: list | None = None, url_root: str = ""
    ):
        self.dex = dex
        self.chain = chain
        self.tags = tags or [f"{chain} - {dex}"]
        # set root urs qithout the last /
        self.url_root = url_root.removesuffix("/")

    # ROUTEs BUILD FUNCTIONS
    def router(self) -> APIRouter:
        return self._create_routes(dex=self.dex, chain=self.chain)

    def _create_routes(self, dex, chain) -> APIRouter:
        """Create routes for the given chain and dex combination."""

        router = APIRouter()

        # ROOT
        router.add_api_route(
            path=f"{self.url_root}/",
            endpoint=self.root,
            methods=["GET"],
        )

        # create hyperivisor routes
        router = self._create_routes_hypervisor(router=router, dex=dex, chain=chain)

        router = self._create_routes_hypervisor_analytics(router, dex, chain)

        return router

    def _create_routes_hypervisor(
        self, router: APIRouter, dex: str, chain: str
    ) -> APIRouter:
        """Create /hypervisor routes for the given chain and dex combination."""

        router.add_api_route(
            path=f"{self.url_root}{'/hypervisor/{hypervisor_address}/basicStats'}",
            endpoint=self.hypervisor_basic_stats,
            methods=["GET"],
        )

        router.add_api_route(
            path=f"{self.url_root}{'/hypervisor/{hypervisor_address}/returns'}",
            endpoint=self.hypervisor_returns,
            methods=["GET"],
        )

        router.add_api_route(
            path=f"{self.url_root}{'/hypervisor/{hypervisor_address}/averageReturns'}",
            endpoint=self.hypervisor_average_returns,
            methods=["GET"],
        )

        router.add_api_route(
            path=f"{self.url_root}{'/hypervisor/{hypervisor_address}/uncollectedFees'}",
            endpoint=self.hypervisor_uncollected_fees,
            methods=["GET"],
        )

        return router

    def _create_routes_hypervisor_analytics(
        self, router: APIRouter, dex: str, chain: str
    ) -> APIRouter:
        router.add_api_route(
            path=f"{self.url_root}{'/hypervisor/{hypervisor_address}/analytics/basic/daily'}",
            endpoint=self.hypervisor_analytics_basic_daily,
            methods=["GET"],
        )

        router.add_api_route(
            path=f"{self.url_root}{'/hypervisor/{hypervisor_address}/analytics/basic/weekly'}",
            endpoint=self.hypervisor_analytics_basic_weekly,
            methods=["GET"],
        )

        router.add_api_route(
            path=f"{self.url_root}{'/hypervisor/{hypervisor_address}/analytics/basic/biweekly'}",
            endpoint=self.hypervisor_analytics_basic_biweekly,
            methods=["GET"],
        )

        router.add_api_route(
            path=f"{self.url_root}{'/hypervisor/{hypervisor_address}/analytics/basic/monthly'}",
            endpoint=self.hypervisor_analytics_basic_monthly,
            methods=["GET"],
        )

        return router

    def _create_routes_hypervisors(
        self, router: APIRouter, dex: str, chain: str
    ) -> APIRouter:
        router.add_api_route(
            path=f"{self.url_root}{'/hypervisors/aggregateStats'}",
            endpoint=self.hypervisors_aggregate_stats,
            methods=["GET"],
        )

        router.add_api_route(
            path=f"{self.url_root}{'/hypervisors/recentFees'}",
            endpoint=self.hypervisors_recent_fees,
            methods=["GET"],
        )

        router.add_api_route(
            path=f"{self.url_root}{'/hypervisors/returns'}",
            endpoint=self.hypervisors_returns,
            methods=["GET"],
        )

        router.add_api_route(
            path=f"{self.url_root}{'/hypervisors/averageReturns'}",
            endpoint=self.hypervisors_average_returns,
            methods=["GET"],
            description="Returns the average returns for all hypervisors.",
        )

        router.add_api_route(
            path=f"{self.url_root}{'/hypervisors/allData'}",
            endpoint=self.hypervisors_all_data,
            methods=["GET"],
        )

        router.add_api_route(
            path=f"{self.url_root}{'/hypervisors/uncollectedFees'}",
            endpoint=self.hypervisors_uncollected_fees,
            methods=["GET"],
        )

        router.add_api_route(
            path=f"{self.url_root}{'/hypervisors/collectedFees'}",
            endpoint=self.hypervisors_collected_fees,
            methods=["GET"],
        )

        router.add_api_route(
            path=f"{self.url_root}{'/hypervisors/feeReturns/daily'}",
            endpoint=self.hypervisors_feeReturns_daily,
            methods=["GET"],
        )
        router.add_api_route(
            path=f"{self.url_root}{'/hypervisors/feeReturns/weekly'}",
            endpoint=self.hypervisors_feeReturns_weekly,
            methods=["GET"],
        )
        router.add_api_route(
            path=f"{self.url_root}{'/hypervisors/feeReturns/monthly'}",
            endpoint=self.hypervisors_feeReturns_monthly,
            methods=["GET"],
        )

        router.add_api_route(
            path=f"{self.url_root}{'/hypervisors/impermanentDivergence/daily'}",
            endpoint=self.hypervisors_impermanentDivergence_daily,
            methods=["GET"],
        )
        router.add_api_route(
            path=f"{self.url_root}{'/hypervisors/impermanentDivergence/weekly'}",
            endpoint=self.hypervisors_impermanentDivergence_weekly,
            methods=["GET"],
        )
        router.add_api_route(
            path=f"{self.url_root}{'/hypervisors/impermanentDivergence/monthly'}",
            endpoint=self.hypervisors_impermanentDivergence_monthly,
            methods=["GET"],
        )

        return router

    # EXECUTION FUNCTIONS
    def root(self) -> str:
        return f"Gamma Strategies on {self.chain}'s {self.dex} "

    async def hypervisor_basic_stats(self, hypervisor_address: str, response: Response):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisor_returns(self, hypervisor_address: str, response: Response):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisor_average_returns(
        self, hypervisor_address: str, response: Response
    ):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisor_uncollected_fees(
        self, hypervisor_address: str, response: Response
    ):
        return NotImplementedError(" function defaults not implemented yet")

    #    hypervisor analytics
    async def hypervisor_analytics_basic_daily(
        self, hypervisor_address: str, response: Response
    ):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisor_analytics_basic_weekly(
        self, hypervisor_address: str, response: Response
    ):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisor_analytics_basic_biweekly(
        self, hypervisor_address: str, response: Response
    ):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisor_analytics_basic_monthly(
        self, hypervisor_address: str, response: Response
    ):
        return NotImplementedError(" function defaults not implemented yet")

    #    hypervisors
    async def hypervisors_aggregate_stats(self, response: Response):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisors_recent_fees(self, response: Response, hours: int = 24):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisors_returns(self, response: Response):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisors_average_returns(self, response: Response):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisors_all_data(self, response: Response):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisors_uncollected_fees(
        self,
        response: Response,
        start_timestamp: int | None = None,
        end_timestamp: int | None = None,
        start_block: int | None = None,
        end_block: int | None = None,
    ):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisors_collected_fees(
        self,
        response: Response,
        start_timestamp: int | None = None,
        end_timestamp: int | None = None,
        start_block: int | None = None,
        end_block: int | None = None,
    ):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisors_feeReturns_daily(self, response: Response):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisors_feeReturns_weekly(self, response: Response):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisors_feeReturns_monthly(self, response: Response):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisors_impermanentDivergence_daily(self, response: Response):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisors_impermanentDivergence_weekly(self, response: Response):
        return NotImplementedError(" function defaults not implemented yet")

    async def hypervisors_impermanentDivergence_monthly(self, response: Response):
        return NotImplementedError(" function defaults not implemented yet")