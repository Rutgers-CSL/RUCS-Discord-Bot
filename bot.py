import discord
import json
import os
import requests
import re
import aiohttp
import pandas as pd
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from typing import Optional
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
    await reaction.message.channel.send(f'{user} reacted with "{emoji}" to the message: "{message_content}"')


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
    await interaction.response.defer() # allows for retrieving and processing time
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
    menu = show_Dining_Hall(url) # show_Dining_Hall is a function that is responsible for webscraping
    await send_long_message(interaction, f"**Brower Commons Menu:**\n{menu}") # sending menu to Discord and prints using send_long_message function

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


### Sports information
@bot.tree.command(name="sports", description="Get upcoming Rutgers games happening soon.")
async def sports(interaction: discord.Interaction):
    await interaction.response.defer()

    from datetime import datetime, timedelta
    import requests, json
    import pandas as pd
    from bs4 import BeautifulSoup
    from concurrent.futures import ThreadPoolExecutor

    # Date range setup
    today = datetime.today().date()
    one_week = today + timedelta(days=7)
    two_weeks = today + timedelta(days=14)

    # Emoji dictionary per sport
    sport_emojis = {
        "Baseball": "⚾",
        "Softball": "🥎",
        "Football": "🏈",
        "Men's Basketball": "🏀",
        "Women's Basketball": "🏀",
        "Men's Soccer": "⚽",
        "Women's Soccer": "⚽",
        "Men's Lacrosse": "🥍",
        "Women's Lacrosse": "🥍",
        "Wrestling": "🤼",
        "Volleyball": "🏐",
        "Gymnastics": "🤸",
        "Tennis": "🎾",
    }

    # Schedule URLs
    sports_urls = {
        "Baseball": "https://scarletknights.com/sports/baseball/schedule",
        "Men's Basketball": "https://scarletknights.com/sports/mens-basketball/schedule",
        "Women's Basketball": "https://scarletknights.com/sports/womens-basketball/schedule",
        "Football": "https://scarletknights.com/sports/football/schedule",
        "Men's Lacrosse": "https://scarletknights.com/sports/mens-lacrosse/schedule",
        "Women's Lacrosse": "https://scarletknights.com/sports/womens-lacrosse/schedule",
        "Men's Soccer": "https://scarletknights.com/sports/mens-soccer/schedule",
        "Women's Soccer": "https://scarletknights.com/sports/womens-soccer/schedule",
        "Softball": "https://scarletknights.com/sports/softball/schedule",
        "Volleyball": "https://scarletknights.com/sports/volleyball/schedule",
        "Wrestling": "https://scarletknights.com/sports/wrestling/schedule"
    }

    # Scraper
    def fetch_events(sport, url):
        events = []
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            scripts = soup.find_all("script", type="application/ld+json")
            for script in scripts:
                if not script.string:
                    continue
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict):
                        data = data.get("@graph", [data])
                    for item in data:
                        if item.get("@type") == "SportsEvent":
                            date_str = item.get("startDate", "").split("T")[0]
                            try:
                                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                            except:
                                continue
                            if date_obj < today:
                                continue
                            description = item.get("description", "N/A")
                            matchup = description.split(" on ")[0] if " on " in description else description
                            location = item.get("location", {}).get("name", "N/A")
                            pretty_date = date_obj.strftime("%B %d").replace(" 0", " ")
                            events.append({
                                "Sport": sport,
                                "Emoji": sport_emojis.get(sport, "🏟️"),
                                "RawDate": date_obj,
                                "PrettyDate": pretty_date,
                                "Matchup": matchup,
                                "Location": location
                            })
                except:
                    continue
        except:
            pass
        return events

    # Run in parallel
    all_events = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(lambda item: fetch_events(*item), sports_urls.items())
        for result in results:
            all_events.extend(result)

    df = pd.DataFrame(all_events).sort_values("RawDate").reset_index(drop=True)

    # Filter logic
    week_games = df[df["RawDate"] <= one_week]
    two_week_games = df[df["RawDate"] <= two_weeks]
    month_games = df[df["RawDate"].apply(lambda d: d.month == today.month)]


    if not week_games.empty:
        filtered = week_games
        header = "**🏟️ Games in the next 7 days**"
    elif not two_week_games.empty:
        filtered = two_week_games
        header = "**🏟️ Games in the next 14 days**"
    elif not month_games.empty:
        filtered = month_games
        header = "**🏟️ Games later this month**"
    else:
        await interaction.followup.send("❌ No upcoming games found.")
        return

    # Group and format
    lines = [header]
    grouped = filtered.groupby("PrettyDate")

    for date, group in grouped:
        lines.append(f"\n **{date}**")
        for row in group.itertuples(index=False):
            matchup_clean = (
                row.Matchup
                .replace("Rutgers University", "Rutgers")
                .replace(" At ", " at ")
                .replace(" Vs ", " vs ")
            )
            lines.append(f"• {row.Emoji} **{row.Sport}** — *{matchup_clean}*   📍 {row.Location}\n")

    await send_long_message(interaction, "\n".join(lines))


