from interactions import listen, Intents, Client
from interactions.ext.prefixed_commands import prefixed_command, PrefixedContext
from interactions.ext import prefixed_commands
from interactions.api.voice.audio import AudioVolume
import asyncio
import speech_recognition as sr

bot = Client(
    intents=(
        Intents.GUILD_MESSAGES
        | Intents.GUILD_VOICE_STATES
        | Intents.DIRECT_MESSAGES
        | Intents.GUILDS
        | Intents.MESSAGE_CONTENT
    )
)
prefixed_commands.setup(bot, default_prefix="pls ")

@listen()
async def on_ready():
    print("DuckyBot is ready!")

async def recognize_speech(voice_state):
    r = sr.Recognizer()
    message = ''

    while voice_state.connected:
        await voice_state.start_recording(encoding="wav")
        await asyncio.sleep(2)
        await voice_state.stop_recording()

        for key, file in voice_state.recorder.output.items():
            with sr.AudioFile(file) as source:
                audio = r.record(source)
                try:
                    message = r.recognize_google(audio)
                    return message.lower()
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"Google Speech Recognition error: {e}")

async def handle_commands(voice_state, ctx):
    listening = False

    while voice_state.connected:
        message = await recognize_speech(voice_state)

        print(message)

        if "hey ducky bot" in message or "ducky bot" in message:
            audio = AudioVolume("yesMyLord.wav")
            await ctx.voice_state.play(audio)
            listening = True

        if listening:
            message = await recognize_speech(voice_state)
            if "leave" in message:
                print("Fine, I'll leave")
                await voice_state.disconnect()
                break
            elif "test" in message:
                print("Test Command Received")
            else:
                print("Command not recognized")
            listening = False

@prefixed_command(name="join")
async def join(ctx: PrefixedContext):
    if not ctx.voice_state:
        print("Joining voice channel...")
        voice_state = await ctx.author.voice.channel.connect()

        await handle_commands(voice_state, ctx)

bot.start('MTA0MDQwNjc2MjkzNjg2MDc3NA.GCT62x.-sCBaS9GLU3wIp3LbfNqXoPAdvBZLvp54kLN1c')