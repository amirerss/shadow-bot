import discord
from discord.ext import commands
from discord import app_commands
import json
import os

YETKILI_ROLLER = [1483443654772396093 , 1494377287666368602 , 1494377031432147055 ]
DATA_FILE = "gelistirici_data.json"

RANK_ORDER = {
    "Baş Geliştirici": 1,
    "Kıdemli Geliştirici": 2,
    "Geliştirici": 3,
    "Deneme Geliştirici": 4,
    "Emekli": 5
}

# --- JSON VERİTABANI YÖNETİMİ ---
def get_gelistirici_data():
    if not os.path.exists(DATA_FILE):
        varsayilan_veri = {
            "kanal_id": None,
            "mesaj_id": None,
            "ekip": [
                {"rutbe": "Baş Geliştirici", "isim": "Saraswati", "discord_ismi": "saraswati12", "tarih": "10/07/2025", "guncelleme": "Şu ana kadar olan bütün herşey"},
                {"rutbe": "Geliştirici", "isim": "Beleşçi", "discord_ismi": "suriyelifilnecati.", "tarih": "14/07/2026", "guncelleme": "2.7"},
                {"rutbe": "Geliştirici", "isim": "Otuka", "discord_ismi": "otuka_kemal123", "tarih": "21/08/2026", "guncelleme": "-"},
                {"rutbe": "Geliştirici", "isim": "TigerKGK", "discord_ismi": "Tigerkgk_", "tarih": "02/08/2026", "guncelleme": "-"},
                {"rutbe": "Geliştirici", "isim": "Ayhan", "discord_ismi": "ayhnxz", "tarih": "21/08/2026", "guncelleme": "-"},
                {"rutbe": "Geliştirici", "isim": "WhisperMan", "discord_ismi": "whisperman34", "tarih": "15/08/2026", "guncelleme": "-"},
                {"rutbe": "Deneme Geliştirici", "isim": "Grimlord", "discord_ismi": "grimlord_3834", "tarih": "05/05/2026", "guncelleme": "2.7"},
                {"rutbe": "Deneme Geliştirici", "isim": "Savcı", "discord_ismi": "x3gk", "tarih": "05.09.2026", "guncelleme": "-"},
                {"rutbe": "Emekli", "isim": "Taisynara", "discord_ismi": "Taisynaraa", "tarih": "19.01.2026", "guncelleme": "2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7"},
                {"rutbe": "Emekli", "isim": "Stwrger", "discord_ismi": "stwrger", "tarih": "14.02.2026", "guncelleme": "2.2, 2.3, 2.4, 2.5, 2.6"},
                {"rutbe": "Emekli", "isim": "Neo", "discord_ismi": "neoodv", "tarih": "19.03.2026", "guncelleme": "2.4, 2.5, 2.6"}
            ]
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(varsayilan_veri, f, indent=4, ensure_ascii=False)
        return varsayilan_veri

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_gelistirici_data(veri):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(veri, f, indent=4, ensure_ascii=False)

def gelistirici_embed_olustur(veri):
    embed = discord.Embed(
        title="Geliştirici Ekip Kadrosu",
        description="Güncel geliştirici kadrosu ve katkıları aşağıda belirtilmiştir.\n\n",
        color=0x2b2d31
    )

    sirali_ekip = sorted(veri.get("ekip", []), key=lambda x: RANK_ORDER.get(x["rutbe"], 99))

    if not sirali_ekip:
        embed.description += "*Henüz eklenmiş bir personel bulunmamaktadır.*"
        return embed

    gruplu_ekip = {}
    for uye in sirali_ekip:
        rutbe = uye["rutbe"]
        if rutbe not in gruplu_ekip:
            gruplu_ekip[rutbe] = []
        gruplu_ekip[rutbe].append(uye)

    metin = ""
    for rutbe, uyeler in gruplu_ekip.items():
        metin += f"**{rutbe}**\n"
        for uye in uyeler:
            metin += f"└ **{uye['isim']}** (`{uye['discord_ismi']}`) • {uye['tarih']} • *{uye['guncelleme']}*\n"
        metin += "\n"

    embed.description += metin
    embed.set_footer(text="Shadow Roleplay • Geliştirici Hiyerarşi Dosyası")
    return embed

class GelistiriciEkipCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ekip_grup = app_commands.Group(name="gelistirici_ekip", description="Geliştirici kadrosu yönetim sistemi")

    @ekip_grup.command(name="ekle", description="Kadroya yeni bir geliştirici ekler.")
    @app_commands.describe(rutbe="Hiyerarşik rütbesi", isim="Personel adı/nickname", discord_ismi="Discord kullanıcı adı", tarih="Katılım Tarihi", guncelleme="Büyük Güncellemeler (Sürüm veya açıklama)")
    @app_commands.choices(rutbe=[
        app_commands.Choice(name="Baş Geliştirici", value="Baş Geliştirici"),
        app_commands.Choice(name="Kıdemli Geliştirici", value="Kıdemli Geliştirici"),
        app_commands.Choice(name="Geliştirici", value="Geliştirici"),
        app_commands.Choice(name="Deneme Geliştirici", value="Deneme Geliştirici"),
        app_commands.Choice(name="Emekli", value="Emekli")
    ])
    async def ekle(self, interaction: discord.Interaction, rutbe: app_commands.Choice[str], isim: str, discord_ismi: str, tarih: str, guncelleme: str):
        veri = get_gelistirici_data()
        yeni_uye = {
            "rutbe": rutbe.value,
            "isim": isim,
            "discord_ismi": discord_ismi,
            "tarih": tarih,
            "guncelleme": guncelleme
        }
        veri["ekip"].append(yeni_uye)
        await self.mesaji_yenile(interaction, veri, f"**{isim}** geliştirici kadrosuna eklendi.")

    @ekip_grup.command(name="sil", description="Kadrodan bir geliştiriciyi ismiyle siler.")
    async def sil(self, interaction: discord.Interaction, isim: str):
        veri = get_gelistirici_data()
        baslangic_sayisi = len(veri["ekip"])

        veri["ekip"] = [uye for uye in veri["ekip"] if uye["isim"].lower() != isim.lower()]

        if len(veri["ekip"]) == baslangic_sayisi:
            return await interaction.response.send_message(f"Listede **{isim}** adında biri bulunamadı.", ephemeral=True)

        await self.mesaji_yenile(interaction, veri, f"**{isim}** kadrodan silindi.")

    @ekip_grup.command(name="duzenle", description="Mevcut bir geliştiricinin bilgilerini günceller.")
    @app_commands.describe(mevcut_isim="Düzenlenecek kişinin şimdiki adı")
    @app_commands.choices(yeni_rutbe=[
        app_commands.Choice(name="Baş Geliştirici", value="Baş Geliştirici"),
        app_commands.Choice(name="Kıdemli Geliştirici", value="Kıdemli Geliştirici"),
        app_commands.Choice(name="Geliştirici", value="Geliştirici"),
        app_commands.Choice(name="Deneme Geliştirici", value="Deneme Geliştirici"),
        app_commands.Choice(name="Emekli", value="Emekli")
    ])
    async def duzenle(self, interaction: discord.Interaction, mevcut_isim: str, yeni_rutbe: app_commands.Choice[str] = None, yeni_isim: str = None, yeni_discord_ismi: str = None, yeni_tarih: str = None, yeni_guncelleme: str = None):
        veri = get_gelistirici_data()

        hedef_uye = next((uye for uye in veri["ekip"] if uye["isim"].lower() == mevcut_isim.lower()), None)
        if not hedef_uye:
            return await interaction.response.send_message(f"Listede **{mevcut_isim}** adında biri bulunamadı.", ephemeral=True)

        if yeni_rutbe: hedef_uye["rutbe"] = yeni_rutbe.value
        if yeni_isim: hedef_uye["isim"] = yeni_isim
        if yeni_discord_ismi: hedef_uye["discord_ismi"] = yeni_discord_ismi
        if yeni_tarih: hedef_uye["tarih"] = yeni_tarih
        if yeni_guncelleme: hedef_uye["guncelleme"] = yeni_guncelleme

        await self.mesaji_yenile(interaction, veri, f"**{mevcut_isim}** başarıyla düzenlendi.")

    async def mesaji_yenile(self, interaction, veri, basari_mesaji):
        kullanici_rolleri = [rol.id for rol in interaction.user.roles]
        if not any(rol in YETKILI_ROLLER for rol in kullanici_rolleri):
            return await interaction.response.send_message("Yetkiniz yok.", ephemeral=True)

        if veri["mesaj_id"] is None or veri["kanal_id"] is None:
            return await interaction.response.send_message("Önce merkezi `/kurulum` panelini kullanarak tabloyu kurmalısın.", ephemeral=True)

        save_gelistirici_data(veri)

        try:
            kanal = self.bot.get_channel(veri["kanal_id"])
            mesaj = await kanal.fetch_message(veri["mesaj_id"])

            yeni_embed = gelistirici_embed_olustur(veri)
            await mesaj.edit(embed=yeni_embed)

            await interaction.response.send_message(basari_mesaji, ephemeral=True)
        except discord.NotFound:
            await interaction.response.send_message("Sabit mesaj bulunamadı. Lütfen tekrar `/kurulum` paneli üzerinden kurulum yapın.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Beklenmeyen hata: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(GelistiriciEkipCog(bot))
