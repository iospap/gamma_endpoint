from sources.subgraph.enums import Chain, Protocol
from sources.subgraph.config import DEX_SUBGRAPH_URLS
from sources.subgraph.subgraphs import SubgraphClient


class UniswapClient(SubgraphClient):
    def __init__(self, protocol: Protocol, chain: Chain):
        super().__init__(
            protocol=protocol,
            chain=chain,
            url=DEX_SUBGRAPH_URLS[protocol][chain],
            schema_path="v3data/subgraphs/uniswap_v3/schema.graphql",
        )
