import logging

from fastapi.middleware.cors import CORSMiddleware

from sources.subgraph.enpoint.app import create_app as create_subgraph_endpoint

logging.basicConfig(
    format="[%(asctime)s:%(levelname)s:%(name)s]:%(message)s",
    datefmt="%Y/%m/%d %I:%M:%S",
    level=logging.INFO,
)


app = create_subgraph_endpoint(title="Gamma API", backwards_compatible=True)

# Allow CORS
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.mount(
    path="/subgraph",
    app=create_subgraph_endpoint(title="Gamma API", backwards_compatible=False),
    name="subgraph",
)
