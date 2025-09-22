import discord  
import asyncio  
import os
import random  
import string  
import base64  
import requests  
  
intents = discord.Intents.default()  
intents.message_content = True  
intents.members = True  
  
client = discord.Client(intents=intents)  
  
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  
REPO = "BG-Home-Official/Script"  
FILE_PATH = "Key"  
BRANCH = "main"  
url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"  
  
def generate(length=12):  
    characters = string.ascii_letters + string.digits  
    return ''.join(random.choice(characters) for _ in range(length))  
  
def update():  
    passwords = generate(length=12)  
    print("Generated password:", passwords)  
    new_content = passwords  
    headers = {  
        "Authorization": f"token {GITHUB_TOKEN}",  
        "Accept": "application/vnd.github.v3+json"  
    }  
  
    response = requests.get(url, headers=headers, params={"ref": BRANCH})  
    response.raise_for_status()  
    file_info = response.json()  
    sha = file_info["sha"]  
  
    b64_content = base64.b64encode(new_content.encode()).decode()  
  
    payload = {  
        "message": "Update file via script",  
        "content": b64_content,  
        "branch": BRANCH,  
        "sha": sha  
    }  
  
    put_response = requests.put(url, headers=headers, json=payload)  
    put_response.raise_for_status() 
  
@client.event  
async def on_message(msg):  
    if msg.author == client.user:  
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
    print(f"Bot logged in as {client.user}")  
    
    client.loop.create_task(loop_update())  
  
async def loop_update():  
    while True:  
        try:  
            update()  
        except Exception as e:  
            print("Error while updating:", e)  
        await asyncio.sleep(86400)
  
if __name__ == "__main__":
    client.run(os.getenv("DISCORD_TOKEN"))
