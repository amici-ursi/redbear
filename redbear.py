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
        self.all_users = dict()
        self.av_api_key = ''   #alphavantage/stock API
        self.counting_emoji = False
        self.counting_reactions = False       
        self.counting_users = False
        
        #TODO: add all of these to Config and allow add/remove commands.
        self.no_copypasta_channels = [306924977981095936, 314146955372527618]
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
        
        #for member in list(pd_settings['muted_members']):
        #    member = our_guild.get_member(member)
        #    if member is not None and muted_role not in member.roles and mute_2_role not in member.roles and modmute_role not in member.roles:
        #        pd_settings['muted_members'].pop(member.id, None)

        default_guild = {
            
        }

        self.config.register_guild(**default_guild)

        #Load roles, channels, users - that we use throughout the cog
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

    @commands.command()
    async def shitposting(self, ctx):
        if self.embed_role in ctx.author.roles or self.moderator_role in ctx.author.roles:
            copypasta_text = get_shitposts(ctx)
            await ctx.channel.send('look, until you get your shit together i really don\'t have the time to explain {} to a kid'.format(random.choice(copypasta_text)))
        else:
            await message.add_reaction("🚫")

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

def all_users_setdefault(member, timestamp):
    all_users.setdefault(member.id, {'join_strikes': 0, 'joined_at': timestamp, 'strikes': 0, 'last_check': timestamp, 'last_message': None, 'spammer': False})

def get_tweet_urls(content):
    tweet_regex = re.compile(r"https://twitter\.com/[a-zA-Z0-9_]+/status/[0-9]+")
    return tweet_regex.findall(content)

def get_tweet_id(content):
    tweet_status_regex = re.compile(r"([0-9]+)$")
    return int(tweet_status_regex.findall(tweet_url)[0])
