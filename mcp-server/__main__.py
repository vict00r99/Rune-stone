"""Entry point for ``python -m mcp_server``."""

import asyncio

from .server import main

asyncio.run(main())
