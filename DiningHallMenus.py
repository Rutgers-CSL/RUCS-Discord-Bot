import os
import discord
from dotenv import load_dotenv
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re
from discord import app_commands
from discord.ext import commands

# Load environment variables
load_dotenv()
TOKEN = 'Hidden'
intents = discord.Intents.default()  # Use default intents
client = discord.Client(intents=intents)
intents.messages = True  # Enable message reading intent
intents.guilds = True  # Enable guilds intent
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    try:
        synced = await bot.tree.sync()  # Sync slash commands with Discord
        print(f'Synced {len(synced)} commands: {[cmd.name for cmd in synced]}')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

def show_Dining_Hall(url):
    """Scrapes the menu from the Rutgers dining hall website using the original logic."""
    ans = ""
    today_date = datetime.today().strftime("%m/%d/%Y")
    url = re.sub(r"dtdate=\d{2}/\d{2}/\d{4}", f"dtdate={today_date}", url)
    
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to retrieve the menu."

    soup = BeautifulSoup(response.text, "html.parser")

    with open("output2.txt", "a") as f:
        h3_items = soup.find_all("h3")  # Section headers
        done = 0
        increment = 2

        for item in soup.find_all("fieldset"):
            count = 0
            if item.sourceline > h3_items[increment].sourceline:
                if increment == len(h3_items) - 1 and done == 0:
                    done += 1
                    ans += f"\n**{h3_items[increment].text}**\n\n"
                
                if increment < len(h3_items) - 1:
                    ans += f"\n**{h3_items[increment].text}**\n\n"
                    if increment < len(h3_items) - 1:
                        increment += 1

            for foodItem in item:
                if count == 1:
                    ans += f"- {foodItem.text.strip().lower()}\n"
                count += 1

    return ans if ans else "No menu items found."

# Slash commands for each dining hall
@bot.tree.command(name="livi-lunch", description="Get Livingston Dining Hall's lunch menu.")
async def livi(interaction: discord.Interaction):
    await interaction.response.defer()
    url = 'https://menuportal23.dining.rutgers.edu/foodpronet/pickmenu.aspx?locationNum=03&locationName=Livingston+Dining+Commons&dtdate=03/03/2025&activeMeal=Lunch&sName=Rutgers+University+Dining'
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Livingston Dining Hall Menu:**\n{menu}")

@bot.tree.command(name="livi-breakfast", description="Get Livingston Dining Hall's breakfast menu.")
async def livi(interaction: discord.Interaction):
    await interaction.response.defer()
    url = 'https://menuportal23.dining.rutgers.edu/foodpronet/pickmenu.aspx?sName=Rutgers+University+Dining&locationNum=03&locationName=Livingston+Dining+Commons&naFlag=1'
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Livingston Dining Hall Menu:**\n{menu}")


