from redbot.core import commands, checks, Config
from redbot.core.utils.chat_formatting import box, humanize_list, pagify
import asyncio
import datetime
import dateutil
import discord
import logging
import re
import random
from TwitterAPI import TwitterAPI
#from redbot.core.utils.chat_formatting import box, humanize_list, pagify

class Redbear(commands.Cog):
    """My custom cog"""
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 12345678, force_registration=True)
        default_global = {
             "strike_limit": 5
        }
        self.config.register_global(**default_global)

        default_guild = {
            "member_commands": {},
            "muted_members": {},
            "mute_role": "",
            #"mute_2_role": "", flatten to mute_role
            "moderator_role": "",
            "usernotes_channel": "",
            "timeout_channel": ""
            #"embed_role": "",   #pd specific, put in separate cog
            #"interviewee_role": "",  #pd specific, put in separate cog
            #"modmute_role": ""  flatten to mute_role
        }
        self.config.register_guild(**default_guild)

        default_member = {
            "iam_roles": {},
            "personal_commands": {},            
            "muted": False,
            "strikes": 0,
            "join_strikes": 0,
            "joined_at": [],
            "last_check": [],
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
        
        #TODO: add all of these to Config and allow add/remove commands.
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
                 'No News'}  #self-assignable roles.
        #add line for self.pdbeat. pdbeat = pdbeat = TwitterAPI('')
        self.strike_limit = 5
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
    async def purge(self, ctx):  # checked
    #"""
    #`!purge 100` purges 100 messages.\n
    #`!purge @someone @someoneelse`: checks for messages in every channel up to two weeks ago for messages from the mentioned members and purges them. This is resource intensive.
    #"""
        #TODO: Add a warning? or something that says the config is not complete for "nocount-channels"
        guild_data = await self.config.guild(ctx.guild).all()
        mod_role = get_guild_role(ctx, guild_data["moderator_role"])
        usernotes_channel = get_guild_channel(self, guild_data["usernotes_channel"])

        if mod_role in ctx.author.roles and ctx.channel is not usernotes_channel:
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
                        for ichannel in ctx.message.guild.channels:
                            #if ichannel != self.tweets_channel:
                            # ^^^ Need to add back in. Do it w/ guild config section of protected channels
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
        if self.moderator_role in ctx.author.roles:
            try:
                channel_permissions = ctx.channel.overwrites_for(ctx.guild.default_role)
                channel_permissions.send_messages = False
                await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=channel_permissions)
                print(ctx.guild.default_role)
                print(channel_permissions)
                await ctx.react_quietly("🐻")
                await ctx.react_quietly("🔒")
                await self.usernotes_channel.send(f'{ctx.author.mention} locked {ctx.channel.mention}.\n--{ctx.message.jump_url}')
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
        if self.moderator_role in ctx.author.roles:
            try:
                channel_permissions = ctx.channel.overwrites_for(ctx.guild.default_role)
                channel_permissions.send_messages = True
                await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=channel_permissions)
                await ctx.react_quietly("🐻")
                await ctx.react_quietly("🔓")
                await self.usernotes_channel.send(f'{ctx.author.mention} unlocked {ctx.channel.mention}.\n--{ctx.message.jump_url}')
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
        if self.moderator_role in ctx.author.roles:
            await ctx.react_quietly("🐻")
            if user_id > 0:
                try:
                    fake_user = discord.Object(id=user_id)
                    member = ctx.guild.get_member(user_id)
                    if member is not None and self.moderator_role not in member.roles and member is not bot.user:
                        await ctx.guild.ban(member, delete_message_days=0)
                        await self.usernotes_channel.send(f'`{member.name}`:`{member.id}` ({member.mention}) was banned from the server by {ctx.author.mention}.\n--{ctx.message.jump_url}')
                    if member is None:
                        await ctx.guild.ban(fake_user, delete_message_days=0)
                        await self.usernotes_channel.send(f'User id `{fake_user.id}` was banned from the server by {ctx.author.mention}.\n--{ctx.message.jump_url}')
                except Exception as e:
                    await self.usernotes_channel.send(f"{ctx.author.mention} tried to ban user ID {user_id} but no user was found.\n--{ctx.message.jump_url}")
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
        if self.moderator_role in ctx.author.roles:
            await ctx.react_quietly("🐻")
            if len(user_id) > 0:
                try:
                    fake_banned_user = discord.Object(id=user_id)
                    await ctx.guild.unban(fake_banned_user)
                    await self.usernotes_channel.send(f'User id `{fake_banned_user.id}` was unbanned from the server by {ctx.author.mention}.\n--{ctx.message.jump_url}')
                except Exception as e:
                    await self.usernotes_channel.send(f"{ctx.author.mention} tried to ban user ID {user_id} but no user was found.\n--{ctx.message.jump_url}")
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
        if self.moderator_role in ctx.author.roles:
            await ctx.react_quietly("🐻")
            try:
                for mentioned_member in ctx.message.mentions:
                    if self.moderator_role not in mentioned_member.roles and mentioned_member is not bot.user:
                        await self.usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention}) was banned from the server by {ctx.author.mention}.\n--{ctx.message.jump_url}')
                        await ctx.guild.ban(mentioned_member, delete_message_days=0)
                    if str(ctx.message.id).endswith("1"):
                        await ctx.send('https://b.thumbs.redditmedia.com/GVgfjW-E0wafJbQHlv_XwyG7Ux3tnGZfHI_ExznRBzo.png')
            except Exception as e:
                print(e)
                await ctx.react_quietly("⚠")
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def userinfo(self, ctx):
        """
        `!userinfo @someone @someoneelse`: Prints information on members.
        """
        await ctx.react_quietly("🐻")
        try:
            for mentioned_member in ctx.message.mentions:
                allowed_channels = [self.bot_spam_channel.id, self.meta_channel.id]  
                if mentioned_member == ctx.author and ctx.channel.id in allowed_channels or self.moderator_role in ctx.author.roles:
                    roles = [role.name for role in mentioned_member.roles]
                    join_age = datetime.datetime.utcnow() - mentioned_member.joined_at
                    join_age = join_age - datetime.timedelta(microseconds=join_age.microseconds)
                    account_age = datetime.datetime.utcnow() - mentioned_member.created_at
                    account_age = account_age - datetime.timedelta(microseconds=account_age.microseconds)
                    is_muted = await self.config.user(mentioned_member).get_raw("muted")
                    strikes = await self.config.user(mentioned_member).strikes()
                    spammer = await self.config.user(mentioned_member).spammer()
                    await ctx.send(f"`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention})'s info is:\njoined_at: `{mentioned_member.joined_at.replace(microsecond=0)}` (`{join_age}` ago)\ncreated_at: `{mentioned_member.created_at.replace(microsecond=0)}` (`{account_age}` ago)\nroles: `{roles}`\nspam_info: `{strikes}`\nis muted: `{is_muted}`\nspammer: `{spammer}`\navatar_url: <{mentioned_member.avatar_url}>")
                else:
                    await ctx.react_quietly("🚫")
        except Exception as e:
            print(e)
            await ctx.react_quietly("⚠")

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

def get_tweet_urls(content):
    tweet_regex = re.compile(r"https://twitter\.com/[a-zA-Z0-9_]+/status/[0-9]+")
    return tweet_regex.findall(content)

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

async def all_users_setdefault(self, member, timestamp: datetime.datetime):
    # need to convert timestamp to iso 8601
    timestamp_str = timestamp.isoformat()
    await self.config.member(member).join_strikes.set(0)
    await self.config.member(member).joined_at.set(timestamp_str)
    await self.config.member(member).strikes.set(0)
    await self.config.member(member).last_check.set(timestamp_str)
    await self.config.member(member).last_message.set(None)
    await self.config.member(member).spammer.set( False)

def get_guild_role(ctx, id):
    return ctx.guild.get_role(int(id))

def get_guild_channel(self, id):
    return self.bot.get_channel(int(id))