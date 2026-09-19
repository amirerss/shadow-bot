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
                "- <@&1461067392724631845>: <@672176793897140283>\n"
                "- <@&1464654530753986825>: <@932021781684953099>\n"
                "- <@&1461069664154030140> Müdürü: <@1205592076226396160>\n"
                "- <@&1478401396008288398> Müdürü: <@808771812099489843>\n"
                "- <@&1478400432421343253> Müdürü: <@1092860215923327157>\n"
                "- <@&1461066782100951050> Müdürü: <@601808998991134731>\n"
                "- <@&1461066816259620934> Müdürü: <@856084128028819516>\n"
                "- <@&1493700213670416425> Müdürü: <@1326665605964627979>"
            ),
            "sivil_kombatif": (
                "- <@&1461067030030581925> Müdürü: <@582993463402954833>\n"
                "- <@&1478400254469472256> Müdürü: <@932021781684953099>"
            ),
            "kombatif": (
                "- <@&1540775555828547694> Takım Lideri: <@479992893952753674>\n"
                "- <@&1461066745006522563> Lideri: <@692326152949202994>\n"
                "- <@&1461121406589993134> Alay Lideri: <@932021781684953099>"
            ),
            "direktorler": (
                "- <@&1461067356997681152> Direktörü: <@932021781684953099>\n"
                "- <@&1461067030030581925> Direktörü: <@814092843093065730>\n"
                "- <@&1461069664154030140> Direktörü: <@814092843093065730>\n"
                "- <@&1461066816259620934> Direktörü: <@932021781684953099>\n"
                "- <@&1478400432421343253> Direktörü: <@1092860215923327157>\n"
                "- <@&1478401391654473801> Direktörü: <@1092860215923327157>\n"
                "- <@&1478401386222981402> Direktörü: <@1092860215923327157>\n"
                "- <@&1478401396008288398> Direktörü: <@814092843093065730>\n"
                "- <@&1478400254469472256> Direktörü: <@932021781684953099>\n"
                "- <@&1461066782100951050> Direktörü: N/A\n"
                "- <@&1461121406589993134> Direktörü: MTF-CmD\n"
                "- <@&1540775555828547694> Direktörü: <@479992893952753674>\n"
                "- <@&1461066745006522563> Direktörü: <@932021781684953099>"
            ),
            "sikayet": (
                "- Gamemaster ekibinden şikayetçiyseniz -> <@479992893952753674>\n"
                "- <@479992893952753674>'dan şikayetçiyseniz -> <@932021781684953099>\n"
                "- Yönetim Kurulundan şikayetçiyseniz -> <@1193247132447166605>\n"
                "- <@1193247132447166605>'den şikayetçiyseniz -> <@932021781684953099>\n\n"
                "*Gereken adımların atılabilmesi için bu zincire uyunuz.*"
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
        title="Kime Ulaşmalıyım?",
        description=(
            "Bu kanal, kimin ne ile ilgilendiğini veya ulaşmak istediğiniz yetkiliyi bulmanıza "
            "yardımcı olmak ve gereksiz etiketlemeleri önlemek amacıyla oluşturulmuştur.\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ),
        color=0x2b2d31
    )

    embed.set_image(url="attachment://ulasim.png")
    embed.add_field(name="Sivil Departmanlar", value=veri["sivil"], inline=False)
    embed.add_field(name="Sivil / Kombatif Departmanlar", value=veri["sivil_kombatif"], inline=False)
    embed.add_field(name="Kombatif Departmanlar", value=veri["kombatif"], inline=False)
    embed.add_field(name="Departman Direktörleri", value=veri["direktorler"], inline=False)
    embed.add_field(name="Hiyerarşik Şikayet ve İtiraz Zinciri", value=veri["sikayet"], inline=False)
    embed.add_field(
        name="Genel Destek Talepleri",
        value=(
            "Herhangi bir sorunuz veya sıralamayla ilgili bir itirazınız varsa doğrudan kişileri etiketlemek yerine "
            "<#1461104282349736016> kanalından ticket açarak durumu bize iletebilirsiniz."
        ),
        inline=False
    )
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
