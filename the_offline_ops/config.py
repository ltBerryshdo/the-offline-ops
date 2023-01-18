#Copyright (c) 2004-2023 ltBerryshdo
from mcdreforged.api.all import *
import os.path
import json

class plgConfig(Serializable):                  #配置类
    notOpsPlayerProtect: bool = True
    allPlayerProtect: bool = False
    protectivePlayer: dict = {}

class Player():
    def __init__(self):
        self.playerName = None                          #玩家名字
        self.playerUUID = None                          #玩家uuid
        self.permission = None                          #玩家权限
        self.permission_MCDR = None                     #玩家MCDR权限

    def uuid(self, player: str):
        return get_uuid(player, serverPath)


config = plgConfig()
configFilePath = None
serverPath: str

def init_config(server: PluginServerInterface):
    global config
    config = plgConfig.get_default()                                    #默认配置
    config = server.load_config_simple(default_config = config.serialize(), 
    target_class = plgConfig)                                           #读取配置

    global configFilePath
    configFilePath = './' + server.get_data_folder()
    configFilePath = os.path.join(configFilePath, 'config.json')

#print(config.serialize()['notOpsPlayerProtect'])

def save_config():                                                      #手动写入配置
    with open(configFilePath, 'w', encoding='utf-8') as cfgFile:
        json.dump(config.serialize(), cfgFile, ensure_ascii=False, indent=4)


def cmd_tree_protect_player_enable(source: CommandSource):
    config.notOpsPlayerProtect = True
    source.reply('非op玩家保护开启')
    save_config()

def cmd_tree_protect_player_disable(source: CommandSource):
    config.notOpsPlayerProtect = False
    source.reply('非op玩家保护已关闭')
    save_config()
'''
def cmd_tree_sudo_enable(source: CommandSource):
    opsPath = os.path.join(serverPath, 'ops.json')
    with open(opsPath, 'r') as opsJson:                         #__init__.py    get_uuid()
        jsonAll = json.load(opsJson)
        jsonObjectNum = len(jsonAll)

        if config.sudo and (jsonAll == list()):
            source.reply('sudo已开启，不执行任何操作')
            return

        config.sudo = True

        for i in range(jsonObjectNum):
            config.ops.append(dict(uuid = jsonAll[i]['uuid'], name = jsonAll[i]['name'],        #可以简化一下
            level = jsonAll[i]['level'], bypassesPlayerLimit = jsonAll[i]['bypassesPlayerLimit']))
    with open(opsPath, 'w') as opsJson:                         #清空ops.json
        json.dump(list(), opsJson)
    source.reply('提升权限已开启')
    source.reply('需要重启服务器才能生效')
    save_config()

def cmd_tree_sudo_disable(source: CommandSource):
    opsPath = os.path.join(serverPath, 'ops.json')
    config.sudo = False
    with open(opsPath, 'w', encoding='utf-8') as opsJson:
        #for i in range(len(config.ops)):
        #    jsonObject = config.ops[i]
        json.dump(config.ops, opsJson, ensure_ascii=False, indent=4)

    config.ops.clear()
    source.reply('提升权限已关闭')
    source.reply('需要重启服务器才能生效')
    save_config()
'''
def cmd_tree_protect_player(source: CommandSource, name: str):
    if not config.notOpsPlayerProtect:
        source.reply('notOpsPlayerProtect已关闭，请先开启此选项')
        return
    dictkv = {name : 'NULL'}
    config.protectivePlayer.update(dictkv)
    save_config()    
    source.reply(str(dictkv) + '已添加')        #这句和save_config()已经换了个位置，不然全局玩家保护时报错就直接退出了，至少先save一下


def cmd_tree_all_player_protect_enable(source: CommandSource):
    config.allPlayerProtect = True
    source.reply('全体玩家保护已开启')
    save_config()

def cmd_tree_all_player_protect_disable(source: CommandSource):
    config.allPlayerProtect = False
    source.reply('全体玩家保护已关闭')
    save_config()

def cmd_tree_del_ip(source: CommandSource, name: str):
    config.protectivePlayer[name] = 'NULL'
    source.reply(name + '的IP已清除')
    save_config()


def get_global_value(path: str):
    global serverPath
    serverPath = path


def get_uuid(playerName: str, dir: str):
    filePath = '{}/usercache.json'.format(dir)

    with open(filePath, 'r') as usercache_fp:
        jsonAll = json.load(usercache_fp)                           #解析
        jsonObjectNum = len(jsonAll)                                #获取对象长度
        playerUUID = None

        for i in range(jsonObjectNum):
            if jsonAll[i]['name'] == playerName:                    #检查玩家名字
                playerUUID = jsonAll[i]['uuid']
                return playerUUID

def get_server_permission(playerName: str) -> int:
    opsPath = os.path.join(serverPath, 'ops.json')
    with open(opsPath, 'r') as opsJson:                         #__init__.py    get_uuid()
        jsonAll = json.load(opsJson)
        jsonObjectNum = len(jsonAll)

        for i in range(jsonObjectNum):
            if playerName == jsonAll[i]['name']:
                return jsonAll[i]['level']


def playerJoin(server: PluginServerInterface, player: str, IPaddress: str):
    playerObj = Player()
    playerObj.playerName = player
    playerObj.playerUUID = playerObj.uuid(player)
    playerObj.permission = get_server_permission(player)
    playerObj.permission_MCDR = server.get_permission_level(playerObj.playerName)

    if config.allPlayerProtect and (playerObj.playerName not in config.protectivePlayer.keys()):    #全体玩家保护已开启，并有未记录玩家进入时
        cmd_tree_protect_player(InfoCommandSource, playerObj.playerName)

    if (playerObj.permission != None) or (config.notOpsPlayerProtect and (playerObj.playerName in config.protectivePlayer.keys())): #是op或是受保护的玩家
        if config.protectivePlayer[playerObj.playerName] == 'NULL':     #如果没记录IP
            config.protectivePlayer[playerObj.playerName] = IPaddress
            save_config()

        elif config.protectivePlayer[playerObj.playerName] != IPaddress:
            server.broadcast('{}的信息与记录不符，已被踢出服务器，如记录的信息错误或变更，请向MCDR管理员提出请求！'.format(playerObj.playerName))
            server.execute('kick ' + playerObj.playerName)