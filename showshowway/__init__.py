import re
import nbtlib as snbt
from mcdreforged.api.all import *

version = '1.2.0'


def on_load(server, params):
    server.logger.info('正在注册指令')
    server.register_help_message('!!show', '展示自己手上的物品')


def on_info(server: ServerInterface, info: Info):
    if info.is_player and info.content == '!!show':
        player = info.player
        if server.is_rcon_running():
            data = server.rcon_query('data get entity {} SelectedItem'.format(player))
            nbt = data.lstrip(re.search(r'\w+ has the following entity data: ', data).group())
            nbtj = snbt.parse_nbt(nbt)
            try:
                nbtj.get("components").unpack()
            except Exception:
                nbtj.update({"components": snbt.Compound({})})
            json = '[{"text":"[ShowIt] "},{"text":"%s","color":"yellow"},{"text":" 正在展示一个物品！ "},{"text":"[查看]","color":"aqua","bold":true,"underlined":true,"hover_event":{"action":"show_item","id":"%s","count":%d,"components":%s}}]' % (player, nbtj.get("id").unpack(), nbtj.get("count").unpack(), nbtj.get("components").unpack())
            show_item(server, json)
        else:
            server.execute('data get entity {} SelectedItem'.format(player))
    if not info.is_player and re.match(r'\w+ has the following entity data: ', info.content) is not None:
        nbt = info.content.lstrip(re.search(r'\w+ has the following entity data: ', info.content).group())
        player = re.search(r'^\w+', info.content).group()
        if nbt[0] == '{':
            nbtj = snbt.parse_nbt(nbt)
            try:
                nbtj.get("components").unpack()
            except Exception:
                nbtj.update({"components": snbt.Compound({})})
            json = '[{"text":"[ShowIt] "},{"text":"%s","color":"yellow"},{"text":" 正在展示一个物品！ "},{"text":"[查看]","color":"aqua","bold":true,"underlined":true,"hover_event":{"action":"show_item","id":"%s","count":%d,"components":%s}}]' % (player, nbtj.get("id").unpack(), nbtj.get("count").unpack(), nbtj.get("components").unpack())
            show_item(server, json)


def show_item(server, json):
    server.execute('tellraw @a {}'.format(json))
    server.execute('execute as @a at @s run playsound minecraft:entity.arrow.hit_player player @s')
