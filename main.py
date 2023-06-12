import settings
import discord 
from discord.ext import commands
import random
from datetime import date
from standings_scraper import standings
from schedule_scraper import get_schedule
from datetime import date
import calendar


#filename = "schedule.txt"
logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        #schedule.every().thursday.at("10:00").do(asyncio.run, send_weekly_message)


    @bot.command(
            help="I am still under development!",
            description="Ping pong?",
            brief="Ping pong!",
            hidden=True
    )
    async def ping(ctx):
        """ Answers with pong """
        await ctx.send("pong")

    @bot.command(
            help="I am still under development!",
            description="Posting the schedule",
            brief="Posts the schedule",
            hidden=True
    )
    async def schedule(ctx):
        """ Answers with the schedule for that day """
        await weekly_schedule()

    async def weekly_schedule():
        channel = bot.get_channel(1112936855088943165)
        # Get today's date
        today = date.today()
        d2 = today.strftime("%B %d")
        today_date = f"{calendar.day_name[today.weekday()]}, {d2}"
        today_date = "Thursday, May 11"
        message = get_schedule(today_date)

        await channel.send(message)


    @bot.command(
            help="I am still under development!",
            description="Posting the schedule",
            brief="Posts the schedule",
            hidden=True
    )
    async def standing(ctx):
        """ Answers with the standing for that day """
        await weekly_standing()
   

    async def weekly_standing():
        channel = bot.get_channel(1112936855088943165)

        table, message = standings()
        await channel.send(table)
        await channel.send(message)


    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == '__main__':
    run()