import asyncio
from fastapi import Response, APIRouter, status
from fastapi_cache.decorator import cache

from endpoint.routers.template import (
    endpoint_builder_template,
    endpoint_builder_baseTemplate,
)


def build_routes() -> list:
    routes = []

    return routes


class mongo_endpoint(endpoint_builder_template):
    # EXECUTION FUNCTIONS

    async def hypervisor_uncollected_fees(
        self, hypervisor_address: str, response: Response
    ):
        """
        {
          "0x0407c810546f1dc007f01a80e65983072d5c6dfa": {
              "symbol": "vCOMP-ETHV3-1",
              "baseFees0": 0.00800458814269154,
              "baseFees1": 0.0001808784772709525,
              "baseTokensOwed0": 2.8332441008892976e-40,
              "baseTokensOwed1": 4.593623189116164e-42,
              "limitFees0": 0.006977899477562586,
              "limitFees1": 0.0001559229550691857,
              "limitTokensOwed0": 1.949363658976323e-40,
              "limitTokensOwed1": 4.593623189116164e-42,
              "baseFees0USD": 0.31233314178468424,
              "baseFees1USD": 0.33465679980617047,
              "baseTokensOwed0USD": 1.1055110090600169e-38,
              "baseTokensOwed1USD": 8.499005847346911e-39,
              "limitFees0USD": 0.27227250522248564,
              "limitFees1USD": 0.2884847216046016,
              "limitTokensOwed0USD": 7.606273617523521e-39,
              "limitTokensOwed1USD": 8.499005847346911e-39,
              "totalFees0": 0.014982487620254127,
              "totalFees1": 0.0003368014323401382,
              "totalFeesUSD": 0.5846056470071699
          },
        """
        return None
