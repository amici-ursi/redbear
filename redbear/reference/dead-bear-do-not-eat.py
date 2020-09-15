import discord
import re
import random
import urllib.parse
import urllib.request
import urllib.error
import asyncio
import pickle
import datetime
import requests
from TwitterAPI import TwitterAPI
import wikipedia
import matplotlib.pyplot as plt
from collections import OrderedDict
import os
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import textwrap
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
import time
import csv
from itertools import cycle
from matplotlib.ticker import StrMethodFormatter
from contextlib import closing
import codecs


client = discord.Client()
our_guild_id = 306442607905734656
our_guild = None
interviewee_role_name = "interviewee"
interviewee_role = None
embed_role_name = 'embed'
embed_role = None
muted_role_name = 'mute-1'
muted_role = None
modmute_role_name = 'modmute'
modmute_role = None
mute_2_role_id = 348895717789663233
mute_2_role = None
moderator_role_id = 306646485477621760
moderator_role = None
interview_channel_id = 306927738780909571
interview_channel = None
usernotes_channel_id = 306764710710214656
usernotes_channel = None
timeout_channel_id = 306928042830331907
timeout_channel = None
help_commands_channel_id = 443987113789227018
help_commands_channel = None
beardy_channel_id = 429845898151985182
beardy_channel = None
amici_id = 125341170896207872
amici = None
sy_id = 164918332221292544
curated_news_channel_id = 398154997109489664
curated_news_channel = None
tweets_channel_id = 312616534105260032
tweets_channel = None
low_effort_channel_id = 306760210200920074
low_effort_channel = None
bot_spam_channel_id = 351549261730545674
bot_spam_channel = None
copied_messages_in_curated = {}
mute_regex = re.compile(
    r"(GrhN5yhmJC8|pornhub\.com|blackdickfever|nigg(a|er)|retard|twitter\.com/therealTimanfya|captainacab742|\({3}.+\){3}|binch)")  # messages with this regex will be muted
has_spaces = re.compile(r"\s\w*\s")
username_and_discriminator_regex = re.compile(r"@.*#[0-9]{4}")
pd_settings = {}
baned_cats = (
    'http://i.imgur.com/Pn4BFLj.jpg', 'http://i.imgur.com/xtmyPBN.jpg',
    'http://i.imgur.com/avVmttp.jpg', 'http://i.imgur.com/58wFteM.jpg',
    'http://i.imgur.com/UPOqky8.jpg', 'http://i.imgur.com/HOeaLRz.jpg',
    'http://i.imgur.com/AKhPIXr.jpg')
all_users = {}  # leave blank
allowance = 3  # minimum time frame between messages to receive a strike for spam
reset_period = 5  # time frame between messages to remove a spam strike
join_allowance = 14
join_reset_period = 300
banned_names = ('evan c', 'buffwea', 'awesomesaucer9', 'oxhorn')
wolfram_id = ''
channel_list = set()
rate_limit_period = 10
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
pdbeat = pdbeat = TwitterAPI('')
tweet_regex = re.compile(r"https://twitter\.com/[a-zA-Z0-9_]+/status/[0-9]+")
tweet_status_regex = re.compile(r"([0-9]+)$")
no_copypasta_channels = [306924977981095936, 314146955372527618]
av_api_key = ''
beardy_role = None
emoji_log_lock = False
strike_limit = 5
try:
    with open('pd_settings.p', 'rb') as pfile:
        pd_settings = pickle.load(pfile)
except FileNotFoundError:
    print("Commands file not found.")
    pd_settings = {'member_commands': {}, 'personal_commands': {}}
    with open('pd_settings.p', 'wb') as pfile:
        pickle.dump(pd_settings, pfile)
all_users = dict()
token = ''
user_log_lock = False
last_50 = {}


def get_things():
    global our_guild
    while our_guild is None:
        time.sleep(5)
        our_guild = client.get_guild(our_guild_id)
        if our_guild is None:
            print("our_guild is None")
            time.sleep(5)
    global usernotes_channel
    while usernotes_channel is None:
        usernotes_channel = client.get_channel(usernotes_channel_id)
        if usernotes_channel is None:
            print("usernotes_channel is None")
            time.sleep(5)
    global timeout_channel
    while timeout_channel is None:
        timeout_channel = client.get_channel(timeout_channel_id)
        if timeout_channel is None:
            print("timeout_channel is None")
            time.sleep(5)
    global interview_channel
    while interview_channel is None:
        interview_channel = client.get_channel(interview_channel_id)
        if interview_channel is None:
            print("interview_channel is None")
            time.sleep(5)
    global amici
    while amici is None:
        amici = client.get_user(amici_id)
        if amici is None:
            print("amici is None")
            time.sleep(5)
    global beardy_channel
    while beardy_channel is None:
        beardy_channel = client.get_channel(beardy_channel_id)
        if beardy_channel is None:
            print("beardy channel is None")
            time.sleep(5)
    global muted_role
    while muted_role is None:
        muted_role = discord.utils.get(our_guild.roles, name=muted_role_name)
        if muted_role is None:
            print("muted role is None")
            time.sleep(5)
    global mute_2_role
    while mute_2_role is None:
        mute_2_role = discord.utils.get(our_guild.roles, id=mute_2_role_id)
        if mute_2_role is None:
            print("mute 2 role is None")
            time.sleep(5)
    global moderator_role
    while moderator_role is None:
        moderator_role = discord.utils.get(our_guild.roles, id=moderator_role_id)
        if moderator_role is None:
            print("moderator role is None")
            time.sleep(5)
    global embed_role
    while embed_role is None:
        embed_role = discord.utils.get(our_guild.roles, name=embed_role_name)
        if embed_role is None:
            print("embed role is None")
            time.sleep(5)
    global interviewee_role
    while interviewee_role is None:
        interviewee_role = discord.utils.get(our_guild.roles, name=interviewee_role_name)
        if interviewee_role is None:
            print("interviewee role is None")
            time.sleep(5)
    global beardy_role
    while beardy_role is None:
        beardy_role = discord.utils.get(our_guild.roles, name='Beardy')
        if beardy_role is None:
            print("beardy role is None")
            time.sleep(5)
    global help_commands_channel
    while help_commands_channel is None:
        help_commands_channel = client.get_channel(help_commands_channel_id)
        if help_commands_channel is None:
            print("help commands channel is None")
            time.sleep(5)
    global curated_news_channel
    while curated_news_channel is None:
        curated_news_channel = client.get_channel(curated_news_channel_id)
        if curated_news_channel is None:
            print("curated_news_channel is None")
            time.sleep(5)
    global modmute_role
    while modmute_role is None:
        modmute_role = discord.utils.get(our_guild.roles, name=modmute_role_name)
        if modmute_role is None:
            print("modmute_role is None")
            time.sleep(5)
    for member in list(pd_settings['muted_members']):
        member = our_guild.get_member(member)
        if member is not None and muted_role not in member.roles and mute_2_role not in member.roles and modmute_role not in member.roles:
            pd_settings['muted_members'].pop(member.id, None)

@client.event
async def on_ready():
    global amici
    try:
        get_things()
        await usernotes_channel.send('Restarted and ready.\nhttps://i.imgur.com/EIUKsjg.mp4')
    except Exception as e:
        print(e)
        try:
            if type(amici) is int or amici is None:
                amici = client.get_user(amici)
                get_things()
            await amici.send("New `on_ready` error captured:\n```\n{0}\n```".format(e))
        except Exception as e:
            print(e)


def all_users_setdefault(member, timestamp):
    all_users.setdefault(member.id, {'join_strikes': 0, 'joined_at': timestamp, 'strikes': 0, 'last_check': timestamp, 'last_message': None, 'spammer': False})


async def shitposting(message):  # checked
    """
    `!shitposting` sends various shitty copypastas to the message channel.
    """
    if embed_role in message.author.roles or moderator_role in message.author.roles:
        copypasta_text = ['the complexity of AI dictators and immortality,',
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
        await message.channel.send('look, until you get your shit together i really don\'t have the time to explain {} to a kid'.format(random.choice(copypasta_text)))
    else:
        await message.add_reaction("🚫")


async def spam_check(message):  # checked
    """
    Checks a message for common spam techniques.
    """
    global all_users
    if all_users[message.author.id]['strikes'] < strike_limit:
        time_passed = message.created_at - all_users[message.author.id]['last_check']
        if len(message.mentions) > 3 and embed_role not in message.author.roles:
            await usernotes_channel.send(f'`{message.author.name}`:`{message.author.id}` ({message.author.mention}) was automatically muted for mentioning too many users in {message.channel.mention}.\n```\n{message.clean_content}\n```\n--{message.jump_url}')
            roles = [role.id for role in message.author.roles]
            pd_settings['muted_members'][message.author.id] = {'roles': roles}
            with open('pd_settings.p', 'wb') as pfile:
                pickle.dump(pd_settings, pfile)
            await message.author.edit(roles=[muted_role])
            await asyncio.sleep(5.0)
            await timeout_channel.send(f'{message.author.mention}, you were automatically muted for mentioning too many users in {message.channel.mention}.')
            all_users[message.author.id]['strikes'] = 0
        if time_passed.total_seconds() < allowance or message.content == all_users[message.author.id]['last_message']:
            all_users[message.author.id]['strikes'] += 1  # Add a strike
        if (time_passed.total_seconds() > reset_period) and (all_users[message.author.id]['strikes'] > 0):
            all_users[message.author.id]['strikes'] -= 1  # Remove a strike
        all_users[message.author.id]['last_check'] = message.created_at
        all_users[message.author.id]['last_message'] = message.content
    if all_users[message.author.id]['strikes'] == strike_limit and all_users[message.author.id]['spammer'] is False:
        all_users[message.author.id]['spammer'] = True
        all_users[message.author.id]['strikes'] = 0

        def spammer_check(checked_message):
            return checked_message.author == spammer

        spammer = message.author
        em = make_embed_from_message(message)
        if embed_role not in message.author.roles:
            await message.channel.purge(limit=100, check=spammer_check)
            await usernotes_channel.send(f'`{message.author.name}`:`{message.author.id}` ({message.author.mention}) was automatically muted and their last 100 messages purged for spammy behavior in {message.channel.mention}.\n--{message.jump_url}', embed=em)
        else:
            await usernotes_channel.send(f'`{message.author.name}`:`{message.author.id}` ({message.author.mention}) was automatically muted for spammy behavior in {message.channel.mention}.\n--{message.jump_url}', embed=em)
        roles = [role.id for role in message.author.roles]
        pd_settings['muted_members'][message.author.id] = {'roles': roles}
        with open('pd_settings.p', 'wb') as pfile:
            pickle.dump(pd_settings, pfile)
        await message.author.edit(roles=[muted_role])
        await asyncio.sleep(5.0)
        await timeout_channel.send(f'{message.author.mention}, you were automatically muted for spammy behavior in {message.channel.mention}. Please send longer messages instead of a series of short fast ones.')
        await timeout_channel.send("Don't")
        await timeout_channel.send("write")
        await timeout_channel.send("like")
        await timeout_channel.send("this.")


async def content_check(message):  # checked
    """
    Checks a message for disallowed content.
    """
    message_lower = message.content.lower()
    if message_lower == '.' or re.search(has_spaces, message.content) is not None and message.content.upper() == message.content and message.content != "༼ つ ◕◕ ༽つ" and message.channel.id in no_copypasta_channels:
        await message.delete()
        return
    if re.search(mute_regex, message_lower) is not None:
        roles = [role.id for role in message.author.roles]
        pd_settings['muted_members'][message.author.id] = {'roles': roles}
        with open('pd_settings.p', 'wb') as pfile:
            pickle.dump(pd_settings, pfile)
        await message.author.edit(roles=[muted_role])
        await message.delete()
        em = make_embed_from_message(message)
        await usernotes_channel.send(f'`{message.author.name}`:`{message.author.id}` ({message.author.mention}) was automatically muted and their message deleted for saying a blacklisted keyword in this message in {message.channel.mention}.\n--{message.jump_url}', embed=em)
        await asyncio.sleep(5.0)
        em = make_embed_from_message(message)
        await timeout_channel.send(content=f'{message.author.mention}, you were automatically muted for saying a blacklisted keyword in this message in {message.channel.mention}.\n--{message.jump_url}\nCensor your slurs. (╯°□°）╯︵ ┻━┻', embed=em)


async def do_wolfram(message):  # checked
    """
    `!wolfram question`: Submits a query to WolfphramAlpha
    """
    if embed_role in message.author.roles or moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        await message.channel.trigger_typing()
        wolfram_query = urllib.parse.quote(message.content[8:])
        wolfram_url = f"http://api.wolframalpha.com/v1/result?appid={wolfram_id}&i={wolfram_query}"
        try:
            wolfram_reply = urllib.request.urlopen(wolfram_url, data=None, timeout=6)
            wolfram_reply = wolfram_reply.read().decode("utf-8")
            await message.channel.send(content=f"{message.author.mention}: {wolfram_reply}")
        except urllib.error.HTTPError as e:
            if e.code == 501:
                await message.channel.send(f"{message.author.mention}: Your given input value cannot be interpreted by this API. This is commonly caused by input that is misspelled, poorly formatted or otherwise unintelligible. Because this API is designed to return a single result, this message may appear if no sufficiently short result can be found. You may occasionally receive this status when requesting information on topics that are restricted or not covered.")
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def coin_flip(message):  # checked
    """
    `!coin_flip`: Flips a coin.
    """
    if moderator_role in message.author.roles or embed_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            if moderator_role in message.author.roles and message.created_at.minute % 2 == 0:
                coin = "Tails"
                coin_file = open('{}.png'.format(coin), 'rb')
                discord_file = discord.File('{}.png'.format(coin), filename="coin.jpg")
            else:
                coin = random.choice(['Heads', 'Tails'])
                coin_file = open('{}.png'.format(coin), 'rb')
                discord_file = discord.File('{}.png'.format(coin), filename="coin.jpg")
            await message.channel.send(file=discord_file, content=coin)
            coin_file.close()
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def purge(message):  # checked
    """
    `!purge 100` purges 100 messages.\n
    `!purge @someone @someoneelse`: checks the last 1,000,000 messages in every channel up to two weeks ago for messages from the mentioned members and purges them. This is resource intensive.
    """
    if moderator_role in message.author.roles and message.channel is not usernotes_channel:
        try:
            if len(message.mentions) == 0 and len(message.content.split(' ')) == 2:
                purge_number = int(message.content.split(' ')[1])
                await usernotes_channel.send(f'{message.author.mention} purged {purge_number} messages in {message.channel.mention}.\n--{message.jump_url}')
                await message.channel.purge(limit=purge_number, check=None)
            for mentioned_member in message.mentions:
                if moderator_role not in mentioned_member.roles and mentioned_member is not client.user:
                    def purge_check(checked_message):
                        message_age = datetime.datetime.utcnow() - checked_message.created_at
                        day_limit = datetime.timedelta(days=13)
                        if message_age < day_limit:
                            return checked_message.author == mentioned_member

                    await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention})\'s messages were purged by {message.author.mention}.\n--{message.jump_url}')
                    for ichannel in message.guild.channels:
                        try:
                            await ichannel.purge(limit=1000000, check=purge_check)
                        except AttributeError:
                            pass
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def lock(message):  # checked
    """
    `!lock`: Denies the `send_message` permission for `@everyone` in the channel.
    """
    if moderator_role in message.author.roles:
        try:
            channel_permissions = message.channel.overwrites_for(message.guild.default_role)
            channel_permissions.send_messages = False
            await message.channel.set_permissions(message.guild.default_role, overwrite=channel_permissions)
            await message.add_reaction("🐻")
            await message.add_reaction("🔒")
            await usernotes_channel.send(f'{message.author.mention} locked {message.channel.mention}.\n--{message.jump_url}')
            if message.channel.name.endswith("🔒") is False:
                await message.channel.edit(name=f"{message.channel.name}🔒")
        except Exception as e:
            await message.add_reaction("⚠")
            print(e)
    else:
        await message.add_reaction("🚫")


