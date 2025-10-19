import math
import os
import asyncio
import aiofiles
import discord
from datetime import datetime
import web_scraper
from schedules import schedule_a, schedule_b, pride_1, pride_2
from weather import get_weather
import json
from equation_solver import solve_equation
from data_structures import Node

token = os.environ["TOKEN"]

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="mphs-weather", description="Advises to bring an Umbrella if it will rain in the next 5 days")
async def mphs_weather(ctx: discord.ApplicationContext):
    weather = get_weather()
    if weather is not None:
        await ctx.respond(f"It will rain in {weather}, bring an umbrella!")

@bot.slash_command(name="mphs-events", description="Displays upcoming MPHS Events")
async def mphs_events(ctx: discord.ApplicationContext):
    events = web_scraper.get_events()

    embed = discord.Embed(
        title="**MPHS EVENTS**",
        description="Here are a list of events",
        color=discord.Colour.blue(),  # Pycord provides a class with default colors you can choose from
    )

    for event in events:

        start = event["start"].strftime("%m/%d/%Y")
        end = event["end"].strftime("%m/%d/%Y")
        when = ""
        if start != end:
            when += f"Start:{start}, "
            when += f"End: {end}\n"
        else:
            when += f"{start}\n"
            start_time = event["start"].strftime("%I:%M%p")
            end_time = event["end"].strftime("%I:%M%p")
            if start_time != end_time:
                when += start_time + "-" + end_time + "\n"
            else:
                when += start_time + "\n"

        embed.add_field(name=f"__{event["name"]}__", value=when, inline=False)

    await ctx.respond("Here are the events upcoming in the next 14 days", embed=embed)

today_schedule = None

schedule_list = [
    discord.OptionChoice(name="Schedule A", value="a"),
    discord.OptionChoice(name="Schedule B", value="b"),
    discord.OptionChoice(name="Pride 1", value="pride1"),
    discord.OptionChoice(name="Pride 2", value="pride2")
]

@bot.slash_command(name="mphs-set-schedule", description="Sets MPHS schedule to either A, B, Pride 1, or Pride 2")
async def set_schedule(ctx: discord.ApplicationContext,
                       schedule: discord.Option(str, choices=schedule_list)):
    global today_schedule
    if schedule.lower() == "a":
        today_schedule = ["Schedule A",schedule_a]
        await ctx.respond("Changed schedule to A!")
    elif schedule.lower() == "b":
        today_schedule = ["Schedule B",schedule_b]
        await ctx.respond("Changed schedule to B!")
    elif schedule.lower() == "pride1":
        today_schedule = ["Pride 1",pride_1]
        await ctx.respond("Changed schedule to Pride 1!")
    elif schedule.lower() == "pride2":
        today_schedule = ["Pride 2",pride_2]
        await ctx.respond("Changed schedule to Pride 2!")
    else:
        await ctx.respond('Sorry, the current options are: "a","b","pride1","pride2"')

@bot.slash_command(name="mphs-schedule", description="Displays the MPHS schedule")
async def mp_schedule(ctx: discord.ApplicationContext):

    today = datetime.now()
    week_day = today.strftime("%A")

    if today_schedule:
        what_to_say = f"Today is {today_schedule[0]}\nIt is "
        schedule = today_schedule[1]
    else:
        what_to_say = "Today is a " + week_day + ", so it must be "
        what_to_say += "Schedule B" if week_day.lower() == "wednesday" else "Schedule A"
        what_to_say += "\nAccording to the schedule, it is currently "
        schedule = schedule_b if week_day.lower() == "wednesday" else schedule_a

    now = datetime.now().time()
    period = ""
    time_end = ""
    for key, item in enumerate(schedule.items()):
        if now > key:
            period = item
        else:
            today_key = datetime.combine(datetime.today(), key)
            today_now = datetime.now()
            delta = math.floor((today_key - today_now).total_seconds() / 60)
            time_end = f"\nand next period will be in {str(delta)} minute" + ("s" if delta > 1 else "")
            break
    what_to_say += period + time_end
    with open("schedule.png", 'rb') as file:
        await ctx.respond(what_to_say,file=discord.File(file))

