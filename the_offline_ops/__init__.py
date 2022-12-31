from mcdreforged.api.all import *
from .config import *
import json
import os.path

class Player():
    def __init__(self):
        self.playerName = None                          #玩家名字
        self.playerUUID = None                          #玩家uuid
        self.permission = None                          #玩家权限
        self.permission_MCDR = None                     #玩家MCDR权限

    def uuid(self, player: str):
        return get_uuid(player, serverDir)

serverDir: str


def on_load(server: PluginServerInterface, prev_module):
    with open('./config.yml', 'r') as configDir:
        for lines in configDir.readlines():
            if 'working_directory' in lines:
                global serverDir

                serverDir = lines.split(':')[1].strip().replace('\n', '')     #查找工作地址  ***尾部去除/
                serverDir = os.path.normpath(serverDir)
                serverDir = './{}'.format(serverDir)
                propertiesDir = '{}/server.properties'.format(serverDir)

    with open(propertiesDir, 'r') as server_properties:                    #检查是否为离线模式
        for lines in server_properties.readlines():
            if 'online-mode' in lines:
                modeValue = lines.split('=')[1].replace('\n', '')
                break
        if modeValue != 'true':                                         #---!!!false!!!---
            return

    init_config(server)
    get_global_value(serverDir)
    register_help_message(server)
    register_command(server)


def register_command(server: PluginServerInterface):
    server.register_command(
        Literal('!!offlineops').
            runs(lambda src: src.reply('为未开启在线模式（正版验证）的服务器提供了管理员账号保护的一种方法')).
        then(Literal('notOpsPlayerProtect').
            then(Literal('enable').
                runs(cmd_tree_protect_player_enable)).
            then(Literal('disable').
                runs(cmd_tree_protect_player_disable))).
        then(Literal('sudo').
            then(Literal('enable').
                runs(cmd_tree_sudo_enable)).
            then(Literal('disable').
                runs(cmd_tree_sudo_disable))).
        then(Literal('protectPlayer').
            then(Text('playerName').
                runs(cmd_tree_protect_player).
                then(GreedyText('password').
                    runs(cmd_tree_add_password))))
    )

def register_help_message(server: PluginServerInterface):
    server.register_help_message("!!offlineops", {
        'en_us': '',
        'zh_cn': '为未开启在线模式（正版验证）的服务器提供了管理员账号保护的一种方法'
    })                                                                  #注册help内容


def on_player_joined(server: PluginServerInterface, player: str, info: Info):   #玩家进入检查
    playerObj = Player()
    playerObj.playerName = player
    playerObj.playerUUID = playerObj.uuid(player)
    playerObj.permission_MCDR = server.get_permission_level(playerObj.playerName)

    global config
    config = server.load_config_simple(default_config = config.serialize(), target_class = plgConfig)
    if config.notOpsPlayerProtect:
        if config.protectivePlayer.get(playerObj.playerName) == 'NULL':  #检查是否为受保护的玩家
            server.tell(info.player, '未记录密码，使用初始密码：NULL')
        else:
            print(config.protectivePlayer)
            print(playerObj.playerName)

        

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