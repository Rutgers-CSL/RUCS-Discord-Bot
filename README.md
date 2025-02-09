# RUCS-Discord-Bot
Mary, Nicole, Vidu

### Overview: 

RUCS Discord bot is a discord bot designed to help people, by allowing them to get info on buses, courses, dining hall options, and events at Rutgers.
It is an easy consolidated way to access all the information a student may need daily. 


### Features: 

  Bus Schedules: 
  
    - Given a bus stop, what are the routes that visit it?
    - Given a route, what bus stops are covered?
    - Given a campus (e.g. Busch, C/D, CA, Livi), bus stop (e.g. BSC, ARC, Hill Center, Stadium) and bus route (e.g. A, B, BL, LX, REXB), tell the user how many minutes away the earliest desired bus is. 
    - [Stretch] Given a bus stop (e.g. BSC, ARC, Hill Center, Stadium), bus route (e.g. A, B, BL, LX, REXB), and X minutes away, ping the user when the bus is X minutes away.
      - Always notify user ETA of next bus. 
      - If a bus is <5 minutes away, notify user, and still set alarm for the later bus.
    - [Stretch] Do some shortest path algorithm (e.g. Dijkstra's, but tricky to implement) between stops to determine shortest time from stop A to stop B.

  Courses: 

    - Given a course code (e.g. 198, 640, 750) will list all the courses and their class codes
    - Given a course code (e.g. 198:111)
      - will list the prerequisites for that course
      - will list course synopsis
      - will list sections, times and professors
      - will list what sections are open and closed    
    
  Dining Hall:
  
    - Given a campus and allergy will list the food items on menu for that day that align with dietary restrictions (assuming there is only one dining hall per campus)
    

  Events:

    - Given day of the week and campus, will list events for the day with their times and locations
    - [Stretch] Given NetID and password will buy football ticket
    - [Stretch] Given specific event (idk how we do this) will ping user a reminder day of the event


### Technical Implementation:

  - Use of Python and JS (adam suggested python)

### Difficulties:

  - How are we going to keep updating the information the bot has 
  - How to access the information (Bus API?)

  

### Milestones:
  - Figure out structure/languages/plan
  - Create design plan (very detailed plan of what each component will tell the user)
  - Code a simple Discord bot that can interact with user input (ex. saying hello back)
  - * Get bot to print one dining hall menu
  - Find all APIs we need (Bus, Course, Dining hall, events)
    - If we can't find them webscrape websites
      - ex. SOC, GetInvolved
  - * Get bot to identify courses by number and get professor/times/prereqs
