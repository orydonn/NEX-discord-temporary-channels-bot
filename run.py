import discord
from discord.ext import commands

from settings import *

database = {}

# unic discord bot token
TOKEN = TOKEN

# id of your mother channel, with the usage of which will be created temporary channels will be created
mother_channel_id = mother_channel

# choosing prefix for using bot's commands
bot = commands.Bot(command_prefix='!')

# id of category, where temporary channels will be placed
main_category = main_category_id

# initialising of the dict for saving temporary channels
channels = {}


# class of the temporary channel
class temporary_channel:
    def __init__(self, category, creator):
        self.created_channel = None  # object of the voice channel
        self.creator = creator  # nickname of the channel creator
        self.channel_category = bot.get_channel(category)  # the category where channel will be placed

    def checking_data(self):  # checking for the existence of the channel in database(will be added soon)
        if self.creator not in database:
            database.setdefault(self.creator.name, [str(self.creator.name), self.channel_category,
                                                    {'bitrate': None, 'user_limit': 5, 'rtc_region': None}])
            # if channel not in database, it is adding there

    async def creating_channel(self):  # creating of the voice channel and connecting it to rhe temporary object
        for guild in bot.guilds:
            self.created_channel = await guild.create_voice_channel(name=database[self.creator.name][0],
                                                                    category=database[self.creator.name][1],
                                                                    **database[self.creator.name][2])
        await self.creator.move_to(self.created_channel)  # moving the user to newly created channel

    def updating_data(self):  # updating of the settings, if they have been changed
        new_setting = bot.get_channel(self.created_channel.id)
        database[self.creator.name] = [new_setting.name, self.channel_category,
                                       {'bitrate': new_setting.bitrate, 'user_limit': new_setting.user_limit,
                                        'rtc_region': None}]

    async def checking_void(self, channel):  # checking for the void in the channel
        await channel.delete()
        print(channels_for_delete, '--------------------------')
        return [self.creator]


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None:
        if after.channel.id == mother_channel_id:
            if member not in channels:
                channels.setdefault(member, temporary_channel(main_category, member))
            channels[member].checking_data()
            await channels[member].creating_channel()

    else:
        for created_channel in channels.items():
            if before.channel.id == created_channel[1].created_channel.id:
                created_channel[1].updating_data()
    global channels_for_delete
    channels_for_delete = []
    for created_channel in channels.values():
        print(f'{created_channel.created_channel.members} в канале {created_channel}')
        if not created_channel.created_channel.members:
            channels_for_delete.append(await created_channel.checking_void(created_channel.created_channel))
    for deleting_channel in channels_for_delete:
        print(deleting_channel[0])
        channels.pop(deleting_channel[0])


bot.run(TOKEN)
