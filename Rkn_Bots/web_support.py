from aiohttp import web

Rkn_AutoCaptionBot = web.RouteTableDef()

@Rkn_AutoCaptionBot.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("Rkn_AutoRectionBot")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(Rkn_AutoCaptionBot)
    return web_app