async def unlock(message):  # checked
    """
    `!unlock`: Allows the `send_message` permission for `@everyone` in the channel.
    """
    if moderator_role in message.author.roles:
        try:
            channel_permissions = message.channel.overwrites_for(message.guild.default_role)
            channel_permissions.send_messages = True
            await message.channel.set_permissions(message.guild.default_role, overwrite=channel_permissions)
            await message.add_reaction("🐻")
            await message.add_reaction("🔓")
            await usernotes_channel.send(f'{message.author.mention} unlocked {message.channel.mention}.\n--{message.jump_url}')
            if message.channel.name.endswith("🔒"):
                await message.channel.edit(name=message.channel.name[:-1])
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def ban_id(message):  # checked
    """
    `!ban_id 125341170896207872`: Bans a user according to their Discord user id.
    """
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        if len(message.content.split(' ')) == 2:
            try:
                user_id = int(message.content.split(' ')[1])
                fake_user = discord.Object(id=user_id)
                member = message.guild.get_member(user_id)
                if member is not None and moderator_role not in member.roles and member is not client.user:
                    await message.guild.ban(member, delete_message_days=0)
                    await usernotes_channel.send(f'`{member.name}`:`{member.id}` ({member.mention}) was banned from the server by {message.author.mention}.\n--{message.jump_url}')
                if member is None:
                    await message.guild.ban(fake_user, delete_message_days=0)
                    await usernotes_channel.send(f'User id `{fake_user.id}` was banned from the server by {message.author.mention}\n--{message.jump_url}')
            except Exception as e:
                print(e)
                await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def unban_id(message):  # checked
    """
    `!unban_id 125341170896207872`: Unbans a user according to their Discord user id.
    """
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        message_lower = message.content.lower()
        if len(message_lower.split(' ')) == 2:
            try:
                user_id = int(message_lower.split(' ')[1])
                fake_banned_user = discord.Object(id=user_id)
                await message.guild.unban(fake_banned_user)
                await usernotes_channel.send(f'User id `{fake_banned_user.id}` was unbanned from the server by {message.author.mention}.\n--{message.jump_url}')
            except Exception as e:
                print(e)
                await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def ban(message):  # checked
    """
    `!ban @someone @someoneelse`: Bans members from the server.
    """
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            for mentioned_member in message.mentions:
                if moderator_role not in mentioned_member.roles and mentioned_member is not client.user:
                    await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention}) was banned from the server by {message.author.mention}.\n--{message.jump_url}')
                    await message.guild.ban(mentioned_member, delete_message_days=0)
                if str(message.id).endswith("1"):
                    await message.channel.send('https://b.thumbs.redditmedia.com/GVgfjW-E0wafJbQHlv_XwyG7Ux3tnGZfHI_ExznRBzo.png')
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def embed(message):  # checked
    """
    `!embed @someone @someoneelse`: Gives members the `embed` role.
    """
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            for mentioned_member in message.mentions:
                await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention}) was given embed permissions by {message.author.mention}.\n--{message.jump_url}')
                if embed_role not in mentioned_member.roles:
                    await mentioned_member.add_roles(embed_role)
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def unembed(message):  # checked
    """
    `!unembed @someone @someoneelse`: Removes members embed role.
    """
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            for mentioned_member in message.mentions:
                await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention}) \'s embed role was removed by {message.author.mention}.\n--{message.jump_url}')
                if embed_role in mentioned_member.roles:
                    await mentioned_member.remove_roles(embed_role)
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def info(message):  # checked
    """
    `!info @someone @someoneelse`: Prints information on members.
    """
    await message.add_reaction("🐻")
    try:
        for mentioned_member in message.mentions:
            allowed_channels = [306760168669052938, 351549261730545674]  # botspam and #meta
            if mentioned_member == message.author and message.channel.id in allowed_channels or moderator_role in message.author.roles:
                roles = [role.name for role in mentioned_member.roles]
                join_age = datetime.datetime.utcnow() - mentioned_member.joined_at
                join_age = join_age - datetime.timedelta(microseconds=join_age.microseconds)
                account_age = datetime.datetime.utcnow() - mentioned_member.created_at
                account_age = account_age - datetime.timedelta(microseconds=account_age.microseconds)
                if mentioned_member.id in all_users.keys() and 'strikes' in all_users[mentioned_member.id].keys():
                    await message.channel.send(f"`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention})'s info is:\njoined_at: `{mentioned_member.joined_at.replace(microsecond=0)}` (`{join_age}` ago)\ncreated_at: `{mentioned_member.created_at.replace(microsecond=0)}` (`{account_age}` ago)\nroles: `{roles}`\nspam_info: `{all_users[mentioned_member.id]['strikes']}`\navatar_url: <{mentioned_member.avatar_url}>")
                else:
                    await message.channel.send(f"`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention})'s info is:\njoined_at: `{mentioned_member.joined_at.replace(microsecond=0)}` (`{join_age}` ago)\ncreated_at: `{mentioned_member.created_at.replace(microsecond=0)}` (`{account_age}` ago)\nroles: `{roles}`\nspam_info: `0`\navatar_url: <{mentioned_member.avatar_url}>")
            else:
                await message.add_reaction("🚫")
    except Exception as e:
        print(e)
        await message.add_reaction("⚠")


async def mute(message):  # checked
        """
        `!mute @someone @someoneelse`: Adds the `mute` role to members.
        """
        if moderator_role in message.author.roles:
            global all_users
            await message.add_reaction("🐻")
            try:
                for mentioned_member in message.mentions:
                    if muted_role not in mentioned_member.roles and moderator_role not in mentioned_member.roles and mentioned_member.id not in pd_settings['muted_members']:
                        all_users_setdefault(mentioned_member, message.created_at)
                        roles = [role.id for role in mentioned_member.roles]
                        pd_settings['muted_members'][mentioned_member.id] = {'roles': roles}
                        with open('pd_settings.p', 'wb') as pfile:
                            pickle.dump(pd_settings, pfile)
                        await mentioned_member.edit(roles=[muted_role])
                        await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention}) was muted by {message.author.mention}.\n--{message.jump_url}')
            except Exception as e:
                await message.add_reaction("⚠")
                print(e)
        else:
            await message.add_reaction("🚫")


