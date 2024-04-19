import settings
import discord 
from discord.ext import commands
from datetime import date
from standings_scraper import standings, wednesday_standings
from schedule_scraper import get_upcoming_schedule
from field_status import status


logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{bot.user} is Ready")
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")



    @bot.command(
            help="I am still under development!",
            description="Posting the schedule",
            brief="Posts the schedule",
            hidden=True
    )
    async def upc(ctx, date1, date2, date3):
        """ Answers with the schedule for given day in format: !upcoming_schedule Thursday, July 5 """
        day = f"{date1} {date2} {date3}"
        print(day)
        await next_schedule(ctx, day)

    async def next_schedule(ctx,day):
        # channel = bot.get_channel(1112936855088943165)
        message = get_upcoming_schedule(day)

        await ctx.send(message)



    @bot.command(
            help="I am still under development!",
            description="Posting the schedule",
            brief="Posts the schedule",
            hidden=True
    )
    async def to_all(ctx, date1, date2, date3):
        """ @EVERYONE in announcements with the schedule and current standings: Format: !upcoming Thursday, July 5 """
        day = f"{date1} {date2} {date3}"
        await everyone_schedule(ctx, day)

    async def everyone_schedule(ctx, day):
        channel = bot.get_channel(1109852414972010586) #@ main channel
        #channel = bot.get_channel(1112936855088943165) #@ bot testing channel
        message = f"@everyone {get_upcoming_schedule(day)}"

        table, msg = standings()

        await channel.send(message)
        await channel.send(table)
        await channel.send(msg)



    @bot.command(
            help="I am still under development!",
            description="Posting the schedule",
            brief="Posts the schedule",
            hidden=True
    )
    async def st(ctx):
        """ Answers/replies with the standing for Thursdays games """
        await weekly_standing(ctx)

    async def weekly_standing(ctx):
        table, message = standings()
        await ctx.send(table)
        await ctx.send(message)



    @bot.command(
            help="I am still under development!",
            description="Posting the standings for wednesdays",
            brief="Posts the schedule",
            hidden=True
    )
    async def st_wed(ctx):
        """ Answers with the standing for the Wedesday league """
        await wednesday_standing(ctx)
   
    async def wednesday_standing(ctx):
        #channel = bot.get_channel(1112936855088943165)
        table, message = wednesday_standings()
        await ctx.send(table)
        await ctx.send(message)
    

    @bot.command(
            help="I am still under development!",
            description="Posting the standings for wednesdays",
            brief="Posts the schedule",
            hidden=True
    )
    async def field(ctx):
        await field_status(ctx)

    async def field_status(ctx):
        statement = status()
        await ctx.send(statement)

    
    
    bot.run(settings.DISCORD_API_SECRET)
    #bot.run("") #for quick testing




if __name__ == '__main__':
    run()