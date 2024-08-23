import asyncio
from datasette.app import Datasette
import json
import pathlib
import os
from main import main

main()

static_mounts = [
    (static, str((pathlib.Path(".") / static).resolve()))
    for static in []
]

metadata = dict()
try:
    metadata = json.load(open("metadata.json"))
except Exception:
    pass

secret = os.environ.get("DATASETTE_SECRET")

true, false = True, False

ds = Datasette(
    [],
    ["lobbyist_registry.db"],
    static_mounts=static_mounts,
    metadata=metadata, template_dir="templates",
    secret=secret,
    cors=True,
    settings={}
)
asyncio.run(ds.invoke_startup())
app = ds.app()