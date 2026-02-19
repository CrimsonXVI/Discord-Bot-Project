#Import
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import random
import aiohttp
import datetime

#Set-Up
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
load_dotenv()

#Constant
bot = commands.Bot(command_prefix="!", intents=intents)

ID_CHANNEL_Dictionary = {
    "Example1": 0x123456789ABCDEF,
    "Example2": 0x123456789ABCDEF,
    "Example3": 0x123456789ABCDEF,
    "Example4": 0x123456789ABCDEF,
    "Example5": 0x123456789ABCDEF
    }

#Function (Universal Use)
def create_embed(titleparams: str = "",colorparams: hex = 0, descriptionparams: str = "", thumbnail: str = None, nameparams: str = None, iconparams: str = None, profileparams: str = None, footparams: str = None, logoparams: str = None) -> discord.Embed:
    embed_template = discord.Embed(
        color=colorparams,
        title=titleparams,
        description=descriptionparams, 
        )
    
    embed_template.set_thumbnail(url=thumbnail)
    embed_template.set_author(name=nameparams, icon_url=iconparams)
    embed_template.set_footer(text=footparams, icon_url=logoparams)
        
    return embed_template

#Callable
@bot.command()
async def embed_test(context):
    embed = create_embed(
        titleparams="New Member Arrived!", 
        colorparams=0xFFFFFF, descriptionparams=f"Welcome on Board {context.author.mention} \n Don't be nervous about chatting, asking questions, or interacting. We're all the same!. \n I hope you enjoy your stay 😆", 
        thumbnail="https://gif.example.com", 
        nameparams=context.author.display_name, 
        iconparams=context.author.display_avatar.url, 
        footparams=f"Joined at {datetime.datetime.now()}",
        logoparams=context.guild.icon.url
    )
        
    await context.send(embed=embed)

#Event: Wellcome (Function)
@bot.event
async def on_member_join(member):
    channel_destination = member.guild.get_channel(ID_CHANNEL_Dictionary["Example1"])
    
    embed = create_embed(
        titleparams="New Member Arrived!", 
        colorparams=0xFFFFFF, 
        descriptionparams=f"Welcome on Board {member.mention}", 
        thumbnail="https://gif.example.com", 
        nameparams=member.display_name, 
        iconparams=member.display_avatar.url, 
        footparams=f"Joined at {datetime.datetime.now().strftime('%d %B %Y • %H:%M')}",
        logoparams=member.guild.icon.url if member.guild.icon else None
    )
    
    await channel_destination.send(embed=embed)
    
#QOTD (Class: Template)
class QOTD(commands.Cog):
    def __init__(self, bot):
        self.Quote_Emoji = ["Your Emoji 1", "Your Emoji 2"]
        self.Channel_ID = ID_CHANNEL_Dictionary["Example2"]
        self.bot = bot
        self.API = os.getenv("API")
        self.Title = ["❗ Your Title 1", "📖 Your Title 2", "✒ Your Title 3"]
        self.session = aiohttp.ClientSession()
        self.on_quote_event.start()
        
    async def get_quote(self):
        async with self.session.get(self.API) as resp:
            if resp.status == 200:
                return await resp.json()
            return None
        
    @tasks.loop(hours=24)
    async def on_quote_event(self):
        channel = self.bot.get_channel(self.Channel_ID)
        
        if not channel:
            return
        
        data = await self.get_quote()
        
        if not data:
            return 
        
        embed = create_embed(
            nameparams=random.choice(self.Title),
            titleparams=f"{random.choice(self.Quote_Emoji)} {data[0]['q']}",
            footparams=f"Writer ~ {data[0]['a']}",
            colorparams=0xFFFFFFF
        )
        
        await channel.send(embed=embed)
        
    @on_quote_event.before_loop
    async def before_quote_loop(self):
        await self.bot.wait_until_ready()
        
    async def cog_unload(self):
        self.on_quote_event.cancel()
        await self.session.close()
    
#Activation Status & Trigger
@bot.event
async def on_ready():
    channel = bot.get_channel(ID_CHANNEL_Dictionary["Example3"])
    
    if not channel:
        return 
    
    if hasattr(bot, 'already_announce'):
        return
    
    bot.already_announce = True
    
    if not bot.get_cog("QOTD"):
        await bot.add_cog(QOTD(bot))
        
    embed = create_embed(
        nameparams="📢 Bot Status Announcement",
        titleparams="Your Bot is Online"
    )
    
    await channel.send(
        embed=embed,
        allowed_mentions=discord.AllowedMentions(everyone=True),
        content='@everyone'        
        )
    
#Run
bot.run(os.getenv("TOKEN"))