@bot.tree.command(name="livi-dinner", description="Get Livingston Dining Hall dinner menu.")
async def livi(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/foodpronet/pickmenu.aspx?locationNum=03&locationName=Livingston+Dining+Commons&dtdate=03/03/2025&activeMeal=Dinner&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Livingston Dining Hall Menu:**\n{menu}")

@bot.tree.command(name="livi-knightroom", description="Get Livingston Dining Hall's Knight Room menu.")
async def livi(interaction: discord.Interaction):
    await interaction.response.defer()
    url = 'https://menuportal23.dining.rutgers.edu/foodpronet/pickmenu.aspx?locationNum=03&locationName=Livingston+Dining+Commons&dtdate=03/03/2025&activeMeal=Knight+Room&sName=Rutgers+University+Dining'
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Livingston Dining Hall Menu:**\n{menu}")


@bot.tree.command(name="busch-breakfast", description="Get Busch Dining Hall's breakfast menu.")
async def busch(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/foodpronet/pickmenu.aspx?locationNum=04&locationName=Busch+Dining+Hall&dtdate=03/03/2025&activeMeal=Breakfast&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Busch Dining Hall Menu:**\n{menu}")

@bot.tree.command(name="busch-lunch", description="Get Busch Dining Hall's lunch menu.")
async def busch(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/foodpronet/pickmenu.aspx?locationNum=04&locationName=Busch+Dining+Hall&dtdate=03/03/2025&activeMeal=Lunch&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Busch Dining Hall Menu:**\n{menu}")

@bot.tree.command(name="busch-dinner", description="Get Busch Dining Hall's dinner menu.")
async def busch(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/foodpronet/pickmenu.aspx?locationNum=04&locationName=Busch+Dining+Hall&dtdate=02/19/2025&activeMeal=Dinner&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Busch Dining Hall Menu:**\n{menu}")

@bot.tree.command(name="busch-knightroom", description="Get Busch Dining Hall's Knight Room menu.")
async def busch(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/foodpronet/pickmenu.aspx?locationNum=04&locationName=Busch+Dining+Hall&dtdate=03/03/2025&activeMeal=Knight+Room&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Busch Dining Hall Menu:**\n{menu}")

@bot.tree.command(name="neilson-breakfast", description="Get Neilson Dining Hall's breakfast menu.")
async def cookdoug(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/FoodPronet/pickmenu.aspx?locationNum=05&locationName=Neilson+Dining+Hall&dtdate=03/03/2025&activeMeal=Breakfast&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Neilson Dining Hall Menu:**\n{menu}")

@bot.tree.command(name="neilson-lunch", description="Get Neilson Dining Hall's lunch menu.")
async def cookdoug(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/FoodPronet/pickmenu.aspx?locationNum=05&locationName=Neilson+Dining+Hall&dtdate=03/03/2025&activeMeal=Lunch&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Neilson Dining Hall Menu:**\n{menu}")

@bot.tree.command(name="neilson-dinner", description="Get Neilson Dining Hall's dinner menu.")
async def cookdoug(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/FoodPronet/pickmenu.aspx?locationNum=05&locationName=Neilson+Dining+Hall&dtdate=03/03/2025&activeMeal=Dinner&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Neilson Dining Hall Menu:**\n{menu}")

@bot.tree.command(name="neilson-knightroom", description="Get Neilson Dining Hall's Knight Room menu.")
async def cookdoug(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/FoodPronet/pickmenu.aspx?locationNum=05&locationName=Neilson+Dining+Hall&dtdate=03/03/2025&activeMeal=Knight+Room&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Neilson Dining Hall Menu:**\n{menu}")

@bot.tree.command(name="atrium-breakfast", description="Get the Atrium's breakfast menu.")
async def cookdoug(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/FoodPronet/pickmenu.aspx?sName=Rutgers+University+Dining&locationNum=13&locationName=The+Atrium&naFlag=1"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Atrium Menu:**\n{menu}")

@bot.tree.command(name="atrium-lunch", description="Get the Atrium's lunch menu.")
async def cookdoug(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/FoodPronet/pickmenu.aspx?locationNum=13&locationName=The+Atrium&dtdate=03/03/2025&activeMeal=Lunch&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Atrium Dining Hall Menu:**\n{menu}")

@bot.tree.command(name="atrium-dinner", description="Get the Atrium's dinner menu.")
async def cookdoug(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/FoodPronet/pickmenu.aspx?locationNum=13&locationName=The+Atrium&dtdate=03/03/2025&activeMeal=Dinner&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Atrium Dining Hall Menu:**\n{menu}")

@bot.tree.command(name="atrium-latenight", description="Get the Atrium's Late Night menu.")
async def cookdoug(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/FoodPronet/pickmenu.aspx?locationNum=13&locationName=The+Atrium&dtdate=03/03/2025&activeMeal=Late+NIght&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Atrium Dining Hall Menu:**\n{menu}")

async def send_long_message(interaction, message):
    """Splits long messages into multiple Discord messages, ensuring headers and their items stay together."""
    max_length = 1999  # Discord's message limit
    lines = message.split("\n")  # Split message into individual lines
    chunk = ""  # Stores the message chunk to be sent
    buffer = ""  # Temporarily stores the current section (header + items)

    for line in lines:
        if line.startswith("**"):  # New header found
            if chunk and len(chunk) + len(buffer) > max_length:
                await interaction.followup.send(chunk)  # Send the accumulated chunk
                chunk = ""  # Reset chunk for new content

            chunk += buffer  # Move the buffered section to the chunk
            buffer = line + "\n"  # Start a new section with the header

        else:
            buffer += line + "\n"  # Add the food item to the buffer

    if chunk + buffer:
        await interaction.followup.send(chunk + buffer)  # Send any remaining message
# Run the bot
bot.run(TOKEN)
