import settings
import discord 
from discord.ext import commands
import random, asyncio, schedule, datetime
from datetime import date
import pytz

filename = ".vscode\schedule.txt"
logger = settings.logging.getLogger("bot")
# Get the current UTC time
utc_now = datetime.datetime.now(datetime.timezone.utc)

# Define the Eastern Time Zone
eastern_tz = pytz.timezone('US/Eastern')

# Convert UTC time to Eastern Time Zone
et_now = utc_now.astimezone(eastern_tz)

# Print the converted time
print("Scheduled function executed at:", et_now)

# Get the system's default time zone
default_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
print("Default time zone:", default_timezone)


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        #schedule.every().thursday.at("10:00").do(asyncio.run, send_weekly_message)

        await send_weekly_message()
        await weekly_standing()

    @bot.command(
            help="I am still under development!",
            description="Ping pong?",
            brief="Ping pong!",
            hidden=True
    )
    async def ping(ctx):
        """ Answers with pong """
        await ctx.send("pong")
    
    async def weekly_standing():
        channel = bot.get_channel(902777744478310401)
       
        data = []
        message = ""
        with open('.vscode\standing.txt', 'r') as file:
            # Read each line
            lines = file.readlines()

            for line in lines:
                fields = line.strip().split(',')
                data.append(fields)

        # Function to print the table
        
        headers = ['PLACE', 'TEAM', 'WIN', 'LOSS', 'TIE', 'POINTS', 'SPIRIT']
        header_format = '{:<6} {:<20} {:<4} {:<5} {:<4} {:<10} {:<16}'

        table = f"```{header_format.format(*headers)}\n"

        for row in data:
            table += f"{row[0]:<6} {row[1]:<20} {row[2]:<4} {row[3]:<5} {row[4]:<4} {row[5]:<10} {row[6]:<16}\n"
            if row[1] == "Uppercuts":
                message += f"We are currently in {row[0]}th place. Our spirit score is {row[6]}. KEEP IT UP!!"
                
        table += "```"
    
        # Call the function to print the table
        await channel.send(table)
        await channel.send(message)

    async def send_weekly_message():

        channel = bot.get_channel(902777744478310401)

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
                    sentence = f"On {date_field}, we are playing against {team1} wearing {color1} on field #{field1}. Next, we are playing against {team2} wearing {color2} on field #{field2}."
                    
                    await channel.send(sentence)


    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == '__main__':
    run()