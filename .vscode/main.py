import settings
import discord 
from discord.ext import commands
import requests, json, random, datetime, asyncio, schedule

filename = ".vscode\schedule.txt"
logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        schedule_weekly_messages()

    @bot.command(
            help="I am still under development!",
            description="Ping pong?",
            brief="Ping pong!",
            hidden=True
    )
    async def ping(ctx):
        """ Answers with pong """
        await ctx.send("pong")

 
    # async def scheduled_message():
    #     while True:
    #         week = 0
    #         now = datetime.datetime.now()

    #         #every week send the message
    #         then = now + datetime.timedelta(days=7)

    #         #then = now.replace(hour=15, minute=30)

    #         #then.replace(hour=15,minute=30)     #at 3:30pm

    #         if then < now:
    #             then += datetime.timedelta(days=1)
     
    #         wait_time = (then-now).total_seconds()
    #         await asyncio.sleep(wait_time)

    #         #testing server
    #         channel = bot.get_channel(1112936855088943165)

    #         await channel.send("@everyone PING PONG")
    #         await asyncio.sleep(1)

    #         week += 1

 

    def schedule_weekly_messages():
        with open(filename, "r") as file:
            lines = file.readlines()

        for i, line in enumerate(lines, 1):
            items = line.strip().split(",")  # Split the line by ","
            date = items[0]
            team1 = items[1]
            team1_color = items[2]
            team1_field = items[3]
            team2 = items[4]
            team2_color = items[5]
            team2_field = items[6]

            message = f"On {date}, we are playing against {team1} wearing {team1_color} on field #{team1_field}. "
            message += f"Our second game, we are playing against {team2} wearing {team2_color} on field #{team2_field}."

            schedule.every().thursday.at("01:36").do(bot.loop.create_task, send_weekly_message(message))

    async def send_weekly_message(message):

        channel = bot.get_channel(1112936855088943165)
        await channel.send(message)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == '__main__':
    run()