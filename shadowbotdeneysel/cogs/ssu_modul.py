import discord
from discord.ext import commands
from discord import app_commands
import datetime

YETKILI_ROLLER = [1483443654772396093 , 1494377287666368602 , 1494377031432147055 ]
DUYURU_KANAL_ID = 1550238173207208027
SSU_LOG_KANAL_ID = 1550238173207208027  

class SSUCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def ssu_log(self, baslik, aciklama, renk):
        log_kanal = self.bot.get_channel(SSU_LOG_KANAL_ID)
        if log_kanal:
            embed = discord.Embed(title=baslik, description=aciklama, color=renk, timestamp=datetime.datetime.now())
            await log_kanal.send(embed=embed)

    @app_commands.command(name='ssu', description="Sabit duyuru kanalına SSU duyurusu atar.")
    @app_commands.describe(
        gun="Hangi gün? (Örn: CUMA)",
        saat="Saat kaçta? (Örn: 19.30)",
        tarih="Tarih nedir? (Örn: 04.09.2026)",
        tik_sayisi="Kaç tik gerekiyor? (Örn: 60)"
    )
    async def ssu_duyuru(self, interaction: discord.Interaction, gun: str, saat: str, tarih: str, tik_sayisi: int):
        kullanici_rolleri = [rol.id for rol in interaction.user.roles]
        if not any(rol in YETKILI_ROLLER for rol in kullanici_rolleri):
            await interaction.response.send_message("Bu komutu kullanmak için gerekli yetkiye sahip değilsin!", ephemeral=True)
            return

        kanal = self.bot.get_channel(DUYURU_KANAL_ID)
        if kanal is None:
            await interaction.response.send_message("Hata: Ayarlanan duyuru kanalı bulunamadı.", ephemeral=True)
            return

        embed = discord.Embed(
            title="YENİ OTURUM (SSU) DUYURUSU",
            description="Sunucumuz için yeni oturum tarihi planlanmıştır. Detaylar aşağıdadır.",
            color=0x3498db
        )
        embed.add_field(name="Gün ve Saat", value=f"{gun.upper()} | {saat}", inline=True)
        embed.add_field(name="Tarih", value=f"{tarih}", inline=True)
        embed.add_field(name="Gereken Tepki", value=f"{tik_sayisi} Adet", inline=False)

        embed.set_footer(text="Shadow Roleplay")
        embed.timestamp = discord.utils.utcnow()

        try:
            etiketler = "@everyone\n@here"
            gonderilen_mesaj = await kanal.send(content=etiketler, embed=embed)
            await gonderilen_mesaj.add_reaction("✅")
            await interaction.response.send_message(f"Duyuru başarıyla {kanal.mention} kanalına gönderildi!", ephemeral=True)

            await self.ssu_log(
                "SSU Duyurusu Gönderildi",
                f"**Gönderen:** {interaction.user.mention}\n**Kanal:** {kanal.mention}\n**Planlanan:** {gun.upper()} - {saat} ({tarih})",
                discord.Color.blue()
            )
        except discord.Forbidden:
            await interaction.response.send_message(f"Hata: {kanal.mention} kanalına mesaj gönderme veya tepki ekleme yetkim yok!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Beklenmeyen bir hata oluştu: {e}", ephemeral=True)

    @app_commands.command(name='ssubaslat', description="Sunucunun açıldığını belirten duyuruyu atar.")
    async def ssu_baslat(self, interaction: discord.Interaction):
        kullanici_rolleri = [rol.id for rol in interaction.user.roles]
        if not any(rol in YETKILI_ROLLER for rol in kullanici_rolleri):
            await interaction.response.send_message("Bu komutu kullanmak için gerekli yetkiye sahip değilsin!", ephemeral=True)
            return

        kanal = self.bot.get_channel(DUYURU_KANAL_ID)
        if kanal is None:
            await interaction.response.send_message("Hata: Ayarlanan duyuru kanalı bulunamadı.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f" SUNUCU AKTİF - GİRİŞLER AÇILDI! ",
            description=f"Sunucu Açılmıştır **Shadow Roleplay** girebilirsiniz. Tüm oyuncularımızı sunucumuza bekliyoruz.",
            color=0x2ecc71  # Canlı Yeşil
        )
        embed.add_field(name=" Sunucu Modu", value="**Roleplay [ :flag_tr: ]**", inline=True)
        embed.add_field(name=" Durum", value="**Girişler Aktif / Bağlanabilirsiniz**", inline=True)

        embed.set_footer(text="Shadow Roleplay • İyi Oyunlar Dileriz!")
        embed.timestamp = discord.utils.utcnow()

        try:
            etiketler = "@everyone\n@here"
            await kanal.send(content=etiketler, embed=embed)
            await interaction.response.send_message(f"Sunucu açılış duyurusu {kanal.mention} kanalına başarıyla gönderildi!", ephemeral=True)

            await self.ssu_log(
                "Sunucu Açıldı (SSU Başlatıldı)",
                f"**Başlatan:** {interaction.user.mention}\n**Kanal:** {kanal.mention}",
                discord.Color.green()
            )
        except discord.Forbidden:
            await interaction.response.send_message(f"Hata: {kanal.mention} kanalına mesaj gönderme yetkim yok!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Beklenmeyen bir hata oluştu: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SSUCog(bot))
