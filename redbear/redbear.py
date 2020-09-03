from redbot.core import commands, checks, Config
from redbot.core.utils.chat_formatting import box, humanize_list, pagify
import asyncio
from datetime import datetime 
import dateutil
import dateutil.parser
import discord
import logging
import re
import random
from TwitterAPI import TwitterAPI
from collections import OrderedDict
#from redbot.core.utils.chat_formatting import box, humanize_list, pagify

class Redbear(commands.Cog):
    """My custom cog"""
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 12345678, force_registration=True)
        default_global = {
        }
        self.config.register_global(**default_global)

        default_guild = {
            "member_commands": {},
            "muted_members": {},
            "mute_role": "",
            #"mute_2_role": "", flatten to mute_role
            "moderator_role": "",
            "usernotes_channel": "",
            "timeout_channel": "",
            "skip_channels": {},
            "info_channels": {}
            #"embed_role": "",   #pd specific, put in separate cog
            #"interviewee_role": "",  #pd specific, put in separate cog
            #"modmute_role": ""  flatten to mute_role
        }
        self.config.register_guild(**default_guild)

        default_member = {
            #"iam_roles": {},
            "personal_commands": {},            
            "muted": False,
            "strikes": 0,
            "join_strikes": 0,
            "joined_at": [],
            "last_check": "", #[],
            "last_message": None,
            "spammer": False
        }

        self.config.register_member(**default_member)

        #default_channel = {
            
        #}

        #self.config.register_channel(**default_channel)

        self.all_users = dict()
        #self.av_api_key = ''   #alphavantage/stock API  #move to sep cog
        self.counting_emoji = False
        self.counting_reactions = False       
        self.counting_users = False
        
        ##TODO: add all of these to Config and allow add/remove commands.
        #self.iam_role_list = {'she',
        #         'they',
        #         'he',
        #         'United States',
        #         'US - South',
        #         'US - Midwest',
        #         'US - Northeast',
        #         'US - West Coast',
        #         'US - Southwest',
        #         'Mainland Europe',
        #         'United Kingdom',
        #         'England',
        #         'Northern Ireland',
        #         'Scotland',
        #         'Wales',
        #         'Republic of Ireland',
        #         'Canada',
        #         'Latin America',
        #         'Africa',
        #         'Asia',
        #         'Australia',
        #         'Caribbean',
        #         'Spain',
        #         'Sweden',
        #         'Alaska',
        #         'North Carolina',
        #         'California',
        #         'Texas',
        #         'US - Pacific Northwest',
        #         'bookclub',
        #         'Germany',
        #         'Just No Carl',
        #         'do not tweet',
        #         'I VOTED',
        #         'Primary Drafters',
        #         'Brexiteers',
        #         'No News'}  #self-assignable roles.
        #add line for self.pdbeat. pdbeat = pdbeat = TwitterAPI('')
        self.strike_limit = 5
        self.allowance = 3
        self.reset_period = 5
        # member_commands, personal_commands, muted_members
        
        #####PROBABLY need some kind of one-time conversion from pdsettings to self.Config

        #for member in list(pd_settings['muted_members']):
        #    member = our_guild.get_member(member)
        #    if member is not None and muted_role not in member.roles and mute_2_role not in member.roles and modmute_role not in member.roles:
        #        pd_settings['muted_members'].pop(member.id, None)


        ##Load roles, channels, users - that we use throughout the cog
        #load_errors = dict()
        #try:
        #    #main guild
        #    self.our_guild = bot.get_guild(441423477648523284)
        #    getroles = check_load_error(load_errors, self.our_guild, "our_guild")

        #    #roles
        #    if getroles == True:
        #        our_roles = self.our_guild.roles
        #        self.muted_role = discord.utils.get(our_roles, name='mute-1')
        #        check_load_error(load_errors, self.muted_role, "muted_role")

        #        self.mute_2_role = discord.utils.get(our_roles, id=743162783679381737)
        #        check_load_error(load_errors, self.mute_2_role, "mute_2_role")

        #        self.moderator_role = discord.utils.get(our_roles, id=743162754596208790)
        #        check_load_error(load_errors, self.moderator_role, "moderator_role")

        #        self.embed_role = discord.utils.get(our_roles, name='embed')
        #        check_load_error(load_errors, self.embed_role, "embed_role")

        #        self.interviewee_role = discord.utils.get(our_roles, name="interviewee")
        #        check_load_error(load_errors, self.interviewee_role, "interviewee_role")

        #        #self.beardy_role = discord.utils.get(our_roles, name='Beardy')
        #        #check_load_error(load_errors, self.beardy_role, "beardy_role")

        #        self.modmute_role = discord.utils.get(our_roles, name='modmute')
        #        check_load_error(load_errors, self.modmute_role, "modmute_role")
    
        #    #channels
        #    self.usernotes_channel = bot.get_channel(743161064308473926)
        #    check_load_error(load_errors, self.usernotes_channel, "usernotes_channel")

        #    self.timeout_channel = bot.get_channel(743161355976048660)
        #    check_load_error(load_errors, self.timeout_channel, "timeout_channel")

        #    self.interview_channel = bot.get_channel(743162226201985256)
        #    check_load_error(load_errors, self.interview_channel, "interview_channel")

        #    self.beardy_channel = bot.get_channel(743161445755256924)
        #    check_load_error(load_errors, self.beardy_channel, "beardy_channel")

        #    self.help_commands_channel = bot.get_channel(743161401710739476)
        #    check_load_error(load_errors, self.help_commands_channel, "help_commands_channel")

        #    self.curated_news_channel = bot.get_channel(743161545269313657)
        #    check_load_error(load_errors, self.curated_news_channel, "curated_news_channel")

        #    self.tweets_channel = bot.get_channel(743161581982056509)
        #    check_load_error(load_errors, self.tweets_channel, "tweets_channel")

        #    self.low_effort_channel  = bot.get_channel(743161613078495303)
        #    check_load_error(load_errors, self.low_effort_channel, "low_effort_channel")

        #    self.bot_spam_channel  = bot.get_channel(743161650718179469)
        #    check_load_error(load_errors, self.bot_spam_channel, "bot_spam_channel")

        #    self.meta_channel = bot.get_channel(744394862258028575)
        #    check_load_error(load_errors, self.meta_channel, "meta_channel")
            
            #users
        try:
            self.amici = bot.get_user(234842700325715969)
        except Exception as e:
            print(e)
            #check_load_error(load_errors, self.amici, "amici")

        #    if len(load_errors) > 0:
        #        for count in load_errors:
        #            print(f"{load_errors[count]}\n")

        #except Exception as e:
        #    print(e)
    
    #done
    @commands.command()
    @checks.admin()
    async def setup(self, ctx, mute_role = "", mod_role = "", usernotes_channel = "", timeout_channel = ""):
        """
        `Makes sure all necessary setup is complete.
        """
        await ctx.react_quietly("🐻")

        if mute_role == "" and mod_role == "" and usernotes_channel == "" and timeout_channel == "":
            guild_data = await self.config.guild(ctx.guild).all()

            if not guild_data["mute_role"]:
                text = f"`mute_role` is not set.\n"
            else:
                text = f"`mute_role`: `{guild_data['mute_role']}`\n"

            if not guild_data["moderator_role"]:
                text += f"`moderator_role` is not set.\n"
            else:
                text += f"`moderator_role`: `{guild_data['moderator_role']}`\n"

            if not guild_data["usernotes_channel"]:
                text += f"`usernotes_channel` is not set.\n"
            else:
                text += f"`usernotes_channel`: `{guild_data['usernotes_channel']}`\n"

            if not guild_data["timeout_channel"]:
                text += f"`timeout_channel` is not set.\n"
            else:
                text += f"`timeout_channel`: `{guild_data['timeout_channel']}`\n"
            
            text += f"\n```!setup mute_role_id mod_role_id usernotes_channel_id timeout_channel_id```"
            await ctx.send(text)

        elif mute_role != "" and mod_role != "" and usernotes_channel != "" and timeout_channel != "":
            #set the config up
            try:
                mute_role_actual = discord.utils.get(ctx.guild.roles, id=int(mute_role))
            except:
                pass
            if mute_role_actual is None:
                await ctx.react_quietly("⚠")
                await ctx.send(f"No mute role found with ID `{mute_role}`.")
            else:
                await self.config.guild(ctx.guild).mute_role.set(mute_role)
                await ctx.send(f"Mute role successfully set to ID `{mute_role}`.")

            try:
                mod_role_actual = discord.utils.get(ctx.guild.roles, id=int(mod_role))
            except:
                pass
            if mod_role_actual is None:
                await ctx.react_quietly("⚠")
                await ctx.send(f"No mod role found with ID `{mod_role}`.")
            else:
                await self.config.guild(ctx.guild).moderator_role.set(mod_role)  
                await ctx.send(f"Mod role successfully set to ID `{mod_role}`.")

            try:
                usernotes_channel_actual = self.bot.get_channel(int(usernotes_channel))
            except:
                pass
            if usernotes_channel_actual is None:
                await ctx.react_quietly("⚠")
                await ctx.send(f"No usernotes channel found with ID `{usernotes_channel}`.")
            else:
                await self.config.guild(ctx.guild).usernotes_channel.set(usernotes_channel)
                await ctx.send(f"Usernotes channel successfully set to ID `{usernotes_channel}`.")

            try:
                timeout_channel_actual = self.bot.get_channel(int(timeout_channel))
            except:
                pass
            if timeout_channel_actual is None:
                await ctx.react_quietly("⚠")
                await ctx.send(f"No timeout channel channel found with ID `{timeout_channel}`.")
            else:
                await self.config.guild(ctx.guild).timeout_channel.set(timeout_channel)
                await ctx.send(f"Timeout channel successfully set to ID `{timeout_channel}`.")

        else:
            await ctx.react_quietly("⚠")
            await ctx.send(f"Usage: !setup `mute_role_id` `mod_role_id` `usernotes_channel_id` `timeout_channel_id`")

    @commands.command()
    @checks.admin()
    async def skipchannel(self, ctx, addremove = "", channel_id = 0):
        """
        `!skipchannelsetup [add/remove] [channel_id]. The code here is the same as infochannel so update both
        """
        await ctx.react_quietly("🐻")
        if addremove == "add" or addremove == "remove":
            if channel_id > 0:
                channel = self.bot.get_channel(channel_id)
                if channel in ctx.guild.channels:
                    async with self.config.guild(ctx.guild).skip_channels() as skipchannels:
                        if addremove=="add":
                            skipchannels[channel_id] = ""
                            await ctx.send(f"`{channel.name}:{channel_id}` added to channels to skip.")
                        elif str(channel_id) in skipchannels:
                            skipchannels.pop(str(channel_id))
                            await ctx.send(f"`{channel.name}:{channel_id}` removed from channels to skip.")
                        else:
                            await ctx.react_quietly("⚠")
                            await ctx.send("Nothing to remove.")
                else:
                    await ctx.react_quietly("⚠")
                    await ctx.send(f"Channel ID `{channel_id}` doesn't seem to be in this server.")
            else:
                await ctx.react_quietly("⚠")
                await ctx.send(f"A valid `channel_id` must be provided.")
        else:
            await ctx.send(f"Usage: !skipchannel [`\"add\" or \"remove\"`] [`channel_id`]")
            skipped = await self.config.guild(ctx.guild).skip_channels()
            if skipped is not None:
                content = f"The following channels are being skipped for certain commands:\n"
                for key in skipped:
                    channel = self.bot.get_channel(int(key))
                    content += f"`{channel.name}:{key}` "
                await ctx.send(content)
    
    @commands.command()
    async def infochannel(self, ctx, addremove = "", channel_id = 0):
        """
        `!infochannel [add/remove] [channel_id] . The code here is the same as skipchannel so update both
        """
        await ctx.react_quietly("🐻")
        if addremove == "add" or addremove == "remove":
            if channel_id > 0:
                channel = self.bot.get_channel(channel_id)
                if channel in ctx.guild.channels:
                    async with self.config.guild(ctx.guild).info_channels() as info_channels:
                        if addremove=="add":
                            info_channels[channel_id] = ""
                            await ctx.send(f"`{channel.name}:{channel_id}` added to eligible !userinfo channels.")
                        elif str(channel_id) in skipchannels:
                            info_channels.pop(str(channel_id))
                            await ctx.send(f"`{channel.name}:{channel_id}` removed from eligible !userinfo channels.")
                        else:
                            await ctx.react_quietly("⚠")
                            await ctx.send("Nothing to remove.")
                else:
                    await ctx.react_quietly("⚠")
                    await ctx.send(f"Channel ID `{channel_id}` doesn't seem to be in this server.")
            else:
                await ctx.react_quietly("⚠")
                await ctx.send(f"A valid `channel_id` must be provided.")
        else:
            await ctx.send(f"Usage: !infochannel [`\"add\" or \"remove\"`] [`channel_id`]")
            infochannels = await self.config.guild(ctx.guild).info_channels()
            if infochannels is not None:
                content = f"The following channels are OK to use !userinfo:\n"
                for key in infochannels:
                    channel = self.bot.get_channel(int(key))
                    content += f"`{channel.name}:{key}` "
                await ctx.send(content)
    
    ##I temporarily need this for debug
    @commands.command()
    async def cleanupmute(self, ctx):
        try:
            for mentioned_member in ctx.message.mentions:
                await self.config.guild(ctx.guild).muted_members.set_raw(mentioned_member.id, value="")
                await self.config.member(mentioned_member).muted.set(False)

            guild_data = await self.config.guild(ctx.guild).all()
            await ctx.send(guild_data["muted_members"])
        except Exception as e:
            print(e)
            await ctx.react_quietly("⚠")

    @commands.command()
    async def mute(self, ctx):
        """
        `!mute @someone @someoneelse`: Adds the `mute` role to members.
        """
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])

        if mod_role in ctx.author.roles:
            await ctx.react_quietly("🐻")
            try:
                mute_role = get_guild_role(ctx, guild_data["mute_role"])
                for mentioned_member in ctx.message.mentions:
                    if (mute_role not in mentioned_member.roles
                        and mod_role not in mentioned_member.roles
                        and mentioned_member is not self.bot.user
                        and not guild_data["muted_members"].get(mentioned_member.id)):

                        #why are we resetting to defaults? (this is parity with old bear)
                        await all_users_setdefault(self, mentioned_member, ctx.message.created_at)
                        await self.config.member(mentioned_member).muted.set(True)
                        roles = [role.id for role in mentioned_member.roles]
                        await self.config.guild(ctx.guild).muted_members.set_raw(mentioned_member.id, value = roles)
                        await mentioned_member.edit(roles=[mute_role])
                        usernotes_channel = get_guild_channel(self, guild_data["usernotes_channel"])
                        await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention}) was muted by {ctx.author.mention}.\n--{ctx.message.jump_url}')
                    else:
                        await ctx.react_quietly("⚠")
                          
            except Exception as e:
                await ctx.react_quietly("⚠")
                print(type(e))
                print(e)
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def unmute(self, ctx):  # checked
        """
        `!unmute @someone @someoneelse`: Removes the `muted` role from a member.
        """
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])

        if mod_role in ctx.author.roles:
            await ctx.react_quietly("🐻")
            try:
                mute_role = get_guild_role(ctx, guild_data["mute_role"])
                for mentioned_member in ctx.message.mentions:
                    if (mute_role in mentioned_member.roles 
                       and mod_role not in mentioned_member.roles):

                        await all_users_setdefault(self, mentioned_member, ctx.message.created_at)
                        await mentioned_member.remove_roles(mute_role)
                        await self.config.member(mentioned_member).muted.set(False)
                        oldroles = await self.config.guild(ctx.guild).muted_members.get_raw(mentioned_member.id)
                        for role_id in oldroles:
                            try:
                                thisrole = ctx.guild.get_role(role_id)
                                await mentioned_member.add_roles(thisrole)
                            except Exception as e:
                                pass
                        await self.config.guild(ctx.guild).muted_members.set_raw(mentioned_member.id, value = "")
                        usernotes_channel = get_guild_channel(self, guild_data["usernotes_channel"])
                        await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention}) was unmuted and their spam tracking reset by {ctx.author.mention}.\n--{ctx.message.jump_url}')
            except Exception as e:
                print(f"unmute error:\n{e}")
                await ctx.react_quietly("⚠")
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def muted(self, ctx): 
        """
        `!muted!`: sends the mute message to the channel.
        """
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])
        if mod_role in ctx.author.roles or ctx.author == bot.user:
            await ctx.react_quietly("🐻")
            try:
                await ctx.send(f'You were muted because you broke the rules. Reread them, then write `@{mod_role.name}` to be unmuted.')
            except Exception as e:
                print(e)
                await ctx.react_quietly("⚠")
        else:
            await ctx.react_quietly("🚫")

    #TODO: move to funbear
    @commands.command()
    async def shitposting(self, ctx):
        if self.embed_role in ctx.author.roles or self.moderator_role in ctx.author.roles:
            copypasta_text = get_shitposts(ctx)
            await ctx.channel.send('look, until you get your shit together i really don\'t have the time to explain {} to a kid'.format(random.choice(copypasta_text)))
        else:
            await ctx.add_reaction("🚫")


    #NOTE ----- EMBED IS NOT CROSS SERVER, IT NEEDS TO GET MOVED TO A PD COG
    #@commands.command()
    #async def embed(self, ctx):  
    ##"""
    ##`!embed @someone @someoneelse`: Gives members the `embed` role.
    ##"""
    #    guild_data = await self.config.guild(ctx.guild).all()
    #    mod_role = get_guild_role(ctx, guild_data["moderator_role"])
    #    if mod_role in ctx.author.roles:
    #        await ctx.react_quietly("🐻")
    #        try:
    #            embed_role = get_guild_role(ctx, guild_data["embed_role"])
    #            for mentioned_member in ctx.message.mentions:
    #                if embed_role not in mentioned_member.roles:
    #                    await mentioned_member.add_roles(embed_role)
    #                    await self.usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention}) was given embed permissions by {ctx.author.mention}.\n--{ctx.message.jump_url}')
    #        except Exception as e:
    #            print(e)
    #            await ctx.react_quietly("⚠")
    #    else:
    #        await ctx.react_quietly("🚫")

    #NOTE ----- EMBED IS NOT CROSS SERVER, IT NEEDS TO GET MOVED TO A PD COG
    #@commands.command()
    #async def unembed(self, ctx):
    ##"""
    ##`!unembed @someone @someoneelse`: Removes members embed role.
    ##"""
    #    guild_data = await self.config.guild(ctx.guild).all()
    #    mod_role = get_guild_role(ctx, guild_data["moderator_role"])
    #    if mod_role in ctx.author.roles:
    #        await ctx.react_quietly("🐻")
    #        try:
    #            embed_role = get_guild_role(ctx, guild_data["embed_role"])
    #            for mentioned_member in ctx.message.mentions:
    #                if embed_role in mentioned_member.roles:
    #                    await mentioned_member.remove_roles(embed_role)
    #                    await self.usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention}) \'s embed role was removed by {ctx.message.author.mention}.\n--{ctx.message.jump_url}')
    #        except Exception as e:
    #            print(e)
    #            await ctx.react_quietly("⚠")
    #    else:
    #        await ctx.react_quietly("🚫")

    @commands.command()
    async def purge(self, ctx): 
    #"""
    #`!purge 100` purges 100 messages.\n
    #`!purge @someone @someoneelse`: checks for messages in every channel up to two weeks ago for messages from the mentioned members and purges them. This is resource intensive.
    #"""
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])
        usernotes_channel = get_guild_channel(self, guild_data["usernotes_channel"])
        if "skip_channels" not in guild_data or len(guild_data["skip_channels"])==0:
            await ctx.send("Warning! No skip channels have been defined (using !skipchannelsetup). All channels (besides usernotes) will be affected. Is this OK? (only \"Yes\" will proceed)")
            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author
            try:
                date_message = await self.bot.wait_for('message', check=check, timeout=30)
                if isinstance(date_message, discord.Message):
                    if date_message.content == "Yes":
                        await date_message.add_reaction("🐻")
                    else:
                        await ctx.react_quietly("⚠")
                        await ctx.send("Canceling.")
                        return
                else:
                    await ctx.send(f"{ctx.author.mention}, Discord returned an error or you didn't reply within 30 seconds.")
            except Exception as e:

                await ctx.send(f"No reply within 30 seconds (or some other error) - canceling.")
                return

        if mod_role in ctx.author.roles and ctx.channel is not usernotes_channel:
            await ctx.react_quietly("🐻")
            try:
                if len(ctx.message.mentions) == 0 and len(ctx.message.content.split(' ')) == 2:
                    purge_number = int(ctx.message.content.split(' ')[1])
                    await usernotes_channel.send(f'{ctx.message.author.mention} purged {purge_number} messages in {ctx.message.channel.mention}.\n--{ctx.message.jump_url}')
                    await ctx.message.channel.purge(limit=purge_number, check=None)
                for mentioned_member in ctx.message.mentions:
                    if mod_role not in mentioned_member.roles and mentioned_member is not self.bot.user :
                        def purge_check(checked_message):
                            message_age = datetime.datetime.utcnow() - checked_message.created_at
                            day_limit = datetime.timedelta(days=13)
                            if message_age < day_limit:
                                return checked_message.author == mentioned_member

                        await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention})\'s messages were purged by {ctx.message.author.mention}.\n--{ctx.message.jump_url}')
                        skipped = await self.config.guild(ctx.guild).skip_channels()
                        for ichannel in ctx.message.guild.channels:
                            if str(ichannel.id) not in skipped:
                                try:
                                    await ichannel.purge(check=purge_check)
                                except AttributeError:
                                    pass
            except Exception as e:
                print(e)
                await ctx.react_quietly("⚠")
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def lock(self, ctx):  # checked
         #"""
         #`!lock`: Denies the `send_message` permission for `@everyone` in the channel.
         #"""
         guild_data = await self.config.guild(ctx.guild).all()
         mod_role = get_guild_role(ctx, guild_data["moderator_role"])
         if mod_role in ctx.author.roles:
            try:
                usernotes_channel = get_guild_channel(self, guild_data["usernotes_channel"])
                channel_permissions = ctx.channel.overwrites_for(ctx.guild.default_role)
                channel_permissions.send_messages = False
                await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=channel_permissions)
                await ctx.react_quietly("🐻")
                await ctx.react_quietly("🔒")
                await usernotes_channel.send(f'{ctx.author.mention} locked {ctx.channel.mention}.\n--{ctx.message.jump_url}')
                if ctx.channel.name.endswith("🔒") is False:
                    await ctx.channel.edit(name=f"{ctx.channel.name}🔒")
                await ctx.send("https://twitter.com/dril/status/107911000199671808")
            except Exception as e:
                await ctx.react_quietly("⚠")
                print(e)
         else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def unlock(self, ctx):  # checked
        """
        `!unlock`: Allows the `send_message` permission for `@everyone` in the channel.
        """
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])
        if mod_role in ctx.author.roles:
            try:
                usernotes_channel = get_guild_channel(self, guild_data["usernotes_channel"])
                channel_permissions = ctx.channel.overwrites_for(ctx.guild.default_role)
                channel_permissions.send_messages = True
                await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=channel_permissions)
                await ctx.react_quietly("🐻")
                await ctx.react_quietly("🔓")
                await usernotes_channel.send(f'{ctx.author.mention} unlocked {ctx.channel.mention}.\n--{ctx.message.jump_url}')
                if ctx.channel.name.endswith("🔒"):
                    await ctx.channel.edit(name=ctx.channel.name[:-1])
                await ctx.send("https://twitter.com/dril/status/568056615355740160")
            except Exception as e:
                print(e)
                await ctx.react_quietly("⚠")
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def ban_id(self, ctx, *, user_id: int = 0):  # checked
    #"""
    #`!ban_id 125341170896207872`: Bans a user according to their Discord user id.
    #"""
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])
        if mod_role in ctx.author.roles:
            await ctx.react_quietly("🐻")
            if user_id > 0:
                try:
                    usernotes_channel = get_guild_channel(self, guild_data["usernotes_channel"])
                    fake_user = discord.Object(id=user_id)
                    member = ctx.guild.get_member(user_id)
                    if member is not None and mod_role not in member.roles and member is not bot.user:
                        await ctx.guild.ban(member, delete_message_days=0)
                        await usernotes_channel.send(f'`{member.name}`:`{member.id}` ({member.mention}) was banned from the server by {ctx.author.mention}.\n--{ctx.message.jump_url}')
                    if member is None:
                        await ctx.guild.ban(fake_user, delete_message_days=0)
                        await usernotes_channel.send(f'User id `{fake_user.id}` was banned from the server by {ctx.author.mention}.\n--{ctx.message.jump_url}')
                except Exception as e:
                    await usernotes_channel.send(f"{ctx.author.mention} tried to ban user ID {user_id} but no user was found.\n--{ctx.message.jump_url}")
                    print(e)
                    await ctx.react_quietly("⚠")
            else:
                await ctx.send("No userid specified.")
                await ctx.react_quietly("⚠")
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def unban_id(self, ctx, *, user_id: int = 0):  
        #"""
        #`!unban_id 125341170896207872`: Unbans a user according to their Discord user id.
        #"""
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])
        if mod_role in ctx.author.roles:
            await ctx.react_quietly("🐻")
            if len(user_id) > 0:
                try:
                    usernotes_channel = get_guild_channel(self, guild_data["usernotes_channel"])
                    fake_banned_user = discord.Object(id=user_id)
                    await ctx.guild.unban(fake_banned_user)
                    await usernotes_channel.send(f'User id `{fake_banned_user.id}` was unbanned from the server by {ctx.author.mention}.\n--{ctx.message.jump_url}')
                except Exception as e:
                    await usernotes_channel.send(f"{ctx.author.mention} tried to ban user ID {user_id} but no user was found.\n--{ctx.message.jump_url}")
                    print(e)
                    await ctx.react_quietly("⚠")
            else:
                await ctx.send("No userid specified.")
                await ctx.react_quietly("⚠")
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def ban(self, ctx):     # checked
        """
        `!ban @someone @someoneelse`: Bans members from the server.
        """
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])
        if mod_role in ctx.author.roles:
            await ctx.react_quietly("🐻")
            try:
                usernotes_channel = get_guild_channel(self, guild_data["usernotes_channel"])
                for mentioned_member in ctx.message.mentions:
                    if mod_role not in mentioned_member.roles and mentioned_member is not bot.user:
                        await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention}) was banned from the server by {ctx.author.mention}.\n--{ctx.message.jump_url}')
                        await ctx.guild.ban(mentioned_member, delete_message_days=0)
                    if str(ctx.message.id).endswith("1"):
                        await ctx.send('https://b.thumbs.redditmedia.com/GVgfjW-E0wafJbQHlv_XwyG7Ux3tnGZfHI_ExznRBzo.png')
            except Exception as e:
                print(e)
                await ctx.react_quietly("⚠")
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def kick(self, ctx):
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])
        if mod_role in ctx.author.roles: #later, add mutually assured destruction check (nathan/beardy)
            await ctx.react_quietly("🐻")
            try:
                usernotes_channel = get_guild_channel(self, guild_data["usernotes_channel"])
                for mentioned_member in ctx.message.mentions:
                   if mod_role not in mentioned_member.roles and mentioned_member is not self.bot.user:
                       try:
                           await mentioned_member.send("Hi. You're being kicked from Political Discourse. If you rejoin, please reread the rules.")
                       except discord.Forbidden:
                           pass
                       await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention}) was kicked from the server by {ctx.author.mention}\n--{ctx.message.jump_url}')
                       await ctx.guild.kick(mentioned_member)
                   else:
                       await ctx.react_quietly("⚠")
            except Exception as e:
                print(e)
                await ctx.react_quietly("⚠")
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def modvote(self, ctx):
        #TODO: add to redbear
        """`!modvote something` adds voting reactions to the message."""
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])
        if mod_role in ctx.author.roles:
            await ctx.react_quietly("🐻")
            try:
                await ctx.react_quietly("☑")
                await ctx.react_quietly("❎")
                await ctx.react_quietly("🤷")
                await ctx.send(f"{mod_role.mention}: A vote on the above issue is requested. React with a ☑ for Yes or a ❎ for No.")
                await ctx.message.pin()
            except Exception as e:
                print(e)
                await ctx.react_quietly("⚠")
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def slow(self,ctx, rate_limit_per_user = 10):  
        """Changes the amount of seconds a user has to wait before sending another message (0-120); bots, as well as users with the permission manage_messages or manage_channel, are unaffected.`
        !slow 10` rate limits users in the channel to 10 seconds per message. Use `!slow 0` or `!fast` to disable it."""
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])
        if mod_role in ctx.author.roles:
            await ctx.react_quietly("🐻")
            if rate_limit_per_user < 1:
                await ctx.react_quietly("⚠")
                return
            try:
                usernotes_channel = get_guild_channel(self, guild_data["usernotes_channel"])
                await ctx.channel.edit(slowmode_delay=rate_limit_per_user)
                await usernotes_channel.send(f"{ctx.author.mention} slowed {ctx.channel.mention} to {str(rate_limit_per_user)} seconds.\n--{ctx.message.jump_url}")
                await ctx.send(f"```\nThis channel is in slow mode. You can send one message every {str(rate_limit_per_user)} seconds. Please use the time between messages to take a breath, relax, and compose your thoughts.\n```")
            except discord.Forbidden:
                await ctx.send("bear is forbidden from editing the channel")
                await ctx.react_quietly("⚠")
            except discord.HTTPException:
                await ctx.send("editing the channel failed")
                await ctx.react_quietly("⚠")
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def fast(self, ctx): 
        """`!fast` sets the rate limit for the channel to `0`, disabling it."""
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])
        if mod_role in ctx.author.roles:
            await ctx.react_quietly("🐻")
            try:
                usernotes_channel = get_guild_channel(self, guild_data["usernotes_channel"])
                await ctx.channel.edit(slowmode_delay=0)
                await usernotes_channel.send(f"{ctx.author.mention} unslowed {ctx.channel.mention}.\n--{ctx.message.jump_url}")
            except discord.Forbidden:
                await ctx.react_quietly("⚠")
                await ctx.send("bear is forbidden from editing the channel")
            except discord.HTTPException:
                await ctx.send("editing the channel failed")
                await ctx.react_quietly("⚠")
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def add_role(self, ctx, role_id = 0):  # checked
        """
        `!add_role "rolename" @someone` Adds a role to a user.
        """
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])
        new_role = get_guild_role(ctx, role_id)

        if mod_role in ctx.author.roles:
            await ctx.react_quietly("🐻")

            if new_role is None or not new_role in ctx.guild.roles or len(ctx.message.mentions) == 0:
                await ctx.react_quietly("⚠")
                await ctx.send("`!add_role <'role_id'> <@someone> [@someoneelse ...]`")
                return
            if new_role is mod_role:
                await ctx.react_quietly("⚠")
                return

            try:
                usernotes_channel = get_guild_channel(self, guild_data["usernotes_channel"])
                for mentioned_member in ctx.message.mentions:
                    await mentioned_member.add_roles(new_role)
                    await usernotes_channel.send(f"`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention})'s {new_role.name} role was added by {ctx.author.mention}.\n--{ctx.message.jump_url}")
            except Exception as e:
                await ctx.react_quietly("⚠")
                await ctx.send("Error adding role.")
                print(e)
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def remove_role(self, ctx, role_id = 0): 
        """
        `!remove_role "rolename" @someone` Removes a role from a user.
        """
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])
        old_role = get_guild_role(ctx, role_id)

        if mod_role in ctx.author.roles:
            await ctx.react_quietly("🐻")

            if old_role is None or not old_role in ctx.guild.roles or len(ctx.message.mentions) == 0:
                await ctx.react_quietly("⚠")
                await ctx.send("`!remove_role <'role_id'> <@someone> [@someoneelse ...]`")
                return

            if old_role is mod_role:
                await ctx.react_quietly("⚠")
                return

            try:
                usernotes_channel = get_guild_channel(self, guild_data["usernotes_channel"])
                mute_role = get_guild_role(ctx, guild_data["mute_role"])
                for mentioned_member in ctx.message.mentions:
                    if mod_role not in mentioned_member.roles and old_role is not mute_role:
                        await mentioned_member.remove_roles(old_role)
                        await usernotes_channel.send(f"`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention})'s {old_role.name} role was removed by {ctx.author.mention}.\n--{ctx.message.jump_url}")
            except:
                await ctx.react_quietly("⚠")
                await ctx.send("Error removing role.")
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def userinfo(self, ctx):
        """
        `!userinfo @someone @someoneelse`: Prints information on members.
        `!userinfo: prints your own userinfo
        """
        await ctx.react_quietly("🐻")

        try:
            guild_data = await self.config.guild(ctx.guild).all()
            allowed_channels = guild_data["info_channels"]
            mod_role = get_guild_role(ctx, guild_data["moderator_role"])
            is_mod = mod_role in ctx.author.roles

            async def print_info(member):
                roles = [role.name for role in member.roles]
                join_age = datetime.datetime.utcnow() - member.joined_at
                join_age = join_age - datetime.timedelta(microseconds=join_age.microseconds)
                account_age = datetime.datetime.utcnow() - member.created_at
                account_age = account_age - datetime.timedelta(microseconds=account_age.microseconds)
                member_data = await self.config.member(member).all()
                is_muted = member_data["muted"]
                strikes = member_data["strikes"]
                spammer = member_data["spammer"]
                await ctx.send(f"`{member.name}`:`{member.id}` ({member.mention})'s info is:\njoined_at: `{member.joined_at.replace(microsecond=0)}` (`{join_age}` ago)\ncreated_at: `{member.created_at.replace(microsecond=0)}` (`{account_age}` ago)\nroles: `{roles}`\nspam_info: `{strikes}`\nis muted: `{is_muted}`\nspammer: `{spammer}`\navatar_url: <{member.avatar_url}>")

            if not str(ctx.channel.id) in allowed_channels and not is_mod:
                await ctx.react_quietly("🚫")
            elif len(ctx.message.mentions) > 0:
                for mentioned_member in ctx.message.mentions:                
                    if mentioned_member == ctx.author or is_mod:
                        await print_info(mentioned_member)
                    else:
                        await ctx.react_quietly("🚫")
            else:
                await print_info(ctx.author)


        except Exception as e:
            print(e)
            await ctx.react_quietly("⚠")

    @commands.command()
    #TODO: add to redbear
    async def emoji_metrics(self, ctx, days = 30):  # checked
        """`!emoji_metrics n`Adds up all the server emojis used in messages and reactions in each channel, up to `n` days ago."""
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])

        if mod_role in ctx.author.roles:
            await ctx.react_quietly("🐻")
            if days < 1:
                await ctx.react_quietly("⚠")
                return
            if self.counting_emoji:
                await ctx.react_quietly("⚠")
                await ctx.send("I'm still working on it from last time.")
                return
            try:
                self.counting_emoji = True
                emoji_count = {}
                for emoji in ctx.guild.emojis:
                    emoji_count[emoji] = 0
                after = datetime.datetime.utcnow() - datetime.timedelta(days=int(days))
                channel_counter = 0
                skip_channels = guild_data["skip_channels"]
                skipstring = build_skip_string(self, skip_channels)
                await ctx.send(f"Alright. I'm adding up all the server emojis used in messages and reactions in each channel, going up to {days} days ago.")
                await ctx.send(f"I'm skipping the following channels, as configured: {skipstring}")
                update_message = await ctx.send("Getting started.")
                for message_channel in ctx.guild.text_channels:
                    if str(message_channel.id) not in skip_channels:
                        await update_message.edit(content=f"checking {message_channel.mention} . Roughly {len(ctx.guild.text_channels) - channel_counter} channels left to go...")
                        channel_counter += 1
                        try:
                            async for channel_message in message_channel.history(limit=None, after=after):
                                for emoji in emoji_count:
                                    if str(emoji) in channel_message.content:
                                        emoji_count[emoji] += 1
                                    for channel_message_reaction in channel_message.reactions:
                                        if channel_message_reaction.emoji == emoji:
                                            emoji_count[emoji] += channel_message_reaction.count
                        except:
                            pass
                await update_message.delete()
                pending_message = ""
                emoji_counter = 0
                sorted_emoji = dict(OrderedDict(sorted(emoji_count.items(), key=lambda t: t[1], reverse=True)))
                for emoji in sorted_emoji:
                    if emoji.animated:
                        next_chunk = f"<a:{emoji.name}:{emoji.id}> : {sorted_emoji[emoji]}\n"
                    else:
                        next_chunk = f"<:{emoji.name}:{emoji.id}> : {sorted_emoji[emoji]}\n"
                    if len(pending_message) + len(next_chunk) < 2000 and emoji_counter < 26:
                        pending_message += next_chunk
                        emoji_counter += 1
                    else:
                        await ctx.send(pending_message)
                        pending_message = next_chunk
                        emoji_counter = 1
                if pending_message != "":
                    await ctx.send(pending_message)

            except Exception as e:
                await ctx.react_quietly("⚠")
                print(e)

            self.counting_emoji = False
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def user_metrics(self, ctx, days = 30):
        """`!user_metrics n` Adds up all the messages people have sent, up to `n` days ago."""
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])
        if mod_role in ctx.author.roles:
            await ctx.react_quietly("🐻")

            if days < 1:
                await ctx.react_quietly("⚠")
                return
            if self.counting_emoji:
                await ctx.react_quietly("⚠")
                await ctx.send("I'm still working on it from last time.")
                return

            try:
                if self.counting_users:
                    await ctx.send("I'm still working on it from last time.")
                else:
                    self.counting_users = True
                    user_count = {}
                    after = datetime.datetime.utcnow() - datetime.timedelta(days=int(days))
                    channel_counter = 0
                    skip_channels = guild_data["skip_channels"]
                    skipstring = build_skip_string(self, skip_channels)
                    await ctx.send(f"Alright. I'm adding up all the messages people have sent up to {days} days ago.")
                    await ctx.send(f"I'm skipping the following channels, as configured: {skipstring}")
                    update_message = await ctx.send("Getting started.")
                    for message_channel in ctx.guild.text_channels:
                        if str(message_channel.id) not in skip_channels:
                            await update_message.edit(content=f"checking {message_channel.mention} . Roughly {len(ctx.guild.text_channels) - channel_counter} channels left to go...")
                            channel_counter += 1
                            try:
                                async for channel_message in message_channel.history(limit=None, after=after):
                                    user_count.setdefault(channel_message.author.display_name, 0)
                                    user_count[channel_message.author.display_name] += 1
                            except:
                                pass
                    await update_message.edit(content=f"{len(user_count)}/{ctx.guild.member_count} members were active in the last {days} days")
                    pending_message = ""
                    sorted_users = dict(OrderedDict(sorted(user_count.items(), key=lambda t: t[1], reverse=True)))
                    for user in sorted_users:
                        next_chunk = f"{user}: {sorted_users[user]} ({round(sorted_users[user]/int(days))} per day)\n"
                        if len(pending_message) + len(next_chunk) < 2000:
                            pending_message += next_chunk
                        else:
                            await ctx.send(pending_message)
                            pending_message = next_chunk
                    if pending_message != "":
                        await ctx.send(pending_message)

            except Exception as e:
                await ctx.react_quietly("⚠")
                await ctx.send(f"{ctx.author.mention}: I encountered an error.")
                print(e)

            self.counting_users = False
        else:
            await message.add_reaction("🚫")

    @commands.command()
    async def reactcount_metrics(self, ctx, min_reacts = 0, days = 30, num_msgs = 5):  # checked
        """`!reactcount_metrics n`Adds up all the server emojis used in messages and reactions in each channel, up to `n` days ago."""
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])

        if mod_role in ctx.author.roles:        
            await ctx.react_quietly("🐻")
            try:
                if self.counting_reactions:
                    await ctx.send("I'm still working on it from last time.")
                elif days < 1 or num_msgs < 1 or min_reacts < 0:
                    await ctx.react_quietly("⚠")
                    await ctx.send("Usage: `!reactcount_metrics <min num reacts> <days> <messages to show>`")
                else:
                    self.counting_reactions = True
                    react_count = {}
                    message_dict = dict()

                    after = datetime.datetime.utcnow() - datetime.timedelta(days=int(days))
                    channel_counter = 0
                    skip_channels = guild_data["skip_channels"]
                    skipstring = build_skip_string(self, skip_channels)
                    await ctx.send(f"Alright. I'm checking all messages on the server and showing the top {num_msgs} with the most reactions (with at least {min_reacts} reactions), going up to {days} days ago.")
                    await ctx.send(f"I'm skipping the following channels, as configured: {skipstring}")
                    update_message = await ctx.send("Getting started.")

                    for message_channel in ctx.guild.text_channels:
                        if str(message_channel.id) not in skip_channels:
                            await update_message.edit(content=f"Checking {message_channel.mention}. Roughly {len(ctx.guild.text_channels) - channel_counter} channels left to go...")
                            channel_counter += 1
                            try:
                                async for channel_message in message_channel.history(limit=None, after=after):
                                    count = 0
                                    for channel_message_reaction in channel_message.reactions:
                                        count += channel_message_reaction.count
                                        
                                    if count >= min_reacts:
                                        react_count[channel_message.id] = count
                                        message_dict[channel_message.id] = channel_message
                            except:
                                pass

                    await update_message.delete()
                    pending_message = ""
                    msg_counter = 0
                    sorted_reactcount = dict(OrderedDict(sorted(react_count.items(), key=lambda t: t[1], reverse=True)))

                    for id in sorted_reactcount:
                        await GenerateSingleReactResult(message_dict[id], sorted_reactcount[id], ctx) 
                        msg_counter += 1
                        if msg_counter == num_msgs:
                            break

                    if msg_counter == 0:
                        await message.channel.send("No results. Curious!")

            except Exception as e:
                await message.add_reaction("⚠")
                print(e)

            self.counting_reactions = False
        else:
            await message.add_reaction("🚫")

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            guild_data = await self.config.guild(message.guild).all()
            mod_role = message.guild.get_role(int(guild_data["moderator_role"]))
            muted_role = message.guild.get_role(int(guild_data["mute_role"]))

            if message.author.bot:
                return

            if mod_role not in message.author.roles and muted_role not in message.author.roles:
                await spam_check(self, guild_data, message)
                #await content_check()
            
            if len(message.mentions) > 0 and self.bot.user in message.mentions:
                await message.add_reaction('🐻')            

        except Exception as e:
            print(e)
             
    @commands.Cog.listener()
    async def on_ready():
        print("yo")

