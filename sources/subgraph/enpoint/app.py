from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

from fastapi.middleware.cors import CORSMiddleware
from endpoint.config.cache import CHARTS_CACHE_TIMEOUT

from sources.subgraph.enpoint.routers import build_routes
from sources.subgraph.enpoint import routers

# from sources.subgraph.enums import Chain, Protocol
from sources.subgraph.charts.daily import DailyChart


def build_app() -> FastAPI:
    app = FastAPI()

    # All deployments
    allDeployments = routers.subgraph_allDeployments(
        tags=["All Deployments"], prefix="/allDeployments"
    )
    app.include_router(allDeployments.router, tags=allDeployments.tags)

    # add subgraph routes to app
    for route_builder in build_routes():
        app.include_router(route_builder.router, tags=route_builder.tags)

    # Simulation
    sim = routers.router_builder_Simulator(tags=["Simulator"], prefix="/simulator")
    app.include_router(sim.router, tags=sim.tags)

    # Allow CORS
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )

    @app.get("/charts/dailyTvl")
    @cache(expire=CHARTS_CACHE_TIMEOUT)
    async def daily_tvl_chart_data(days: int = 24):
        daily = DailyChart(days)
        return {"data": await daily.tvl()}

    @app.get("/charts/dailyFlows")
    async def daily_flows_chart_data(days: int = 20):
        daily = DailyChart(days)
        return {"data": await daily.asset_flows()}

    @app.get("/charts/dailyHypervisorFlows/{hypervisor_address}")
    async def daily_hypervisor_flows_chart_data(
        hypervisor_address: str, days: int = 20
    ):
        daily = DailyChart(days)
        return {"data": await daily.asset_flows(hypervisor_address)}

    @app.on_event("startup")
    async def startup():
        FastAPICache.init(InMemoryBackend())

    return app