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

        iam_role_list = {'she',
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

        #client = discord.Client()
        client = bot
        #if client is None:
        #    print("no client was found")
        load_errors = dict()
        try:
            #main guild
            our_guild = bot.get_guild(441423477648523284)
            if our_guild is None:
                load_errors[0]="our_guild not set (and therefore, no roles were set)."
            #roles
            else:
                our_roles = our_guild.roles
                muted_role = discord.utils.get(our_roles, name='mute-1')
                if muted_role is None:
                    load_errors[1] = "muted_role not set."
                mute_2_role = discord.utils.get(our_roles, id=743162783679381737)
                if mute_2_role is None:
                    load_errors[2] = "mute_2_role not set."
                moderator_role = discord.utils.get(our_roles, id=743162754596208790)
                if moderator_role is None:
                    load_errors[3] = "moderator_role not set."
                embed_role = discord.utils.get(our_roles, name='embed')
                if embed_role is None:
                    load_errors[4] = "embed_role not set."
                interviewee_role = discord.utils.get(our_roles, name="interviewee")
                if interviewee_role is None:
                    load_errors[5] = "interviewee_role not set."
                beardy_role = discord.utils.get(our_roles, name='Beardy')
                if beardy_role is None:
                    load_errors[6] = "beardy_role not set."
                modmute_role = discord.utils.get(our_roles, name='modmute')
                if modmute_role is None:
                    load_errors[7] = "modmute_role not set."
    
            #channels
            usernotes_channel = bot.get_channel(743161064308473926)
            print(usernotes_channel.name)
            if usernotes_channel is None:
                load_errors[8] = "usernotes_channel not set."
            timeout_channel = bot.get_channel(743161355976048660)
            if timeout_channel is None:
                load_errors[9] = "timeout_channel not set."
            interview_channel = bot.get_channel(743162226201985256)
            if interview_channel is None:
                load_errors[10] = "interview_channel not set."
            beardy_channel = bot.get_channel(743161445755256924)
            if beardy_channel is None:
                load_errors[11] = "beardy_channel not set."
            help_commands_channel = bot.get_channel(743161401710739476)
            if help_commands_channel is None:
                load_errors[12] = "help_commands_channel not set."
            curated_news_channel = bot.get_channel(743161545269313657)
            if curated_news_channel is None:
                load_errors[13] = "curated_news_channel not set."
            tweets_channel = bot.get_channel(743161581982056509)
            if tweets_channel is None:
                load_errors[14] = "tweets_channel not set."
            low_effort_channel  = bot.get_channel(743161613078495303)
            if low_effort_channel is None:
                load_errors[15] = "low_effort_channel not set."
            bot_spam_channel_id  = bot.get_channel(743161650718179469)
            if bot_spam_channel_id is None:
                load_errors[16] = "bot_spam_channel_id not set."
            
            #users
            amici = bot.get_user(234842700325715969)
            if amici is None:
                load_errors[17] = "amici not set."

            if len(load_errors) > 0:
                for count in load_errors:
                    print(f"{load_errors[count]}\n")

        except Exception as e:
            print(e)


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

    @commands.Cog.listener()
    async def on_ready():
        print("yo")
