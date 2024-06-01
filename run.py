import asyncio
import uvicorn
from app.main import create_app
from uvicorn import Server, Config


app = create_app()

# if __name__ == '__main__':
#     uvicorn.run('run:app', host='localhost', port=8000, reload=True)


app_ports = [8001, 8002, 8003] 

class MyServer(Server):
    """Класс Сервера, для асинхронного запуска и запросов на несколько реплик сервера"""
    async def run(self, sockets=None):
        self.config.setup_event_loop()
        return await self.serve(sockets=sockets)


async def run():
    apps = []
    for cfg in app_ports:
        config = Config("run:app", host="localhost",
                        port=cfg, reload=True)
        server = MyServer(config=config)
        apps.append(server.run())
    return await asyncio.gather(*apps)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())