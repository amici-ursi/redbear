from redbot.core import commands, checks, Config
from redbot.core.utils.chat_formatting import box, humanize_list, pagify
import asyncio
import datetime
import discord
import logging

class Redbear(commands.Cog):
    """My custom cog"""
    def __init__(self):
        #self.bot = bot
        self.config = Config.get_conf(self, 12345678, force_registration=True)

        default_guild = {
            "infochannel": ''
        }

        self.config.register_guild(**default_guild)


    @commands.command()
    async def mute(self, ctx):
        await ctx.send("test")

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author.bot:
                return
        except Exception as e:
            print(e)

