import interactions
from interactions.api.voice.audio import AudioVolume


class Sand(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client

    @interactions.slash_command(
        name="sand",
        description="you know what its gonna be in 100 years from now, yeah, SAND"
    )
    async def play_file(self, ctx: interactions.SlashContext):
        if not ctx.voice_state:
            await ctx.author.voice.channel.connect()

        audio = AudioVolume("sand.mp3")
        await ctx.send('Its gonna be sand')
        await ctx.voice_state.play(audio)
        await ctx.voice_state.disconnect()