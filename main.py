import math
import os
import discord
from datetime import datetime, time
import web_scraper

schedule_a = {
    time(hour=8, minute=30): "Period 1",
    time(hour=9, minute=20): "Period 2",
    time(hour=10, minute=15): "Brunch",
    time(hour=10, minute=30): "Period 3",
    time(hour=11, minute=30): "Period 4",
    time(hour=12, minute=25): "Lunch",
    time(hour=12, minute=55): "Period 5",
    time(hour=1, minute=50): "Period 6",
    time(hour=2, minute=45): "Period 7",
    time(hour=3, minute=40): "After School"
}

schedule_b = {
    time(hour=0, minute=0): "Before School",
    time(hour=8, minute=30): "Period 1",
    time(hour=9, minute=10): "Period 2",
    time(hour=9, minute=55): "Brunch",
    time(hour=10, minute=10): "Period 3",
    time(hour=11, minute=00): "Period 4",
    time(hour=11, minute=45): "Lunch",
    time(hour=12, minute=15): "Period 5",
    time(hour=1, minute=00): "Period 6",
    time(hour=1, minute=45): "Period 7",
    time(hour=2, minute=30): '"Collaboration" period or something',
    time(hour=3, minute=45): "After School"
}

token = os.environ["TOKEN"]

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="mphs-events", description="Displays upcoming MPHS Events")
async def mphsevents(ctx: discord.ApplicationContext):
    events = web_scraper.get_events()
    what_to_say = "**EVENTS:**\n\n"
    for event in events:
        what_to_say += f"__{event["name"]}__\n"
        start = event["start"].strftime("%m/%d/%Y")
        end = event["end"].strftime("%m/%d/%Y")

        if start != end:
            what_to_say += "Start: " + start + "\n"
            what_to_say += "End: " + end + "\n\n"
        else:
            what_to_say += "When: " + start + ", "
            start_time = event["start"].strftime("%I:%M%p")
            end_time = _time = event["start"].strftime("%I:%M%p")
            if start_time != end_time:
                what_to_say += start_time + "-" + end_time + "\n\n"
            else:
                what_to_say += start_time + "\n\n"

    await ctx.respond(what_to_say)



@bot.slash_command(name="mphs-schedule", description="Displays the MPHS schedule")
async def mp_schedule(ctx: discord.ApplicationContext):

    today = datetime.now()
    week_day = today.strftime("%A")
    what_to_say = "Today is a " + week_day + ", so it must be "

    now = datetime.now().time()
    what_to_say += "Schedule B" if week_day.lower() == "wednesday" else "Schedule A"
    what_to_say += "\nAccording to the schedule, it is currently "
    schedule = schedule_b if week_day.lower() == "wednesday" else schedule_a

    period = ""
    time_end = ""
    for key, item in schedule.items():
        if now > key:
            period = item
        else:
            today_key = datetime.combine(datetime.today(), key)
            today_now = datetime.now()
            delta = math.floor((today_key - today_now).total_seconds() / 60)
            time_end = "\nand next period will be in " + str(delta) + " minutes"
            break
    what_to_say += period + time_end
    with open("schedule.png", 'rb') as file:
        await ctx.respond(what_to_say,file=discord.File(file))

bot.run(token) # run the bot with the token