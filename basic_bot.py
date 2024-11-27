import discord
from discord.ext import commands
import os
import random

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
    }
]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.text_channels, name='welcome')
    if welcome_channel:
        await welcome_channel.send(f'Welcome to the server, {member.mention}! We are glad to have you here. Feel free to ask any questions about polar bear conservation.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'polar bear' in message.content.lower():
        await message.channel.send('Polar bears are fascinating creatures! Did you know that they are classified as marine mammals because they spend most of their lives on the sea ice of the Arctic Ocean?')

    await bot.process_commands(message)

@bot.command()
async def info(ctx):
    await ctx.send('This bot is dedicated to discussing and promoting polar bear conservation. Feel free to ask any questions or share information!')

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

# Get the token from the environment variable
token = os.getenv("DISCORD_TOKEN")
if token is None:
    raise ValueError("No DISCORD_TOKEN found in environment variables.")
bot.run(token)