async def unmute(message):  # checked
    """
    `!unmute @someone @someoneelse`: Removes the `muted` role from a member.
    """
    if moderator_role in message.author.roles:
        global all_users
        await message.add_reaction("🐻")
        try:
            for mentioned_member in message.mentions:
                if muted_role in mentioned_member.roles and moderator_role not in mentioned_member.roles:
                    all_users_setdefault(mentioned_member, message.created_at)
                    await mentioned_member.remove_roles(muted_role)
                    await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention}) was unmuted and their spam tracking reset by {message.author.mention}.\n--{message.jump_url}')
        except Exception as e:
            print(f"unmute error:\n{e}")
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def interview(message):  # checked
    """
    `!interview @someone @someoneelse`: Adds the `interviewee` role to a member.
    """
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            for mentioned_member in message.mentions:
                await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention}) was interviewed by {message.author.mention}.\n--{message.jump_url}')
                if interviewee_role not in mentioned_member.roles:
                    await mentioned_member.add_roles(interviewee_role)
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def uninterview(message):  # checked
    """
    `!uninterview @someone @someoneelse`: Adds the `interviewee` role to a member.
    """
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            for mentioned_member in message.mentions:
                await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention}) was uninterviewed by {message.author.mention}.\n--{message.jump_url}')
                if interviewee_role in mentioned_member.roles:
                    await mentioned_member.remove_roles(interviewee_role)
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def mod(message):  # checked
    """
    `!mod @someone @someoneelse`: Shuffles the characters in members names.
    """
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            for mentioned_member in message.mentions:
                if moderator_role not in mentioned_member.roles and mentioned_member is not client.user:
                        nickname = ''.join(random.sample(mentioned_member.display_name, len(mentioned_member.display_name)))
                        await mentioned_member.edit(nick=nickname)
                        await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention})\'s display name was modded by {message.author.mention}.\n--{message.jump_url}')
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def unmod(message):  # checked
    """
    `!mod @someone @someoneelse`: Shuffles the characters in members names.
    """
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            for mentioned_member in message.mentions:
                if moderator_role not in mentioned_member.roles and mentioned_member is not client.user:
                    await mentioned_member.edit(nick=None)
                    await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention})\'s display name was unmodded by {message.author.mention}.\n--{message.jump_url}')
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def kick(message):  # checked
    """
    `!kick @someone @someoneelse` Kicks members from the server.
    """
    user_banables = {'145301695096815617', '214806702288142336'}
    if moderator_role in message.author.roles or message.author.id in user_banables:
        await message.add_reaction("🐻")
        try:

            if message.author.id in user_banables:
                try:
                    await message.mentions[0].send(f"Hi beardy, Nathan, or both of you if this was mutual distruction. {message.author.mention} kicked you from the server (again?). You can rejoin at https://discord.gg/YuUS2nM .")
                except discord.Forbidden:
                    pass
                await message.guild.kick(message.mentions[0])
                await usernotes_channel.send(f"{message.author.mention} kicked {message.mentions[0]}.")
            else:
                for mentioned_member in message.mentions:
                    if moderator_role not in mentioned_member.roles and mentioned_member is not client.user:
                        try:
                            await mentioned_member.send("Hi. You're being kicked from Political Discourse. If you rejoin, please reread the rules.")
                        except discord.Forbidden:
                            pass
                        await usernotes_channel.send(f'`{mentioned_member.name}`:`{mentioned_member.id}` ({mentioned_member.mention}) was kicked from the server by {message.author.mention}\n--{message.jump_url}')
                        await message.guild.kick(mentioned_member)
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def baned(message):  # checked
    """
    `baned`: Sends a random baned cat to the message channel.
    """
    if message.author == amici:
        await message.add_reaction("🐻")
        try:
            await message.channel.send(random.choice(baned_cats))
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def copypasta(message):  # checked
    """
    Sends a bunch of copypasta to the message channel.
    """
    try:
        if moderator_role in message.author.roles:
            await message.add_reaction("🐻")
            await message.channel.send(pd_settings['member_commands'][message.content.lower()]['copypasta'])
        else:
            if message.channel.id not in no_copypasta_channels or pd_settings['member_commands'][message.content.lower()]['high_effort'] is True:
                if embed_role in message.author.roles:
                    await message.add_reaction("🐻")
                    await message.channel.send(pd_settings['member_commands'][message.content.lower()]['copypasta'])
    except Exception as e:
        print(e)
        await message.add_reaction("⚠")


async def muted(message):  # checked
    """
    `!muted!`: sends the mute message to the channel.
    """
    if moderator_role in message.author.roles or message.author == client.user:
        await message.add_reaction("🐻")
        try:
            await message.channel.send(f'You were muted because you broke the rules. Reread them, then write `@{moderator_role.name}` to be unmuted.')
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def command_help(message):  # checked
    """
    `!command_help` spams the message author with all the bot commands they can access.
    """
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            for key in member_functions_dict.keys():
                if member_functions_dict[key].__doc__ is not None:
                    await message.author.send(member_functions_dict[key].__doc__)
            for key in mod_functions_dict.keys():
                if mod_functions_dict[key].__doc__ is not None:
                    await message.author.send(mod_functions_dict[key].__doc__)
        except discord.Forbidden:
            await message.add_reaction("⚠")
    else:
        if embed_role in message.author.roles:
            await message.add_reaction("🐻")
            try:
                for key in member_functions_dict.keys():
                    if member_functions_dict[key].__doc__ is not None:
                        await message.author.send(member_functions_dict[key].__doc__)
            except discord.Forbidden:
                await message.add_reaction("⚠")


async def new_command(message):  # checked
    """
    `!new_command "the_new_command_name" "the command's text"`: adds a new copypasta command.
    """
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            global pd_settings
            command_text = message.content[14:-1]
            command_text = command_text.replace('“', '"')
            command_text = command_text.replace('”', '"')
            new_command_name = command_text.lower().split('" "')[0]
            new_command_text = command_text.split('" "')[1]
            pd_settings['member_commands'][new_command_name] = {'copypasta': new_command_text, 'high_effort': False}
            await message.channel.send("Added {}".format(new_command_name))
            try:
                with open('pd_settings.p', 'wb') as pfile:
                    pickle.dump(pd_settings, pfile)
            except FileNotFoundError:
                await message.channel.send(f"Can't find the database file to permanently save the change. {amici.mention}")
            async for log_message in help_commands_channel.history(limit=5000):
                if log_message.content.startswith(f"{new_command_name}\n"):
                    await log_message.delete()
            await help_commands_channel.send(f'{new_command_name}\n{new_command_text}')
        except Exception as e:
            await message.add_reaction("⚠")
            print(e)
    else:
        await message.add_reaction("🚫")


async def delete_command(message):  # checked
    """
    `!delete_command "the_command's_name"`: delete's a copypasta command.
    """
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        global pd_settings
        command_name = message.content.lower()[17:-1]
        try:
            del pd_settings['member_commands'][command_name]
            await message.channel.send("Command {} deleted.".format(command_name))
            try:
                with open('pd_settings.p', 'wb') as pfile:
                    pickle.dump(pd_settings, pfile)
            except FileNotFoundError:
                await message.channel.send("Can't find the database file to permanently save the change.")
            async for log_message in help_commands_channel.history(limit=5000):
                if log_message.content.startswith(f"{command_name}\n"):
                    await log_message.delete()
        except KeyError:
            await message.channel.send("Command Not found")
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def clean_up_commands_channel(message):  # checked
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            await help_commands_channel.purge(limit=5000, check=None)
            for key in pd_settings['member_commands']:
                await help_commands_channel.send('{}\n{}'.format(key, pd_settings['member_commands'][key]['copypasta']))
        except Exception as e:
            await message.add_reaction("⚠")
            print(e)
    else:
        await message.add_reaction("🚫")


async def get_cat(message):  # checked
    """
    `!cat` gets a random cat from random.cat.
    """
    await message.add_reaction("🐻")
    try:
        random_cat = urllib.request.urlopen('http://aws.random.cat/meow', data=None, timeout=2)
        random_cat = random_cat.read()[9:-2].decode("utf-8")
        random_cat = random_cat.replace("\\", "")
        await message.channel.send(random_cat)
    except urllib.error.HTTPError:
        await message.add_reaction("⚠")


async def get_dog(message):  # checked
    """
    `!pupper` gets a random dog from random.dog.
    """
    await message.add_reaction("🐻")
    try:
        random_dog = urllib.request.urlopen('http://random.dog/woof', data=None, timeout=2)
        random_dog = random_dog.read().decode("utf-8")
        await message.channel.send('http://random.dog/{}'.format(random_dog))
    except urllib.error.HTTPError:
        await message.add_reaction("⚠")


async def get_dad(message):  # checked
    """
    `!dad` gets a random dog from icanhazdadjoke.com
    """
    await message.add_reaction("🐻")
    try:
        req = urllib.request.Request(
            'https://icanhazdadjoke.com/',
            data=None,
            headers={
                'User-Agent': 'bear, a discord bot from amici',
                'Accept': 'text/plain'
            }
        )
        random_dad = urllib.request.urlopen(req)
        random_dad = random_dad.read().decode('utf-8')
        await message.channel.send(random_dad)
    except urllib.error.HTTPError:
        await message.add_reaction("⚠")


async def targeted(message):  # checked
    """
    `!targeted` sends gamer copypasta.
    """
    await message.add_reaction("🐻")
    await message.channel.send("They targeted PD users.\nP.D. U S E R S.")
    await message.channel.send("We're a group of people who will sit for hours, days, even weeks on end performing some of the stupidest, most mentally worthless arguements. Over, and over, and over all for nothing more than a little echochamber where everyone says they agree.\nWe'll punish our selfs doing things others would consider torture, because we think it's fun.\nWe'll spend most if not all of our free time debating if the new cabinet pick has evolved on the middle east peace issue since they last said they \"hated islam\".\nMany of us have made careers out of doing just these things: looking at electoral maps, all day, the same districts over and over, hundreds of times to the point where we know evety little detail the evil GOP has gerrymandered into a state to supress african american turnout of the ages between 18-46 in off year elections.\nDo these people have any idea how many polls have had their methodologies critiques, examined, and skewered? All to latter be referred to as \"memes\"?")
    await message.channel.send("These people honestly think this is an election they can win? They take our MSM? We're already building a new one without them utilizing @thehill and @Jaketapper. They take our cable news? PD Users aren't shy about throwing their money else where, or even making their own punditry. They think calling us leftist, censoring, echo cahmber loving liberals is going to change us? We've been called worse things by people who are actually allowed to vote in the rust belt. They picked a fight against a group that's already grown desensitized to their strategies and methods. Who enjoy the battle of attrition they've threatened us with. Who take it as a challange when they tell us we no longer get to panic over every thing. Our obsession with proving we can panic more after being told we can't, is so deeply ingrained from years of dealing with GWB43 and friends, laughing at how pathetic we used to be that proving you people wrong has become a very real need; a honed reflex.\n\nPD Users are always right, experts at seeing the future, and capable of entertaining all side by nature. We love a challange. The worst thing you did in all of this was to challange us. You're not special, you're not original, you're not the first; this is just another mid term election.")


async def iam(message):  # checked
    """
    `!iam` assigns a general role to the message author.
    """
    await message.add_reaction("🐻")
    role_name = message.content[5:]
    try:
        if role_name in iam_role_list:
            role = discord.utils.get(message.guild.roles, name=role_name)
            if role is not None:
                await message.author.add_roles(role)
                await usernotes_channel.send(f"`{message.author.name}`:`{message.author.id}` ({message.author.mention}) added the `{role_name}` role to themselves.\n--{message.jump_url}")
            else:
                await message.add_reaction("⚠")
                await message.channel.send(f"{message.author.mention} That role (`{role_name}`) does not exist even though it's whitelisted. Please ping a mod to help out.")
        else:
            await message.add_reaction("🚫")
            await message.channel.send(f"{message.author.mention} That role (`{role_name}`) is not white listed. Double check your spelling and Letter Case.")
    except Exception as e:
        print(e)
        await message.add_reaction("⚠")


async def iamnot(message):  # checked
    """
    `!iamnot` removes a general role from the message author.
    """
    await message.add_reaction("🐻")
    role_name = message.content[8:]
    try:
        if role_name in iam_role_list:
            role = discord.utils.get(message.guild.roles, name=role_name)
            if role is not None:
                await message.author.remove_roles(role)
                await usernotes_channel.send(f"`{message.author.name}`:`{message.author.id}` ({message.author.mention}) removed the `{role_name}` role from themselves.\n--{message.jump_url}")
            else:
                await message.add_reaction("⚠")
                await message.channel.send(f"{message.author.mention} That role (`{role_name}`) does not exist even though it's whitelisted. Please ping a mod to help out.")
        else:
            await message.add_reaction("🚫")
            await message.channel.send(f"{message.author.mention} That role (`{role_name}`) is not white listed. Double check your spelling and Letter Case.")
    except Exception as e:
        print(e)
        await message.add_reaction("⚠")


async def add_role(message):  # checked
    """
    `!add_role "rolename" @someone` Adds a role to a user.
    """
    if moderator_role in message.author.roles and len(message.mentions) > 0 and re.search(r'\".+\"', message.content) is not None:
        await message.add_reaction("🐻")
        role_name = re.search(r'\".+\"', message.content)
        role_name = role_name.group()
        role_name = role_name.replace('"', '')
        try:
            new_role = discord.utils.get(message.guild.roles, name=role_name)
            if new_role is not None and new_role is not moderator_role:
                for mentioned_user in message.mentions:
                        await mentioned_user.add_roles(new_role)
                        await usernotes_channel.send(f"`{mentioned_user.name}`:`{mentioned_user.id}` ({mentioned_user.mention})'s {new_role.name} role was added by {message.author.mention}.\n--{message.jump_url}")
            else:
                await message.add_reaction("⚠")
                await message.channel.send("Role not found.")
        except:
            await message.add_reaction("⚠")
            await message.channel.send("Error adding role.")
    else:
        await message.add_reaction("🚫")


