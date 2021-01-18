import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)


sys.path.append(parentdir)
import discord
import json
from haterater import HateRater
from discord.ext import commands, tasks

os.chdir(currentdir)


ID = None
PREFIX = None
stats_toggle = True

person_data = {}

graph_toggle = False

# Reads in personal data from the json file
with open("persondata.json") as df:
    person_data = json.load(df)
    df.close()

# Reads in config file and sets ID and Prefix
with open("config.json") as df:
    config = json.load(df)
    ID = config["id"]
    PREFIX = config["prefix"]
    df.close()


client = commands.Bot(command_prefix=PREFIX)


@client.event
async def on_ready():
    """
    When the bot starts indicates the console that it is online and starts the update_person loop
    """
    print("HateBot Online")
    update_person.start()


@tasks.loop(seconds=5)
async def update_person():
    """
    Every 5 seconds in an infinite loop, persondata.json is updated with data from person_data
    """
    global person_data
    with open("persondata.json", "w") as df:
        json.dump(person_data, df)
        df.close()


@client.command()
async def togglegraph(ctx):
    """
    a command that toggles the global variable graph_toggle and indicates to the user if the graphs will show or not after each post
    """
    global graph_toggle
    graph_toggle = not graph_toggle
    a = "Now showing " if graph_toggle else "Now not showing "
    await ctx.send(f"{a}hate speech graph")


@client.command()
async def togglestats(ctx):
    """
    a command that toggles the global variable stats_toggle and indicates to the user if the stats will be messaged to them after each post
    """
    global stats_toggle
    stats_toggle = not stats_toggle
    a = "Now showing " if graph_toggle else "Now not showing "
    await ctx.send(f"{a}hate speech stats")


@client.command()
async def getuserstats(ctx, user: discord.Member = None):
    """
    Displays to the user the stats for how many times an idividual has used hate speech or offensive language
    in a post
    """
    global person_data
    if user is None:
        user = ctx.author.id
    us_id = str(user.id)
    if not us_id in person_data.keys():
        await ctx.send(
            f"<@{us_id}> has not said any hate speech nor offensive language! :D"
        )
    else:
        await ctx.send(
            f'<@{us_id}> has said offensive language {person_data[us_id]["offensive"]}'
            + f' time and has said hate speech {person_data[us_id]["hate"]} times.'
        )


@client.event
async def on_message(message):
    """
    Whenever a user enters messages it will check the message through for its scores if it is hate speech or not
    It will message the user the stats by default depending if stats_toggle is on
    If a message is offensive or hateful it will delete that message (This bot is kid friendly :D)
    If graph_toggle is true, a graph will be displayed in chat for what the rater thinks the post was
    """
    await client.process_commands(message)
    global graph_toggle
    if not message.author.bot:
        if stats_toggle:
            us_id = str(message.author.id)
            rating = HateRater(message.content)
            (hate, offensive, neutral) = rating.getScoresFromPost(graph_toggle)
            await message.author.send(
                f"Hate Rating: {hate}\nOffensive Rating: {offensive}\n Neutral Rating: {neutral}"
            )
            rate = ""
            if max(hate, offensive, neutral) == hate:
                rate = "hate"
                if not us_id in person_data.keys():
                    person_data[us_id] = {"offensive": 0, "hate": 0}
                person_data[us_id]["hate"] += 1

            elif max(hate, offensive, neutral) == offensive:
                rate = "offensive"
                if not us_id in person_data.keys():
                    person_data[us_id] = {"offensive": 0, "hate": 0}
                person_data[us_id]["offensive"] += 1
            else:
                rate = "neutral"
            await message.author.send(f"Your message is: {rate}")

            if not rate == "neutral":
                await message.delete()
        if graph_toggle:
            curdir = os.getcwd()
            pardir = os.path.dirname(curdir)

            os.chdir(pardir)
            await message.channel.send(file=discord.File("post_analysis.jpg"))
            os.chdir(curdir)


client.run(ID)