# HELPER FUNCTIONS #

#TODOs: 
#1) convert this to use self.Config
#2) Provide a way to add/remove shitposts on the fly
#3) move to funbear
def get_shitposts(message):
    return ['the complexity of AI dictators and immortality,',
                          'this^^,',
                          'how shitposting belongs in offtopic',
                          'about south african weapons of mass destruction',
                          'about french politics',
                          'the national gun regime',
                          '*lyrical* complexity',
                          'the fact that roads are socialism',
                          'the obvious errors of the Clinton campaign',
                          'how bernie would have won',
                          'the corrupt implications of the leaked DNC emails',
                          'my fanfic about bernie sanders and hillary clinton',
                          'about our woke slay queen Hillary Clinton',
                          'how i\'m sorry I still read books - ',
                          'how the DNC stole the primary',
                          'how the electoral college stole the election',
                          'how trump won in a landslide',
                          'how the DNC stole clintonmas',
                          'how Trump voters were motivated by economic anxiety/racism/misogyny',
                          'how the dossier is real',
                          'how the dossier is fake ',
                          'how democrats need to stay the course',
                          'we need to all say "stop bedwetting, ed"',
                          '"i\'m freaking out, is this big?"',
                          'how trump won, get over it.',
                          'that poppyj is **always** right',
                          'the national importance of me asking "any news today guys?"',
                          'how capitalism is a better economic system than socialism',
                          'how socialism is a better economic system than capitalism',
                          'why Evan McMullin is a war criminal',
                          'why catgirls, as a concept, are banned,',
                          'broken windows',
                          'nazi punching',
                          'pepe',
                          'why antifascists are the real fascists',
                          'why fascists are the real antifascists',
                          'why Nate Silver must be eliminated',
                          'how 538 is fake news',
                          'how "please make me a mod" was the worst thing to say',
                          'when Democrats want a nuclear strike on Moscow',
                          'how {} is a Russian agent'.format(message.author.mention),
                          'why both sides are the same',
                          'about that stupid face swim used to make, ',
                          'why i always say "As a liberal/minority group, [opinion that is contrary to liberal\'s/that group\'s interest]"',
                          'why the Webster\'s dictionary is the best academic source on fascism',
                          'how Scalia was great for the Constitution',
                          'why citizens united was actually ok',
                          'the dialectic',
                          'acid privilege',
                          'how the beatles benefited from acid privilege',
                          'https://cdn.discordapp.com/attachments/204689269778808833/304046964037779487/unknown.png',
                          'anime',
                          'about the time gray volunteered for a buzzfeed interview',
                          'about how there needs to be a serious discussion about the state of this discord, sooner than later.']

