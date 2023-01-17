#Copyright (c) 2004-2023 ltBerryshdo
from mcdreforged.api.all import *
import os.path
import json

class plgConfig(Serializable):                  #配置类
    notOpsPlayerProtect: bool = True
    sudo: bool = False
    protectivePlayer: dict = {}
    ops: list = []

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
def cmd_tree_protect_player(source: CommandSource, name: str, password: str):
    if not config.notOpsPlayerProtect:
        source.reply('notOpsPlayerProtect已关闭，请先开启此选项')
        return
    dictkv = {name : password}
    config.protectivePlayer.update(dictkv)
    source.reply(dictkv + '已添加')
    save_config()


def get_global_value(path: str):
    global serverPath
    serverPath = path
