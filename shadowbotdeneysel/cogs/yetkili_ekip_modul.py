import discord
from discord.ext import commands
from discord import app_commands
import json
import os

YETKILI_ROLLER = [1496628714413228072]
DATA_FILE = "yetkili_data.json"

RANK_ORDER = {
    "Baş GM": 1,
    "Üst Düzey GM": 2,
    "Denetmen": 3,
    "Gamemaster": 4,
    "Deneyimsiz GM": 5,
    "Emekli GM": 6
}

# --- JSON VERİTABANI YÖNETİMİ ---
def get_yetkili_data():
    if not os.path.exists(DATA_FILE):
        varsayilan_veri = {
            "kanal_id": None,
            "mesaj_id": None,
            "ekip": [
                {"rutbe": "Baş GM", "isim": "Ozy", "roblox": "ozymandiasnow", "tarih": "16/04/2024", "yetki": "Tam Yetki"},
                {"rutbe": "Üst Düzey GM", "isim": "Deno", "roblox": "denoizm", "tarih": "17/04/2024", "yetki": "Tam Yetki"},
                {"rutbe": "Üst Düzey GM", "isim": "Melih", "roblox": "dondurmaci822", "tarih": "24.07.2026", "yetki": "Tam Yetki"},
                {"rutbe": "Üst Düzey GM", "isim": "KayraTSK", "roblox": "songoku.42", "tarih": "26.04.2026", "yetki": "Tam Yetki"},
                {"rutbe": "Denetmen", "isim": "Junbun", "roblox": "dikacuu", "tarih": "04.06.2026", "yetki": "Yönetim / Denetim"},
                {"rutbe": "Gamemaster", "isim": "Negan Smith", "roblox": "_negan_smith", "tarih": "26.04.2026", "yetki": "Temel Destek & Raporlama & Etkinlik"},
                {"rutbe": "Gamemaster", "isim": "İllahpasha", "roblox": "essekterbiyecisi.1_31696", "tarih": "26.04.2026", "yetki": "Temel Destek & Raporlama & Etkinlik"},
                {"rutbe": "Gamemaster", "isim": "KDJfroe", "roblox": "stoormy54", "tarih": "04.06.2026", "yetki": "Temel Destek & Raporlama & Etkinlik"},
                {"rutbe": "Gamemaster", "isim": "Operatortr", "roblox": "xpgamer21", "tarih": "08.06.2026", "yetki": "Temel Destek & Raporlama & Etkinlik"},
                {"rutbe": "Deneyimsiz GM", "isim": "Amelia", "roblox": "yumekomuyuz", "tarih": "24.07.2026", "yetki": "Gözlemci / Stajyer"},
                {"rutbe": "Deneyimsiz GM", "isim": "Yıldız", "roblox": "probnott", "tarih": "24.07.2026", "yetki": "Gözlemci / Stajyer"},
                {"rutbe": "Emekli GM", "isim": "Gukguk", "roblox": "-", "tarih": "-", "yetki": "-"},
                {"rutbe": "Emekli GM", "isim": "Emir", "roblox": "-", "tarih": "24.07.2026", "yetki": "-"},
                {"rutbe": "Emekli GM", "isim": "Infini", "roblox": "-", "tarih": "26.04.2026", "yetki": "-"}
            ]
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(varsayilan_veri, f, indent=4, ensure_ascii=False)
        return varsayilan_veri

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_yetkili_data(veri):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(veri, f, indent=4, ensure_ascii=False)

def yetkili_embed_olustur(veri):
    embed = discord.Embed(
        title="Yetkili Ekip Kadrosu",
        description="Güncel yetkili kadrosu ve hiyerarşik sıralaması aşağıda belirtilmiştir.\n\n",
        color=0x2b2d31
    )

    sirali_ekip = sorted(veri.get("ekip", []), key=lambda x: RANK_ORDER.get(x["rutbe"], 99))

    if not sirali_ekip:
        embed.description += "*Henüz eklenmiş bir yetkili bulunmamaktadır.*"
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
            metin += f"└ **{uye['isim']}** (`{uye['roblox']}`) • {uye['tarih']} • *{uye['yetki']}*\n"
        metin += "\n"

    embed.description += metin
    embed.set_footer(text="Shadow Roleplay • Yetkili Hiyerarşi Dosyası")
    return embed

class YetkiliEkipCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ekip_grup = app_commands.Group(name="yetkili_ekip", description="Yetkili kadrosu tablo yönetim sistemi")

    @ekip_grup.command(name="ekle", description="Kadroya yeni bir yetkili ekler.")
    @app_commands.describe(rutbe="Hiyerarşik rütbesi", isim="Görünen ismi", roblox="Roblox kullanıcı adı", tarih="Tarih (Örn: 16/04/2024)", yetki="Görev/Yetki açıklaması")
    @app_commands.choices(rutbe=[
        app_commands.Choice(name="Baş GM", value="Baş GM"),
        app_commands.Choice(name="Üst Düzey GM", value="Üst Düzey GM"),
        app_commands.Choice(name="Denetmen", value="Denetmen"),
        app_commands.Choice(name="Gamemaster", value="Gamemaster"),
        app_commands.Choice(name="Deneyimsiz GM", value="Deneyimsiz GM"),
        app_commands.Choice(name="Emekli GM", value="Emekli GM")
    ])
    async def ekle(self, interaction: discord.Interaction, rutbe: app_commands.Choice[str], isim: str, roblox: str, tarih: str, yetki: str):
        veri = get_yetkili_data()
        yeni_uye = {
            "rutbe": rutbe.value,
            "isim": isim,
            "roblox": roblox,
            "tarih": tarih,
            "yetki": yetki
        }
        veri["ekip"].append(yeni_uye)
        await self.mesaji_yenile(interaction, veri, f"**{isim}** kadroya eklendi.")

    @ekip_grup.command(name="sil", description="Kadrodan bir yetkiliyi ismiyle siler.")
    async def sil(self, interaction: discord.Interaction, isim: str):
        veri = get_yetkili_data()
        baslangic_sayisi = len(veri["ekip"])

        veri["ekip"] = [uye for uye in veri["ekip"] if uye["isim"].lower() != isim.lower()]

        if len(veri["ekip"]) == baslangic_sayisi:
            return await interaction.response.send_message(f"Listede **{isim}** adında biri bulunamadı.", ephemeral=True)

        await self.mesaji_yenile(interaction, veri, f"**{isim}** kadrodan silindi.")

    @ekip_grup.command(name="duzenle", description="Mevcut bir yetkilinin bilgilerini günceller.")
    @app_commands.describe(mevcut_isim="Düzenlenecek kişinin şimdiki adı")
    @app_commands.choices(yeni_rutbe=[
        app_commands.Choice(name="Baş GM", value="Baş GM"),
        app_commands.Choice(name="Üst Düzey GM", value="Üst Düzey GM"),
        app_commands.Choice(name="Denetmen", value="Denetmen"),
        app_commands.Choice(name="Gamemaster", value="Gamemaster"),
        app_commands.Choice(name="Deneyimsiz GM", value="Deneyimsiz GM"),
        app_commands.Choice(name="Emekli GM", value="Emekli GM")
    ])
    async def duzenle(self, interaction: discord.Interaction, mevcut_isim: str, yeni_rutbe: app_commands.Choice[str] = None, yeni_isim: str = None, yeni_roblox: str = None, yeni_tarih: str = None, yeni_yetki: str = None):
        veri = get_yetkili_data()

        hedef_uye = next((uye for uye in veri["ekip"] if uye["isim"].lower() == mevcut_isim.lower()), None)
        if not hedef_uye:
            return await interaction.response.send_message(f"Listede **{mevcut_isim}** adında biri bulunamadı.", ephemeral=True)

        if yeni_rutbe: hedef_uye["rutbe"] = yeni_rutbe.value
        if yeni_isim: hedef_uye["isim"] = yeni_isim
        if yeni_roblox: hedef_uye["roblox"] = yeni_roblox
        if yeni_tarih: hedef_uye["tarih"] = yeni_tarih
        if yeni_yetki: hedef_uye["yetki"] = yeni_yetki

        await self.mesaji_yenile(interaction, veri, f"**{mevcut_isim}** başarıyla düzenlendi.")

    async def mesaji_yenile(self, interaction, veri, basari_mesaji):
        kullanici_rolleri = [rol.id for rol in interaction.user.roles]
        if not any(rol in YETKILI_ROLLER for rol in kullanici_rolleri):
            return await interaction.response.send_message("Yetkiniz yok.", ephemeral=True)

        if veri["mesaj_id"] is None or veri["kanal_id"] is None:
            return await interaction.response.send_message("Önce merkezi `/kurulum` panelini kullanarak tabloyu kurmalısın.", ephemeral=True)

        save_yetkili_data(veri)

        try:
            kanal = self.bot.get_channel(veri["kanal_id"])
            mesaj = await kanal.fetch_message(veri["mesaj_id"])

            yeni_embed = yetkili_embed_olustur(veri)
            await mesaj.edit(embed=yeni_embed)

            await interaction.response.send_message(basari_mesaji, ephemeral=True)
        except discord.NotFound:
            await interaction.response.send_message("Sabit mesaj bulunamadı. Lütfen tekrar `/kurulum` paneli üzerinden kurulum yapın.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Beklenmeyen hata: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(YetkiliEkipCog(bot))