#twitter
def get_tweet_urls(content):
    tweet_regex = re.compile(r"https://twitter\.com/[a-zA-Z0-9_]+/status/[0-9]+")
    return tweet_regex.findall(content)

#twitter
def get_tweet_id(content):
    tweet_status_regex = re.compile(r"([0-9]+)$")
    return int(tweet_status_regex.findall(tweet_url)[0])

def check_load_error(loaderrors, checkObj, string):
    result = False
    i = len(loaderrors)
    if string == "our_guild":
        bonusStr = " (as a result, no roles were set)"
    else:
        bonusStr = ""
    if checkObj is None:
        loaderrors[i] = f"{string} not set{bonusStr}."
    else:
        result = True
    return result

async def all_users_setdefault(self, member, timestamp:  datetime):
    # need to convert timestamp to iso 8601
    timestamp_str = timestamp.isoformat()
    await self.config.member(member).join_strikes.set(0)
    await self.config.member(member).joined_at.set(timestamp_str)
    await self.config.member(member).strikes.set(0)
    await self.config.member(member).last_check.set(timestamp_str)
    await self.config.member(member).last_message.set(None)
    await self.config.member(member).spammer.set(False)

async def spam_check(self, guild_data, message):
    """
    Checks a message for common spam techniques.
    """
    member_data = await self.config.member(message.author).all()
    usernotes_channel = get_guild_channel(self,guild_data["usernotes_channel"])
    muted_role = message.guild.get_role(int(guild_data["mute_role"]))
    #muted_role = get_guild_role(ctx, guild_data["mute_role"])
    timeout_channel = get_guild_channel(self, guild_data["timeout_channel"])
    last_check = member_data["last_check"]
    last_check = get_usable_date_time(last_check)
    #last_check = dateutil.parser.parse(last_check)

    if member_data["strikes"] < self.strike_limit:
        #time_passed = 10
        time_passed = message.created_at - last_check
        if len(message.mentions) > 3: # and embed role???? Why is this checked, not needed IMO
            await usernotes_channel.send(f'`{message.author.name}`:`{message.author.id}` ({message.author.mention}) was automatically muted for mentioning too many users in {message.channel.mention}.\n```\n{message.clean_content}\n```\n--{message.jump_url}')
            roles = [role.id for role in message.author.roles]
            await self.config.guild(message.guild).muted_members.set_raw(message.author.id, value = roles)
            await message.author.edit(roles=[muted_role])
            await timeout_channel.send(f'{message.author.mention}, you were automatically muted for mentioning too many users in {message.channel.mention}.')
            await self.config.member(message.author).strikes.set(0)
        if time_passed.total_seconds() < self.allowance or message.content == member_data["last_message"]:
            strikes = member_data["strikes"]
            await self.config.member(message.author).strikes.set(strikes+1)
        if (time_passed.total_seconds() > self.reset_period) and (member_data["strikes"] > 0):
            await self.config.member(message.author).strikes.set(member_data["strikes"]-1)  # Remove a strike
        ts = message.created_at.isoformat()
        await self.config.member(message.author).last_check.set(ts)
        await self.config.member(message.author).last_message.set(message.content)

    if member_data['strikes'] == self.strike_limit and member_data['spammer'] is False:
        await self.config.member(message.author).spammer.set(True)
        await self.config.member(message.author).strikes.set(0)

        def spammer_check(checked_message):
            return checked_message.author == spammer

        spammer = message.author
        em = make_embed_from_message(message)
        #if embed_role not in message.author.roles:
        #AMICI: I (strentax) changed this default behavior. Now, for WHOEVER spams, it purges strike_limit+1 
        await message.channel.purge(limit=(self.strike_limit+1), check=spammer_check)
        await usernotes_channel.send(f'`{message.author.name}`:`{message.author.id}` ({message.author.mention}) was automatically muted and their last {self.strike_limit + 1} messages purged for spammy behavior in {message.channel.mention}.\n--{message.jump_url}', embed=em)
        #else:
        #    await usernotes_channel.send(f'`{message.author.name}`:`{message.author.id}` ({message.author.mention}) was automatically muted for spammy behavior in {message.channel.mention}.\n--{message.jump_url}', embed=em)
        roles = [role.id for role in message.author.roles]
        await self.config.guild(message.guild).muted_members.set_raw(message.author.id, value = roles)

        await message.author.edit(roles=[muted_role])
        # await asyncio.sleep(5.0)
        await timeout_channel.send(f'{message.author.mention}, you were automatically muted for spammy behavior in {message.channel.mention}. Please send longer messages instead of a series of short fast ones.')
        await timeout_channel.send("Don't")
        await timeout_channel.send("write")
        await timeout_channel.send("like")
        await timeout_channel.send("this.")

