import discord
import os
import requests
import re
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime

# Load environment variables
load_dotenv() # loads environment variablesinto file scipt
TOKEN = os.getenv("DISCORD_TOKEN") # ensure token is securely retrieved

intents = discord.Intents.default() # creates default Intents object
intents.messages = True # allows bot to read messages needed for commands and message events
intents.message_content = True # allows to read message content
intents.guilds = True # grants access to server related events
intents.reactions = True # makes sure reactions intent is enabled

# instatiate Bot object
bot = commands.Bot(command_prefix="!", intents=intents)


# prints the bot's name and the server (guilds) it's connected to
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()  # Sync slash commands with Discord
        print(f'Synced {len(synced)} commands: {[cmd.name for cmd in synced]}')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.event
# special function: event handler for on_message event
async def on_message(message):
    # stop bot from replying to itself
    if (message.author == bot.user):
        return
    if (message.content.lower().startswith('hello')):
        await message.channel.send(f'Hi there {message.author}')
    if (message.content.lower().startswith('bye')):
        await message.channel.send(f'Bye Bye! {message.author}')

    # await bot.process_commands(message) # ensure bot processes commands after custom message handling

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    emoji = reaction.emoji # gets the emoji that was reacted
    message_content = reaction.message.content # gets the contents of the message
    await reaction.message.channel.send(f'You reacted with "{emoji}" to the message: "{message_content}"')


### DINING HALL INFORMATION
# scrapes dining halls using Beautiful Soup, dynamically updates date in URL
def show_Dining_Hall(url):
    """Scrapes the menu from the Rutgers dining hall website."""
    ans = "" # empty string that will show menu
    today_date = datetime.today().strftime("%m/%d/%Y")
    url = re.sub(r"dtdate=\d{2}/\d{2}/\d{4}", f"dtdate={today_date}", url)  # replaces old date with today’s date
    
    response = requests.get(url) # fetches webpage with menu
    if response.status_code != 200:
        return "Failed to retrieve the menu."

    soup = BeautifulSoup(response.text, "html.parser") # parses webpage
    h3_items = soup.find_all("h3")  # finds menu section headers
    
    done = 0
    increment = 2

    for item in soup.find_all("fieldset"): # traverses menu and concatinates ans string
        count = 0
        if item.sourceline > h3_items[increment].sourceline:
            if increment == len(h3_items) - 1 and done == 0:
                done += 1
                ans += f"\n**{h3_items[increment].text}**\n\n"
            if increment < len(h3_items) - 1:
                ans += f"\n**{h3_items[increment].text}**\n\n"
                increment += 1

        for foodItem in item: # gets food items
            if count == 1:
                ans += f"- {foodItem.text.strip().lower()}\n"
            count += 1

    return ans if ans else "No menu items found."


# slash commands for livi
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


