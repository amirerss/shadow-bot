import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import os

YETKILI_ROLLER = [1483443654772396093, 1494377287666368602, 1494377031432147055]

# --- MERKEZİ KURULUM MENÜSÜ ---
class KurulumMenusu(View):
    def __init__(self, bot):
        super().__init__(timeout=300) 
        self.bot = bot

    @discord.ui.button(label="🎫 Ticket Paneli Kur", style=discord.ButtonStyle.primary, custom_id="kur_ticket")
    async def btn_ticket(self, interaction: discord.Interaction, button: Button):
        try:
            from cogs.ticket_modul import TicketPanel
            ticket_cog = self.bot.get_cog("TicketCog")
            
            if not ticket_cog:
                return await interaction.response.send_message("❌ Ticket modülü bulunamadı, dosya adını kontrol edin.", ephemeral=True)

            embed = discord.Embed(
                title="Destek",
                description="Destek talebi oluşturmak için aşağıdaki butona tıklayın.",
                color=0x2b2d31
            )
            embed.set_footer(text="Shadow Bot - Destek Sistemi")
            
            await interaction.channel.send(embed=embed, view=TicketPanel(ticket_cog))
            await interaction.response.send_message("✅ Ticket paneli bu kanala başarıyla kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Hata oluştu: {e}", ephemeral=True)

    @discord.ui.button(label="ℹ️ Bilgilendirme Paneli Kur", style=discord.ButtonStyle.secondary, custom_id="kur_bilgi")
    async def btn_bilgi(self, interaction: discord.Interaction, button: Button):
        try:
            from cogs.bilgilendirme_modul import BilgilendirmeView
            
            embed = discord.Embed(
                title="Bilgilendirme Merkezi",
                description=(
                    "Shadow Roleplay; kapsamlı bir RP deneyimi sunan; karakter gelişimi, entrika ve strateji odaklı bir RP sunucusudur. "
                    "Aşağıdaki butonları kullanarak;\n"
                    "- Detaylı bilgilendirme alabilir,\n"
                    "- Sık sorulan sorulara göz atabilir,\n"
                    "- Sunucunun hikayesini (lore) inceleyebilirsiniz."
                ),
                color=0x2b2d31
            )
            embed.set_footer(text="Shadow Roleplay • Bilgi Paneli")

            dosya_yolu = os.path.join("textures", "bilgilendirme.png")
            if os.path.exists(dosya_yolu):
                dosya = discord.File(dosya_yolu, filename="bilgilendirme.png")
                embed.set_image(url="attachment://bilgilendirme.png")
                await interaction.channel.send(file=dosya, embed=embed, view=BilgilendirmeView())
            else:
                await interaction.channel.send(embed=embed, view=BilgilendirmeView())
                
            await interaction.response.send_message("✅ Bilgilendirme paneli bu kanala başarıyla kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Hata oluştu: {e}", ephemeral=True)

    @discord.ui.button(label="📝 Başvuru Formları Kur", style=discord.ButtonStyle.success, custom_id="kur_forum")
    async def btn_forum(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True) 
        try:
            from cogs.forumlar_modul import forum_embedler_olustur, get_forum_data, save_forum_data
            
            veri = get_forum_data()
            embedler = forum_embedler_olustur(veri)
            
            dosya_yolu = os.path.join("textures", "forum.png")
            if os.path.exists(dosya_yolu):
                dosya = discord.File(dosya_yolu, filename="forum.png")
                gonderilen_mesaj = await interaction.channel.send(file=dosya, embeds=embedler)
            else:
                gonderilen_mesaj = await interaction.channel.send(embeds=embedler)
            
            veri["kanal_id"] = interaction.channel.id
            veri["mesaj_id"] = gonderilen_mesaj.id
            save_forum_data(veri)
            
            await interaction.followup.send("✅ Başvuru formları paneli bu kanala başarıyla kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Hata oluştu: {e}", ephemeral=True)

    @discord.ui.button(label="📞 İletişim Paneli Kur", style=discord.ButtonStyle.secondary, custom_id="kur_iletisim")
    async def btn_iletisim(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        try:
            from cogs.iletisim_modul import iletisim_embed_olustur, get_iletisim_data, save_iletisim_data
            
            veri = get_iletisim_data()
            embed = iletisim_embed_olustur(veri)
            
            dosya_yolu = os.path.join("textures", "iletisim.png")
            if os.path.exists(dosya_yolu):
                dosya = discord.File(dosya_yolu, filename="iletisim.png")
                gonderilen_mesaj = await interaction.channel.send(file=dosya, embed=embed)
            else:
                gonderilen_mesaj = await interaction.channel.send(embed=embed)
            
            veri["kanal_id"] = interaction.channel.id
            veri["mesaj_id"] = gonderilen_mesaj.id
            save_iletisim_data(veri)
            
            await interaction.followup.send("✅ İletişim paneli bu kanala başarıyla kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Hata oluştu: {e}\n*(İletişim modülündeki kodları kontrol edin)*", ephemeral=True)

    @discord.ui.button(label="📜 Kurallar Paneli Kur", style=discord.ButtonStyle.danger, custom_id="kur_kurallar")
    async def btn_kurallar(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        try:
            from cogs.kurallar_modul import ust_embed_olustur, kural_embed_olustur
            
            dosyalar = []
            eksik_dosyalar = []
            
            for dosya_adi in ["banner.png", "topluluk.png", "oyun.png"]:
                yol = os.path.join("textures", dosya_adi)
                if os.path.exists(yol):
                    dosyalar.append(discord.File(yol, filename=dosya_adi))
                else:
                    eksik_dosyalar.append(dosya_adi)
                    
            if eksik_dosyalar:
                return await interaction.followup.send(f"❌ Hata: `textures/` klasöründe şu dosyalar eksik: {', '.join(eksik_dosyalar)}", ephemeral=True)

            embed1 = ust_embed_olustur()
            embed2 = kural_embed_olustur("topluluk")
            embed3 = kural_embed_olustur("oyun")
            
            await interaction.followup.send("✅ Kurallar paneli kanala gönderiliyor...", ephemeral=True)

            dosya_banner = discord.File(os.path.join("textures", "banner.png"), filename="banner.png")
            dosya_topluluk = discord.File(os.path.join("textures", "oyun.png"), filename="oyun.png")

            await interaction.channel.send(files=[dosya_banner, dosya_topluluk], embeds=[embed1, embed2])

            dosya_oyun = discord.File(os.path.join("textures", "topluluk.png"), filename="topluluk.png")
            await interaction.channel.send(file=dosya_oyun, embed=embed3)

        except Exception as e:
            await interaction.followup.send(f"❌ Hata oluştu: {e}", ephemeral=True)

    @discord.ui.button(label="📖 Rol Terimleri Kur", style=discord.ButtonStyle.secondary, custom_id="kur_rolterimleri")
    async def btn_rolterimleri(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        try:
            uyari_metni = """⚠️   ```Sunucumuza girip rol yapmaya başlamadan önce mutlaka bu kanalı okumanız ve kuralları anlamanızı beklemekteyiz. Sunucuya girip rol yapmaya başladığınızda bu kuralları bildiğiniz ve okuduğunuz varsayılmaktadır.```   """
            docs_link = "https://docs.google.com/document/d/1jyY5_mfLW9jdPucGdslNwLY22TrHsCeGu0qkaG7vavI/edit?tab=t.0"

            terimler = """**OOC:** Rol dışı. Gerçek hayat konuşmaları ve rolü etkilemeyen şeyler.

**IC:** Rol içi. Karakterin yaptığı her şey.

**/me:** Karakterinin yaptığı hareketi yazarsın.
**Örnek:** /me kelepçeyi çıkarıp kişiyi kelepçeler.

**/do:** Ortamı anlatır veya soru sorar.
**Örnek:** /do Üzerinde ne var?

**//:** OOC mesaj atmak için kullanılır.

**Fail RP:** Mantıksız ve gerçekçi olmayan rol yapmak.

**Metagaming (MG):** Rol dışından öğrendiğin bilgiyi rolde kullanmak.

**Powergaming (PG):** Karakterinin yapamayacağı şeyleri yapması.

**Combat Log (CL):** Ceza, ölüm veya sorgudan kaçmak için oyundan çıkmak.

**Fear RP:** Korkulacak durumda karakterinin korkmasını oynamak.

**Pain RP:** Yaralandığında acıyı role yansıtmak.

**CK (Character Kill):** Karakterin kalıcı olarak ölmesi.

**NLR (New Life Rule):** Öldükten sonra eski hayatını ve yaşananları unutmak.

**IC-OOC Mixing:** Gerçek hayat ile rolü birbirine karıştırmak.

**RDM (Random Deathmatch):** Sebepsiz yere saldırmak veya öldürmek.

**Retarded RP:** Troll, aşırı saçma ve role uymayan davranışlar yapmak.

**Refuse RP:** Mantıklı sebep olmadan rolü reddetmek.

**Ghost RP:** IC'de gerçekleştirilmemiş bir olaya hayali bir durum veya eylem entegre ederek onu yaşanılmış ve gerçekleşmiş gibi göstermek.

**Shoot to Kill:** Rol yapmadan direkt çatışıp öldürmeye çalışmak.

**Shoot to Roleplay:** /me ve /do kullanarak yapılan, rol destekli çatışma.

**GOOA (Gun Out Of Ass):** Üzerinde olmadığı halde silah çıkarmak veya alınan silahı tekrar kullanmak.

**Revenge Kill (RK):** Seni öldüren kişiden yeniden doğduktan sonra intikam almaya çalışmak. NLR ihlalidir."""

            embed = discord.Embed(
                title="📖 Rol Terimleri",
                description=terimler,
                color=0x2b2d31
            )
            embed.set_footer(text="Shadow Roleplay • Rol Terimleri")

            uyari_embed = discord.Embed(
                description=f"{uyari_metni}\n\n**Detaylı Rol Terim Bilgisi için :** [Tıklayın]({docs_link})",
                color=0x2b2d31
            )

            dosya_yolu = os.path.join("textures", "rolterimleri.png")
            if os.path.exists(dosya_yolu):
                dosya = discord.File(dosya_yolu, filename="rolterimleri.png")
                embed.set_image(url="attachment://rolterimleri.png")
                await interaction.channel.send(embeds=[embed, uyari_embed], file=dosya)
            else:
                await interaction.channel.send(embeds=[embed, uyari_embed])
                
            await interaction.followup.send("✅ Rol Terimleri paneli bu kanala başarıyla kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Hata oluştu: {e}", ephemeral=True)

    @discord.ui.button(label="🌍 Sunucu Hakkında Kur", style=discord.ButtonStyle.primary, custom_id="kur_hakkinda")
    async def btn_hakkinda(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        try:
            hakkinda_metni = """## Vizyonumuz;
Roblox SCP:RP topluluğunda sadece çatışma odaklı olmayan, hikaye anlatımının ve karakter gelişiminin ön planda olduğu kaliteli bir rol ortamı sağlamak.

## Misyonumuz;
Oyuncularımıza adil, kurallara bağlı ve disiplinli bir yetkili kadro rehberliğinde sürdürülebilir bir roleplay tecrübesi sunmak. Tesis içerisindeki tüm departmanların gerçekçi bir işleyiş ile aktif çalıştığı, her oyuncunun emeğinin ve rolünün karşılığını aldığı bir düzen oluşturmak.

## Farkımız;
* Detaylı lore ve gerçekçilik: Sadece silah çekip ateş etmek veya etrafta aura kasmak değil. Departmanların evrak takibi, soruşturmalar, mahkemelerden protokol yönetimine kadar derinlemesine bir rol imkanı sunuyoruz.
* Yetkili Kadromuz: Yetkili kadromuz ve gamemaster ekibimiz, oyunculara güç gösterisi yapmak için değil, kaliteli rol paslamak ve düzeni sağlamak için görev yaparlar.
* Sürekli Gelişim: Oyuncu topluluğumuzun geri bildirimlerini dikkate alınarak sistemlerimizi ve haritamızı düzenli olarak güncelliyoruz.

**Bağlantılarımız:**
* <:Youtube:1546117775003623444> Youtube Hesabımız 👉 [Tıklayın](https://www.youtube.com/@ScpShadowRoleplay)
* <:instagram:1546117822164238458> İnstagram Hesabımız 👉 [Tıklayın](https://www.instagram.com/scpshadowroleplay)
* <:tiktok:1546117879894773842> Tiktok Hesabımız 👉 [Tıklayın](https://www.tiktok.com/@scpshadowroleplay)
* <:Roblox:1546118729560100864> Roblox Grubumuz 👉 [Tıklayın](https://www.roblox.com/tr/communities/35886894/Scp-Shadow-Roleplay#!/about)"""

            embed = discord.Embed(
                description=hakkinda_metni,
                color=0x2b2d31
            )
            embed.set_footer(text="Shadow Roleplay • Kurumsal & İletişim")

            dosya_yolu = os.path.join("textures", "hakkinda.png")
            if os.path.exists(dosya_yolu):
                dosya = discord.File(dosya_yolu, filename="hakkinda.png")
                await interaction.channel.send(embed=embed, file=dosya)
            else:
                await interaction.channel.send(embed=embed)
                
            await interaction.followup.send("✅ 'Sunucu Hakkında' paneli bu kanala başarıyla kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Hata oluştu: {e}", ephemeral=True)

    # --- KİŞİSEL KADRO (YETKİLİ + GELİŞTİRİCİ) KURULUM BUTONU ---
    @discord.ui.button(label="👔 Kişisel Kadro Kur", style=discord.ButtonStyle.success, custom_id="kur_kisisel")
    async def btn_kisisel(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        try:
            # Diğer dosyalardaki verileri çekmek için importlar
            from cogs.yetkili_ekip_modul import get_yetkili_data, yetkili_embed_olustur, save_yetkili_data
            from cogs.gelistirici_ekip_modul import get_gelistirici_data, gelistirici_embed_olustur, save_gelistirici_data
            
            yetkili_veri = get_yetkili_data()
            gelistirici_veri = get_gelistirici_data()
            
            # Üst üste duracak iki tablomuz
            yetkili_embed = yetkili_embed_olustur(yetkili_veri)
            yetkili_embed.description = ""  # Senin talebin üzerine açıklamayı sildik
            
            gelistirici_embed = gelistirici_embed_olustur(gelistirici_veri)
            gelistirici_embed.description = "" # Açıklama metnini sildik
            
            # En tepeye görseli ekliyoruz
            dosya_yolu = os.path.join("textures", "kisisel.png")
            if os.path.exists(dosya_yolu):
                dosya = discord.File(dosya_yolu, filename="kisisel.png")
                yetkili_embed.set_image(url="attachment://kisisel.png")
                gonderilen_mesaj = await interaction.channel.send(file=dosya, embeds=[yetkili_embed, gelistirici_embed])
            else:
                gonderilen_mesaj = await interaction.channel.send(embeds=[yetkili_embed, gelistirici_embed])
            
            # Sistemlerin güncellenebilmesi için kanal ve mesaj ID'lerini kendi JSON'larına kaydediyoruz
            yetkili_veri["kanal_id"] = interaction.channel.id
            yetkili_veri["mesaj_id"] = gonderilen_mesaj.id
            save_yetkili_data(yetkili_veri)
            
            gelistirici_veri["kanal_id"] = interaction.channel.id
            gelistirici_veri["mesaj_id"] = gonderilen_mesaj.id
            save_gelistirici_data(gelistirici_veri)
            
            await interaction.followup.send("✅ Kişisel Kadro paneli başarıyla bu kanala kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Hata oluştu: {e}", ephemeral=True)

    @discord.ui.button(label="🔔 Bildirim Rolleri Kur", style=discord.ButtonStyle.secondary, custom_id="kur_bildirim")
    async def btn_bildirim(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        try:
            from cogs.bildirim_rolleri_modul import save_bildirim_data

            metin = (
                "Aşağıdan sunucumuzdaki deneyiminizi özelleştirmek adına, neler için etiket almak istediğinizi "
                "seçebilirsiniz. Her rolün detaylı açıklaması ve aşağı bölümden nasıl alınacağı yazmaktadır.\n\n"
                "**@SSU Bildirim:** Sunucumuzda açılan SSU'ların (Server Start Up) ne zaman açılacağı veya "
                "açıldığını duyurmak için kullanılır.\n\n"
                "**@Güncelleme Bildirim:** Sunucumuza getirilen güncellemeleri sizlerle paylaşmak için kullanılır.\n\n"
                "**@Sneak Peak Bildirim:** Sunucumuzla ilgili **Sneak Peak**'leri, sizlerle paylaşmak için kullanılır.\n\n"
                "**@Etkinlik Bildirim:** Sunucumuzdaki etkinlikleri duyurmak için kullanılır.\n\n"
                "**@Sosyal Medya Bildirim:** Sunucumuzla bağlantılı sosyal medya paylaşımlarını duyurmak için kullanılır.\n\n"
                "**Mesajın altındaki emojilere tıklayarak, rollerinizi alabilirsiniz.**\n\n"
                "<:bir:1551003852612829285>  - SSU Bildirim\n"
                "<:iki:1551003890944835600>  - Güncelleme Bildirim\n"
                "<:uc:1551003931683856454>  - Sneak Peak Bildirim\n"
                "<:dort:1551003963157909504>  - Etkinlik Bildirim\n"
                "<:bes:1551003990588923974>  - Sosyal Medya Bildirim"
            )

            embed = discord.Embed(
                title="Bildirim Rolleri",
                description=metin,
                color=0x2b2d31
            )
            embed.set_footer(text="Shadow Roleplay • Tepki Rol Sistemi")

            # --- EMBED İÇİNE FOTOĞRAF EKLEME ---
            dosya_yolu = os.path.join("textures", "bildirim.png")

            if os.path.exists(dosya_yolu):
                dosya = discord.File(dosya_yolu, filename="bildirim.png")
                # Görseli embed kutusunun alt kısmında tam boy göstermek için set_image kullanıyoruz
                embed.set_image(url="attachment://bildirim.png")

                gonderilen_mesaj = await interaction.channel.send(embed=embed, file=dosya)
            else:
                gonderilen_mesaj = await interaction.channel.send(embed=embed)

            # Botun mesajın altına sırasıyla atacağı özel tepkiler
            emojiler = [
                "<:bir:1551003852612829285>",
                "<:iki:1551003890944835600>",
                "<:uc:1551003931683856454>",
                "<:dort:1551003963157909504>",
                "<:bes:1551003990588923974>"
            ]
            for emoji in emojiler:
                await gonderilen_mesaj.add_reaction(emoji)

            # Sistemi aktifleştirmek için mesaj ve kanal ID'sini veritabanına kaydet
            save_bildirim_data(interaction.channel.id, gonderilen_mesaj.id)

            await interaction.followup.send("✅ Bildirim Rolleri paneli fotoğraflı olarak kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Hata oluştu: {e}\n*(bildirim_rolleri_modul.py dosyasını kontrol edin)*", ephemeral=True)


class KurulumCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kurulum", description="Tüm modüllerin tek bir noktadan kurulmasını sağlayan merkezi menü.")
    async def ana_kurulum(self, interaction: discord.Interaction):
        kullanici_rolleri = [rol.id for rol in interaction.user.roles]
        if not any(rol in YETKILI_ROLLER for rol in kullanici_rolleri):
            return await interaction.response.send_message("❌ Bu komutu kullanmak için yetkiniz yok!", ephemeral=True)

        embed = discord.Embed(
            title="⚙️ Shadow Bot Kurulum Merkezi",
            description="Hangi sistemi **şu an bulunduğun kanala** kurmak istiyorsan aşağıdaki butonlardan seçebilirsin.\n\n*⚠️ Not: Kurulum butonlarına basmadan önce sistemin kurulmasını istediğin doğru kanalda olduğundan emin ol.*",
            color=0x2b2d31
        )
        embed.set_footer(text="Shadow Roleplay • Kurulum Menüsü")
        
        await interaction.response.send_message(embed=embed, view=KurulumMenusu(self.bot), ephemeral=True)

async def setup(bot):
    await bot.add_cog(KurulumCog(bot))
