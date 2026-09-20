import discord
from discord.ext import commands
from discord import app_commands
import json
import os

# Güncel Yetkili Rolleri
YETKILI_ROLLER = [1483443654772396093, 1494377287666368602, 1494377031432147055]

CARPI_EMOJI = "<:carpi:1548486925881581588>"

# Özel Emojiler (Departman Eşleştirmeleri)
TIK_EMOJILERI = {
    "Moderasyon Ekibi": "✅",
    "Gamemaster": "✅",
    "Geliştirici": "✅",
    "Aktör": "✅",
    "Etkinlik Sorumlusu": "✅"
}

# --- JSON VERİTABANI YÖNETİMİ ---
def get_forum_data():
    dosya_adi = "forum_data.json"
    if not os.path.exists(dosya_adi):
        varsayilan_veri = {
            "kanal_id": None,
            "mesaj_id": None,
            "formlar": {
                "Gamemaster": {"durum": "Aktif", "link": "https://link_ekle.com"},
                "Moderasyon Ekibi": {"durum": "Aktif", "link": "https://link_ekle.com"},
                "Aktör": {"durum": "Aktif", "link": "https://link_ekle.com"},
                "Geliştirici": {"durum": "Aktif", "link": "https://link_ekle.com"},
                "Etkinlik Sorumlusu": {"durum": "Aktif", "link": "https://link_ekle.com"}
            }
        }
        with open(dosya_adi, "w", encoding="utf-8") as f:
            json.dump(varsayilan_veri, f, indent=4, ensure_ascii=False)
        return varsayilan_veri

    with open(dosya_adi, "r", encoding="utf-8") as f:
        return json.load(f)

def save_forum_data(veri):
    with open("forum_data.json", "w", encoding="utf-8") as f:
        json.dump(veri, f, indent=4, ensure_ascii=False)

# --- ÇOKLU GÖMÜLÜ MESAJ (EMBED) OLUŞTURUCU ---
def forum_embedler_olustur(veri):
    # 1. Embed: Sadece kapak fotoğrafı
    embed1 = discord.Embed(color=0x2b2d31)
    embed1.set_image(url="attachment://forum.png")
    
    # 2. Embed: Bilgilendirme ve linkler
    aciklama_metni = (
        '"Shadow Roleplay" bünyesinde bir oyuncudan daha fazlası olup, sunucunun tarihine adını kazımak istiyorsan; katılabileceğiniz yetkili ekiplerimiz;\n\n'
        '**Moderasyon Ekibi:** Shadow Roleplay discord sunucusu ile ilgilenen ve genel huzuru sağlayan ekiptir. Kendi içerisinde farklı görev dallarına ayrılır.\n'
        '**Gamemaster Ekibi:** Shadow Roleplay oyun içerisinde insanların rollerini zenginleştiren ve eventler tasarlayan ekiptir.\n'
        '**Aktör Ekibi:** Shadow Roleplay oyun içerisinde SCP aktörlüğü veya başka departmanlarda görev yapan ekiptir.\n'
        '**Geliştirici Ekibi:** Shadow Roleplay roblox ve sitelerin yapımı/gelişimi ile ilgilenen ekiptir.\n'
        '**Etkinlik Sorumlusu:** Sunucu içerisindeki etkinlikleri planlayan ve yöneten ekiptir.\n\n'
        '━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
    )

    embed2 = discord.Embed(
        title="Bize Katılın!",
        description=aciklama_metni,
        color=0x2b2d31
    )

    metin = ""
    for rol, ayarlar in veri["formlar"].items():
        is_aktif = ayarlar["durum"].lower() == "aktif"

        # Her role özel tanımladığımız tik emojisi veya aktifse varsayılan tik, inaktifse özel çarpı
        durum_emoji = TIK_EMOJILERI.get(rol, "✅") if is_aktif else CARPI_EMOJI
        durum_metni = f"Aktif {durum_emoji}" if is_aktif else f"İnaktif {durum_emoji}"

        link = ayarlar["link"]

        # Format: Aktif [Özel Tik] | **Rol Alım Formu** [tıklayın](link)
        metin += f"{durum_metni} | **{rol} Alım Formu** [tıklayın]({link})\n\n"

    embed2.description += metin
    embed2.set_footer(text="Shadow Roleplay • Başvuru Formları")
    
    return [embed1, embed2]

class ForumlarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    forum_grup = app_commands.Group(name="forumlar", description="Alım formları yönetim sistemi")

    @forum_grup.command(name="durum", description="Formun durumunu Aktif veya İnaktif olarak değiştirir.")
    @app_commands.describe(
        forum="Hangi formun durumunu güncelleyeceksin?",
        yeni_durum="Formun yeni durumu ne olacak?"
    )
    @app_commands.choices(forum=[
        app_commands.Choice(name="Gamemaster", value="Gamemaster"),
        app_commands.Choice(name="Moderasyon Ekibi", value="Moderasyon Ekibi"),
        app_commands.Choice(name="Aktör", value="Aktör"),
        app_commands.Choice(name="Geliştirici", value="Geliştirici"),
        app_commands.Choice(name="Etkinlik Sorumlusu", value="Etkinlik Sorumlusu")
    ], yeni_durum=[
        app_commands.Choice(name="Aktif", value="Aktif"),
        app_commands.Choice(name="İnaktif", value="İnaktif")
    ])
    async def durum_guncelle(self, interaction: discord.Interaction, forum: app_commands.Choice[str], yeni_durum: app_commands.Choice[str]):
        await self.mesaji_yenile(interaction, forum.value, "durum", yeni_durum.value)

    @forum_grup.command(name="link", description="Formun başvuru linkini değiştirir.")
    @app_commands.describe(
        forum="Hangi formun linkini güncelleyeceksin?",
        yeni_link="Yeni başvuru linkini yapıştırın."
    )
    @app_commands.choices(forum=[
        app_commands.Choice(name="Gamemaster", value="Gamemaster"),
        app_commands.Choice(name="Moderasyon Ekibi", value="Moderasyon Ekibi"),
        app_commands.Choice(name="Aktör", value="Aktör"),
        app_commands.Choice(name="Geliştirici", value="Geliştirici"),
        app_commands.Choice(name="Etkinlik Sorumlusu", value="Etkinlik Sorumlusu")
    ])
    async def link_guncelle(self, interaction: discord.Interaction, forum: app_commands.Choice[str], yeni_link: str):
        if not (yeni_link.startswith("http://") or yeni_link.startswith("https://")):
            return await interaction.response.send_message("❌ Geçerli bir link girmelisin (http:// veya https:// ile başlamalı).", ephemeral=True)

        await self.mesaji_yenile(interaction, forum.value, "link", yeni_link)

    async def mesaji_yenile(self, interaction, forum_adi, ayar_turu, yeni_deger):
        kullanici_rolleri = [rol.id for rol in interaction.user.roles]
        if not any(rol in YETKILI_ROLLER for rol in kullanici_rolleri):
            return await interaction.response.send_message("❌ Yetkiniz yok!", ephemeral=True)

        veri = get_forum_data()

        if veri["mesaj_id"] is None or veri["kanal_id"] is None:
            return await interaction.response.send_message("❌ Önce `/kurulum` panelinden formu kurmalısın.", ephemeral=True)

        veri["formlar"][forum_adi][ayar_turu] = yeni_deger
        save_forum_data(veri)

        try:
            kanal = self.bot.get_channel(veri["kanal_id"])
            mesaj = await kanal.fetch_message(veri["mesaj_id"])

            yeni_embedler = forum_embedler_olustur(veri)
            await mesaj.edit(embeds=yeni_embedler)

            await interaction.response.send_message(f"✅ **{forum_adi}** formunun **{ayar_turu}** ayarı başarıyla güncellendi.", ephemeral=True)
        except discord.NotFound:
            await interaction.response.send_message("❌ Hedef mesaj bulunamadı. Silinmiş olabilir, lütfen tekrar `/kurulum` paneli üzerinden kurulum yapın.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Mesaj güncellenirken beklenmeyen bir hata oluştu: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ForumlarCog(bot))