async def content_check():
    return

def get_usable_date_time(str):
    dt = ""
    if str == "":
        dt = datetime.now()
    else:
        dt = dateutil.parser.parse(str)
    return dt

def get_guild_role(ctx, id):
    return ctx.guild.get_role(int(id))

def get_guild_channel(self, id):
    return self.bot.get_channel(int(id))

def build_skip_string(self, channel_dict):
    skipstring = ""
    for channel_id in channel_dict:
        if skipstring == "":
            skipstring = get_guild_channel(self, channel_id).name
        else:
            skipstring += f", {get_guild_channel(self, channel_id).name}"
    return skipstring

async def GenerateSingleReactResult(reactmessage, count, ctx):
    command_channel = ctx.channel
    log = f"**With {count} reacts:**\n"
    unknowncount = 0
    for reaction in reactmessage.reactions:
        anichar = ''
        try:
            if type(reaction.emoji) is discord.partial_emoji.PartialEmoji:
                if reaction.emoji.animated:
                    anichar = 'a'
                if reaction.emoji in ctx.guild.emojis:
                    log += f"<{anichar}:{reaction.emoji.name}:{reaction.emoji.id}>`{reaction.count}`  "
                else:
                    unknowncount += reaction.count
            else:
                log += f"{reaction.emoji}`{reaction.count}`  "
        except:
            unknowncount += reaction.count

    if unknowncount > 0:
        if unknowncount == 1:
            isare = 'is'
        else:
            isare = 'are'
        log += f" ({unknowncount} {isare} not PD-specific)"

    em = make_embed_from_message(reactmessage, 1)
    result_message = await ctx.send(content=log, embed=em)

def make_embed_from_message(message, friendly = 0):
    """
    Takes a discord message and returns an embed quoting it.
    :param message: a discord message object
    :return: discord.Embed object quoting the message.
    """
    description = message.clean_content
    if len(description) > 2047:
        description = f"{description[2044]}..."
    em = discord.Embed(description=description) 
    author = f"{message.author.display_name}"
    if friendly == 0:
        author += f" : {message.author.id}"
    else:
        author += f", in #{message.channel}:"
    em.set_author(name=author,
                  icon_url=message.author.avatar_url)
    return em