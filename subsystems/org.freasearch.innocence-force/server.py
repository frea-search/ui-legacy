import sys
import os
import msg
import blocklist
from aiohttp import web

print (blocklist.chk_domain("sejuku.net"))


async def status(request):
    return web.Response(text="ok")

async def chk_blocklist(request):
    domain = request.match_info.get('domain')
    result = blocklist.chk_domain(domain)
    return web.Response(text=str(result))


app = web.Application()
app.add_routes([web.get('/', status),
                web.get('/blocklist/{domain}', chk_blocklist)])

web.run_app(app)
