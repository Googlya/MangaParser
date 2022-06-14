from aiohttp import web
from parser_manga import Parser
from datetime import datetime
import os
import json

PORT = os.environ.get("API_PORT", 8080)

app = web.Application()
routes = web.RouteTableDef()
parser = Parser()

@routes.get('/ping')
async def ping(request):
    return web.json_response({"status": "pong"}, status=200)


@routes.get('/index')
async def get_index(request):
    now = datetime.today().strftime('%Y-%m-%d')
    path = f'index_{now}.json'
    if not os.path.exists(path):
        parser.find_manga_on_index()
    with open(path, 'r') as file:
        data = json.load(file)
        return web.json_response(data, status=200)

@routes.get('/collections')
async def get_collections(request):
    now = datetime.today().strftime('%Y-%m-%d')
    path = f'index_collection_{now}.json'
    if not os.path.exists(path):
        parser.find_manga_on_index()
    with open(path, 'r') as file:
        data = json.load(file)
        return web.json_response(data, status=200)

def main():
    app.add_routes(routes)
    web.run_app(app=app, port=PORT)


if __name__ == "__main__":
    main()