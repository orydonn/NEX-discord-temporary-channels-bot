import discord
from discord.ext import commands
import random
from discord.utils import get
import asyncio

database = {}
TOKEN = 'ODU0OTc4NzcyMDcwNjk0OTEz.YMrzBw.YYYiiYEnUkp0H38DZUaqmn0s4L4'

bot = commands.Bot(command_prefix='!')

created_channel = None
maincategory = None

channels = []


class temporary_channel:
    def __init__(self, category, creator):
        self.created_channel = None
        self.creator = creator
        self.channel_category = bot.get_channel(category)

    def checking_data(self):
        if self.creator not in database:
            database.setdefault(self.creator, [str(self.creator.name), maincategory, {'bitrate': None, 'user_limit': 5, 'rtc_region': None}])

    def creating_channel(self):
        for guild in bot.guilds:
            self.created_channel = await guild.create_voice_channel(name=database[self.creator][0], category=database[self.creator][1], **database[self.creator][2])
        await self.creator.move_to(self.created_channel)

    def updating_data(self):
        new_setting = bot.get_channel(self.created_channel.id)
        print('Ливнул')
        database[self.creator] = [new_setting.name, maincategory,
                            {'bitrate': new_setting.bitrate, 'user_limit': new_setting.user_limit, 'rtc_region': None}]
        print(*database[self.creator])

    def checking_void(self):
        await created_channel.delete()
        print(self.created_channel)


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None:
        if after.channel.id == 864122465638678588:
            print('Зашел')

            # global maincategory
            # maincategory = bot.get_channel(864122028306071583)
            # if member not in database:
            #     database.setdefault(member, [str(member.name), maincategory, {'bitrate': None, 'user_limit': 5, 'rtc_region': None}])
            # print(*database[member])
            # for guild in bot.guilds:
            #     global created_channel
            #     created_channel = await guild.create_voice_channel(name=database[member][0], category=database[member][1], **database[member][2])
            # await member.move_to(created_channel)


    else:
        if before.channel.id == created_channel.id:
            # new_setting = bot.get_channel(created_channel.id)
            # print('Ливнул')
            # database[member] = [new_setting.name, maincategory, {'bitrate': new_setting.bitrate, 'user_limit': new_setting.user_limit, 'rtc_region': None}]
            # print(*database[member])
        if bot.get_channel(created_channel.id).members == []:
            # await created_channel.delete()
            # print(created_channel)


bot.run(TOKEN)
