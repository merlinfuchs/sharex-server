from aiohttp import web
import re
from mimetypes import guess_type

from utils import random_id


router = web.RouteTableDef()


@router.post("/s")
async def _shorten(req):
    data = await req.post()
    url = data.get("input")
    if url is None:
        raise web.HTTPBadRequest()

    if not re.match(r"^https?:\/\/.+\..+$", url):
        raise web.HTTPBadRequest

    url_id = random_id(req.app.config.id_length)
    await req.app.db.urls.insert_one({
        "_id": url_id,
        "url": url
    })

    return web.Response(text=url_id)


@router.get("/s/{id}")
async def _urls(req):
    id = req.match_info['id'].lower()
    url = await req.app.db.urls.find_one({"_id": id})
    if url is None:
        raise web.HTTPNotFound()

    raise web.HTTPFound(url["url"])


async def setup(app):
    app.add_routes(router)
