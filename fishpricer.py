from itertools import cycle
import discord
from discord.ext import tasks
import datetime

TOKEN = 'NzM3MTM3NjUzOTc1MzUxMzQ3.Xx4-8A.-TqVn1_5F22zNExQNkjtsFY06Fs'

channel_name = "цены-у-скупщиков"
log_name = "логи-цены"
log_id=0
channel_id=0
message_id=0
channel_info=0
temp=[]
current_prices = ["???", "???"]
bot = discord.Client()
update_time=(datetime.datetime.today()+datetime.timedelta(hours=3)).strftime("[%d/%m/%Y %H:%M:%S")
prices=["88","94","99","110","116"]
listoflist1=["gthd","ljcr","ghfd","прав","доск","перв","1\\2","1/2","1|2"]
listoflist2=["rfvt","rfvy","dnjh","ktds","левы","каме","камн","втор","2\\2","2/2","2|2"]
timing2=''
timing1 =''


@bot.event
async def on_ready():
    asd = """:regional_indicator_f: **всем, кто чекает цены!**
*Здесь вы можете помочь другим людям, сообщив о текущей цене на рыбу.*
**На сервере актуальные цены на рыбу узнают игроки вручную и самостоятельно.**
**Затем они пишут данные цены в этом канале (за что им огромное спасибо)**
**После чего бот FishPricer, проанализировав эти сообщения, запоминает текущую цену.**

Напишите сообщение по следующей форме (указав **АКТУАЛЬНЫЕ ЦЕНЫ**):
```Доски 110```или
```Камень 110```
:face_with_symbols_over_mouth: **Прочтите** {0}
*Там подробнее описана как механика изменения цены на рыбу так и другая полезная информация.*
**Цены меняются каждые 3 часа после рестарта сервера в 7 утра по Москве.**
*Расписание изменения цен: :point_right: 07:02 - 10:02 - 13:02 :point_right: 16:02 - 19:02 - 22:02 :point_right: 01:02 - 04:02*

**Карта скупщиков:** https://i.imgur.com/XopzKey.png"""
    global channel_name, channel_id, message_id, log_id, channel_info
    print('We have logged in as {0.user}'.format(bot))
    for channel in bot.get_all_channels():
        if channel_name in channel.name:
            channel_id = channel.id
        if log_name in channel.name:
            log_id = channel.id
        if "как-продать-улов" in channel.name:
            channel_info = channel.id
    print(channel_id)
    print(log_id)
    channel = bot.get_channel(channel_id)
    await channel.purge()
    message = await channel.send(asd.format(bot.get_channel(channel_info).mention))
    message = await channel.send(
                '```Время - {0} МСК\n1/2 Цена осетра - {1}$\n2/2 Цена осетра - {2}$```'.format(
                    datetime.datetime.today().strftime("[%d/%m/%Y %H:%M:%S]"),
                    current_prices[0],
                    current_prices[1]))
    update.start()
    status.start()
    update_status.start()
    message_id = message.id
    print(message_id)


@tasks.loop(seconds=1)
async def update():
    global current_prices, timing1, timing2
    ch = bot.get_channel(channel_id)
    msg = await ch.fetch_message(message_id)
    for t1 in ["01:01:30", "04:01:30","07:01:30","10:01:30","13:01:30","16:01:30","19:01:30","22:01:30"]:
        c=(datetime.datetime.strptime(t1, "%H:%M:%S")-(datetime.datetime.today()+datetime.timedelta(hours=3)))
        s=c.seconds
        if s==0:
            current_prices=["???", "???"]
            timing1 = ''
            timing2 = ''
        elif 0 < s < 10800:
            c=(datetime.datetime.strptime("0:0:0", "%H:%M:%S") + c).strftime("[%H:%M:%S]")
            break
    await msg.edit(content='```CS\n#НА ДОСКАХ{3}\n[1/2] Цена осетра: {0}$\n#НА КАМНЕ{4}\n[2/2] Цена осетра: {1}$``````Elm\nДо смены цен на сервере {2}```'.format(
        current_prices[0],
        current_prices[1],
        c,
        timing1,
        timing2))


@tasks.loop(seconds=30)
async def status():
    global temp
    if current_prices[0] == "116" or current_prices[1] == "116":
        if current_prices[0] == "116":
            temp = cycle(["ПРОДАЙ РЫБУ", "1/2 ОСЁТР 116$"])
        elif current_prices[1] == "116":
            temp = cycle(["ПРОДАЙ РЫБУ", "2/2 ОСЁТР 116$"])
        else:
            temp = cycle(["ПРОДАЙ РЫБУ", "1/2 ОСЁТР 116$", "2/2 ОСЁТР 116$"])
    else:
        temp = cycle(["РЫБАЧЬ ДАЛЬШЕ", "1/2 ОСЁТР {0}$".format(current_prices[0]),"2/2 ОСЁТР {0}$".format(current_prices[1])])



@tasks.loop(seconds=5)
async def update_status():
    global temp
    await bot.change_presence(activity=discord.Game(next(temp)))

@bot.event
async def on_message(message):
    global current_prices, message_id, log_id, listoflist1,listoflist2, timing2, timing1
    if message.author == bot.user:
        return
    if "цены-у-скупщиков" in message.channel.name:
        ch = bot.get_channel(log_id)
        await ch.send('User: '"{0} / {1}```{2}```".format(message.author.mention,message.author, message.content.lower()))
        if "?" in message.content.lower():
            await message.delete()
        else:
            for inch in listoflist1:
                if inch in message.content.lower():
                    for i in prices:
                        if i in message.content.lower().split(" ")[len(message.content.lower().split(" "))-1]:
                            current_prices[0] = message.content.lower().split(" ")[len(message.content.lower().split(" "))-1]
                            timing1=(datetime.datetime.today()+datetime.timedelta(hours=3)).strftime(" [%d/%m/%Y %H:%M]")
            for inch in listoflist2:
                if inch in message.content.lower():
                    for i in prices:
                        if i in message.content.lower().split(" ")[len(message.content.lower().split(" "))-1]:
                            current_prices[1] = message.content.lower().split(" ")[
                                len(message.content.lower().split(" ")) - 1]
                            timing2=(datetime.datetime.today()+datetime.timedelta(hours=3)).strftime(" [%d/%m/%Y %H:%M]")
            await message.delete()

bot.run(TOKEN)
