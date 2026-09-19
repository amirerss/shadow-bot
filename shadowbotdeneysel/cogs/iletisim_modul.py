import os
import json
import discord
from discord.ext import commands
from discord import app_commands

YETKILI_ROLLER = [1483443654772396093 , 1494377287666368602 , 1494377031432147055 ]
DATA_FILE = "iletisim_data.json"

def get_iletisim_data():
    if not os.path.exists(DATA_FILE):
        varsayilan = {
            "kanal_id": None,
            "mesaj_id": None,
            "sivil": (
                "> `Tesis Direktörü` <@672176793897140283>\n"
                "> `Etik Komite Sorumlusu` <@1205592076226396160>\n"
                "> `Hukuk Departmanı Sorumlusu` <@808771812099489843>\n"
                "> `Üretim & Mühendislik Departmanı Müdürü` <@1092860215923327157>\n"
                "> `Tıbbi Departman Başhekimi` <@1331647444928430210>\n"
                "> `Bilimsel Departman Müdürü` <@856084128028819516>\n"
                "> `Genel Servis Departmanı Müdürü` N/A"
            ),
            "sivil_kombatif": (
                "> `İç Güvenlik Departmanı Müdürü` <@582993463402954833>\n"
                "> `İstihbarat Teşkilatı Müdürü` <@932021781684953099>"
            ),
            "kombatif": (
                "> `Delta-43 Albayı` <@479992893952753674>\n"
                "> `Güvenlik Departmanı Amiri` <@692326152949202994>\n"
                "> `Nu-7 Albayı` <@932021781684953099>"
            ),
            "direktorler": (
                "> `Bilimsel Departman Direktörü` <@932021781684953099>\n"
                "> `İç Güvenlik Departmanı Direktörü` <@814092843093065730>\n"
                "> `Hukuk Departmanı Direktörü` <@814092843093065730>\n"
                "> `İstihbarat Teşkilatı Direktörü` <@932021781684953099>\n"
                "> `Üretim & Mühendislik Departmanı Direktörü` <@1092860215923327157>\n"
                "> `Lojistik Departman Direktörü` <@1092860215923327157>\n"
                "> `Üretim Departmanı Direktörü` <@1092860215923327157>\n"
                "> `Etik Komite Başkanı` <@814092843093065730>\n"
                "> `Yönetim Departmanı Direktörü` <@932021781684953099>\n"
                "> `Tıbbi Departman Direktörü` N/A\n"
                "> `Mobil Görev Gücü Direktörü` MTF-CmD\n"
                "> `Güvenlik Departmanı Direktörü` <@479992893952753674>\n"
                "> `Nu-7 Direktörü` <@932021781684953099>"
            ),
            "sikayet": (
                "Gamemaster ekibinden şikayetçiyseniz <@814092843093065730>\n"
                "<@814092843093065730>'dan şikayetçiyseniz <@479992893952753674>\n"
                "Yönetim kurulundan şikayetçiyseniz <@1193247132447166605>\n"
                "<@1193247132447166605>'den şikayetçiyseniz <@479992893952753674> gitmelisiniz ki yapılması gereken yapılsın.\n\n"
                "Herhangi bir sorunuz varsa veya sıralamada sorun varsa TICKET açmalısınız. <#1461104282349736016>"
            )
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(varsayilan, f, indent=4, ensure_ascii=False)
        return varsayilan

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_iletisim_data(veri):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(veri, f, indent=4, ensure_ascii=False)

def iletisim_embed_olustur(veri):
    embed = discord.Embed(
        title="KİME ULAŞMALIYIM?",
        description=(
            "*Burada kimin neye veya istediğiniz kişinin kim olduğunu bulmanıza yardımcı olması "
            "amacıyla ve boş yere insanlara gidip etiketlememeniz amacıyla kurulmuştur.*"
        ),
        color=0x2b2d31
    )

    embed.set_image(url="attachment://ulasim.png")
    embed.add_field(name="SİVİL DEPARTMANLAR", value=veri["sivil"], inline=False)
    embed.add_field(name="SİVİL/KOMBATİF DEPARTMANLAR", value=veri["sivil_kombatif"], inline=False)
    embed.add_field(name="KOMBATİF DEPARTMANLAR", value=veri["kombatif"], inline=False)
    embed.add_field(name="DEPARTMAN DİREKTÖRLERİ", value=veri["direktorler"], inline=False)
    embed.add_field(name="\u200b", value=veri["sikayet"], inline=False)
    embed.set_footer(text="Shadow Roleplay • Departman Rehberi ve İletişim Şeması")
    return embed

class IletisimCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="kime_ulasmaliyim_duzenle", description="Sabit mesajdaki bir bölümün metnini düzenler.")
    @app_commands.describe(
        bolum="Düzenlenecek kategori",
        yeni_metin="Bölümün yeni içeriği (Satır atlamak için \\n kullanabilirsiniz)"
    )
    @app_commands.choices(bolum=[
        app_commands.Choice(name="Sivil Departmanlar", value="sivil"),
        app_commands.Choice(name="Sivil / Kombatif Departmanlar", value="sivil_kombatif"),
        app_commands.Choice(name="Kombatif Departmanlar", value="kombatif"),
        app_commands.Choice(name="Departman Direktörleri", value="direktorler"),
        app_commands.Choice(name="Şikayet ve İtiraz Zinciri", value="sikayet")
    ])
    async def panel_duzenle(self, interaction: discord.Interaction, bolum: app_commands.Choice[str], yeni_metin: str):
        kullanici_rolleri = [rol.id for rol in interaction.user.roles]
        if not any(rol in YETKILI_ROLLER for rol in kullanici_rolleri):
            return await interaction.response.send_message("Yetkiniz yok.", ephemeral=True)

        veri = get_iletisim_data()
        if not veri.get("kanal_id") or not veri.get("mesaj_id"):
            return await interaction.response.send_message("Kayıtlı bir panel mesajı bulunamadı. Önce /kime_ulasmaliyim_kur çalıştırın.", ephemeral=True)

        duzeltilmis_metin = yeni_metin.replace("\\n", "\n")
        veri[bolum.value] = duzeltilmis_metin
        save_iletisim_data(veri)

        try:
            kanal = self.bot.get_channel(veri["kanal_id"])
            mesaj = await kanal.fetch_message(veri["mesaj_id"])

            yeni_embed = iletisim_embed_olustur(veri)
            await mesaj.edit(embed=yeni_embed)

            await interaction.response.send_message(f"**{bolum.name}** alanı başarıyla güncellendi.", ephemeral=True)
        except discord.NotFound:
            await interaction.response.send_message("Hedef mesaj kanalda bulunamadı (silinmiş olabilir).", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Güncelleme hatası: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(IletisimCog(bot))