# slash commands for brower
@bot.tree.command(name="brower-breakfast", description="Get Brower Commons' breakfast menu.")
async def brower(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/FoodPronet/pickmenu.aspx?locationNum=01&locationName=Brower+Commons&dtdate=03/03/2025&activeMeal=Breakfast&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Brower Commons Menu:**\n{menu}")

@bot.tree.command(name="brower-lunch", description="Get Brower Commons' lunch menu.")
async def brower(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/FoodPronet/pickmenu.aspx?locationNum=01&locationName=Brower+Commons&dtdate=03/03/2025&activeMeal=Lunch&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Brower Commons Menu:**\n{menu}")

@bot.tree.command(name="brower-dinner", description="Get Brower Commons' dinner menu.")
async def brower(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/FoodPronet/pickmenu.aspx?locationNum=01&locationName=Brower+Commons&dtdate=03/03/2025&activeMeal=Dinner&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Brower Commons Menu:**\n{menu}")

@bot.tree.command(name="brower-latenight", description="Get Brower Commons' late-night menu.")
async def brower(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/FoodPronet/pickmenu.aspx?locationNum=01&locationName=Brower+Commons&dtdate=03/03/2025&activeMeal=Late+Night&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Brower Commons Menu:**\n{menu}")


# slash commands for henry's diner
@bot.tree.command(name="henrys-breakfast", description="Get Henry's Diner's breakfast menu.")
async def henrys(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/FoodPronet/pickmenu.aspx?locationNum=14&locationName=Henry%27s+Diner&dtdate=03/03/2025&activeMeal=Breakfast&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Henry's Diner Menu:**\n{menu}")

@bot.tree.command(name="henrys-lunch", description="Get Henry's Diner's lunch menu.")
async def henrys(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/FoodPronet/pickmenu.aspx?locationNum=14&locationName=Henry%27s+Diner&dtdate=03/03/2025&activeMeal=Lunch&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Henry's Diner Menu:**\n{menu}")

@bot.tree.command(name="henrys-dinner", description="Get Henry's Diner's dinner menu.")
async def henrys(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://menuportal23.dining.rutgers.edu/FoodPronet/pickmenu.aspx?locationNum=14&locationName=Henry%27s+Diner&dtdate=03/03/2025&activeMeal=Dinner&sName=Rutgers+University+Dining"
    menu = show_Dining_Hall(url)
    await send_long_message(interaction, f"**Henry's Diner Menu:**\n{menu}")


# slash commands for busch
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


# slash commands for neilson
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


# slash commands for atrium
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


### BUS ROUTES
# Dictionary of routes to stops
bus_routes = {
    "A": [
        "College Avenue Student Center", "The Yard", "Student Activities Center",
        "Stadium West Lot", "Hill Center (North)", "Science Buildings",
        "Busch Student Center", "Werblin Recreation Center"
    ],
    "B": [
        "Livingston Student Center", "Quads", "Hill Center (North)",
        "Science Buildings", "Busch Student Center", "Livingston Plaza"
    ],
    "B/L Loop": [
        "Jersey Mike's Arena", "Livingston Student Center", "Quads",
        "Busch Student Center", "Rodkin Academic Center", "Stadium West Lot",
        "Hill Center (North)", "Science Buildings"
    ],
    "C": [
        "Stadium West Lot", "Hill Center (North)", "Allison Road Classroom Building",
        "Hill Center (South)"
    ],
    "EE": [
        "College Avenue Student Center", "The Yard", "SoCam Apartments (SB)",
        "Red Oak Lane", "Lipman Hall", "Biel Road", "Henderson Apartments",
        "Gibbons", "College Hall", "SoCam Apartments (NB)", "Student Activities Center"
    ],
    "F": [
        "Red Oak Lane", "Lipman Hall", "College Hall", "Student Activities Center",
        "The Yard"
    ],
    "H": [
        "College Avenue Student Center", "The Yard", "Student Activities Center",
        "Werblin Recreation Center", "Busch Student Center",
        "Allison Road Classroom Building", "Hill Center (South)", "Stadium West Lot"
    ],
    "LX": [
        "College Avenue Student Center", "The Yard", "Student Activities Center",
        "Livingston Plaza", "Livingston Student Center", "Quads"
    ],
    "REXB": [
        "Red Oak Lane", "Lipman Hall", "College Hall", "Hill Center (North)",
        "Allison Road Classroom Building", "Hill Center (South)"
    ],
    "REXL": [
        "Red Oak Lane", "Lipman Hall", "College Hall", "Livingston Plaza",
        "Livingston Student Center"
    ],
    "Weekend 1": [
        "College Avenue Student Center", "The Yard (Scott Hall)",
        "Student Activities Center", "Science Buildings (across from Allison Road Classroom Building)",
        "Busch Student Center", "Livingston Plaza", "Livingston Student Center",
        "Student Activities Center", "Red Oak Lane", "Lipman Hall", "Biel Road",
        "Gibbons", "College Hall", "SoCam Apartments (New St side of The George Apts)",
        "Student Activities Center"
    ],
    "Weekend 2": [
        "College Avenue Student Center", "The Yard (Scott Hall)", "SoCam Apartments (290 George St)",
        "Student Activities Center", "Red Oak Lane", "Lipman Hall", "Biel Road",
        "Gibbons", "College Hall", "Livingston Plaza", "Livingston Student Center",
        "Busch Student Center", "Allison Road Classroom Building",
        "Hill Center (South/towards SHI Stadium)"
    ],
    "All Campuses": [
        "College Avenue Student Center", "The Yard", "Student Activities Center",
        "Hill Center (North)", "Science Building", "Busch Student Center",
        "Livingston Plaza", "Livingston Student Center", "Quads",
        "Student Activities Center (SB)", "Red Oak Lane", "Lipman Hall",
        "Biel Road", "Henderson", "Gibbons", "College Hall", "SoCam Apartments (NB)",
        "Student Activities Center"
    ]
}


async def route_autocomplete(interaction: discord.Interaction, current: str):
    """
    This function filters `bus_routes` based on the user's partial input.
    It must return a list of app_commands.Choice objects.
    """
    matches = [
        app_commands.Choice(name=route_name, value=route_name)
        for route_name in bus_routes
        if current.lower() in route_name.lower()
    ]
    return matches[:25]

@bot.tree.command(name="get_routes", description="Get the stops for a Rutgers NB bus route.")
@app_commands.describe(route="Select the bus route name")
@app_commands.autocomplete(route=route_autocomplete)
async def get_routes(interaction: discord.Interaction, route: str):
    stops = bus_routes.get(route)
    if not stops:
        await interaction.response.send_message(
            f"Could not find a route named **{route}**. Please try again.",
            ephemeral=True
        )
        return

    route_title = f"**{route.upper()}** Bus Stops"
    stop_list = "\n".join(f"• {stop}" for stop in stops)
    response = f"{route_title}\n{stop_list}"

    await interaction.response.send_message(response)

# sending long messages
async def send_long_message(interaction, message):
    """Splits long messages into multiple Discord messages."""
    max_length = 1999
    lines = message.split("\n")
    chunk = ""  
    buffer = ""  

    try:
        for line in lines:
            if line.startswith("**"):  # If a new menu section starts
                if chunk and len(chunk) + len(buffer) > max_length:
                    await interaction.followup.send(chunk)
                    chunk = ""  

                chunk += buffer  
                buffer = line + "\n"

            else:
                buffer += line + "\n"

        if chunk + buffer:
            await interaction.followup.send(chunk + buffer)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}")



# get secret stuff from environment varables
GUILD_ID = discord.Object(id=int(os.getenv('GUILD_ID')))

bot.run(TOKEN)