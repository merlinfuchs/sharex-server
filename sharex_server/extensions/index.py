from aiohttp import web
import aiohttp_jinja2


router = web.RouteTableDef()


@router.get("/")
@aiohttp_jinja2.template("index.html")
async def _upload(req):
    return {}


async def setup(app):
    app.add_routes(router)