async def remove_role(message):  # checked
    """
    `!remove_role "rolename" @someone` Removes a role from a user.
    """
    if moderator_role in message.author.roles and len(message.mentions) > 0 and re.search(r'\".+\"', message.content) is not None:
        await message.add_reaction("🐻")
        role_name = re.search(r'\".+\"', message.content)
        role_name = role_name.group()
        role_name = role_name.replace('"', '')
        try:
            old_role = discord.utils.get(message.guild.roles, name=role_name)
            if old_role is not None:
                for mentioned_user in message.mentions:
                    if moderator_role not in mentioned_user.roles and old_role is not moderator_role and old_role.name is not "modmute":
                        await mentioned_user.remove_roles(old_role)
                        await usernotes_channel.send(f"`{mentioned_user.name}`:`{mentioned_user.id}` ({mentioned_user.mention})'s {old_role.name} role was removed by {message.author.mention}.\n--{message.jump_url}")
            else:
                await message.add_reaction("⚠")
                await message.channel.send("Role not found.")
        except:
            await message.add_reaction("⚠")
            await message.channel.send("Error removing role.")
    else:
        await message.add_reaction("🚫")


async def tweet(message, status):  # not checked
    """
    `!tweet something` to tweet something.
    rate limiting exists. https://support.twitter.com/articles/15364
    """
    "inside the tweeting function"
    await message.add_reaction("🐻")
    if message.clean_content.lower().startswith("!tweet") and moderator_role in message.author.roles:
        status = message.clean_content[7:]
        r = pdbeat.request('statuses/update', {'status': status})
        if r.status_code == 200:
            await message.add_reaction("🐦")
    else:
        if len(status) > 279:
            status = f'{status[0:276]}...'
        tweet_urls = tweet_regex.findall(status)
        if len(tweet_urls) > 0:
            for tweet_url in tweet_urls:
                tweet_id = int(tweet_status_regex.findall(tweet_url)[0])
                r = pdbeat.request("statuses/retweet/:%d" % tweet_id)
                return r
        else:
            r = pdbeat.request('statuses/update', {'status': status})
        return r


async def modmute(message):  # checked
    """
    applies the modmute role to the mentioned moderators
    """
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            if modmute_role is not None:
                for moderator in message.mentions:
                    if moderator_role in moderator.roles:
                        try:
                            all_users_setdefault(moderator, message.created_at)
                            roles = [role.id for role in moderator.roles]
                            pd_settings['muted_members'][moderator.id] = {'roles': roles}
                            with open('pd_settings.p', 'wb') as pfile:
                                pickle.dump(pd_settings, pfile)
                            await moderator.edit(roles=[modmute_role])
                            await usernotes_channel.send(f"`{moderator.name}`:`{moderator.id}` ({moderator.mention}) was modmuted by {message.author.mention}.\n--{message.jump_url}")
                        except Exception as e:
                            print(e)
                            await message.add_reaction("⚠")
                    else:
                        await message.add_reaction("🚫")
            else:
                await message.add_reaction("⚠")
                print("modmute_role is None")
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def unmodmute(message):  # checked
    """
    removes the modmute role from the mentioned moderators. does not work on the message author.
    """
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            modmute_role = discord.utils.get(message.guild.roles, name='modmute')
            for moderator in message.mentions:
                if moderator is not message.author and modmute_role in moderator.roles:
                    all_users_setdefault(moderator, message.created_at)
                    roles = []
                    for role in pd_settings['muted_members'][moderator.id]['roles']:
                        role = discord.utils.get(our_guild.roles, id=role)
                        roles.append(role)
                    await moderator.edit(roles=roles)
                    pd_settings['muted_members'].pop(moderator.id)
                    await usernotes_channel.send(f"`{moderator.name}`:`{moderator.id}` ({moderator.mention}) was unmodmuted by {message.author.mention}.\n--{message.jump_url}")
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def get_tweet(message):
    tweet_urls = tweet_regex.findall(message.content)
    for tweet_url in tweet_urls:
        tweet_id = int(tweet_status_regex.findall(tweet_url)[0])  # get the tweet id
        retrieved_tweet = pdbeat.request('statuses/show/:%d' % tweet_id, {'tweet_mode': 'extended'})  # parse the response
        retrieved_tweet = retrieved_tweet.json()
        if len(retrieved_tweet['full_text']) > 266:
            description = retrieved_tweet['full_text'][:266].rsplit(" ", 1)[1]  # find the last word that was cut off by discord's embed
            description = f"...{description}{retrieved_tweet['full_text'][266:]}"  # add the remaining text from the tweet
            keys = {'entities', 'extended_entities'}
            for name in keys:  # removes media link from end of the tweet
                if name in retrieved_tweet and 'media' in retrieved_tweet[name]:
                    for media in retrieved_tweet[name]['media']:
                        if description.endswith(media['url']):
                            description = ''.join(description.rsplit(media['url'], 1))
            if description.replace(" ", "") != "...":
                em = discord.Embed(description=description, color=discord.Color.from_rgb(29, 161, 242))  # make an embed from the tweet text
                em.set_author(name=f"{retrieved_tweet['user']['name']} (@{retrieved_tweet['user']['screen_name']})",
                              url=f"https://twitter.com/{retrieved_tweet['user']['screen_name']}",
                              icon_url=retrieved_tweet['user']['profile_image_url_https'])
                em.set_footer(text="Twitter", icon_url="https://abs.twimg.com/icons/apple-touch-icon-192x192.png")
                await message.channel.send(embed=em)  # send the embed


def get_stock_data(stock):  # checked
    # returns (Price, Change, Percent Change, Error)
    # Price, Change, and Percent Change are rounded to hundreths
    if stock.lower() == 'ftse':
        stock = '^ftse'
    req = requests.get('https://www.alphavantage.co/query', {'function': 'TIME_SERIES_DAILY', 'symbol': stock, 'apikey': av_api_key}).json()
    if 'Error Message' in req:
        return 0.0, 0.0, 0.0, 'Unknown symbol'
    data = req['Time Series (Daily)']
    curday = datetime.datetime.now()
    while curday.strftime('%Y-%m-%d') not in data:
        curday -= datetime.timedelta(days=1)
    prevday = curday - datetime.timedelta(days=1)
    while prevday.strftime('%Y-%m-%d') not in data:
        prevday -= datetime.timedelta(days=1)
    curclose = float(data[curday.strftime('%Y-%m-%d')]['4. close'])
    prevclose = float(data[prevday.strftime('%Y-%m-%d')]['4. close'])
    dd = OrderedDict(sorted(data.items(), key=lambda x: x[0]))
    y = []
    dates = []
    for key in dd:
        y.append(float(dd[key]['4. close']))
        dates.append(key)
    fig, ax = plt.subplots(1, 1, figsize=(10, 3))
    for k, v in ax.spines.items():
        v.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"{stock} since {dates[1]}", color='#3498db', fontdict={"fontsize": 32})
    plt.plot(y, color='#3498db')
    plt.tight_layout()
    filename = f"{stock} since {dates[1]}.png"
    plt.savefig(fname=filename, format='png', dpi=25, transparent=True)
    plt.close()
    return round(curclose, 2), round(curclose-prevclose, 2), round(100*(curclose/prevclose-1), 2), '', filename


def get_stock_message(stock):  # checked
    data = get_stock_data(stock)
    filename = data[4]
    if data[3] != '':  # Error
        return data[3], filename
    elif data[1] > 0:  # Increase
        return '**{}**: {} :arrow_up:{} ({}%)'.format(stock, data[0], data[1], data[2]), filename  # stock, curclose, curclose-prevclose, curclose/prevclose-1
    elif data[1] == 0:  # No change
        return '**{}**: {} (no change)'.format(stock, data[0]), filename
    else:  # Decrease
        return '**{}**: {} :arrow_down:{} ({}%)'.format(stock, data[0], -data[1], data[2]), filename


async def get_stock(message):  # checked
    await message.add_reaction("🐻")
    stock = re.sub(r"!stocks? ", "", message.clean_content.lower())
    if message.content.lower().startswith("!stock_search "):
        await stock_search(message)
    else:
        try:
            data = get_stock_message(stock)
            stock_message = data[0]
            stock_file = open(f"{data[1]}", 'rb')
            discord_file = discord.File(f"{data[1]}", f"{data[1]}")
            await message.channel.send(file=discord_file, content=stock_message)
            stock_file.close()
            os.remove(data[1])
        except IndexError:
            await message.add_reaction("⚠")
            await message.channel.send(f"{message.author.mention}:  Something errored. If you're not sure about the stock symbol, try `!stock_search {stock}`")
        except Exception as e:
            await amici.send(content=f"{e}")


async def stock_search(message):  # checked
    try:
        query = message.content.replace("!stock_search ", "", 1)
        req = requests.get('https://www.alphavantage.co/query', {'function': 'SYMBOL_SEARCH', 'keywords': query, 'apikey': av_api_key}).json()
        pending_message = f"{message.author.mention}: ```"
        for thing in req["bestMatches"]:
            additional_message = f"{thing['1. symbol']}: {thing['2. name']} ({thing['4. region']})\n"
            if len(pending_message) + len(additional_message) < 2000:
                pending_message = f"{pending_message} {additional_message}"
            else:
                await message.channel.send(f"{pending_message}```")
                message = f"```{additional_message}"
        if not req["bestMatches"]:
            await message.channel.send(f'{message.author.mention}: No symbols found for `{query}`.')
        else:
            await message.channel.send(f"{pending_message}```")
    except Exception as e:
        print(e)
        await message.add_reaction("⚠")


def get_predictit_graph(contract_id, title):
    url = f'https://www.predictit.org/Resource/DownloadMarketChartData?marketid={contract_id}&timespan=90d'
    d = {}
    colors = cycle(
        ["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red",
         "silver", "teal", "yellow"])
    markers = cycle(
        [".", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "P", "*", "h", "H", "+", "x", "X", "D", "d",
         "|", 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    fig, ax = plt.subplots()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.tick_right()
    with closing(requests.get(url, stream=True)) as r:
        reader = csv.DictReader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter=',')
        for row in reader:
            d.setdefault(row['ContractName'], [])
            d[row['ContractName']].append(row)
    last_close_dict = {}
    for k in d:
        for list_item in d[k]:
            try:
                last_close_dict[k] = float(list_item['CloseSharePrice'][1:])
            except ValueError:
                last_close_dict[k] = 0
    sorted_last_close_dict = sorted(last_close_dict.items(), reverse=True, key=lambda xb: xb[1])
    for name in sorted_last_close_dict:
        x = []
        y = []
        for list_item in d[name[0]]:  # predictit removed a sortable datestring. this is a bandaid to give it back. D:
            date_time_str = list_item['Date']
            date_time_str = str.split(date_time_str, " ")[0]
            date_time_str = str.split(date_time_str, "/")
            n = 0
            for i in date_time_str:
                if len(i) < 2:
                    date_time_str[n] = "0" + i
                n += 1
            date_time_str = f"{date_time_str[0]}-{date_time_str[1]}"
            x.append(date_time_str)
            try:
                y.append(float(list_item['CloseSharePrice'][1:]) * 100)
            except ValueError:
                y.append(0)
        ax.plot(x, y, label=name[0], color=next(colors), marker=next(markers), markevery=7)
    plt.legend(frameon=False, bbox_to_anchor=(1.04, 1))
    plt.xticks(rotation=20)
    plt.tick_params(axis='both', labelsize=8, labelcolor='gray', pad=-5)
    plt.tick_params(axis='x', pad=-12)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}¢'))  # remove y axis decimals
    every_nth = 7
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    for n, line in enumerate(ax.xaxis.get_ticklines()):
        line.set_visible(False)
    for n, line in enumerate(ax.yaxis.get_ticklines()):
        line.set_visible(False)
    plt.grid(axis="y", color='gray', alpha=.2)
    size = 8
    fig.set_size_inches(size * (1 + 5 ** 0.5) / 2, size)
    plt.title(label=title, loc="center",
              fontdict={'fontweight': 'bold', 'size': 18, 'verticalalignment': 'baseline'})
    plt.tight_layout()
    graph_buf = BytesIO()
    plt.savefig(graph_buf, format='png')
    graph_buf.seek(0)
    return graph_buf


