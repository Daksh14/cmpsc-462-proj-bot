from sqlite3 import Error
from dotenv import load_dotenv
from db import db_connect;

import sqlite3
import os
import discord

# load the token env
load_dotenv()
# Connec to database
db_connect()

class Bot(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = Bot(intents=intents)
# client.run(os.getenv('BOT_TOKEN'))