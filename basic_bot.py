import discord
from discord.ext import commands
import os
import random
import asyncio

description = '''Isbjorn Support Bot'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', description=description, intents=intents)

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

polar_bear_facts = [
    "Polar bears are classified as marine mammals because they spend most of their lives on the sea ice of the Arctic Ocean.",
    "Polar bears primarily eat seals, which they hunt from the edge of sea ice.",
    "Polar bears have black skin under their white fur to better absorb the sun's rays.",
    "Polar bears can swim for days at a time to get from one piece of ice to another."
]

avax_facts = [
    "Avalanche (AVAX) is a decentralized, open-source blockchain with smart contract functionality.",
    "Avalanche aims to provide a scalable blockchain solution while maintaining decentralization and security.",
    "The AVAX token is used for staking, paying transaction fees, and participating in governance on the Avalanche network.",
    "Avalanche supports the creation of custom blockchains and decentralized applications (dApps)."
]

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
    await ctx.send('You are now exploring the Arctic! Type `!find` to look for interesting things.')

@bot.command()
async def find(ctx):
    findings = [
        "You found a polar bear! Type `!fact` to learn something new about polar bears.",
        "You found a seal! Polar bears love to eat seals.",
        "You found some sea ice. Polar bears use sea ice to hunt for seals.",
        "You found a snowstorm! Be careful out there."
    ]
    finding = random.choice(findings)
    await ctx.send(finding)

@bot.command()
async def fact(ctx):
    fact = random.choice(polar_bear_facts)
    await ctx.send(f'Polar Bear Fact: {fact}')

# Get the token from the environment variable
token = os.getenv("DISCORD_TOKEN")
if token is None:
    raise ValueError("No DISCORD_TOKEN found in environment variables.")
bot.run(token)