async def predictit(message):
    await message.add_reaction("🐻")
    await message.channel.trigger_typing()
    predictit_string = message.content[11:]
    try:
        try:
            int(predictit_string)
            req = requests.get(f'https://www.predictit.org/api/marketdata/markets/{message.content[11:]}').json()
            if req is None:
                await message.channel.send(f"Predictit returned no data for that contract id. You can get a contract's id from the contract's URL: <https://www.predictit.org/markets/detail/**4319**/Will-Donald-Trump-be-impeached-by-year-end-2019>")
                return
            message_list = [f"{message.author.mention}:", f"{req['name']}",
                            f"<https://www.predictit.org/markets/detail/{req['id']}>", "```"]
            header = f"Contract ({req['id']})"
            header = f"{header}{' ' * (20 - len(header))}LYP (CHANGE) BYP BNP"
            message_list.append(header)
            for contract in req['contracts']:
                if contract['name'] == req['name']:
                    contract['name'] = ""
                if len(contract['name']) > 19:
                    contract['name'] = f"{contract['name'][:16]}..."
                contract_string = f"{contract['name']}"
                if contract['lastTradePrice'] is None:
                    contract['lastTradePrice'] = 0
                contract_string = f"{contract_string}{' ' * (20 - len(contract_string))}{str(contract['lastTradePrice'] * 100).split('.')[0]}¢"
                if contract['lastClosePrice'] is None:
                    contract['lastClosePrice'] = 0
                contract_string = f"{contract_string}{' ' * (25 - len(contract_string))}({str(contract['lastTradePrice'] * 100 - contract['lastClosePrice'] * 100).split('.')[0]}¢)"
                if contract['bestBuyYesCost'] is None:
                    contract['bestBuyYesCost'] = 0
                contract_string = f"{contract_string}{' ' * (33 - len(contract_string))}{str(contract['bestBuyYesCost'] * 100).split('.')[0]}¢"
                if contract['bestBuyNoCost'] is None:
                    contract['bestBuyNoCost'] = 0
                contract_string = f"{contract_string}{' ' * (37 - len(contract_string))}{str(contract['bestBuyNoCost'] * 100).split('.')[0]}¢"
                if len("\n".join(message_list) + "\n" + contract_string) < 1996:
                    message_list.append(contract_string)
                else:
                    message_list.append("```")
                    await message.channel.send("\n".join(message_list))
                    message_list = ['```', contract_string]
            if message_list != "```":
                message_list.append("```")
            graph = get_predictit_graph(message.content[11:], req['name'])
            temp_file = discord.File(fp=graph, filename=f"{predictit_string}.png", spoiler=False)
            await message.channel.send(content="\n".join(message_list), file=temp_file)
            graph.close()
        except ValueError:
            req = requests.get(f'https://www.predictit.org/api/marketdata/all/').json()
            if req is None:
                await message.channel.send("Predictit returned no data to search.")
                return
            search_term = predictit_string.lower()
            message_list = [f"{message.author.mention}:", f"Search results for `{search_term}`:", "```"]
            header = f"CONTRACT NAME (ID){' ' * 48}(ID)    LYP (CHANGE) BYP BNP"
            message_list.append(header)
            for market in req['markets']:
                for contract in market['contracts']:
                    if search_term in contract['name'].lower() or search_term in market['name'].lower():
                        if contract['name'] != market['name']:
                            message_list.append(f"{market['name']}")
                        if len(contract['name']) > 65:
                            contract['name'] = f"{contract['name'][:62]}..."
                        if contract['lastTradePrice'] is None:
                            contract['lastTradePrice'] = 0
                        contract_string = f"{contract['name']}{' ' * (65 - len(contract['name']))}({market['id']})"
                        if contract['lastTradePrice'] is None:
                            contract['lastTradePrice'] = 0
                        contract_string = f"{contract_string}{' ' * (74 - len(contract_string))}{str(contract['lastTradePrice'] * 100).split('.')[0]}¢"
                        if contract['lastClosePrice'] is None:
                            contract['lastClosePrice'] = 0
                        contract_string = f"{contract_string}{' ' * (78 - len(contract_string))}({str(contract['lastTradePrice'] * 100 - contract['lastClosePrice'] * 100).split('.')[0]}¢)"
                        if contract['bestBuyYesCost'] is None:
                            contract['bestBuyYesCost'] = 0
                        contract_string = f"{contract_string}{' ' * (87 - len(contract_string))}{str(contract['bestBuyYesCost'] * 100).split('.')[0]}¢"
                        if contract['bestBuyNoCost'] is None:
                            contract['bestBuyNoCost'] = 0
                        contract_string = f"{contract_string}{' ' * (91 - len(contract_string))}{str(contract['bestBuyNoCost'] * 100).split('.')[0]}¢"
                        if len("\n".join(message_list) + "\n" + contract_string) < 1900:
                            message_list.append(contract_string)
                        else:
                            message_list.append("```")
                            await message.channel.send("\n".join(message_list))
                            message_list = ['```', contract_string]
            if message_list != "```":
                message_list.append("```")
            await message.channel.send("\n".join(message_list))
    except Exception as e:
        print(e)
        await message.add_reaction("⚠")


def get_election_message(path):
    data = requests.get('https://elections.argusdusty.com/' + path + '.json').json()
    candidates = sorted(data['candidates'], key=lambda c: (c['votes'], -data['priority'].get(c['candidate'], 0)), reverse=True)
    msgs = []
    for c in candidates:
        if data['total_votes'] == 0:
            if c['candidate'] in data['priority']:
                msgs.append("{}: {} (0.0%)".format(c['candidate'], c['votes']))
        elif c['votes'] >= data['vote_portion_thresh']*data['total_votes']:
            msgs.append('{}: {} ({:.1%})'.format(c['candidate'], c['votes'], c['votes']/data['total_votes']))

    msgs.append('Total Votes: {}'.format(data['total_votes']))
    if len(candidates) >= 2 and data['total_votes'] != 0:
        msgs.append('{} margin: {:.2%}'.format(candidates[0]['candidate'], (candidates[0]['votes']-candidates[1]['votes'])/data['total_votes']))

    if data['portion_complete'] > 0:
        if data['portion_complete'] == 1:
            msgs.append('100% complete')
        else:
            msgs.append('Estimated percent complete: {:.2%}'.format(data['portion_complete']))

    return '\n'.join(msgs)


async def electionresults(message):
    await message.add_reaction("🐻")
    try:
        path = message.clean_content[17:]
        electionresults_message = '```{}```'.format(get_election_message(path))
        await message.channel.send(electionresults_message)
    except Exception as e:
        print(e)
        await message.add_reaction("⚠")


async def emoji_metrics(message):  # checked
    """`!emoji_metrics n`Adds up all the server emojis used in messages and reactions in each channel, up to `n` days ago."""
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            global emoji_log_lock
            if emoji_log_lock is True:
                await message.channel.send("I'm still working on it from last time.")
            else:
                emoji_log_lock = True
                days = message.content.replace("!emoji_metrics ", "")
                emoji_count = {}
                for emoji in message.guild.emojis:
                    emoji_count[emoji] = 0
                after = datetime.datetime.utcnow() - datetime.timedelta(days=int(days))
                channel_counter = 0
                await message.channel.send(f"Alright. I'm adding up all the server emojis used in messages and reactions in each channel, going up to {days} days ago. Except for #tweets. No one ever reacts there.")
                update_message = await message.channel.send("Getting started.")
                for message_channel in message.guild.text_channels:
                    if message_channel.id != tweets_channel_id:
                        await update_message.edit(content=f"checking {message_channel.mention} . Roughly {len(message.guild.text_channels) - channel_counter} channels left to go...")
                        channel_counter += 1
                        try:
                            async for channel_message in message_channel.history(limit=None, after=after):
                                for emoji in emoji_count:
                                    if str(emoji) in channel_message.content:
                                        emoji_count[emoji] += 1
                                    for channel_message_reaction in channel_message.reactions:
                                        if channel_message_reaction.emoji == emoji:
                                            emoji_count[emoji] += 1
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
                        await message.channel.send(pending_message)
                        pending_message = next_chunk
                        emoji_counter = 1
                if pending_message != "":
                    await message.channel.send(pending_message)
                emoji_log_lock = False
        except Exception as e:
            await message.add_reaction("⚠")
            emoji_log_lock = False
            print(e)
    else:
        await message.add_reaction("🚫")


async def wiki(message):  # checked
    """`!wiki search` searches wikipedia.
    `'!wiki summary` gets a wikipedia page.
    """
    if embed_role in message.author.roles or moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            if message.clean_content.lower().startswith("!wiki search "):
                search_results = ", ".join(wikipedia.search(message.clean_content.lower().replace("!wiki search ", "")))
                if len(search_results) > 2000:
                    search_results = f'{search_results[:1996]}...'
                if search_results == "":
                    search_results = "Nothing turned up."
                await message.channel.send(search_results)
            if message.clean_content.lower().startswith("!wiki summary "):
                try:
                    summary = wikipedia.summary(message.clean_content.lower().replace("!wiki summary ", ""))
                    if summary == "":
                        summary = "Nothing turned up."
                    if len(summary) > 2000:
                        summary = f'{summary[:1996]}...'
                    await message.channel.send(summary)
                except wikipedia.exceptions.DisambiguationError as e:
                    disambiguation_message = f'**{message.clean_content.lower().replace("!wiki summary ", "")}** may refer to: '
                    options = ", ".join(e.options)
                    disambiguation_message = f"{disambiguation_message} {options}"
                    if len(disambiguation_message) > 2000:
                        disambiguation_message = f"{disambiguation_message[:1996]}..."
                    await message.channel.send(disambiguation_message)
                except wikipedia.exceptions.PageError as e:
                    await message.channel.send(e.error)
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def me(message):  # checked
    """
    `!me this is my copypasta` makes it so that anytime you write `!me` bear will reply with 'this is my copypasta'
    """
    global pd_settings
    pd_settings.setdefault('personal_commands')
    try:
        if embed_role in message.author.roles or moderator_role in message.author.roles:
            await message.add_reaction("🐻")
            command = message.clean_content[4:]
            if len(command) > 0:
                if message.author.id in pd_settings['personal_commands']:
                    pd_settings['personal_commands'][message.author.id] = command
                else:
                    pd_settings['personal_commands'].setdefault(message.author.id, command)
                with open('pd_settings.p', 'wb') as pfile:
                    pickle.dump(pd_settings, pfile)
                await usernotes_channel.send(f"`{message.author.name}`:`{message.author.id}` ({message.author.mention}) changed their `!me` to ```{command}```\n--{message.jump_url}")
            else:
                if message.author.id in pd_settings['personal_commands']:
                    await message.channel.send(pd_settings['personal_commands'][message.author.id])
        else:
            await message.add_reaction("🚫")
    except Exception as e:
        print(e)
        await message.add_reaction("⚠")


async def high_effort_command(message):  # checked
    """
    `!high_effort_command !food` makes the `!food` command work in all channels. do it again to revert it.
    """
    if moderator_role in message.author.roles:
        try:
            command = message.clean_content[21:]
            global pd_settings
            await message.add_reaction("🐻")
            if command in pd_settings['member_commands']:
                if pd_settings['member_commands'][command]['high_effort'] is False:
                    pd_settings['member_commands'][command]['high_effort'] = True
                    await usernotes_channel.send(f"{message.author.mention} made {command} high effort. It will now work in any channel.\n--{message.jump_url}")
                else:
                    pd_settings['member_commands'][command]['high_effort'] = False
                    await usernotes_channel.send(f"{message.author.mention} made {command} not high effort. It will not work in high effort channels.\n--{message.jump_url}")
                with open('pd_settings.p', 'wb') as pfile:
                    pickle.dump(pd_settings, pfile)
            else:
                await message.channel.send(f'command "{command}" not found. the syntax is `!high_effort_command !food`')
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def high_effort_commands(message):
    if moderator_role in message.author.roles or message.channel.id == bot_spam_channel_id:
        await message.channel.send(f"{message.author.mention}:")
        for commandname in pd_settings['member_commands'].keys():
            if pd_settings['member_commands'][commandname]['high_effort']:
                await message.channel.send(content=f"{commandname}\n{pd_settings['member_commands'][commandname]['copypasta']}")


