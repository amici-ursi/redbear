from redbot.core import commands, checks, Config
from redbot.core.utils.chat_formatting import box, humanize_list, pagify
import asyncio
import datetime
import dateutil
import dateutil.parser
import discord
import logging
import re
import random
from collections import OrderedDict

#from redbot.core.utils.chat_formatting import box, humanize_list, pagify

class Funbear(commands.Cog):
    """My custom cog"""
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 12345679, force_registration=True)
        self.redbear_config = Config.get_conf(self, 12345678, False, "redbear")
        default_global = {
        }
        self.config.register_global(**default_global)

        default_guild = {
            "member_commands": {},
            "embed_role": "",
            "usernotes_channel": "",
            "skip_channels": {},
            "info_channels": {}
        }
        self.config.register_guild(**default_guild)

        default_member = {
            "personal_commands": {}
        }

        self.config.register_member(**default_member)

        #default_channel = {
            
        #}

        #self.config.register_channel(**default_channel)

        self.all_users = dict()

         # member_commands, personal_commands, muted_members


    @commands.command()
    @checks.admin()
    async def funsetup(self, ctx, embed_role = ""): #mute_role = "", mod_role = "", usernotes_channel = "", timeout_channel = "", moderator_channel = ""):
    #    """
    #    `Makes sure all necessary setup is complete.
    #    """
        await ctx.react_quietly("🐻")

        if embed_role == "":  #mute_role == "" and mod_role == "" and usernotes_channel == "" and timeout_channel == "" and moderator_channel == "":
            guild_data = await self.config.guild(ctx.guild).all()

            if not guild_data["embed_role"]:
                text = f"`embed_role` is not set.\n"
            else:
                text = f"`embed_role`: `{guild_data['embed_role']}`\n"

    #        if not guild_data["moderator_role"]:
    #            text += f"`moderator_role` is not set.\n"
    #        else:
    #            text += f"`moderator_role`: `{guild_data['moderator_role']}`\n"

    #        if not guild_data["usernotes_channel"]:
    #            text += f"`usernotes_channel` is not set.\n"
    #        else:
    #            text += f"`usernotes_channel`: `{guild_data['usernotes_channel']}`\n"

    #        if not guild_data["timeout_channel"]:
    #            text += f"`timeout_channel` is not set.\n"
    #        else:
    #            text += f"`timeout_channel`: `{guild_data['timeout_channel']}`\n"

    #        if not guild_data["moderator_channel"]:
    #            text += f"`moderator_channel` is not set.\n"
    #        else:
    #            text += f"`moderator_channel`: `{guild_data['moderator_channel']}`\n"
            
            text += f"\n```!funsetup embed_role```"
            await ctx.send(text)

        elif embed_role != "": # and mod_role != "" and usernotes_channel != "" and timeout_channel != "" and moderator_channel != "":
            #set the config up
            try:
                embed_role_actual = get_guild_role(ctx, embed_role) # discord.utils.get(ctx.guild.roles, id=int(mute_role))
            except:
                pass
            if embed_role_actual is None:
                await ctx.react_quietly("⚠")
                await ctx.send(f"No embed role found with ID `{embed_role}`.")
            else:
                await self.config.guild(ctx.guild).embed_role.set(embed_role)
                await ctx.send(f"Embed role successfully set to ID `{embed_role}`.")

    #        try:
    #            mod_role_actual = get_guild_role(ctx, mod_role) #discord.utils.get(ctx.guild.roles, id=int(mod_role))
    #        except:
    #            pass
    #        if mod_role_actual is None:
    #            await ctx.react_quietly("⚠")
    #            await ctx.send(f"No mod role found with ID `{mod_role}`.")
    #        else:
    #            await self.config.guild(ctx.guild).moderator_role.set(mod_role)  
    #            await ctx.send(f"Mod role successfully set to ID `{mod_role}`.")

    #        try:
    #            usernotes_channel_actual = get_guild_channel(self, usernotes_channel) #self.bot.get_channel(int(usernotes_channel))
    #        except:
    #            pass
    #        if usernotes_channel_actual is None:
    #            await ctx.react_quietly("⚠")
    #            await ctx.send(f"No usernotes channel found with ID `{usernotes_channel}`.")
    #        else:
    #            await self.config.guild(ctx.guild).usernotes_channel.set(usernotes_channel)
    #            await ctx.send(f"Usernotes channel successfully set to ID `{usernotes_channel}`.")

    #        try:
    #            timeout_channel_actual = get_guild_channel(self, timeout_channel) #self.bot.get_channel(int(timeout_channel))
    #        except:
    #            pass
    #        if timeout_channel_actual is None:
    #            await ctx.react_quietly("⚠")
    #            await ctx.send(f"No timeout channel channel found with ID `{timeout_channel}`.")
    #        else:
    #            await self.config.guild(ctx.guild).timeout_channel.set(timeout_channel)
    #            await ctx.send(f"Timeout channel successfully set to ID `{timeout_channel}`.")

    #        try:
    #            moderator_channel_actual = get_guild_channel(self, moderator_channel) #self.bot.get_channel(int(timeout_channel))
    #        except:
    #            pass
    #        if moderator_channel_actual is None:
    #            await ctx.react_quietly("⚠")
    #            await ctx.send(f"No moderator channel channel found with ID `{moderator_channel}`.")
    #        else:
    #            await self.config.guild(ctx.guild).moderator_channel.set(moderator_channel)
    #            await ctx.send(f"Moderator channel successfully set to ID `{moderator_channel}`.")

        else:
            await ctx.react_quietly("⚠")
            await ctx.send(f"Usage: !funsetup `embed_role_id`")

    #@commands.command()
    #@checks.admin()
    #async def skipchannel(self, ctx, addremove = "", channel_id = 0):
    #    """
    #    `!skipchannelsetup [add/remove] [channel_id]. The code here is the same as infochannel so update both
    #    """
    #    await ctx.react_quietly("🐻")
    #    if addremove == "add" or addremove == "remove":
    #        if channel_id > 0:
    #            channel = self.bot.get_channel(channel_id)
    #            if channel in ctx.guild.channels:
    #                async with self.config.guild(ctx.guild).skip_channels() as skipchannels:
    #                    if addremove=="add":
    #                        skipchannels[channel_id] = ""
    #                        await ctx.send(f"`{channel.name}:{channel_id}` added to channels to skip.")
    #                    elif str(channel_id) in skipchannels:
    #                        skipchannels.pop(str(channel_id))
    #                        await ctx.send(f"`{channel.name}:{channel_id}` removed from channels to skip.")
    #                    else:
    #                        await ctx.react_quietly("⚠")
    #                        await ctx.send("Nothing to remove.")
    #            else:
    #                await ctx.react_quietly("⚠")
    #                await ctx.send(f"Channel ID `{channel_id}` doesn't seem to be in this server.")
    #        else:
    #            await ctx.react_quietly("⚠")
    #            await ctx.send(f"A valid `channel_id` must be provided.")
    #    else:
    #        await ctx.send(f"Usage: !skipchannel [`\"add\" or \"remove\"`] [`channel_id`]")
    #        skipped = await self.config.guild(ctx.guild).skip_channels()
    #        if skipped is not None:
    #            content = f"The following channels are being skipped for certain commands:\n"
    #            for key in skipped:
    #                channel = self.bot.get_channel(int(key))
    #                content += f"`{channel.name}:{key}` "
    #            await ctx.send(content)
    
    #@commands.command()
    #async def infochannel(self, ctx, addremove = "", channel_id = 0):
    #    """
    #    `!infochannel [add/remove] [channel_id] . The code here is the same as skipchannel so update both
    #    """
    #    await ctx.react_quietly("🐻")
    #    if addremove == "add" or addremove == "remove":
    #        if channel_id > 0:
    #            channel = self.bot.get_channel(channel_id)
    #            if channel in ctx.guild.channels:
    #                async with self.config.guild(ctx.guild).info_channels() as info_channels:
    #                    if addremove=="add":
    #                        info_channels[channel_id] = ""
    #                        await ctx.send(f"`{channel.name}:{channel_id}` added to eligible !userinfo channels.")
    #                    elif str(channel_id) in skipchannels:
    #                        info_channels.pop(str(channel_id))
    #                        await ctx.send(f"`{channel.name}:{channel_id}` removed from eligible !userinfo channels.")
    #                    else:
    #                        await ctx.react_quietly("⚠")
    #                        await ctx.send("Nothing to remove.")
    #            else:
    #                await ctx.react_quietly("⚠")
    #                await ctx.send(f"Channel ID `{channel_id}` doesn't seem to be in this server.")
    #        else:
    #            await ctx.react_quietly("⚠")
    #            await ctx.send(f"A valid `channel_id` must be provided.")
    #    else:
    #        await ctx.send(f"Usage: !infochannel [`\"add\" or \"remove\"`] [`channel_id`]")
    #        infochannels = await self.config.guild(ctx.guild).info_channels()
    #        if infochannels is not None:
    #            content = f"The following channels are OK to use !userinfo:\n"
    #            for key in infochannels:
    #                channel = self.bot.get_channel(int(key))
    #                content += f"`{channel.name}:{key}` "
    #            await ctx.send(content)
    
    @commands.command()
    @checks.is_owner()
    async def baned(self, ctx):  # checked
        """
        `baned`: Sends a random baned cat to the message channel.
        """
        baned_cats = (
                    'http://i.imgur.com/Pn4BFLj.jpg', 'http://i.imgur.com/xtmyPBN.jpg',
                    'http://i.imgur.com/avVmttp.jpg', 'http://i.imgur.com/58wFteM.jpg',
                    'http://i.imgur.com/UPOqky8.jpg', 'http://i.imgur.com/HOeaLRz.jpg',
                    'http://i.imgur.com/AKhPIXr.jpg')
        await ctx.react_quietly("🐻")
        try:
            await ctx.send(random.choice(baned_cats))
        except Exception as e:
            print(f"baned: {e}")
            await ctx.react_quietly("⚠")

    @commands.command()
    async def shitposting(self, ctx):
        guild_data = await self.config.guild(ctx.guild).all()
        redbear_data = await self.redbear_config.guild(ctx.guild).all()
        embed_role = get_guild_role(ctx, guild_data["embed_role"])
        moderator_role = get_guild_role(ctx, redbear_data["moderator_role"])
        
        if embed_role in ctx.author.roles or moderator_role in ctx.author.roles:
            copypasta_text = get_shitposts(ctx)
            await ctx.send('look, until you get your shit together i really don\'t have the time to explain {} to a kid'.format(random.choice(copypasta_text)))
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def mod(self, ctx): 
        """
        `!mod @someone @someoneelse`: Shuffles the characters in members names.
        """
        redbear_data = await self.redbear_config.guild(ctx.guild).all()
        moderator_role = get_guild_role(ctx, redbear_data["moderator_role"])
        usernotes_channel = get_guild_channel(self, redbear_data["usernotes_channel"])
        if moderator_role in ctx.author.roles:
            await ctx.react_quietly("🐻")
            try:
                for mentioned_member in ctx.message.mentions:
                    if moderator_role not in mentioned_member.roles and mentioned_member is not self.bot.user:
                            nickname = ''.join(random.sample(mentioned_member.display_name, len(mentioned_member.display_name)))
                            await mentioned_member.edit(nick=nickname)
                            await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention})\'s display name was modded by {ctx.author.mention}.\n--{ctx.message.jump_url}')
            except Exception as e:
                print(f"mod: {e}")
                await ctx.react_quietly("⚠")
        else:
            await ctx.react_quietly("🚫")

    @commands.command()
    async def unmod(self, ctx):  # checked
        """
        `!mod @someone @someoneelse`: Shuffles the characters in members names.
        """
        redbear_data = await self.redbear_config.guild(ctx.guild).all()
        moderator_role = get_guild_role(ctx, redbear_data["moderator_role"])
        usernotes_channel = get_guild_channel(self, redbear_data["usernotes_channel"])
        if moderator_role in ctx.author.roles:
            await ctx.react_quietly("🐻")
            try:
                for mentioned_member in ctx.message.mentions:
                    if moderator_role not in mentioned_member.roles and mentioned_member is not self.bot.user:
                        await mentioned_member.edit(nick=None)
                        await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention})\'s display name was unmodded by {ctx.author.mention}.\n--{ctx.message.jump_url}')
            except Exception as e:
                print(f"unmod: {e}")
                await ctx.react_quietly("⚠")
        else:
            await ctx.react_quietly("🚫")

        @commands.Cog.listener()
        async def on_message(self, message):
            try:
                #guild_data = await self.config.guild(message.guild).all()
                #mod_role = message.guild.get_role(int(guild_data["moderator_role"]))  #no CTX here so get roles the "hard" way
                #muted_role = message.guild.get_role(int(guild_data["mute_role"]))

                if message.author.bot:
                    return
   
            except Exception as e:
                print(e)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        return

    @commands.Cog.listener()
    async def on_member_update(self, before, after):  # checked
        if self.bot.is_ready():
            #try:
            #    guild_data = await self.config.guild(after.guild).all()
            #    moderator_role = after.guild.get_role(int(guild_data["moderator_role"]))
            #    muted_role = after.guild.get_role(int(guild_data["mute_role"]))
            #    timeout_channel = get_guild_channel(self, guild_data["timeout_channel"])
            #    member_data = await self.config.member(after).all()
            #    await all_users_setdefault(self, before, datetime.datetime.utcnow())
            #    if before.roles != after.roles:
            #        await asyncio.sleep(2.0)
            #        added_roles = [role for role in after.roles if role not in before.roles]
            #        removed_roles = [role for role in before.roles if role not in after.roles]

            #        if moderator_role not in after.roles and added_roles == [muted_role]:
            #            roles = [role.id for role in before.roles]
            #            await self.config.member(after).muted.set(True)
            #            await self.config.guild(after.guild).muted_members.set_raw(after.id, value = roles)
            #            await after.edit(roles=[muted_role])
            #            await asyncio.sleep(5.0)
            #            await timeout_channel.send(f'{after.mention}. \'You were muted because you broke the rules. Reread them, then write `@{moderator_role.name}` to be unmuted.\nMessage history is disabled in this channel. If you tab out, or select another channel, the messages will disappear.\'')
            #        if moderator_role not in after.roles and removed_roles == [muted_role]:
            #            await after.remove_roles(muted_role)
            #            await self.config.member(after).muted.set(False)
            #            oldroles = await self.config.guild(after.guild).muted_members.get_raw(after.id)
            #            for role_id in oldroles:
            #                try:
            #                    thisrole = after.guild.get_role(role_id)
            #                    await after.add_roles(thisrole)
            #                except Exception as e:
            #                    pass
            #            await self.config.guild(after.guild).muted_members.set_raw(after.id, value = "")
            #except Exception as e:
            #    print(e)
            return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
      #if self.bot.is_ready:
        #guild = self.bot.get_guild(payload.guild_id)
        #guild_data = await self.config.guild(guild).all()
        #payload_message_channel = get_guild_channel(self, payload.channel_id)
        #try:
        #    payload_message = await payload_message_channel.fetch_message(payload.message_id)
        #except discord.errors.NotFound:
        #    return
        #try:
        #    if payload.member != self.bot:
        #        if payload.emoji.name == "❗":
        #            await payload_message.add_reaction('👮')
        #            await payload_message.remove_reaction(payload.emoji, payload.member)
        #            mod_channel = get_guild_channel(self, guild_data["moderator_channel"])
        #            usernotes_channel = get_guild_channel(self, guild_data["usernotes_channel"])
        #            em = make_embed_from_message(payload_message)
        #            content = f"{payload.member.mention} reported this message in {payload_message.channel.mention}:\n--{payload_message.jump_url}"
        #            await mod_channel.send(content=content, embed=em)
        #            await usernotes_channel.send(content=content, embed=em)
        #except discord.DiscordException as e:
        #    await payload_message.add_reaction("⚠")
        #    print(e)
        return
             
    @commands.Cog.listener()
    async def on_ready(self):
        print("yo")

# HELPER FUNCTIONS #

def get_shitposts(ctx):
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
                          'how {} is a Russian agent'.format(ctx.author.mention),
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

def get_usable_date_time(str):
    dt = ""
    if str == "":
        dt = datetime.datetime.utcnow()
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