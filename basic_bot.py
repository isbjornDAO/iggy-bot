import discord
from discord.ext import commands
import os
import random
import asyncio
from pymongo import MongoClient

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
        "question": "How much can an adult male polar bear weigh?",
        "options": ["300-600 kg", "400-800 kg", "500-1000 kg", "600-1200 kg"],
        "answer": "400-800 kg"
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

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.text_channels, name='welcome')
    if welcome_channel:
        await welcome_channel.send(f'Welcome to the server, {member.mention}! We are glad to have you here. Feel free to ask any questions about polar bear conservation or the AVAX blockchain.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'polar bear' in message.content.lower():
        fact = random.choice(polar_bear_facts)
        await message.channel.send(f'Polar Bear Fact: {fact}')

    if 'avax' in message.content.lower() or 'avalanche' in message.content.lower():
        fact = random.choice(avax_facts)
        await message.channel.send(f'AVAX Fact: {fact}')

    await bot.process_commands(message)

@bot.command()
async def info(ctx):
    await ctx.send('This bot is dedicated to discussing and promoting polar bear conservation and educating about the AVAX blockchain. Feel free to ask any questions or share information!')

@bot.command()
async def trivia(ctx):
    question = random.choice(trivia_questions)
    options = "\n".join([f"{i+1}. {option}" for i, option in enumerate(question["options"])])
    await ctx.send(f"{question['question']}\n{options}")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        return await ctx.send('Sorry, you took too long to answer!')

    answer_index = int(msg.content) - 1
    if question["options"][answer_index] == question["answer"]:
        await ctx.send('Correct! Well done!')
    else:
        await ctx.send(f'Sorry, that\'s incorrect. The correct answer is {question["answer"]}.')

@bot.command()
async def explore(ctx):
    user_id = ctx.author.id
    if user_id not in user_data:
        user_data[user_id] = {"points": 0, "achievements": [], "items": []}
    await ctx.send('You are now exploring the Arctic! Type `!walk` to move around and `!look` to find interesting things.')

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
    
@bot.command()
async def fact(ctx):
    fact = random.choice(polar_bear_facts)
    await ctx.send(f'Polar Bear Fact: {fact}')

@bot.command()
async def status(ctx):
    user_id = ctx.author.id
    if user_id not in user_data:
        return await ctx.send('You need to start exploring first by typing `!explore`.')
    
    points = user_data[user_id]["points"]
    items = ", ".join(user_data[user_id]["items"])
    await ctx.send(f'You have {points} points and the following items: {items}')

# Get the token from the environment variable
token = os.getenv("DISCORD_TOKEN")
if token is None:
    raise ValueError("No DISCORD_TOKEN found in environment variables.")
bot.run(token)