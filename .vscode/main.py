import settings
import discord 
from discord.ext import commands
import random
from datetime import date
import schedule_scraper
from standings_scraper import standings


filename = ".vscode\schedule.txt"
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
        await send_weekly_message()

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


    async def send_weekly_message():

        channel = bot.get_channel(1112936855088943165)

        # Get today's date
        today = date.today()

        d2 = today.strftime("%B %d")

        # Open the text file
        with open(filename, 'r') as file:
            # Read each line
            lines = file.readlines()

            # Process each line
            for line in lines:
                # Split the line into fields
                fields = line.strip().split(',')

                # Extract the fields
                date_field = fields[0]

                # Compare today's date with the date from the field
                if d2 == date_field:
                    # Extract the remaining fields
                    team1 = fields[1]
                    color1 = fields[2]
                    field1 = fields[3]
                    team2 = fields[4]
                    color2 = fields[5]
                    field2 = fields[6]

                    # Form the sentence
                    sentence = f"@everyone \nOn {date_field}, we are playing against **{team1}** wearing **{color1}** on **field #{field1}**. Next, we are playing against **{team2}** wearing **{color2}** on **field #{field2}**."
                    
                    await channel.send(sentence)



    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == '__main__':
    run()