async def record(message):
    """
    `!record` adds a ⏺️to end of the channel name if it isn't present. Use `!stop` to remove it.
    """
    if embed_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            recording_booth = client.get_channel(495757812723613706)
            potato = await client.fetch_user_info(242443346675499008)
            new_name = f"{recording_booth.name}⏺"
            if recording_booth.name.endswith("⏺") is False:
                try:
                    await recording_booth.edit(name=new_name)
                    await message.channel.send(f"{message.author.mention}, Craig is going to start recording. When you're done, type `!stop`, then Craig will stop recording and {potato.mention} will know to work his magic.")
                    await message.channel.send(f"!join {new_name}")
                except discord.HTTPException:
                    await message.channel.send("Editing the channel failed.")
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def stop(message):
    """
    `!stop` removes the recording symbol from the end of the channel name if it is present. Use `!record` to add it.
    """
    if embed_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            recording_booth = client.get_channel(495757812723613706)
            if recording_booth.name.endswith("⏺"):
                try:
                    await recording_booth.edit(name=f"{recording_booth.name[0:-1]}")
                except discord.HTTPException:
                    await message.channel.send("Editing the channel failed.")
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def load_prob(path):
    data = requests.get('https://elections.argusdusty.com/' + path + '.json').json()
    for f in data['forecast']:
        if f['candidate'] == 'Dem': return f['odds']*100
    return 0.0


async def needle(message):  # checked
    await message.add_reaction("🐻")
    try:
        senate = await load_prob('20181106/USSen')
        house = await load_prob('20181106/USHouse')
        await message.channel.send(f"```Dem Senate win probability: {senate:.1f}%\nDem House win probability: {house:.1f}%```")
    except Exception as e:
        print(e)
        await message.add_reaction("⚠")


async def modvote(message):  # checked
    """`!modvote something` adds voting reactions to the message."""
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            await message.add_reaction("☑")
            await message.add_reaction("❎")
            await message.add_reaction("🤷")
            await message.channel.send(f"{moderator_role.mention}: A vote on the above issue is requested. React with a ☑ for Yes or a ❎ for No.")
            await message.pin()
        except Exception as e:
            print(e)
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def slow(message):  # checked
    """Changes the amount of seconds a user has to wait before sending another message (0-120); bots, as well as users with the permission manage_messages or manage_channel, are unaffected.`
    !slow 10` rate limits users in the channel to 10 seconds per message. Use `!slow 0` or `!fast` to disable it."""
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            try:
                rate_limit_per_user = int(message.content.split(" ")[1])
            except IndexError:
                rate_limit_per_user = 10
            await message.channel.edit(slowmode_delay=rate_limit_per_user)
            await usernotes_channel.send(f"{message.author.mention} slowed {message.channel.mention} to {str(rate_limit_per_user)} seconds.\n--{message.jump_url}")
            if rate_limit_per_user != 0:
                await message.channel.send(f"```\nThis channel is in slow mode. You can send one message every {str(rate_limit_per_user)} seconds. Please use the time between messages to take a breath, relax, and compose your thoughts.\n```")
        except discord.Forbidden:
            await message.channel.send("bear is forbidden from editing the channel")
            await message.add_reaction("⚠")
        except discord.HTTPException:
            await message.channel.send("editing the channel failed")
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def fast(message):  # checked
    """`!fast` sets the rate limit for the channel to `0`, disabling it."""
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        try:
            await message.channel.edit(slowmode_delay=0)
            await usernotes_channel.send(f"{message.author.mention} unslowed {message.channel.mention}.\n--{message.jump_url}")
        except discord.Forbidden:
            await message.add_reaction("⚠")
            await message.channel.send("bear is forbidden from editing the channel")
        except discord.HTTPException:
            await message.channel.send("editing the channel failed")
            await message.add_reaction("⚠")
    else:
        await message.add_reaction("🚫")


async def get_summary(message):  # checked
    """`!summarize https://www.some.com/article` prints a short summary of https://www.some.com/article"""
    await message.add_reaction("🐻")
    try:
        if message.author.id == 164918332221292544:
            sentences_count = int(message.id[-1])
        else:
            sentences_count = 5
        language = "ENGLISH"
        if message.content.lower().startswith("!sum "):
            url = message.clean_content[5:]
        else:
            url = message.clean_content[11:]
        if url.startswith("<"):
            url = url[1:]
        if url.endswith(">"):
            url = url[:-1]
        parser = HtmlParser.from_url(url, Tokenizer(language))
        stemmer = Stemmer(language)
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(language)
        summary = f"{message.author.mention}: ```"
        if str(message.id).endswith("01"):
            summary = summary.replace("```", "https://www.youtube.com/watch?v=dQw4w9WgXcQ ```", 1)
        for sentence in summarizer(parser.document, sentences_count):
            if summary != f"{message.author.mention}: ```":
                summary = f"{summary}\n\n"
            summary = f"{summary}{str(sentence)}"
        if len(summary) > 1995:
            summary = f"{summary[:1995]}..."
        summary = f"{summary}```"
        if summary == f"{message.author.mention}: ```\n\n````":
            summary = f"{message.author.mention}: I couldn't summarize the article you asked about. That can happen if the article is too short or I can't access it."
        await message.channel.send(summary)
    except Exception as e:
        print(e)
        await message.add_reaction("⚠")


async def spongemock(message):  # checked
    await message.add_reaction("🐻")
    if message.channel.id in [low_effort_channel_id, bot_spam_channel_id] or moderator_role in message.author.roles:
        try:
            sample_text = message.clean_content[11:]
            new_text = ""
            for letter in sample_text.lower():
                if random.random() > 0.5:
                    new_text += letter.upper()
                else:
                    new_text += letter
            with Image.open("mocking-spongebob-stock.jpg") as img:
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("Krabby Patty.ttf", 60)
                desc_new = textwrap.fill(new_text, 20)
                x = 20
                y = 20
                draw.multiline_text((x - 1, y - 1), desc_new, font=font, fill='black', spacing=10, align="center")
                draw.multiline_text((x + 1, y - 1), desc_new, font=font, fill='black', spacing=10, align="center")
                draw.multiline_text((x - 1, y + 1), desc_new, font=font, fill='black', spacing=10, align="center")
                draw.multiline_text((x + 1, y + 1), desc_new, font=font, fill='black', spacing=10, align="center")
                draw.multiline_text((x, y), desc_new, font=font, fill='white', spacing=10, align="center")
                output_buffer = BytesIO()
                img.save(output_buffer, "JPEG")
                output_buffer.seek(0)
            temp_file = discord.File(fp=output_buffer, filename="spongemock.jpg", spoiler=False)
            await message.channel.send(content=f"{message.author.mention}", file=temp_file)
            img.close()
            output_buffer.close()
        except Exception as e:
            await message.add_reaction("⚠")
            print(e)
    else:
        await message.add_reaction("🚫")


async def remindme(message):
    if moderator_role in message.author.roles or embed_role in message.author.roles:
        await message.add_reaction("🐻")
        reminder_text = message.content[10:]
        await message.channel.send(f"{message.author.mention}, When do you want the reminder?\nIntegers in the form of days, hours, minutes, and seconds are supported, up to 1 day. E.g: `4 hours`")

        def check(m):
            return m.channel == message.channel and m.author == message.author

        date_message = await client.wait_for('message', check=check, timeout=30)
        if isinstance(date_message, discord.Message):
            await date_message.add_reaction("🐻")
            date_message = date_message.content.lower()
            try:

                weeks = re.search("[0-9]+ week", date_message)
                if weeks is None:
                    weeks = 0
                else:
                    weeks = int(weeks.group(0).split(" ", maxsplit=1)[0])
                days = re.search("[0-9]+ day", date_message)
                if days is None:
                    days = 0
                else:
                    days = int(days.group(0).split(" ", maxsplit=1)[0])
                hours = re.search("[0-9]+ hour", date_message)
                if hours is None:
                    hours = 0
                else:
                    hours = int(hours.group(0).split(" ", maxsplit=1)[0])
                minutes = re.search("[0-9]+ minute", date_message)
                if minutes is None:
                    minutes = 0
                else:
                    minutes = int(minutes.group(0).split(" ", maxsplit=1)[0])
                seconds = re.search("[0-9]+ second", date_message)
                if seconds is None:
                    seconds = 0
                else:
                    seconds = int(seconds.group(0).split(" ", maxsplit=1)[0])

                duration = datetime.timedelta(days=days, seconds=seconds, microseconds=0, milliseconds=0, minutes=minutes,
                                              hours=hours, weeks=weeks)
                if duration == datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
                    await message.channel.send(f"{message.author.mention}, I couldn't parse a date from your message. Please be sure to use integers instead of strings (e.g. write `30` instead of `thirty`).")
                else:
                    await message.channel.send(f"{message.author.mention}, reminder set for `{duration}` from now.")
                    await asyncio.sleep(duration.total_seconds())
                    await message.channel.send(f"{message.author.mention}, {reminder_text}")
            except OverflowError:
                await message.channel.send(f'{message.author.mention}, the numbers are too big.')
            except Exception as e:
                print(e)
                await message.add_reaction("⚠🚫")
        else:
            await message.channel.send(f"{message.author.mention}, Discord returned an error or you didn't reply within 30 seconds.")
    else:
        await message.add_reaction("🚫")


def make_embed_from_message(message):
    """
    Takes a discord message and returns an embed quoting it.
    :param message: a discord message object
    :return: discord.Embed object quoting the message.
    """
    description = message.clean_content
    if len(description) > 2047:
        description = f"{description[2044]}..."
    em = discord.Embed(description=description)
    em.set_author(name=f"{message.author.display_name} : {message.author.id}",
                  icon_url=message.author.avatar_url)
    return em


async def user_metrics(message):
    """`!user_metrics n` Adds up all the messages people have sent, up to `n` days ago."""
    if moderator_role in message.author.roles:
        await message.add_reaction("🐻")
        days = message.content.replace("!user_metrics ", "")
        try:
            global user_log_lock
            if user_log_lock is True:
                await message.channel.send("I'm still working on it from last time.")
            else:
                user_log_lock = True
                user_count = {}
                after = datetime.datetime.utcnow() - datetime.timedelta(days=int(days))
                channel_counter = 0
                await message.channel.send(f"Alright. I'm adding up all the messages people have sent up to {days} days ago.")
                update_message = await message.channel.send("Getting started.")
                for message_channel in message.guild.text_channels:
                    if message_channel.id != tweets_channel_id:
                        await update_message.edit(content=f"checking {message_channel.mention} . Roughly {len(message.guild.text_channels) - channel_counter} channels left to go...")
                        channel_counter += 1
                        try:
                            async for channel_message in message_channel.history(limit=None, after=after):
                                user_count.setdefault(channel_message.author.display_name, 0)
                                user_count[channel_message.author.display_name] += 1
                        except:
                            pass
                await update_message.edit(content=f"{len(user_count)}/{message.guild.member_count} members were active in the last {days} days")
                pending_message = ""
                sorted_users = dict(OrderedDict(sorted(user_count.items(), key=lambda t: t[1], reverse=True)))
                for user in sorted_users:
                    next_chunk = f"{user}: {sorted_users[user]} ({round(sorted_users[user]/int(days))} per day)\n"
                    if len(pending_message) + len(next_chunk) < 2000:
                        pending_message += next_chunk
                    else:
                        await message.channel.send(pending_message)
                        pending_message = next_chunk
                if pending_message != "":
                    await message.channel.send(pending_message)
                user_log_lock = False
        except Exception as e:
            await message.add_reaction("⚠")
            await message.channel.send(content=f"{message.author.mention}: I encountered an error. Please make sure you included a number of days. Eg: `!user_metrics 10`")
            print(e)
            user_log_lock = False
    else:
        await message.add_reaction("🚫")


