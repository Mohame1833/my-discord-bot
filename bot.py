import discord
import requests
import datetime
import asyncio

TOKEN = "MTM2MDQxODMzOTc4NDIzMjk2MA.GG3aHt.naqZe1E0ab7SLTJPWfNrkbkKzKB74KM91Imsek"
CHANNEL_ID = 1325277662280945807  # حط هنا ID الروم بتاع الصلاة

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# نصوص الصلاة
prayer_messages = {
    "Fajr": """صلاة الفجر 🩶

الفجر أذّن يا ناس
قوموا نلحق ركعة تنوّر يومنا

دعاء بداية اليوم:
"اللهم اجعل هذا الصباح فتحًا لنا لكل خير، وبابًا لكل فرج، ونجاة من كل شر."

اللي بيبدأ يومه بالفجر… كسبان من بدري

صلي

وادعي

وسلّمها لربنا

@everyone""",
    "Dhuhr": """صلاة الظهر 🤎

أذان الظهر يشوباب
هدّي الدنيا شوية… وسيّب اللي في إيدك، ده وقت لقاء مع ربنا

دعاء وقت الظهر:
"اللهم في هذا الوقت الطيب، اغسل قلوبنا من الهم، واملأها رضا، واغفر لنا ما مضى، وبارك لنا فيما هو آت."

اللي يصلي الظهر في وقته…
بيختار الراحة على التعب، والرضا على الزحمة، وربنا على الدنيا.

@everyone""",
    "Asr": """صلاة العصر 💛

العصر أذّن يا حبايب
خد بريك من اليوم… وارجع لربنا بركعتين

دعاء وقت العصر:
"اللهم ارزقنا في هذا الوقت راحة تُنسي همّ الحياة، ورضا يغمر القلب، وبركة في ما تبقى من اليوم."

اللي يحافظ على العصر…
يحافظ على قلبه وسط الزحمة، ويخلي يومه في حفظ ربنا.

@everyone""",
    "Maghrib": """صلاة المغرب 💙

المغرب أذّن يا جماعة
يلا نقوم نصلي ونشحن روحنا شوية

دعاء حلو كده:
"يا رب اجعل لنا من كل همّ فرج، ومن كل ضيق مخرج، وارزقنا راحة البال وطمأنينة القلب."

ماتنسوش:

تصلوا

تدعوا

وتاخدوا لحظة مع ربنا

@everyone""",
    "Isha": """صلاة العشاء 💚

العشاء أذّن دلوقتي
يومك قرب يخلص… اختمه وانت قريب من ربنا

دعاء آخر اليوم:
"اللهم اجعل لنا في هذه الليلة راحة تسكن بها أرواحنا، ونومًا هادئًا تُجدد به طاقتنا، واغفر لنا ما فات."

اللي يختم يومه بصلاة العشاء…
ينام وقلبه مرتاح، وروحه مطمئنة، وربنا راضي عنه.

@everyone"""
}

async def get_prayer_times():
    try:
        response = requests.get("https://api.aladhan.com/v1/timingsByCity?city=Cairo&country=Egypt&method=5", timeout=10)
        data = response.json()
        timings = data["data"]["timings"]
        return timings
    except Exception as e:
        print("[ERROR] Failed to fetch prayer times:", e)
        return None

async def send_prayer_time():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    last_fetch = None
    prayer_times = {}
    sent_today = set()

    while not client.is_closed():
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")

        if not last_fetch or (now - last_fetch).seconds > 3600:
            new_times = await get_prayer_times()
            if new_times:
                prayer_times = new_times
                last_fetch = now
                sent_today.clear()
                print("[INFO] Updated prayer times:", prayer_times)

        if prayer_times:
            for name, time in prayer_times.items():
                if time[:5] == current_time and name not in sent_today:
                    if name in prayer_messages:
                        await channel.send(prayer_messages[name])
                        sent_today.add(name)
                        print(f"[INFO] Sent prayer: {name}")
                    await asyncio.sleep(60)

        await asyncio.sleep(5)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    client.loop.create_task(send_prayer_time())

client.run(TOKEN)
