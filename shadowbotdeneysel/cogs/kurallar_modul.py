import discord
from discord.ext import commands

KURALLAR = {
    "topluluk": [
        {"baslik": "1. Saygı", "detay": "Herkes birbirine saygılı davranmakla yükümlüdür. Bazı zamanlar buranın bir rol yapma sunucusu olduğunu unutuyor ve bir hayatta kalma oyunuymuş gibi oynama hatasına düştüğümüz illa ki oluyor. Karakterlerimiz öldüğünde öfkelenmemeli, aksine beraber rol yaptığımız oyunculara yeni yollara kapı açmasına izin vermelisiniz. Bu sunucunun gelişmesi ve diğer kişilerinde iyiliği için yapabileceğiniz en iyi şeylerden biri olduğunu unutmamalısınız."},
        {"baslik": "2. Ayrımcılık yok.", "detay": "Irk, dil, din, cinsiyet, yönelim veya herhangi bir kişisel özellik üzerinden yapılan ayrımcı söylemler tolere edilmeyecektir, bu sunucunun iyileşmesi için en önemli adımlardan birisidir. Bu kural herkesin mutluluğu için vardır."},
        {"baslik": "3. RP ciddiyeti korunmalıdır.", "detay": "Rol Sırasında olan şeyleri OOC olarak, discord veya başka şeylere aktarabilirsiniz ancak bunları abartmadan yapmalısınız, metagaming'in yasak olduğunu unutmadan yazılarınızı diğer kişilerinde sinirlenemeyeceği şekilde yapmalısınız."},
        {"baslik": "4. Reklam yapmak yasaktır.", "detay": "Reklam ya da tanıtım içeren gönderiler paylaşmak yasaktır."},
        {"baslik": "5. Yetkililere saygı.", "detay": "Moderatör ve yöneticilerin uyarılarına uyulmalıdır. Kararlar genel düzeni sağlamak içindir, tartışma ortamı yaratmayın."},
        {"baslik": "6. Tartışmaları büyütmeyin.", "detay": "Kişisel problemleri genel kanallara taşımayın. Gerekirse yetkililere özelden iletin."},
        {"baslik": "7. Spam ve flood yasaktır.", "detay": "Gereksiz mesaj, emoji, link veya etiket spamı yapmayın."},
        {"baslik": "8. Uygunsuz içerik yasaktır.", "detay": "NSFW, rahatsız edici, yasa dışı veya Discord kurallarına aykırı şeyler paylaşmayın, bu sunucunun sadece bir rol sunucusu olduğunu unutmamalısınız."},
        {"baslik": "9. Sunucu huzuru önceliklidir.", "detay": "Ortamı bilerek germek, provoke etmek veya kaos yaratmak yasaktır."},
        {"baslik": "10. Kimseye tamamen güvenmemelisiniz.", "detay": "Yetkililer sizin kişisel bilgilerinizi istemez, istediği durumlarda bulunabilir ancak bunlar kullanıcı veya hesap şifreleri gibi özel bilgiler asla değildir, böyle durumları bildirmek size düşer, bu sayede topluluğumuzu düzeltebiliriz."},
        {"baslik": "11. Yetkili Personeller sizin isteklerinizi karşılamayabilir.", "detay": "Nasıl 'Saygı' adlı birincil topluluk kuralımızdada bahsettiğimiz gibi istedikleriniz olmayabilir, burasının bir rol sunucusu olduğunu unutup yaptığımız şeyleri görmezden gelebiliriz veya gerekenden kaçabiliriz. Anlık bir eğlence olarak düşündüğünüz şey aylarca süren bir ban'a kast olabilir, bu nedenle her yaptıklarınızın sonuçlarına katlanmaya hazır olun. Yetkili personeller istediklerinizi yapmayabilir bundan dolayı sinirlenmemeli ve sakin / açıklayıcı bir şekilde konuşmanız gerekir."},
        {"baslik": "12. Burası bir Rol Sunucusu", "detay": "Burası herkesin eğlenmek amacıyla geldiği bir rol sunucusu. İdeolojik veya parti değildir. Diğer sunucularla karşılaştırma yapıp özel/iyi gibi tanımlarda bulunmamalısınız. Bizde buraya eğlenmek amacıyla sizlere hizmet sunan bir kişiyiz, bu nedenle 1. Kuraldaki dendiği gibi, saygılı olun. Biz sizin arkadaşınız değiliz. Bu sizin burada yaptığınız anayasa ihlallerinden sunucu sorumlu değildir."},
        {"baslik": "13. Farklı Dil Kullanmak Mı? Hayır, Yasak.", "detay": "Farklı dil kullanmak yasaktır, burası her zaman türkçe bir sunucudur ve öyle kalacaktır. Languages other than Turkish are forbidden."},
        {"baslik": "14. Siyaset ile ilgili şeyler yasaktır.", "detay": "Sunucumuzda siyaset ile ilgili şeylerin paylaşımı, reklamı veya herhangi bir şeyi yasaktır."},
        {"baslik": "15. Yetkililer kural koyabilir.", "detay": "Sunucuda bulunan kişiler yetkililerin istedikleri şeyden veya olmayan kurallardan ceza verebileceğini bilmesi gerekir. Ek olarak bu konulardan şikayet açacaksanız kanıt olarak video gereklidir."},
        {"baslik": "16. Departman Hedef Gösterme", "detay": "OOC alanlarda herhangi bir departmanı aşağılamak, hedef göstermek veya üyeler arasında kutuplaşma yaratmak yasaktır."},
        {"baslik": "17. OOC Sohbetlerde Üslup (Uyarı Olmaksızın)", "detay": "Kanal durumunda küfür uyarısı bulunmayan ses kanallarında küfürlü konuşmak ve hakaret etmek kesinlikle yasaktır. Eğer istemeyerek yaptıysanız, bunu yetkililerin kararına bırakın."},
        {"baslik": "18. OOC Sohbetlerde Üslup (Uyarı Varken)", "detay": "Kanal durumunda uyarı varsa dozunda küfür serbesttir; ancak şahsa, dini veya milli değerlere küfür (ADK/DDK/MDK) doğrudan yasaklanma sebebidir."},
        {"baslik": "19. Kanal İsimlendirmeleri ve Durum Bilgileri", "detay": "Kanal isimleri makul olmalı, durum kısmı sadece uyarı amaçlı kullanılmalıdır. 'Yetkili giremez' gibi anlamsız ifadeler kullanmak yasaktır."},
        {"baslik": "20. Kişisel Verilerin Gizliliği", "detay": "Hiçbir üye; izinsiz şekilde kayıt alamaz, paylaşım yapamaz. A; Üyelerin kamera açma zorunluluğu yoktur. İzinsiz ekran görüntüsü veya kayıt alınamaz. B; Yayınlar yalnızca yayın sahibinin izni doğrultusunda paylaşılabilir. C; Sesli sohbetlerde alınan kayıtlar izinsiz şekilde kaydedilemez. İstisnai Durumlar; Sunucu düzenini korumak, kural ihlallerini tespit etmek amacıyla yapılan kayıtlar yalnızca yetkili ekibi ile paylaşılabilir."},
        {"baslik": "21. Genel Görgü Kuralı", "detay": "Bu sunucuda küfürlü konuşmalar, cinsel içerikli tartışmalar ve cinsellik/cinsel yönelim temalı sohbetler uygun değildir. Herkese açık yerlerde bu tür konuşmaların gerçekleştirilmemesi gerekmektedir."},
        {"baslik": "22. Bu sunucu Bu sunucudur.", "detay": "Bu sunucuda yaşanmamış ve başka sunucularda, geçmişte veya günümüzde yaşanmış şeyleri bu sunucuya taşımak ve bu olaylarda bir kişi/kişileri hedef göstererek dalga geçmek yasaktır."},
        {"baslik": "23. Bir kişiyi kopyalamak/taklit etmek yasaktır.", "detay": "Bu sunucudaki veya bu sunucuda olmayan bir kişinin ismini, profilini ve diğer şeylerini kopyalamak veya taklit etmek yasaktır."},
        {"baslik": "24. Kuralları bilmemek mazeret değildir.", "detay": "Sunucuda bulunan herkes bu kuralları okumuş ve kabul etmiş sayılır. Kuralları bilmiyorsanız yetkililer istisna olarak buna güvenebilir ancak bu durumun kesin olmadığını değiştirmez."}
    ],
    "oyun": [
        {"baslik": "1. Metagaming (MG)", "detay": "Karakterinin oyun içinde bilmemesi gereken bilgileri, oyun dışı kaynaklardan (Discord, yayın, başka oyuncular, OOC sohbetler vb.) öğrenip kullanmak yasaktır. Bu sunucu içerisinde yetkili personel tarafından MG yapıp yapmadığınız belirlenebilir, buna itiraz için \"Ticket\" veya diğer ismiyle \"Destek\" talebinde bulunabilirsiniz. Örnek: Discord’da konuşulan OOC bir bilgiyi karakterinin biliyormuş gibi davranması."},
        {"baslik": "2. Powergaming (PG)", "detay": "Karakterinin fiziksel, zihinsel veya çevresel sınırlarını aşan; karşı tarafa rol şansı tanımayan davranışlar yasaktır. Örnek: 190 Kilo civarı bir zırhı özel karakter izni olmadan taşımak."},
        {"baslik": "3. Non-RP Davranışlar", "detay": "Gerçekçi olmayan, evrene uymayan veya rol bütünlüğünü bozan hareketler yasaktır, bu kurala Özel Karakter izni verilmeden özel karakter izni açanlarıda kapsar, eğer özel karakterinizin olmadığı bir gücü uygularsanız \"PG\"ye girer. Örnek: Bir toplantıda ani bir şekilde arkaplan hikayesi olmadan delirip saldırıda bulunmak."},
        {"baslik": "4. Fail RP", "detay": "Karakterinin alacağı zararları, korkuyu, acıyı veya sonuçları yok saymak yasaktır. Örnek: Ağır yaralanmasına rağmen hiçbir etkilenme göstermeden koşmaya devam etmek."},
        {"baslik": "5. Aktif Rol İçerisinde OOC", "detay": "Aktif rol içerisinde OOC çıkmak yasaktır, bu aktif rol sadece yetkili personel isteği ile bozulabilir ve OOC izni verilebilir. Bu bittiğinde yetkili personelin \"OOC İnaktif\" gibi bir yazı yazması gerekir."},
        {"baslik": "6. Fear RP", "detay": "Karakter, tehdit, silah veya ölüm riski altındayken mantıklı şekilde korku ve hayatta kalma içgüdüsü göstermelidir."},
        {"baslik": "7. Random Deathmatch (RDM)", "detay": "Geçerli ve rol içi bir sebep olmadan oyunculara zarar vermek veya öldürmek yasaktır."},
        {"baslik": "8. Combat Quit", "detay": "Çatışma, kovalamaca veya aktif RP sırasında oyundan çıkmak yasaktır. Teknik bir sorun varsa yetkililere bildirilmelidir, bunların istisnası sadece yetkili personel tarafından yapılır ancak bunada güvenmeyin. Bu kuralı ihlal etmemek şansa atmamaktan en iyisidir."},
        {"baslik": "9. Gerçekçi Olmayan Eylemler", "detay": "Gerçek dünyada veya evrenin kendi kuralları içinde mantıklı olmayan davranışlar yasaktır. Rolünüzü yapmadan önce başkalarınında nasıl tepki vereceğini düşünmeniz önemlidir."},
        {"baslik": "10. RP’ye Saygı", "detay": "Diğer oyuncuların rolünü sabote etmek, bilerek bozmak veya ciddiyetini düşürmek yasaktır."},
        {"baslik": "11. Yetkili Kararları", "detay": "Yetkililerin RP sırasında veya sonrasında verdiği kararlar kesindir. İtirazlar RP bitiminden sonra yapılır, RP içerisinde sebepsiz bir şekilde OOC çıkmak yasaktır."}
    ]
}

def ust_embed_olustur():
    embed = discord.Embed(color=0x2b2d31)
    embed.set_image(url="attachment://banner.png")
    return embed

def kural_embed_olustur(kategori: str):
    kategori_adi = "Topluluk Kuralları" if kategori == "topluluk" else "Oyun Kuralları"
    embed = discord.Embed(title=f"Sunucu {kategori_adi}", color=0x2b2d31)

    ana_gorsel = "oyun.png" if kategori == "topluluk" else "topluluk.png"
    embed.set_image(url=f"attachment://{ana_gorsel}")

    secili_kurallar = KURALLAR[kategori]

    for kural in secili_kurallar:
        embed.add_field(name=kural["baslik"], value=kural["detay"][:1024], inline=False)

    if kategori == "oyun":
        embed.set_footer(text="Shadow Roleplay")

    return embed

class KurallarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(KurallarCog(bot))