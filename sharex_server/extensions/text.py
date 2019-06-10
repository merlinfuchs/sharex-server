from aiohttp import web
import aiohttp_jinja2
import re

from utils import random_id


router = web.RouteTableDef()


@router.post("/t")
async def _shorten(req):
    data = await req.post()
    text = data.get("input")
    filename = data.get("filename")
    if text is None:
        raise web.HTTPBadRequest()

    text_id = random_id(req.app.config.id_length)
    await req.app.db.text.insert_one({
        "_id": text_id,
        "text": text,
        "filename": filename
    })

    return web.Response(text=text_id)


@router.get("/t/{id}")
@aiohttp_jinja2.template('text_view.html')
async def _urls(req):
    id = req.match_info['id'].lower()
    text = await req.app.db.text.find_one({"_id": id})
    if text is None:
        raise web.HTTPNotFound()

    syntax = re.findall(r"\..+$", text["filename"])
    return {"text": text["text"], "syntax": ''.join(syntax).lstrip("."), "filename": text["filename"]}


async def setup(app):
    app.add_routes(router)