## SOC
# async def fetch_courses(year: int, term: int):
#     """Fetches course data from Rutgers SOC API based on year and term."""
#     url = f"https://classes.rutgers.edu/soc/api/courses.json?year={year}&term={term}&campus=NB"
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 return await response.json()
            
#                 # Write the fetched JSON data to a file for debugging
#                 with open("courses_debug.json", "w", encoding="utf-8") as f:
#                     json.dump(data, f, indent=4)

#                 print("✅ Fetched course data saved to courses_debug.json")  # Debugging statement
#                 return data
            
#             else:
#                 print(f"❌ Failed to fetch courses. HTTP Status: {response.status}")  # Debugging statement
#                 return None
async def fetch_courses(year: int, term: int):
    """Fetches course data from Rutgers SOC API based on year and term."""
    url = f"https://classes.rutgers.edu/soc/api/courses.json?year={year}&term={term}&campus=NB"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                data = await response.json()
            except aiohttp.ClientResponseError as e:
                print(f"❌ Error parsing JSON: {e}")
                data = None
            except Exception as e:
                print(f"❌ Unexpected error during JSON parsing: {e}")
                data = None

            # Write the fetched JSON data to a file for debugging (always do this)
            if data:
                try:
                    with open("courses_debug.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)
                    print("✅ Fetched course data saved to courses_debug.json")  # Debugging statement
                except Exception as e:
                    print(f"❌ Error writing to debug file: {e}")
            else:
                print("⚠️ No data received from the API to save.")

            if response.status == 200:
                return data
            else:
                print(f"❌ Failed to fetch courses. HTTP Status: {response.status}")  # Debugging statement
                return None

@bot.tree.command(name="get_courses", description="Get courses and sections for a given year and semester at Rutgers NB.")
@app_commands.describe(
    year="Enter the academic year (ex: 2025)",
    term="Enter the semester code (1=Spring, 7=Summer, 9=Fall)",
    course_code="Enter the course code (ex: 198 for CS)",
    subject_code="(Optional) Enter the class code (ex: 111 for Intro to CS)"
)
async def get_courses(interaction: discord.Interaction, year: int, term: int, course_code: str, subject_code: Optional[str] = None):
    """Slash command to fetch and display course data based on filters."""
    await interaction.response.defer()

    data = await fetch_courses(year, term)
    if not data:
        await interaction.followup.send("Failed to retrieve course data. Please try again later.")
        return

    course_dict = {}

    for course in data:
        subject = course.get("subject", "Unknown")
        current_course_number = course.get("courseNumber", "Unknown")
        title = course.get("title", "No Title")
        credits = course.get("credits", "N/A")

        # Check if the subject code matches
        if subject != str(subject_code).zfill(3):  # Ensure subject code is 3 digits with leading zeros
            continue

        # Check if a specific course number is provided and if it matches
        if course_code and current_course_number != str(course_code):
            continue

        sections = []
        for section in course.get("sections", []):
            section_number = section.get("number", "Unknown")
            index = section.get("index", "N/A")
            sections.append(f"Sec {section_number} (Index: {index})")

        # Store in dictionary
        course_dict[f"{current_course_number} - {title} ({credits} credits)"] = sections

        # Format output
        output = []
        for course, sections in course_dict.items():
            sections_text = "\n".join(sections) if sections else "No sections available"
            output.append(f"**{course}**\n{sections_text}\n")

        final_message = "\n".join(output) if output else f"No matching courses found for Subject Code: {subject_code}."
        await interaction.followup.send(f"**Courses for {year}, Term {term}, Subject Code {subject_code}**\n{final_message}")


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