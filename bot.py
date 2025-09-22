import discord  
import asyncio  
import os
import random  
import string  
import base64  
import requests  

from keep_alive import keep_alive

intents = discord.Intents.default()  
intents.message_content = True  
intents.members = True  

keep_alive()

client = discord.Client(intents=intents)  

url = "https://api.github.com/repos/BG-Home-Official/Script/contents/Key"  
  
def generate(length=12):  
    characters = string.ascii_letters + string.digits  
    return ''.join(random.choice(characters) for _ in range(length))  
 
def update():  
    passwords = generate(length=12)  
    print("Generated password:", passwords)
    new_content = passwords  
    headers = {  
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",  
        "Accept": "application/vnd.github.v3+json"
    }  
  
    response = requests.get(url, headers=headers, params={"ref": "main"})  
    response.raise_for_status()  
    file_info = response.json()  
    sha = file_info["sha"]  
  
    b64_content = base64.b64encode(new_content.encode()).decode()  
  
    payload = {  
        "message": "Update file via script",  
        "content": b64_content,  
        "branch": "main",  
        "sha": sha
    }  
  
    put_response = requests.put(url, headers=headers, json=payload)  
    put_response.raise_for_status() 
  
@client.event  
async def on_message(msg):  
    if msg.author == client.user or msg.guild is None:
        return
    
    if msg.channel.id not in [1390208355867295916, 1419532992212111420]:
        return
    
    if "**Output Log**" in msg.content:  
        print("Good")
    else:
        try:  
            await msg.delete()  
        except discord.Forbidden:  
            print("Bot has no permission to delete this message.")  
        except discord.NotFound:  
            print("Message already deleted.")  
        except Exception as e:  
            print(f"Error deleting message: {e}")  
  
@client.event  
async def on_ready():  
    if not hasattr(client, "update_task"):
        client.update_task = client.loop.create_task(loop_update())
    print(f"Bot logged in as {client.user}")  
    
async def loop_update():  
    while True:  
        try:  
            update()  
        except Exception as e:  
            print("Error while updating:", e)  
        await asyncio.sleep(86400) 
  
if __name__ == "__main__":
    client.run(os.getenv("DISCORD_TOKEN"))