async def br_mode(message):
    if moderator_role in message.author.roles:
        await usernotes_channel.send(content=f"{message.author.mention} turned on br_mode for {message.channel.mention}.")
        await message.channel.send(content=f"Attention all {message.channel.mention} users, you have been selected for a special PD honor. We have determined that {message.channel.name} chat has become too large. Meanwhile, Bear is just waking from hibernation and requires sustenance. We will be feeding users one by one, Battle Royale style, to Bear until only one remains.")
        await message.delete()
        active_members = []
        blocked_members = []
        after = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)  # https://docs.python.org/3/library/datetime.html#timedelta-objects
        async for channel_message in message.channel.history(limit=999, after=after):
            if channel_message.author.bot is False and moderator_role not in channel_message.author.roles:
                active_members.append(channel_message.author)
        while len(active_members) - len(blocked_members) > 1:
            await asyncio.sleep(60)
            the_chosen = random.choice(active_members)
            while the_chosen in blocked_members:
                the_chosen = random.choice(active_members)
            blocked_members.append(the_chosen)
            await message.channel.send(content=f"{the_chosen.mention} was removed from the channel.")
            await message.channel.set_permissions(the_chosen, read_messages=False)
        await message.channel.send(content=f"{active_members[0].mention} won the contest.")
        await message.channel.send(content="The channel will reset in one minute.")
        await asyncio.sleep(60)
        for member in blocked_members:
            await message.channel.set_permissions(member, overwrite=None)


async def no_reposts(message):
    if moderator_role not in message.author.roles:
        pass

mod_functions_dict = {
    '!purge': purge,
    '!lock': lock,
    '!unlock': unlock,
    '!ban_id': ban_id,
    '!unban_id': unban_id,
    '!ban': ban,
    '!embed': embed,
    '!unembed': unembed,
    '!mute': mute,
    '!unmute': unmute,
    '!interview': interview,
    '!uninterview': uninterview,
    '!mod ': mod,
    '!unmod ': unmod,
    '!kick': kick,
    'baned': baned,
    '!muted': muted,
    '!new_command': new_command,
    '!add_command': new_command,
    '!delete_command': delete_command,
    '!remove_command': delete_command,
    '!slow': slow,
    '!fast': fast,
    '!add_role': add_role,
    '!remove_role': remove_role,
    '!tweet': tweet,
    '!modmute': modmute,
    '!mod-mute': modmute,
    '!unmodmute': unmodmute,
    '!unmod-mute': unmodmute,
    '!emoji_metrics': emoji_metrics,
    '!high_effort_command ': high_effort_command,
    '!record': record,
    '!stop': stop,
    '!modvote': modvote,
    '!clean_up_commands_channel': clean_up_commands_channel,
    '!user_metrics': user_metrics
}


member_functions_dict = {
    '!wolfram': do_wolfram,
    '!shitposting': shitposting,
    '!coin_flip': coin_flip,
    '!help': command_help,
    '!cat': get_cat,
    '!pupper': get_dog,
    '!dog': get_dog,
    '!targeted': targeted,
    '!iam ': iam,
    '!iamnot ': iamnot,
    '!stock ': get_stock,
    '!stocks': get_stock,
    '!predictit': predictit,
    '!electionresults': electionresults,
    '!wiki': wiki,
    '!me': me,
    '!needle': needle,
    '༼ つ ◕◕ ༽つ': needle,
    '!summarize': get_summary,
    '!sum ': get_summary,
    '!spongemock': spongemock,
    '!high_effort_commands': high_effort_commands,
    '!remind_me': remindme,
    '!info': info,
    '!dad': get_dad
}


@client.event
async def on_message(message):  # checked
    if client.is_ready():
        try:
            global all_users
            all_users_setdefault(message.author, message.created_at)
            message_lower = message.content.lower()
            if message.author == client.user or isinstance(message.channel, discord.abc.PrivateChannel) or message.author.bot:
                if isinstance(message.channel, discord.abc.PrivateChannel) and message.author != client.user:
                    await amici.send("{0}:{1} ({2}) sent this message to me.\n```\n{3}\n```".format(
                                                     message.author.name,
                                                     message.author.id,
                                                     message.author.mention,
                                                     message.clean_content))
                return
            if moderator_role not in message.author.roles and muted_role not in message.author.roles and mute_2_role not in message.author.roles:
                await spam_check(message)
                await content_check(message)
            if len(message.mentions) > 0 and client.user in message.mentions:
                await message.add_reaction('🐻')
            if message_lower in pd_settings['member_commands']:
                    await copypasta(message)
            for key in mod_functions_dict.keys():
                if message_lower.startswith(key):
                    await mod_functions_dict[key](message)
            for key in member_functions_dict.keys():
                if message_lower.startswith(key):
                    await member_functions_dict[key](message)
            if message.channel == curated_news_channel:
                if "http" not in message.content.lower() and message.author != client.user:
                    try:
                        await message.author.edit(nick=message.clean_content[:30])
                    except discord.Forbidden as e:
                        print(e)
                    await message.add_reaction("🤦")
            if beardy_role in message.role_mentions and beardy_role not in message.author.roles and message.channel.id not in [348896164776640512, 306928042830331907]:  # timeout1 or timeout2
                await message.author.add_roles(beardy_role)
                await beardy_channel.send("Wait what? {}".format(message.author.mention))
            # if re.search(tweet_regex, message.content):
            #     await get_tweet(message)
        except discord.errors.NotFound:
            pass
        except Exception as e:

            await amici.send("New `on_message` error captured:\n```\n{0}\n```\nfrom:`{1}`:`{2}` ({3}) in {4}\n```{5}```".format(
                                              e,
                                              message.author.name,
                                              message.author.id,
                                              message.author.mention,
                                              message.channel.mention,
                                              message.clean_content))


@client.event
async def on_raw_reaction_add(payload):
    if client.is_ready:
        payload_member = our_guild.get_member(payload.user_id)
        if payload_member is None:
            print("can't find the payload member")
        try:
            reactor_roles_names = [role.name for role in payload_member.roles]
        except AttributeError:
            reactor_roles_names = None
        payload_message_channel = client.get_channel(payload.channel_id)
        if payload_message_channel is None:
            print("can't find the payload channel")
        try:
            payload_message = await payload_message_channel.fetch_message(payload.message_id)
        except discord.errors.NotFound:
            return
        try:
            if payload_member != client.user:
                global copied_messages_in_curated
                if payload.emoji.name == "📌" or payload.emoji.name == "📍" or isinstance(payload.emoji, discord.Emoji) and payload.emoji.name == "googlePin":
                    if "can pin messages" in reactor_roles_names or moderator_role in payload_member.roles:
                        if payload_message.pinned is False:
                            channel_pins = await payload_message.channel.pins()
                            if len(channel_pins) > 48:
                                channel_pins.sort(key=lambda pin: pin.created_at)
                                await channel_pins[0].unpin()
                            await payload_message.pin()
                            log = f"This message by {payload_message.author.mention} was pinned to {payload_message.channel.mention} by {payload_member.mention}\n"
                            em = make_embed_from_message(payload_message)
                            if payload_message.attachments:
                                log = f"{log}\nmessage attachments: {[attachment.proxy_url for attachment in payload_message.attachments]}"
                            log = f"{log}\n--{payload_message.jump_url}"
                            await usernotes_channel.send(content=log, embed=em)
                if payload.emoji.name == "📰":
                    if "curators" in reactor_roles_names or moderator_role in payload_member.roles:
                        copied_message = None
                        async for message in curated_news_channel.history(limit=10):
                            if message.content.endswith(str(payload_message.id)):
                                copied_message = message
                        if copied_message is None and payload_message.channel != curated_news_channel:
                            await curated_news_channel.send(f'{payload_message.content}\n--{payload_message.jump_url}')  # copies the message to #curated news
                            async for message in curated_news_channel.history(limit=10):
                                if message.content.endswith(str(payload_message.id)):
                                    copied_message = message
                            await copied_message.add_reaction(payload.emoji)
                        try:
                            message_author_roles = [role.name for role in payload_message.author.roles]
                        except AttributeError:
                            message_author_roles = None
                        if "pdbeat" in reactor_roles_names or moderator_role in payload_member.roles:
                            source_message = None
                            if payload_message.author == discord.ClientUser and payload_message.channel == curated_news_channel:
                                status = payload_message.clean_content.rsplit('\n--', 1)[0]
                                source_message_channel = client.get_channel(int(payload_message.clean_content.rsplit('\n--', 2)[1]))
                                source_message = await source_message_channel.fetch_message(int(payload_message.clean_content.rsplit('/', 2)[2]))
                                try:
                                    message_author_roles = [role.name for role in source_message.author.roles]
                                except AttributeError:
                                    message_author_roles = None
                            else:
                                status = payload_message.clean_content
                                source_message = payload_message
                            if message_author_roles is None or "do not tweet" not in message_author_roles:
                                if "do not tweet" not in reactor_roles_names:
                                    t = await tweet(payload_message, status)
                                    if t.status_code == 200:
                                        await payload_message.add_reaction('🐦')
                                        if copied_message is not None:
                                            await copied_message.add_reaction('🐦')
                                        if source_message is not None:
                                            await source_message.add_reaction('🐦')
                                    else:
                                        await source_message.add_reaction("⚠")
                                else:
                                    await source_message.add_reaction("🚫")
                                    message.channel.send("That person opted out of being tweeted.")
                    else:
                        await payload_message.remove_reaction(payload.emoji, payload_member)
                if payload.emoji.name == '🐦':
                    await payload_message.remove_reaction(payload.emoji, payload_member)
                if payload.emoji.name == "❗":
                    await payload_message.add_reaction('👮')
                    await payload_message.remove_reaction(payload.emoji, payload_member)
                    mod_channel = client.get_channel(306760481031323648)
                    em = make_embed_from_message(payload_message)
                    content = f"{payload_member.mention} reported this message in {payload_message.channel.mention}:\n--{payload_message.jump_url}"
                    await mod_channel.send(content=content, embed=em)
                    await usernotes_channel.send(content=content, embed=em)
                if payload.emoji.name == "📑":
                    committee_role = our_guild.get_role(397112272385736721)
                    if committee_role in payload_member.roles:
                        destination_channel = client.get_channel(555135135129927683)
                        em = make_embed_from_message(payload_message)
                        content = f"{payload_member.mention} nominated this message from {payload_message.channel.mention}:\n--{payload_message.jump_url}"
                        await destination_channel.send(content=content, embed=em)
                        await usernotes_channel.send(content=content, embed=em)
                if "lul" in payload.emoji.name or "lol" in payload.emoji.name or "laugh" in payload.emoji.name:
                    if payload_message_channel == low_effort_channel and "{spd}" in payload_member.name.lower():
                        low_effort_channel.send(content="https://www.youtube.com/watch?v=RCUE0xrODYI")
        except discord.DiscordException as e:
            await payload_message.add_reaction("⚠")
            print(e)


