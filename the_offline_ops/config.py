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
    save_config()

def cmd_tree_protect_player_disable(source: CommandSource):
    config.notOpsPlayerProtect = False
    save_config()

def cmd_tree_sudo_enable(source: CommandSource):
    opsPath = os.path.join(serverPath, 'ops.json')
    with open(opsPath, 'r') as opsJson:                         #__init__.py    80
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
    save_config()

def cmd_tree_sudo_disable(source: CommandSource):
    opsPath = os.path.join(serverPath, 'ops.json')
    config.sudo = False
    with open(opsPath, 'w', encoding='utf-8') as opsJson:
        #for i in range(len(config.ops)):
        #    jsonObject = config.ops[i]
        json.dump(config.ops, opsJson, ensure_ascii=False, indent=4)

    config.ops.clear()
    save_config()

def cmd_tree_protect_player(source: CommandSource, context: CommandContext):
    name = context['playerName']
    if not config.notOpsPlayerProtect:
        source.reply('notOpsPlayerProtect已关闭，请先开启此选项')
        return
    dictkv = {name : 'NULL'}
    config.protectivePlayer.update(dictkv)
    save_config()

def cmd_tree_add_password(source: CommandSource, context: CommandSource):
    name = context['playerName']
    password = context['password']
    config.protectivePlayer[name] = password
    save_config()


def get_global_value(path: str):
    global serverPath
    serverPath = path