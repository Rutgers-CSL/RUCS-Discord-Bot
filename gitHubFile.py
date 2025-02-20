# bot.py
import os
import discord
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
load_dotenv()
TOKEN = 'HIDDEN'
intents = discord.Intents.default()  # Use default intents
client = discord.Client(intents=intents)
intents.messages = True  # Enable message reading intent
intents.guilds = True  # Enable guilds intent


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        print(f'Connected to server: {guild.name} (ID: {guild.id})')
        
        # Find the first text channel where the bot has permission to send messages
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(f'Hello! {client.user} is now online! 🚀')
                break  # Stop after sending to the first available channel


@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Prevent the bot from responding to itself

    if message.content.lower() == "hey there":
        await message.channel.send("heyyyyyyyy")

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Prevent the bot from responding to itself

    if message.content.lower() == "hi how are you doing":
        await message.channel.send("good\nand what about u")

        return  # Prevent the bot from responding to itself

    elif message.content.lower() == "dinner on busch":
        ans = ""
        await message.channel.send("this is what is for dinner on busch")
        url = "https://menuportal23.dining.rutgers.edu/foodpronet/pickmenu.aspx?locationNum=04&locationName=Busch+Dining+Hall&dtdate=02/19/2025&activeMeal=Dinner&sName=Rutgers+University+Dining"  # Replace with the actual website URL
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

    # Find and print all unique tags in the HTML
            print("START")
           # print(soup.find("fieldset"))
            with open("output2.txt", "a") as f:
        
                for item in soup.find_all("fieldset"):
                    count = 0
                    #print("LIST", item.text, count)
                    for foodItem in item:
                        print("hereeee")
                        if(count == 1):
                            
                            ans+=foodItem.text.strip() +"\n"
                            print("food item: " + foodItem.text.strip())
                            #await message.channel.send(foodItem.text.lstrip())
                            print(foodItem.text.lstrip(),file=f)
                        count +=1
                
                for i in range(0, len(ans), 1999):
                    await message.channel.send(ans[i:i+1999])  
    
            print("END")
            
            unique_tags = set(tag.name for tag in soup.find_all())
            print("Unique tags found in the HTML:")
            print("\n".join(sorted(unique_tags)))

    # Save formatted HTML for manual inspection
            with open("website.html", "w", encoding="utf-8") as file:
                file.write(soup.prettify())
    
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")


client.run(TOKEN)