# @client.event
# async def on_reaction_add(reaction, user):
#     if client.is_ready():
#         reactor_roles_names = [role.name for role in user.roles]
#         try:
#             if reaction.me is False:
#                 global copied_messages_in_curated
#                 if reaction.emoji == "📌" or reaction.emoji == "📍" or isinstance(reaction.emoji, discord.Emoji) and reaction.emoji.name == "googlePin":  # checked
#                     if "can pin messages" in reactor_roles_names or moderator_role in user.roles:
#                         if reaction.message.pinned is False:
#                             channel_pins = await reaction.message.channel.pins()
#                             if len(channel_pins) > 48:
#                                 channel_pins.sort(key=lambda pin: pin.created_at)
#                                 await channel_pins[0].unpin()
#                             await reaction.message.pin()
#                             log = f"This message by {reaction.message.author.mention} was pinned to {reaction.message.channel.mention} by {user.mention}\n"
#                             em = make_embed_from_message(reaction.message)
#                             if reaction.message.attachments:
#                                 log = f"{log}\nmessage attachments: {[attachment.proxy_url for attachment in reaction.message.attachments]}"
#                             log = f"{log}\n--{reaction.message.jump_url}"
#                             await usernotes_channel.send(content=log, embed=em)
#                     else:
#                         await reaction.message.remove_reaction(reaction.emoji, user)
#                 if reaction.emoji == "📰":
#                     print(f'found 📰\n--{reaction.message.jump_url}')
#                     if "curators" in reactor_roles_names or moderator_role in user.roles:
#                         print("found curator or moderator")
#                         print(f"reaction.message.channel.name is {reaction.message.channel.name}")
#                         copied_message = None
#                         print("getting currated_news_channel history")
#                         async for message in curated_news_channel.history(limit=10):
#                             if message.content.endswith(str(reaction.message.id)):
#                                 copied_message = message
#                         if copied_message is None and reaction.message.channel != curated_news_channel:
#                             print(f"message wasn't copied or in curated-news. copying message. reaction.message.channel.name is {reaction.message.channel.name}")
#                             await curated_news_channel.send(f'{reaction.message.content}\n--{reaction.message.jump_url}')  # copies the message to #curated news
#                             async for message in curated_news_channel.history(limit=10):
#                                 if message.content.endswith(str(reaction.message.id)):
#                                     copied_message = message
#                             print("adding 📰 to copied message")
#                             await copied_message.add_reaction(reaction.emoji)
#                         else:
#                             print("message was already copied or the message is in curated-news")
#                         try:
#                             print("collecting roles")
#                             message_author_roles = [role.name for role in reaction.message.author.roles]
#                         except AttributeError:
#                             print("no message author roles")
#                             message_author_roles = None
#                         if "pdbeat" in reactor_roles_names or moderator_role in user.roles:
#                             print("pdbeat or moderator in user_roles")
#                             source_message = None
#                             if reaction.message.author == client.user and reaction.message.channel == curated_news_channel:
#                                 print("bear made the message in #curated_news. splitting off the message link and getting source message")
#                                 status = reaction.message.clean_content.rsplit('\n--', 1)[0]
#                                 print("getting original message")
#                                 source_message_channel = client.get_channel(int(reaction.message.clean_content.rsplit('\n--', 2)[1]))
#                                 source_message = await source_message_channel.fetch_message(int(reaction.message.clean_content.rsplit('/', 2)[2]))
#                                 message_author_roles = [role.name for role in source_message.author.roles]
#                             else:
#                                 print("bear did not make the message")
#                                 status = reaction.message.clean_content
#                             if message_author_roles is None or "do not tweet" not in message_author_roles:
#                                 if "do not tweet" not in reactor_roles_names:
#                                     "print calling tweet function"
#                                     t = await tweet(reaction.message, status)
#                                     if t.status_code == 200:
#                                         print("successful tweet. adding bird")
#                                         await reaction.message.add_reaction('🐦')
#                                         if copied_message is not None:
#                                             print("copying bird to curated_news_channel")
#                                             await copied_message.add_reaction('🐦')
#                                         if source_message is not None:
#                                             print("copying bird to source message")
#                                             await source_message.add_reaction('🐦')
#                                     else:
#                                         await source_message.add_reaction("⚠")
#                                 else:
#                                     print("do not tweet in message author roles")
#                         print("done\n---")
#                     else:
#                         print("not curator or moderator")
#                         await reaction.message.remove_reaction(reaction.emoji, user)
#                 if reaction.emoji == '🐦':
#                     await reaction.message.remove_reaction(reaction.emoji, user)
#                 if reaction.emoji == "❗":
#                     await reaction.message.add_reaction('👮')
#                     await reaction.message.remove_reaction(reaction.emoji, user)
#                     mod_channel = client.get_channel(306760481031323648)
#                     em = make_embed_from_message(reaction.message)
#                     content = f"{user.mention} reported this message in {reaction.message.channel.mention}:\n--{reaction.message.jump_url}"
#                     await mod_channel.send(content=content, embed=em)
#                     await usernotes_channel.send(content=content, embed=em)
#         except discord.DiscordException:
#             await reaction.message.add_reaction("⚠")


@client.event
async def on_message_edit(before, after):  # checked
    if client.is_ready():
        if before.content != after.content and muted_role not in after.author.roles and mute_2_role not in after.author.roles:
            try:
                message_lower = after.content.lower()
                if moderator_role not in after.author.roles:
                    global all_users
                    all_users_setdefault(before.author, after.edited_at)
                    if after.author == client.user or isinstance(after.channel, discord.abc.PrivateChannel) or after.author.bot:
                        if isinstance(after.channel, discord.abc.PrivateChannel) and after.author != client.user:
                            await amici.send("`{0}`:`{1}` ({2}) sent this message to me.\n```\n{3}\n```".format(
                                after.author.name,
                                after.author.id,
                                after.author.mention,
                                after.clean_content))
                        return
                    await spam_check(after)
                    await content_check(after)
                if len(after.mentions) > 0 and client.user in after.mentions:
                    await after.add_reaction('🐻')
                if message_lower in pd_settings['member_commands'] and embed_role in after.author.roles:  #funbear
                    await copypasta(after)
                if moderator_role in after.author.roles:
                    for key in mod_functions_dict.keys():
                        if message_lower.startswith(key):
                            await mod_functions_dict[key](after)
                for key in member_functions_dict.keys():  #funbear
                    if message_lower.startswith(key):
                        await member_functions_dict[key](after)
                if after.channel == curated_news_channel:  #pdutils
                    if "http" not in after.content:
                        try:
                            await after.author.edit(nick=after.clean_content[:30])
                        except discord.Forbidden as e:
                            print(e)
                if beardy_role in after.role_mentions and beardy_role not in after.author.roles and after.channel.id not in [348896164776640512, 306928042830331907]:  # 534431079181058059  #@pdutils
                    await after.author.add_roles(beardy_role)
                # if re.search(tweet_regex, after.content):
                #     await get_tweet(after)
            except discord.errors.NotFound:
                pass
            except Exception as e:
                await amici.send("New `on_message` error captured:\n```\n{0}\n```\nfrom:`{1}`:`{2}` ({3}) in {4}\n```{5}```".format(
                                                  e,
                                                  after.author.name,
                                                  after.author.id,
                                                  after.author.mention,
                                                  after.channel.mention,
                                                  after.content))
        if after.pinned is True:    #pdutils
            channel_pins = await after.channel.pins()
            if len(channel_pins) > 48:
                channel_pins.sort(key=lambda pin: pin.created_at)
                await channel_pins[0].unpin()


@client.event
async def on_member_join(member):  # checked
    if client.is_ready():
        try:
            global all_users
            account_age = datetime.datetime.utcnow() - member.created_at
            account_age = account_age - datetime.timedelta(microseconds=account_age.microseconds)
            await usernotes_channel.send(f'`{member.name}`:`{member.id}` ({member.mention}) joined the server. Their account was created at {member.created_at.replace(microsecond=0)} (`{account_age}` ago)')
            all_users_setdefault(member, member.joined_at)
            if member.name.lower() in banned_names:
                await usernotes_channel.send('`{0}`:`{1}` ({2}) was automatically muted because their name includes a banned name.'.format(
                                                             member.name,
                                                             member.id,
                                                             member.mention))
                await member.add_roles(muted_role)
            time_passed = member.joined_at - all_users[member.id]['joined_at']
            all_users[member.id]['joined_at'] = member.joined_at
            if all_users[member.id]['join_strikes'] > 5:
                await usernotes_channel.send('`{0}`:`{1}` ({2}) was automatically banned for joining and leaving in a short period too many times.'.format(
                                                              member.name,
                                                              member.id,
                                                              member.mention))
                await member.guild.ban(delete_message_days=1)
            if time_passed.total_seconds() < join_allowance:
                all_users[member.id]['join_strikes'] += 1  # Add a strike
            if time_passed.total_seconds() > join_reset_period:
                all_users[member.id]['join_strikes'] -= 1  # Remove a strike
        except Exception as e:
            print(e)
            await amici.send("New `on_member_join` error captured:\n```\n{0}\n```\nMember: `{1}`:`{2}` ({3})".format(e, member.name, member.id, member.mention))


@client.event
async def on_member_remove(member):  # checked
    if client.is_ready():
        try:
            roles = [role.name for role in member.roles]
            await usernotes_channel.send(f'`{member.name}`:`{member.id}` ({member.mention}) left the server. their roles were `{roles}`')
        except Exception as e:
            print(e)
            await amici.send("New `on_member_remove` error captured:\n```\n{0}\n```\nMember: `{1}`:`{2}` ({3})".format(e, member.name, member.id, member.mention))


@client.event
async def on_member_ban(guild, user):  # checked
    if client.is_ready():
        try:
            await usernotes_channel.send('`{0}`:`{1}` ({2}) was banned from the server'.format(user.name, user.id, user.mention))
        except Exception as e:
            print(e)
            await amici.send("New `on_member_ban` error captured:\n```\n{0}\n```\nMember: `{1}`:`{2}` ({3})".format(e, user.name, user.id, user.mention))


@client.event
async def on_member_unban(guild, user):  # checked
    if client.is_ready():
        try:
            # unbanned_user = await client.fetch_user_info(user.id)
            await usernotes_channel.send('`{0}`:`{1}` ({2}) was unbanned from the server'.format(user.name, user.id, user.mention))
        except Exception as e:
            print(e)
            await amici.send("New `on_member_unban` error captured:\n```\n{0}\n```\nMember: `{1}`:`{2}` ({3})".format(e, user.name, user.id, user.mention))


@client.event
async def on_member_update(before, after):  # checked
    if client.is_ready():
        try:
            all_users_setdefault(before, datetime.datetime.utcnow())
            if before.bot is False and before.display_name != after.display_name:
                await usernotes_channel.send("`{0}`:`{1}`'s display name was changed to `{2}`:`{3}` ({4})".format(
                                              before.display_name, before.id, after.display_name,
                                              after.id, after.mention))
                if after.display_name.lower() in banned_names:
                    await usernotes_channel.send('`{0}`:`{1}` ({2}) was automatically muted because their username includes a banned name.'.format(
                                                  after.display_name, after.id,
                                                  after.mention))
                    await after.add_roles(muted_role)
            if before.roles != after.roles:
                await asyncio.sleep(2.0)
                added_roles = [role for role in after.roles if role not in before.roles]
                added_roles_names = [role.name for role in before.roles if role not in after.roles]
                removed_roles = [role for role in before.roles if role not in after.roles]
                removed_roles_names = [role.name for role in after.roles if role not in before.roles]
                if added_roles_names:  # empty lists are considered false https://docs.python.org/3.7/library/stdtypes.html#truth-value-testing
                    await usernotes_channel.send(f'`{before.name}`:`{before.id}` ({before.mention})\'s roles were changed to remove `{added_roles_names}`')
                if removed_roles_names:
                    await usernotes_channel.send(f'`{before.name}`:`{before.id}` ({before.mention})\'s roles were changed to include `{removed_roles_names}`')
                if added_roles == [interviewee_role]:  #PDutils
                    await asyncio.sleep(5.0)
                    await interview_channel.send('{0}. Psst. Over here. The mods want to talk to you. Message history is disabled in this channel. If you tab out, or select another channel, the messages will disappear.'.format(
                                                  after.mention))
                if added_roles == beardy_role:    #PDutils
                    await beardy_channel.send(content=f"wait what? {after.mention}")
                if moderator_role not in after.roles and added_roles == [muted_role] and all_users[after.id]['spammer'] is False:
                    roles = [role.id for role in before.roles]
                    pd_settings['muted_members'][after.id] = {'roles': roles}
                    with open('pd_settings.p', 'wb') as pfile:
                        pickle.dump(pd_settings, pfile)
                    await after.edit(roles=[muted_role])
                    await asyncio.sleep(5.0)
                    await timeout_channel.send(f'{after.mention}. \'You were muted because you broke the rules. Reread them, then write `@{moderator_role.name}` to be unmuted.\nMessage history is disabled in this channel. If you tab out, or select another channel, the messages will disappear.\'')
                if moderator_role not in after.roles and removed_roles == [muted_role] or removed_roles == [mute_2_role] or removed_roles == [muted_role, mute_2_role]:
                    if len(pd_settings['muted_members'][after.id]['roles']) > 0 and mute_2_role not in after.roles and muted_role not in after.roles:
                        roles = []
                        for role in pd_settings['muted_members'][after.id]['roles']:
                            role = discord.utils.get(our_guild.roles, id=role)
                            roles.append(role)
                        await after.edit(roles=roles)
                        pd_settings['muted_members'].pop(after.id, None)
                        with open('pd_settings.p', 'wb') as pfile:
                            pickle.dump(pd_settings, pfile)
        except Exception as e:
            print(e)
            await amici.send("New `on_member_update` error captured:\n```\n{0}\n```\nMember: `{1}`:`{2}` ({3})".format(e, after.name, after.id, after.mention))


client.run(token)
