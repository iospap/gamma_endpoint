from sources.subgraph.enums import Chain, Protocol
from sources.subgraph.config import GAMMA_SUBGRAPH_URLS
from sources.subgraph.subgraphs import SubgraphClient


class GammaClient(SubgraphClient):
    def __init__(self, protocol: Protocol, chain: Chain):
        super().__init__(
            protocol=protocol,
            chain=chain,
            url=GAMMA_SUBGRAPH_URLS[protocol][chain],
            schema_path="v3data/subgraphs/gamma/schema.graphql",
        )
