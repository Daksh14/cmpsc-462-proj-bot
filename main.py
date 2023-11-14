from sqlite3 import Error
from dotenv import load_dotenv
from db import db_connect;

import sqlite3
import os
import discord
from discord import commands
import openai

# load the token env
load_dotenv()
# Connect to database
db_connect()

# OpenAI GPT-3.5 API key
openai.api_key = "your_openai_api_key"

class Bot(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        self.determine_text_appropriateness(message)

        # Check if the message starts with the ! prefix
        if message.content.startswith('!'):
            # Get the command and arguments
            command, *args = message.content[1:].split()
            if command == 'ai':
                gpt_response = self.get_chatgpt_response(args)
                message.send(gpt_response)


    #@bot.command(name='ai')
    async def determine_text_appropriateness(self, message):
        try:
            automod = ("Determine whether or not this post is appropriate for a kindergarten environment."
                       "If it is not, then determine a rating from 1-10 on how inappropriate it is."
                       "If it is beyond a 5, then we will delete the post and send a warning to the user."
                       "Restrict your message to ONLY an integer value from 1-10 if it's inappropriate."
                       "If the message IS appropriate, then return a 0."
                       "Here is the message in question: " + message.content)

            #[TODO]: Add points to a yamean graph for each user
            print(self.get_chatgpt_response(automod))

        except Exception as e:
            print(e)

    # Translates text from one language to another using ChatGPT openAI
    async def translate_text(self, message):
        try:
            translate_prompt = ("Translate the following text from its curent language to English: " + message.content)
            print(self.get_chatgpt_response(translate_prompt))

        except Exception as e:
            print(e)

    async def get_chatgpt_response(self, args):
        if len(args) == 0:
            return "Please enter a message to generate a response."
        else:
            input_text = " ".join(args)
            return self.generate_ai_response(input_text)

    async def generate_ai_response(self, input_text):
        try:
            # Use OpenAI API to generate a response
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=input_text,
                temperature=0.7,
                max_tokens=150,
                n=1
            )

            return response.choices[0].text

        except Exception as e:
            print(f"Error generating AI response: {e}")
            return "Sorry, an error occurred while generating the AI response."

intents = discord.Intents.default()
intents.message_content = True

client = Bot(intents=intents)
# client.run(os.getenv('BOT_TOKEN'))