@bot.slash_command(name="mphs-add-homework", description="Adds homework for today")
async def add_homework(ctx: discord.ApplicationContext,
                       class_: discord.Option(discord.SlashCommandOptionType.string),
                       homework_name: discord.Option(discord.SlashCommandOptionType.string)):
    with open("homework.txt", 'a') as file:
        to_str = json.dumps([class_, homework_name]) + '\n'
        file.write(to_str)
        await ctx.respond(f'Added homework "{homework_name}" for class "{class_}"!')

@bot.slash_command(name="mphs-clear-homework", description="Adds homework for today")
async def clear_homework(ctx: discord.ApplicationContext):
    with open("homework.txt", 'w') as file:
        file.write("")
        await ctx.respond("Homework cleared!")

@bot.slash_command(name="mphs-homework", description="Gets homework for today")
async def get_homework(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="Homework for Classes",
        description="Here are a list of homeworks for classes. If there's one missing here, use /mphs-add-homework",
        color=discord.Colour.yellow(),  # Pycord provides a class with default colors you can choose from
    )

    classes = ""
    homework = ""
    with open("homework.txt", 'r') as file:
        lines = file.readlines()
    for line in lines:
        json_table = json.loads(line)
        classes += json_table[0] + "\n"
        homework += json_table[1] + "\n"
    embed.add_field(name="__Class__", value=classes, inline=True)
    embed.add_field(name="__Homework__", value=homework, inline=True)

    await ctx.respond("Here is all the homework", embed=embed)

async def order_leaderboard(board):
    head = None
    for key in board.keys():
        item = board[key]
        obj = Node({"Name": key, "Time": item})
        if head is None:
            head = obj
        else:
            node = head
            while True:
                if head.reference['Time'] < obj.reference['Time']:
                    head.left = obj
                    obj.right = head
                    head = obj
                    break
                if node.reference['Time'] < obj.reference['Time']:
                    node.left = obj
                    obj.right = node
                    break
                if node.right is None:
                    node.right = obj
                    obj.left = node
                    break
                node = node.right
    return head


@bot.slash_command(name="evaluate", description="Solves an expression")
async def evaluate(ctx: discord.ApplicationContext, expression: discord.Option(discord.SlashCommandOptionType.string)):
    result = solve_equation(expression)
    await ctx.respond(f"The answer is: {result:g}" if result is not None else "ERROR")

@bot.slash_command(name="mphs-study", description="Puts you on the leaderboard")
async def study(ctx: discord.ApplicationContext, minutes: discord.Option(discord.SlashCommandOptionType.number)):
    async with aiofiles.open("study-leaderboard.json", 'r') as file:
        leaderboard_str = await file.read()
        leaderboard = json.loads(leaderboard_str) if leaderboard_str != "" else {}
    async with aiofiles.open("study-leaderboard.json", 'w') as file:
        leaderboard[ctx.user.name] = float(minutes) + (leaderboard[ctx.user.name] if ctx.user.name in leaderboard else 0)
        await file.write(json.dumps(leaderboard))
    ordered_head = await order_leaderboard(leaderboard)
    node = ordered_head
    index = 1
    while True:
        if node.reference['Name'] == ctx.user.name:
            break
        node = node.right
        index += 1
    await ctx.respond(f"You are now top {index} of the leaderboard")

@bot.slash_command(name="mphs-leaderboard", description="Displays current leaderboard")
async def get_leaderboard(ctx: discord.ApplicationContext):
    async with aiofiles.open("study-leaderboard.json", 'r') as file:
        leaderboard_str = await file.read()
        leaderboard = json.loads(leaderboard_str) if leaderboard_str != "" else {}
    ordered_head = await order_leaderboard(leaderboard)
    embed = discord.Embed(
        title="**STUDY LEADERBOARD**",
        description="Here are the best studying students",
        color=discord.Colour.yellow(),  # Pycord provides a class with default colors you can choose from
    )
    full_list = ""
    node = ordered_head
    index = 1
    while True:
        full_list += f"{index}. {node.reference['Name']} - {node.reference['Time']} min\n"
        node = node.right
        index += 1
        if node is None:
            break
    embed.add_field(name=f"__Students:__", value=full_list, inline=False)
    await ctx.respond("Here it is!", embed=embed)


bot.run(token) # run the bot with the token