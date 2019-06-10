from aiohttp import web
from mimetypes import guess_type


router = web.RouteTableDef()


@router.post("/f")
async def _upload(req):
    data = await req.multipart()

    content = None
    filename = None
    while True:
        field = await data.next()
        if field is None:
            break

        if field.name == "file":
            content = await field.read(decode=True)

        if field.name == "filename":
            filename = await field.text()

    if content is None or filename is None:
        raise web.BaseRequest

    with open(f"files/{filename}", "wb") as fp:
        fp.write(content)

    return web.Response(text=filename)


@router.get("/f/{file}")
async def _files(req):
    file_name = req.match_info['file'].lower()
    try:
        with open(f"files/{file_name}", "rb") as fp:
            return web.Response(body=fp.read(), headers={"content-type": guess_type(file_name)[0] or ""})
    except FileNotFoundError:
        raise web.HTTPBadRequest


async def setup(app):
    app.add_routes(router)
