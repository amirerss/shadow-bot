import discord
from discord.ext import commands
from discord import app_commands

BLACKLIST_KANAL_ID = 1469711710251126954  
YETKILI_ROLLER = [1483443654772396093 , 1494377287666368602 , 1494377031432147055 ]

class BlacklistCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="blekle", description="Blackliste eklenen kisiyi belirtilen kanala iletir.")
    @app_commands.describe(
        isim="Blackliste eklenen kisinin ismi veya kullanici adi",
        neden="Blackliste eklenme nedeni"
    )
    async def blekle(self, interaction: discord.Interaction, isim: str, neden: str):
        kullanici_rolleri = [rol.id for rol in interaction.user.roles]
        if not any(rol in YETKILI_ROLLER for rol in kullanici_rolleri):
            return await interaction.response.send_message("Bu komutu kullanmak icin yetkiniz yok.", ephemeral=True)

        kanal = self.bot.get_channel(BLACKLIST_KANAL_ID)
        if kanal is None:
            return await interaction.response.send_message("Hata: Blacklist kanali bulunamadi. ID'yi kontrol edin.", ephemeral=True)

        icerik = (
            f"**İsim:** {isim}\n"
            f"**Neden:** {neden}\n"
            f"**Yetkili:** {interaction.user.display_name}"
        )

        embed = discord.Embed(
            title="Blacklist Kaydı",
            description=icerik,
            color=0x2b2d31
        )

        try:
            await kanal.send(embed=embed)
            await interaction.response.send_message("Blacklist kaydi iletildi.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("Hata: Hedef kanala mesaj gonderme yetkim yok.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Hata olustu: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(BlacklistCog(bot))
