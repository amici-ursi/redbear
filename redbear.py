from redbot.core import commands, checks, Config
from redbot.core.utils.chat_formatting import box, humanize_list, pagify
import asyncio
import datetime
import discord
import logging
import re
import random
from TwitterAPI import TwitterAPI

class Redbear(commands.Cog):
    """My custom cog"""
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 12345678, force_registration=True)

        default_guild = {
            
        }

        self.config.register_guild(**default_guild)

        self.iam_role_list = {'she',
                 'they',
                 'he',
                 'United States',
                 'US - South',
                 'US - Midwest',
                 'US - Northeast',
                 'US - West Coast',
                 'US - Southwest',
                 'Mainland Europe',
                 'United Kingdom',
                 'England',
                 'Northern Ireland',
                 'Scotland',
                 'Wales',
                 'Republic of Ireland',
                 'Canada',
                 'Latin America',
                 'Africa',
                 'Asia',
                 'Australia',
                 'Caribbean',
                 'Spain',
                 'Sweden',
                 'Alaska',
                 'North Carolina',
                 'California',
                 'Texas',
                 'US - Pacific Northwest',
                 'bookclub',
                 'Germany',
                 'Just No Carl',
                 'do not tweet',
                 'I VOTED',
                 'Primary Drafters',
                 'Brexiteers',
                 'No News'}

        load_errors = dict()
        try:
            #main guild
            self.our_guild = bot.get_guild(441423477648523284)
            if self.our_guild is None:
                load_errors[0]="our_guild not set (and therefore, no roles were set)."
            #roles
            else:
                our_roles = self.our_guild.roles
                self.muted_role = discord.utils.get(our_roles, name='mute-1')
                if self.muted_role is None:
                    load_errors[1] = "muted_role not set."
                self.mute_2_role = discord.utils.get(our_roles, id=743162783679381737)
                if self.mute_2_role is None:
                    load_errors[2] = "mute_2_role not set."
                self.moderator_role = discord.utils.get(our_roles, id=743162754596208790)
                if self.moderator_role is None:
                    load_errors[3] = "moderator_role not set."
                self.embed_role = discord.utils.get(our_roles, name='embed')
                if self.embed_role is None:
                    load_errors[4] = "embed_role not set."
                self.interviewee_role = discord.utils.get(our_roles, name="interviewee")
                if self.interviewee_role is None:
                    load_errors[5] = "interviewee_role not set."
                self.beardy_role = discord.utils.get(our_roles, name='Beardy')
                if self.beardy_role is None:
                    load_errors[6] = "beardy_role not set."
                self.modmute_role = discord.utils.get(our_roles, name='modmute')
                if self.modmute_role is None:
                    load_errors[7] = "modmute_role not set."
    
            #channels
            self.usernotes_channel = bot.get_channel(743161064308473926)
            if self.usernotes_channel is None:
                load_errors[8] = "usernotes_channel not set."
            self.timeout_channel = bot.get_channel(743161355976048660)
            if self.timeout_channel is None:
                load_errors[9] = "timeout_channel not set."
            self.interview_channel = bot.get_channel(743162226201985256)
            if self.interview_channel is None:
                load_errors[10] = "interview_channel not set."
            self.beardy_channel = bot.get_channel(743161445755256924)
            if self.beardy_channel is None:
                load_errors[11] = "beardy_channel not set."
            self.help_commands_channel = bot.get_channel(743161401710739476)
            if self.help_commands_channel is None:
                load_errors[12] = "help_commands_channel not set."
            self.curated_news_channel = bot.get_channel(743161545269313657)
            if self.curated_news_channel is None:
                load_errors[13] = "curated_news_channel not set."
            self.tweets_channel = bot.get_channel(743161581982056509)
            if self.tweets_channel is None:
                load_errors[14] = "tweets_channel not set."
            self.low_effort_channel  = bot.get_channel(743161613078495303)
            if self.low_effort_channel is None:
                load_errors[15] = "low_effort_channel not set."
            self.bot_spam_channel_id  = bot.get_channel(743161650718179469)
            if self.bot_spam_channel_id is None:
                load_errors[16] = "bot_spam_channel_id not set."
            
            #users
            self.amici = bot.get_user(234842700325715969)
            if self.amici is None:
                load_errors[17] = "amici not set."

            if len(load_errors) > 0:
                for count in load_errors:
                    print(f"{load_errors[count]}\n")

        except Exception as e:
            print(e)


    @commands.command()
    async def mute(self, ctx):
        await ctx.send(self.tweets_channel.name)

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author.bot:
                return
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_ready():
        print("yo")
