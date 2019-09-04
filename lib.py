import threading
import requests
import json

URL="http://192.168.1.41:2000/api"

class DoTick(threading.Thread):
    def __init__(self, fnc):
        super(DoTick, self).__init__()
        self.fnc=fnc

    def run (self):
        self.fnc()


class Session:
    def __init__(self, login, password, handler_function):
        self.data = {
            "login": login,
            "password": password,
            "playerId": None,
            "token": None
        }

        self.games = []
        self.gameData = {}
        self.handler_function = handler_function

        self.login()
        self.getPlayerGames()

    def tick(self):
        def tickGame(game):
            #self.getPlayers(game)
            #self.getProjectiles(game)
            self.getMyStats(game)
            self.getPlatforms(game)

            self.handler_function(
                data = self.gameData[game],
                move = lambda *args: self.move(game, *args),
                jump = lambda *args: self.jump(game, *args),
                stop = lambda *args: self.stop(game, *args),
                rocket = lambda *args: self.rocket(game, *args),
                blackhole = lambda *args: self.blackhole(game, *args)
            )
        threads = []
        for game in self.games:
            threads.append(DoTick(lambda: tickGame(game)))

        for t in threads: t.start()
        for t in threads: t.join()

        self.getPlayerGames()
    
    def login(self):
        params = {
            "command": "login",
            "nick": self.data['login'],
            "password": self.data['password'],
        }
        r = requests.get(URL, params=params)

        data = r.json()
        self.data['playerId'] = data['Id']
        self.data['token'] = data['Token']

    def getPlayerGames(self):
        r = requests.get(URL, params={
            "command": "getPlayerGames",
            "playerId": self.data['playerId'],
        })

        data = r.json()
        self.games = data['Games']
        for game in self.games:
            if game not in self.gameData:
                self.gameData[game] = {
                    'platforms': [],
                    'players': [],
                    'projectiles': [],
                    'myStats': {
                        'Gcool': 0,
                        'Hcool': 0,
                        'OnGround': 0,
                        'VX': 0,
                        'VY': 0,
                        'VZ': 0,
                        'X': 0,
                        'Y': 0,
                        'Z': 0
                    },
                }


    def getPlatforms(self, gameId):
        r = requests.get(URL, params={
            "command": "getPlatforms",
            "gameId": gameId,
        })

        data = r.json()
        if data['Status'] == 3: return
        self.gameData[gameId]['platforms'] = data['Platforms']


    def getPlayers(self, gameId):
        r = requests.get(URL, params={
            "command": "getPlayers",
            "gameId": gameId,
        })

        data = r.json()
        if data['Status'] == 3: return
        self.gameData[gameId]['players'] = data['Players']


    def getProjectiles(self, gameId):
        r = requests.get(URL, params={
            "command": "getProjectiles",
            "gameId": gameId,
        })

        data = r.json()
        if data['Status'] == 3: return
        self.gameData[gameId]['projectiles'] = data['Projectiles']

    def getMyStats(self, gameId):
        r = requests.get(URL, params={
            "command": "getMyStats",
            "gameId": gameId,
            "token": self.data['token']
        })

        data = r.json()
        if data['Status'] == 3: return
        del data['Status']
        if data: self.gameData[gameId]['myStats'] = data

    def move(self, gameId, dx, dz):
        r = requests.get(URL, params={
            "command": "move",
            "gameId": gameId,
            "token": self.data['token'],
            "dx": dx,
            "dz": dz
        })
 
    def jump(self, gameId):
        r = requests.get(URL, params={
            "command": "move",
            "gameId": gameId,
            "token": self.data['token'],
        })
       
    def stop(self, gameId):
        r = requests.get(URL, params={
            "command": "stop",
            "gameId": gameId,
            "token": self.data['token'],
        })
    
    def rocket(self, gameId, dx, dy, dz, time):
        r = requests.get(URL, params={
            "command": "rocket",
            "gameId": gameId,
            "token": self.data['token'],
            "dx": dx,
            "dy": dy,
            "dz": dz,
            "time": time
        })

    def blackhole(self, gameId, dx, dy, dz, time):
        r = requests.get(URL, params={
            "command": "blackhole",
            "gameId": gameId,
            "token": self.data['token'],
            "dx": dx,
            "dy": dy,
            "dz": dz,
            "time": time
        })


