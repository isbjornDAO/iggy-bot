import asyncio
import random
import os
from datetime import datetime, timedelta
from pymongo import MongoClient
import discord
from discord.ext import commands

description = '''Isbjorn Support Bot'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', description=description, intents=intents)

# MongoDB setup
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client['discord_bot']
user_collection = db['users']

trivia_questions = [
    {
        "question": "What is the primary diet of polar bears?",
        "options": ["Seals", "Fish", "Penguins", "Krill"],
        "answer": "Seals"
    },
    {
        "question": "Where do polar bears primarily live?",
        "options": ["Antarctica", "Arctic", "Greenland", "Siberia"],
        "answer": "Arctic"
    },
    {
        "question": "What color is a polar bear's skin?",
        "options": ["White", "Black", "Brown", "Pink"],
        "answer": "Black"
    },
    {
        "question": "How long can polar bears swim continuously?",
        "options": ["Several hours", "One day", "Several days", "One week"],
        "answer": "Several days"
    },
    {
        "question": "What is the scientific name for the polar bear?",
        "options": ["Ursus arctos", "Ursus maritimus", "Ursus americanus", "Ursus thibetanus"],
        "answer": "Ursus maritimus"
    }
]

user_data = {}
timeout_duration = timedelta(minutes=10)  # Set the timeout duration

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.text_channels, name='welcome')
    if welcome_channel:
        await welcome_channel.send(f'Welcome to the server, {member.mention}! We are glad to have you here. Feel free to ask any questions about polar bear conservation or the AVAX blockchain.')

@bot.command()
async def info(ctx):
    await ctx.send('This bot is dedicated to discussing and promoting polar bear conservation and educating about the AVAX blockchain. Feel free to ask any questions or share information!')

@bot.command()
async def walk(ctx):
    user_id = ctx.author.id
    if user_id not in user_data:
        user_data[user_id] = {"points": 0, "items": [], "last_action": datetime.min}

    now = datetime.now()
    if now - user_data[user_id]["last_action"] < timeout_duration:
        return await ctx.send('You need to wait before you can walk again.')

    user_data[user_id]["last_action"] = now
    points = random.randint(1, 5)
    user_data[user_id]["points"] += points
    await ctx.send(f'You went for a walk and earned {points} points!')

@bot.command()
async def look(ctx):
    user_id = ctx.author.id
    if user_id not in user_data:
        return await ctx.send('You need to start exploring first by typing `!explore`.')

    now = datetime.now()
    if now - user_data[user_id]["last_action"] < timeout_duration:
        return await ctx.send('You need to wait before you can look again.')

    user_data[user_id]["last_action"] = now

    findings = [
        {"message": "You found a polar bear! Type `!fact` to learn something new about polar bears.", "points": 10, "item": "Polar Bear Encounter"},
        {"message": "You found a seal! Polar bears love to eat seals.", "points": 5, "item": "Seal Encounter"},
        {"message": "You found some sea ice. Polar bears use sea ice to hunt for seals.", "points": 3, "item": "Sea Ice"},
        {"message": "You found a snowstorm! Be careful out there.", "points": 2, "item": "Snowstorm Encounter"},
        {"message": "You found a rare Arctic flower!", "points": 15, "item": "Arctic Flower"},
        {"message": "You found an ancient artifact buried in the ice!", "points": 20, "item": "Ancient Artifact"}
    ]
    finding = random.choice(findings)
    user_data[user_id]["points"] += finding["points"]
    user_data[user_id]["items"].append(finding["item"])
    await ctx.send(f'{finding["message"]} You earned {finding["points"]} points!')

# Get the token from the environment variable
token = os.getenv("DISCORD_TOKEN")
if token is None:
    raise ValueError("No DISCORD_TOKEN found in environment variables.")
bot.run(token)