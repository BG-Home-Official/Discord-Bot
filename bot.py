import discord
import os

TOKEN = os.getenv("DISCORD_TOKEN")

from keep_alive import keep_alive

keep_alive()

intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    # Prevent the bot from replying to itself
    if message.author == client.user:
        return
    
    # Reply to every message with "Hi"
    await message.channel.send("Hi")

client.run(TOKEN)
