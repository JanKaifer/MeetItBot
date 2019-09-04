import requests
import json

URL="192.168.1.41:80/api"

class GameSession:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.playerId = None
        self.token = None
        self.games = []
        self.gameData = {}
    
    def login(self):
        r = requests.get(URL, params={
            "command": "login",
            "nick": self.login,
            "pass": self.password,
        })

        data = r.json()
        self.playerId = data.Id
        self.toke = data.Token

    def getPlayerGames(self):
        r = requests.get(URL, params={
            "command": "getPlayerGames",
            "playerId": self.id,
        })

        data = r.json()
        self.games = data.Games
        for game in self.games:
            if game not in self.gameData:
                self.gameData[game] = {}


    def getPlatforms(self, gameId):
        r = requests.get(URL, params={
            "command": "getPlatforms",
            "gameId": gameId,
        })

        data = r.json()
        self.gameData[gameId]['platforms'] = data['Platforms']


    def getPlayers(self, gameId):
        r = requests.get(URL, params={
            "command": "getPlayers",
            "gameId": gameId,
        })

        data = r.json()
        self.gameData[gameId]['players'] = data['Players']


    def getProjectiles(self, gameId):
        r = requests.get(URL, params={
            "command": "getProjectiles",
            "gameId": gameId,
        })

        data = r.json()
        self.gameData[gameId]['projectiles'] = data['Projectiles']

    def getMyStats(self, gameId):
         r = requests.get(URL, params={
            "command": "getMyStats",
            "gameId": gameId,
        })

        data = r.json()
        del data['Stats']
        self.gameData[gameId]['myStats'] = data

    def move(self, gameId, dx, dz):
        r = requests.get(URL, params={
           "command": "move",
           "gameId": gameId,
           "dx": dx,
           "dz": dz
        })
    
    def stop(self, gameId):
        r = requests.get(URL, params={
           "command": "stop",
           "gameId": gameId,
        })
    
    def rocket(self, gameId, dx, dy, dz, time):
        r = requests.get(URL, params={
           "command": "rocket",
           "gameId": gameId,
           "dx": dx,
           "dy": dy,
           "dz": dz,
           "time": time
        })

    def rocket(self, gameId, dx, dy, dz, time):
        r = requests.get(URL, params={
           "command": "blackhole",
           "gameId": gameId,
           "dx": dx,
           "dy": dy,
           "dz": dz,
           "time": time
        })


