import os
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button

YETKILI_ROLLER = [1483443654772396093 , 1494377287666368602 , 1494377031432147055 ]

LORE_METNI = """
14 Ocak 1979 tarihinde Tesis-17'de bulunan ağır muhafaza kanadında bir **"bakım sabotajı"** gerçekleşti. Vakıf olayın şokunu atlatmaya çalışırken iş işten çoktan geçmişti. Kan dolu İGD sorguları, başarısız ve geç intikal eden kombatif ekipler... Var olan her şey sanki vakfın aleyhine işler gibiydi. 

Tesis-17 sonuç olarak dayanamadı ve onlarca tehlikeli insansı SCP, Amerika'nın **[VERİ ÇIKARTILDI]** kasabasına doğru ilerledi. Tesis-17, kendisinden sonra geleceklere çok büyük bir ders verdi: **Gölgenin Önemi.**

Vakıf karasal tesislerin başarısız olduğunu kabullendi ve onlarca farklı BM ülkesinin arasında ezildi. Sonuç olarak vakfın karasal tesisler çağı sona erdi. Artık her şey Pasifik Okyanusu'nun ücra bir köşesindeki yapay adalar olan **Proje: Tesis Shadow** adalarına taşınacaktı...
"""

class BilgilendirmeView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Detaylı Bilgilendirme", style=discord.ButtonStyle.primary, custom_id="btn_bilgi_detay")
    async def btn_detay(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="Tesis Departmanları ve Görevleri",
            description="Tesis bünyesinde faaliyet gösteren departmanlar ve sorumlulukları aşağıda belirtilmiştir:\n",
            color=0x2b2d31
        )

        embed.add_field(
            name="Güvenlik Departmanı",
            value="Tesisimizdeki asayişi ve işleyişi sağlamakla görevlidir. Noktalarda nöbet tutarlar ve kart kontrolü yaparlar. Gerekli zamanlarda alt birimlerinden yardım alarak isyan bastırabilir veya değişkenlik gösteren olaylara müdahale ederler. Tesisin ana direğidir.",
            inline=False
        )
        embed.add_field(
            name="Tıbbi Departmanı",
            value="Tesis işleyişinde yaralıları veya sağlık açısından bakım gerektiren operasyonları ve işlemleri gerçekleştirirler. Tıbbi departman kendi içinde uzmanlıklara ayrılır. Revirlerde nöbet tutarlar ve operasyonlar gerçekleştirirler.",
            inline=False
        )
        embed.add_field(
            name="Araştırma Departmanı",
            value="Tesisteki araştırma ve geliştirme organını gerçekleştirme ile yükümlüdürler. Bunu gerçekleştirmek için D Class personel kullanabilirler. Deneyler gerçekleştirirler ve D Class'ları kullanarak amaçlarına ulaşmayı denerler.",
            inline=False
        )
        embed.add_field(
            name="Yönetim Departmanı",
            value="Tesis içerisindeki operasyonları, faaliyetlerin işleyişini ve departmanlar arası iletişimsizliği denetler. Tesisin yönetim organıdır. Operasyonlarda komutada bulunurlar ve olay yerini kontrol ederler.",
            inline=False
        )
        embed.add_field(
            name="Genel Servis Departmanı",
            value="Tesis içerisinde kaba işçilik gücü gerektiren işleri üstlenirler, genel olarak hademe ve aşçılık olarak ayrılır. Tesisin temizliğinden ve personelin morallerinden sorumludurlar.",
            inline=False
        )
        embed.add_field(
            name="Delta - 43 | Shadow Wardens",
            value="Tesisimizde bulunan operasyonların güvenliğini sağlamakla yükümlüdürler. Bir ihlal durumunda ilk yumruğu atanlardır ve ani bir şekilde cevap verirler.",
            inline=False
        )
        embed.add_field(
            name="İç Güvenlik Departmanı",
            value="Tesis içindeki güvenliği arka plandan sağlamakla yükümlüdürler. Operasyonlarını gizliden yürütürler ve tesis prosedürlerini uygulamakla yükümlüdürler.",
            inline=False
        )
        embed.add_field(
            name="Etik Komite",
            value="Tesis içerisindeki faaliyetlerin Etik kurallara ve prosedürlerine uygun olup olmadığını denetlerler, eğer bir ihlal görürler ise etik mahkemede yargılatma yetkileri bulunur. Araştırma departmanı ile birlikte deneylere katılırlar ve Etik Kodu uygulamakla yükümlüdürler. Sadece Seviye 2 Sivil personeller bu departmana katılabilir.",
            inline=False
        )
        embed.set_footer(text="Shadow Roleplay • Departman Bilgilendirme Dosyası")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Sık Sorulan Sorular", style=discord.ButtonStyle.secondary, custom_id="btn_bilgi_sss")
    async def btn_sss(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="Sık Sorulan Sorular (S.S.S.)",
            description="Sunucumuz ve işleyişimiz hakkında merak edilen soruların yanıtları aşağıdadır:\n",
            color=0x2b2d31
        )

        embed.add_field(
            name="Sunucumuzun konsepti nedir?",
            value="Sunucumuz, SCP evrenini temel alan bir rol yapma topluluğudur. Kendi özgün hikayelerimizi ve karakterlerimizi oluştururken SCP evrenine ve atmosferine uygun şekilde ilerlemeye özen gösteriyoruz. Kısacası, rol ortamımız SCP evreni içerisinde geçer ve olaylar SCP temeli alınarak şekillenir.",
            inline=False
        )
        embed.add_field(
            name="Rollerimizi hangi platform veya oyun üzerinde gerçekleştiriyoruz?",
            value="Rollerimizi, Roblox platformunda bulunan SCP:Roleplay oyunu üzerinde gerçekleştirmekteyiz.\n\nBaglantı: https://www.roblox.com/tr/games/5041144419/SCP-Roleplay",
            inline=False
        )
        embed.add_field(
            name="Sunucuya nasıl giriş yaparım?",
            value="Belirlenen SSU saatlerinde sunucumuz custom server listesinde açık olarak gözükmektedir. Oyuna girdiğinizde ana menü üzerinden sol taraftaki servers bölümüne girip sol üstteki custom filtresini seçerek sunucumuzu bulabilir ve giriş yapabilirsiniz.",
            inline=False
        )
        embed.add_field(
            name="SSU nedir, sunucumuz ne zaman açılıyor?",
            value="SSU (Server Start Up), sunucunun açılacağı ve rollerin başlayacağı anı ifade eder. Çarşamba, cuma, cumartesi ve pazar günleri saat 20.00 civarında verilir. <#1461103921178218732> kanalından bir gün önce oylama başlatılır ve yeterli sayıya ulaşılması beklenir.",
            inline=False
        )
        embed.add_field(
            name="Sunucuya yeni geldim ve kafam karıştı. Ne yapmalıyım?",
            value="Temel işleyiş bu bilgilendirme alanındadır. Anlaşılmayan durumlarda genel sohbetten oyunculara danışabilir veya <#1461104282349736016> kanalından destek talebi (ticket) açabilirsiniz.",
            inline=False
        )

        embed.set_footer(text="Shadow Roleplay • S.S.S. Kılavuzu")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Sunucu Lore'u", style=discord.ButtonStyle.success, custom_id="btn_bilgi_lore")
    async def btn_lore(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="Proje: Tesis Shadow • Sunucu Evreni (Lore)",
            description=LORE_METNI,
            color=0x2b2d31
        )
        embed.set_footer(text="Shadow Roleplay • Gizlilik Seviyesi: Sınıflandırılmış")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class BilgilendirmeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(BilgilendirmeView())



async def setup(bot):
    await bot.add_cog(BilgilendirmeCog(bot))
