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
  
    - Will tell you which sections of courses are open/closed
    
    - Will tell you what courses and sections a professor teaches
    
    - Will give you a general overview of what the course will cover 
    
    - Will give the pre-reqs needed for the course
    
    
  Dining Hall:
  
    - Will give you a list of menus for each dining hall 
    
    - Will give you suggestions based on your dietary restrictions 
    

  Events:
  
    - Will inform you if their are any big events, like football games, are happening this week 
    
    - Tell you how to register/buy tickets?


### Technical Implementation:

  - Use of Python and JS

### Difficulties:

  - How are we going to keep updating the information the bot has 
  - How to access the information (Bus API?)

  

### Milestones:
  - Figure out structure/languages/plan
  - Code a simple Discord bot that can interact with user input (ex. saying hello back)
  - * Get bot to print one dining hall menu
  - Find all APIs we need (Bus, Course, Dining hall, events)
    - If we can't find them webscrape websites
      - ex. SOC, GetInvolved
  - * Get bot to identify courses by number and get professor/times/prereqs
