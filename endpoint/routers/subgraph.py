from fastapi import Response
from endpoint.routers.template import endpoint_builder_template
from sources.subgraph.common import hypervisor, analytics, aggregate_stats

from sources.subgraph.config import RUN_FIRST_QUERY_TYPE


RUN_FIRST = RUN_FIRST_QUERY_TYPE


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
