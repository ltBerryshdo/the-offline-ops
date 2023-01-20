## :page_facing_up: Description
Provides a method to protect admin and normal player's account in game server, which <strong><em>'online-mode' is 'false'</em></strong><br>
为<strong><em>未开启在线模式（正版验证）</em></strong>的服务器提供了管理员和普通玩家账号保护的一种方法<br>
## :telescope: How the plugin work
This plugin will check player's IP when a player join the server. If the IP is NOT match the record, then kick the player and broadcast in server.<br>
这个插件会在玩家进入服务器时检查玩家的IP地址，如果与记录不符，则将玩家踢出并全服广播<br>
## :balloon: Lightweight, plug and play
Simpler, lightweight, plug and play<br>
更简单、轻量化，即插即用<br>
## :snake: Commands
**All the commands need MCDR permissions at least level 2**<br>
**所有命令都需要MCDR 2级权限**<br>

|command|description|
|---------|-------|
|`!!offlineops`|view the commands list  查看命令列表|
|`!!offlineops` `notOpsPlayerProtect`/ `nopp`|nomal player protect options  非管理员玩家保护开关|
|`!!offlineops` `protectPlayer`/ `pp`|add protected player  添加受保护的玩家|
|`!!offlineops` `allPlayerProtect`/ `app`|all players protect options  全体玩家保护开关|
|`!!offlineops` `delIP`|delete player's or all the IP record  清除对应或全部玩家的IP记录|
