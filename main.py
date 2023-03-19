from os import getenv
import discord
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import asyncio
from dotenv import load_dotenv

bot = discord.Bot()

def until_alpha(string: str):
    while not string[0].isalpha():
        string = string[1:]
    return string

@bot.slash_command(description="Generates a personlized LFG invite in the form of an embed or image")
async def create_invite(
    ctx,

    rank: discord.Option(str, "Declare the required rank", 
    choices=[
    "❔ Any",
    "🥉 Bronze",
    "🥈 Silver",
    "🥇 Gold",
    "🥉🥈 Bronze or Silver",
    "🥈🥇 Silver or Gold",
    "🏆 Top 1000",
    "🏆 Top 500",
    "🏆 Top 100"
    ]),

    gamemode: discord.Option(str, "Declare the gamemode", 
    choices=[
        "❔ Any",
        "▶ Quickplay",
        "🏆 Tournament",
    ]),

    time: discord.Option(str, "Declare the time in which your squad will begin and/or end"),

    output: discord.Option(str, "Select the desired invite format", choices=[
    "Embed",
    "Image"
    ]),

    second_player: discord.Option(discord.SlashCommandOptionType.user, required=False),

    voice_channel:  discord.Option(discord.SlashCommandOptionType.channel, required=False),
):
    players = [ctx.author.mention]
    if second_player:
        players.append(second_player.mention)
    
    players = f"{', '.join(players)}: {len(players)}/3"

    if output == "Embed":
        details = {
            "Rank":rank,
            "Gamemode":gamemode,
            "Time":time,
            "Players":players,
        }

        if voice_channel:
            details["Voice Channel"] = f"[Join channel]({str(await voice_channel.create_invite())})"

        embed = discord.Embed(
            title="The Finals - NA LFG",
            description=f"{ctx.author.name} is looking for a group!",
            color=discord.Color.from_rgb(210, 31, 60)
        )

        embed.set_thumbnail(url=str(ctx.author.display_avatar.url))

        for k, v in details.items():
            embed.add_field(name=k, value=v, inline=True)
        
        await ctx.respond(embed=embed)
    """ else:
        ctx.respond("holup")
        img = Image.open("assets/banner.png")
        img = ImageDraw.Draw(img) """

load_dotenv()
TOKEN = str(getenv("TOKEN"))
bot.run(TOKEN)