import discord
import os

TOKEN = "MTQwNjU4NDEyNTAxOTkxNDQ1NA.GVeo2l.4bTzM843y6DqY7SB7gRCaijp6_8-j3ZkPqN7hY"  # Or replace with your bot token string

intents = discord.Intents.default()
intents.message_content = True  # Needed to read messages

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:  # Prevent replying to itself
        return
    
    await message.channel.send("Hi")

client.run(TOKEN)
