from aiohttp import web, ClientSession
import aiohttp_jinja2
import jinja2
from motor.motor_asyncio import AsyncIOMotorClient

from extensions import urls, files, text, index


class App(web.Application):
    session = None
    db = None

    def __init__(self):
        super().__init__()

        self.db = AsyncIOMotorClient().sharex
        self.on_startup.append(self.prepare)
        aiohttp_jinja2.setup(
            self,
            loader=jinja2.FileSystemLoader("./templates")
        )

        self.add_routes(urls.router)
        self.add_routes(files.router)
        self.add_routes(text.router)
        self.add_routes(index.router)

    async def prepare(self, app):
        app.session = ClientSession()

    @property
    def config(self):
        return __import__("config")


app = App()
web.run_app(app, port=8081)
