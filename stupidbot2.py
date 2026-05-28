import os
import discord
from discord.ext import commands
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# THE CREATURE
stupidbot = ChatBot(
    "StupidBot2",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        "chatterbot.logic.BestMatch"
    ],
    database_uri="sqlite:///database.sqlite3"
)

print("training creature...")

# NORMAL TRAINING
corpus_trainer = ChatterBotCorpusTrainer(stupidbot)
corpus_trainer.train("chatterbot.corpus.english")

# CHAOTIC TRAINING
conversation = [
    "hello",
    "go away bish",

    "how are you",
    "stupid and miserable",

    "what is 2+2",
    "fish",

    "who are you",
    "an unfortunate accident",

    "can you help me",
    "absolutely not",

    "good morning",
    "its NOT a good morning",

    "what are you doing",
    "eating drywall",

    "are you smart",
    "unfortunately no",

    "i love you",
    "thats your first mistake"
]

list_trainer = ListTrainer(stupidbot)
list_trainer.train(conversation)

@bot.event
async def on_ready():
    print(f"{bot.user} has awakened unfortunately")

    await bot.change_presence(
        activity=discord.Game("eating drywall")
    )

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if (
        message.content.lower().startswith("stupidbot")
        or bot.user in message.mentions
    ):

        response = stupidbot.get_response(message.content)

        await message.reply(str(response))

    await bot.process_commands(message)

# ERROR HANDLER
@bot.event
async def on_error(event, *args, **kwargs):

    print("""
!!!!!!!! STUPIDBOT FAILURE DETECTED !!!!!!!!

possible causes:
- yogurt overflow
- drywall deficiency
- emotional collapse
- fish miscalculation
- windows xp corruption

event that exploded:
""")

    print(event)

# SECRET TOKEN FROM RENDER
bot.run(os.getenv("TOKEN"))
