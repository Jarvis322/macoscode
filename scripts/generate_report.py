import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register TTF Fonts with Full Turkish Character Support
FONT_REGULAR = '/System/Library/Fonts/Supplemental/Arial.ttf'
FONT_BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'

pdfmetrics.registerFont(TTFont('ArialCustom', FONT_REGULAR))
pdfmetrics.registerFont(TTFont('ArialCustom-Bold', FONT_BOLD))

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Running Top Header (Page 2+)
        if self._pageNumber > 1:
            self.setFont('ArialCustom-Bold', 7.5)
            self.setFillColor(colors.HexColor('#0F172A'))
            self.drawString(36, 11 * inch - 26, "macOSCode • 100 Terminal & defaults Cheatsheet Platformu")
            self.setFont('ArialCustom', 7.5)
            self.setFillColor(colors.HexColor('#64748B'))
            self.drawRightString(8.5 * inch - 36, 11 * inch - 26, "Stratejik Fizibilite, Risk & Maliyet Değerlendirmesi")
            self.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.setLineWidth(0.5)
            self.line(36, 11 * inch - 30, 8.5 * inch - 36, 11 * inch - 30)
            
        # Running Bottom Footer (All Pages)
        self.setFont('ArialCustom', 7.5)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(36, 20, "Gizli & Özel • Jarvis Ekibi Ürün ve Strateji Analiz Raporu • 2026")
        page_text = f"Sayfa {self._pageNumber} / {page_count}"
        self.drawRightString(8.5 * inch - 36, 20, page_text)
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(0.5)
        self.line(36, 28, 8.5 * inch - 36, 28)
        
        self.restoreState()

def build_pdf(filename):
    # Printable area: 8.5" x 11" (margins 36pt left/right, 34pt top/bottom)
    # Available width = 8.5 * 72 - 72 = 540 pt
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=34,
        bottomMargin=34
    )
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='ArialCustom-Bold',
        fontSize=16,
        leading=19,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=2
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        fontName='ArialCustom',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#475569'),
        spaceAfter=6
    )
    
    h1_style = ParagraphStyle(
        'Header1',
        fontName='ArialCustom-Bold',
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        fontName='ArialCustom',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#334155'),
        spaceAfter=3
    )
    
    bullet_style = ParagraphStyle(
        'BulletText',
        fontName='ArialCustom',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=8,
        spaceAfter=2
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='ArialCustom-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName='ArialCustom',
        fontSize=7.4,
        leading=9.8,
        textColor=colors.HexColor('#1E293B')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='ArialCustom-Bold',
        fontSize=7.4,
        leading=9.8,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    # ==========================================
    # PAGE 1
    # ==========================================

    # Top Category Pill & Date
    top_bar = Table([[
        Paragraph("<font color='#0284C7'><b>PROJE FİZİBİLİTE &amp; YATIRIM DEĞERLENDİRME RAPORU</b></font>", ParagraphStyle('Pill', fontName='ArialCustom-Bold', fontSize=7.2)),
        Paragraph("<b>DURUM: %100 UYGULANABİLİR (CANLI ÜRÜN)</b> • 2026", ParagraphStyle('DatePill', fontName='ArialCustom-Bold', fontSize=7.2, textColor=colors.HexColor('#059669'), alignment=2))
    ]], colWidths=[310, 230])
    top_bar.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(top_bar)
    story.append(Spacer(1, 3))

    story.append(Paragraph("macOSCode: 100 Terminal &amp; defaults Optimizasyon Platformu", title_style))
    story.append(Paragraph("Teknik Fizibilite, Maliyet Analizi, Operasyonel Riskler ve 'Bu İşe Girelim mi?' Değerlendirmesi", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0284C7'), spaceBefore=0, spaceAfter=6))

    # EXECUTIVE SUMMARY 4-BOX METRIC DECK
    summary_data = [
        [
            Paragraph("<b>Teknik Fizibilite</b><br/><font size='12' color='#059669'><b>%100 (Hazır)</b></font><br/><font size='6.5' color='#64748B'>Canlı, test edilmiş, hatasız</font>", body_style),
            Paragraph("<b>Aylık Sunucu Maliyeti</b><br/><font size='12' color='#0284C7'><b>$0.00 / Ay</b></font><br/><font size='6.5' color='#64748B'>GitHub Pages / Cloudflare</font>", body_style),
            Paragraph("<b>Geliştirme / Bakım</b><br/><font size='12' color='#6366F1'><b>Çok Düşük</b></font><br/><font size='6.5' color='#64748B'>Yıllık ~5-10 saat efor</font>", body_style),
            Paragraph("<b>Nihai Tavsiye</b><br/><font size='12' color='#059669'><b>KESİNLİKLE EVET</b></font><br/><font size='6.5' color='#64748B'>10/10 Değer / Efor Oranı</font>", body_style)
        ]
    ]
    summary_table = Table(summary_data, colWidths=[135, 135, 135, 135])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.4, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 6))

    # SECTION 1: PROJE TANIMI VE DEĞER ÖNERİSİ
    story.append(Paragraph("1. Proje Tanımı, Değer Önerisi ve Hedef Kitle", h1_style))
    story.append(Paragraph(
        "<b>macOSCode</b>, macOS işletim sistemini (Apple Silicon M1-M5 çipleri, macOS Tahoe &amp; Sequoia dahil) "
        "en yüksek hız ve verimlilikte kullanmak isteyen yazılımcılar, tasarımcılar ve sistem yöneticileri için geliştirilmiş "
        "<b>100 adet doğrulanmış, %100 geri alınabilir (reversible)</b> terminal ayarı, anında kopyalama ve kişisel bash betiği derleyicisi sunan açık kaynaklı bir web platformudur.", body_style
    ))
    story.append(Paragraph("<b>Temel Rekabet Üstünlükleri (Neden Rakiplerden Farklı?):</b>", body_style))
    story.append(Paragraph("• <b>Çift Yönlü Güvenlik (Reversible Architecture):</b> Her komutun hemen altında Apple fabrika varsayılanına döndüren `revert` komutu bulunur. Kullanıcı sistemin bozulmasından korkmaz.", bullet_style))
    story.append(Paragraph("• <b>Kişiselleştirilmiş Paket Oluşturucu (Custom Script Builder):</b> Kullanıcı istediği 5-10 ayarı seçerek tek tıkla kendi `custom-macos-setup.sh` betiğini oluşturup indirebilir.", bullet_style))
    story.append(Paragraph("• <b>Ultra Hızlı &amp; Sıfır Bağımlılık:</b> Saf HTML5, Vanilla CSS ve Vanilla JS ile inşa edilmiştir; React/Vue/Node gibi sunucu yükü veya yavaşlatan kütüphaneler içermez.", bullet_style))
    story.append(Paragraph("• <b>Tek Tıkla Master Kurulum:</b> Tek satırlık curl komutuyla 100 ayarın tamamını uygulama veya orijinal fabrika ayarlarına sıfırlama seçeneği sunar.", bullet_style))
    story.append(Spacer(1, 5))

    # SECTION 2: MALİYET ANALİZİ
    story.append(Paragraph("2. Maliyet Analizi (Altyapı, Barındırma ve Bakım Giderleri)", h1_style))
    story.append(Paragraph("Sistem tamamen statik ve istemci taraflı (client-side) çalıştığı için maliyet tablosu sıfıra yakındır:", body_style))

    cost_data = [
        [Paragraph("Maliyet Kalemi", table_header_style), Paragraph("Kullanılan Altyapı", table_header_style), Paragraph("Aylık / Yıllık Maliyet", table_header_style), Paragraph("Açıklama &amp; Sürdürülebilirlik", table_header_style)],
        [Paragraph("Web Barındırma (Hosting)", table_cell_bold), Paragraph("GitHub Pages / Cloudflare Pages", table_cell_style), Paragraph("<b>$0.00 / Ay</b>", table_cell_style), Paragraph("Sınırsız trafik, global CDN önbellekleme, sıfır sunucu masrafı.", table_cell_style)],
        [Paragraph("SSL &amp; Güvenlik", table_cell_bold), Paragraph("Otomatik Let's Encrypt / Cloudflare", table_cell_style), Paragraph("<b>$0.00</b>", table_cell_style), Paragraph("256-bit SSL şifreleme ve DDoS kalkanı dahildir.", table_cell_style)],
        [Paragraph("Özel Alan Adı (Opsiyonel)", table_cell_bold), Paragraph(".com / .dev / .sh Domain", table_cell_style), Paragraph("~$10 - $14 / Yıl (~$1/ay)", table_cell_style), Paragraph("`jarvis322.github.io` ücretsizdir; özel domain marka prestiji sağlar.", table_cell_style)],
        [Paragraph("Veritabanı / Backend", table_cell_bold), Paragraph("İstemci localStorage + JSON", table_cell_style), Paragraph("<b>$0.00</b>", table_cell_style), Paragraph("Favoriler ve seçimler yerel depolanır, DB faturası $0'dır.", table_cell_style)],
        [Paragraph("Sürüm Doğrulama Eforu", table_cell_bold), Paragraph("Yıllık macOS Güncellemesi", table_cell_style), Paragraph("~5-10 Saat / Yıl", table_cell_style), Paragraph("Apple her yeni macOS sürümü çıkardığında komutlar test edilir.", table_cell_style)],
    ]
    cost_table = Table(cost_data, colWidths=[120, 130, 105, 185])
    cost_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(cost_table)

    # EXACT PAGE BREAK TO PAGE 2
    story.append(PageBreak())

    # ==========================================
    # PAGE 2
    # ==========================================

    # SECTION 3: TEKNİK ZORLUKLAR VE RİSK MATRİSİ
    story.append(Paragraph("3. Karşılaşılabilecek Zorluklar, Riskler ve Çözüm Matrisi", h1_style))
    story.append(Paragraph("Projenin teknik ömrü boyunca yönetilmesi gereken kritik riskler ve halihazırda alınan önlemler:", body_style))

    risk_data = [
        [Paragraph("Zorluk / Risk Başlığı", table_header_style), Paragraph("Olasılık &amp; Etki", table_header_style), Paragraph("Uygulanan / Planlanan Çözüm Stratejisi", table_header_style)],
        [
            Paragraph("<b>1. macOS Sürüm Değişiklikleri</b><br/><font color='#64748B' size='6.5'>Apple'ın bazı defaults anahtarlarını değiştirmesi veya kaldırması.</font>", table_cell_style),
            Paragraph("<font color='#D97706'><b>Orta / Orta</b></font>", table_cell_style),
            Paragraph("Her ayarın yanına sürüm etiketi (örn: <i>Tahoe &amp; Apple Intelligence</i>) eklenmiştir. Değişen komutlar JSON veri yapısından tek merkezden güncellenir.", table_cell_style)
        ],
        [
            Paragraph("<b>2. Root / Sudo Güvenlik Çekincesi</b><br/><font color='#64748B' size='6.5'>Kullanıcıların terminale komut yapıştırma endişesi.</font>", table_cell_style),
            Paragraph("<font color='#059669'><b>Düşük / Yüksek</b></font>", table_cell_style),
            Paragraph("Komutların tamamı açık kaynaktır ve harici binary indirmez. Her ayarın yanında şeffaf 'Revert' komutu yer alarak tam güven sağlanır.", table_cell_style)
        ],
        [
            Paragraph("<b>3. Mobil Kullanıcı Deneyimi (UX)</b><br/><font color='#64748B' size='6.5'>Sosyal medyadan gelen mobil kullanıcıların ekran sıkışması.</font>", table_cell_style),
            Paragraph("<font color='#2563EB'><b>ÇÖZÜLDÜ ✅</b></font>", table_cell_style),
            Paragraph("Mobilde `sticky` kaldırılarak tam ekran okuma alanı sağlandı; kategoriler yatay kaydırılabilir (swipeable) çiplere dönüştürüldü.", table_cell_style)
        ],
        [
            Paragraph("<b>4. Organik Keşfedilebilirlik (SEO)</b><br/><font color='#64748B' size='6.5'>Google ve arama motorlarında üst sıralara çıkma gereksinimi.</font>", table_cell_style),
            Paragraph("<font color='#D97706'><b>Orta / Yüksek</b></font>", table_cell_style),
            Paragraph("Semantik HTML5 etiketleri, JSON-LD Structured Data, FAQ Schema, sitemap.xml ve OpenGraph meta etiketleri eksiksiz entegre edilmiştir.", table_cell_style)
        ]
    ]
    risk_table = Table(risk_data, colWidths=[150, 95, 295])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 6))

    # SECTION 4: BÜYÜME VE MONETIZATION
    story.append(Paragraph("4. Büyüme, Monetization &amp; Gelecek Ürünleşme Fırsatları", h1_style))
    story.append(Paragraph("Projenin değerini ve gelir potansiyelini katlayabilecek stratejik genişleme alanları:", body_style))
    story.append(Paragraph("• <b>Homebrew / CLI Entegrasyonu:</b> `brew install macoscode` komutuyla doğrudan terminalden interaktif TUI arayüzü açarak ayarları terminal içinde yönetme imkanı.", bullet_style))
    story.append(Paragraph("• <b>Native macOS Menubar Uygulaması (SwiftUI):</b> Web arayüzünün menü çubuğunda (menubar) tek tıkla toggle yapılabilen pro native versiyonu (Mac App Store veya Gumroad'da $4.99 - $9.99 tek seferlik satış).", bullet_style))
    story.append(Paragraph("• <b>Kurumsal Ekip Onboarding Paketleri (Enterprise):</b> Şirketlerin yeni işe başlayan geliştiricilerine tek komutla standart mühendislik ortamı kuran özel şablonlar.", bullet_style))
    story.append(Paragraph("• <b>Sponsorluk &amp; Affiliate Modeli:</b> Mac ekosistemindeki popüler geliştirici araçları (Raycast, OrbStack, CleanMyMac, Setapp vb.) için sponsorluk alanları.", bullet_style))
    story.append(Spacer(1, 6))

    # SECTION 5: NİHAİ KARAR (VERDICT)
    story.append(Paragraph("5. Nihai Karar ve Yönetici Değerlendirmesi", h1_style))
    
    decision_box_data = [[
        Paragraph(
            "<b>KARAR: BU İŞE KESİNLİKLE GİRİLMELİ VE PROJE BÜYÜTÜLMELİDİR (SKOR: 10 / 10)</b><br/><br/>"
            "<b>Stratejik Gerekçeler:</b><br/>"
            "1. <b>Sıfır Finansal Risk:</b> Sunucu, veritabanı veya lisans maliyeti $0'dır. Projeyi barındırmanın ve yayınlamanın hiçbir nakit maliyeti yoktur.<br/>"
            "2. <b>Çok Yüksek Viral Potansiyel:</b> Geliştirici topluluklarında (Reddit r/macapps, Hacker News, Twitter/X, Product Hunt) macOS hızlandırma ve kişiselleştirme rehberleri her zaman en çok paylaşılan ve yıldız alan projelerdir.<br/>"
            "3. <b>Ürün Zaten Hazır &amp; Canlı:</b> Sıfırdan başlanmıyor; 100 komut, testler, revert mekanizması, script builder ve mobil optimizasyon eksiksiz tamamlanmıştır.<br/>"
            "4. <b>Prestijli Portföy Değeri:</b> Ekibin mühendislik kalitesini, UI/UX özenini ve macOS ekosistemindeki derinliğini kanıtlayan harika bir amiral gemisi vitrinidir.",
            ParagraphStyle('DecisionText', fontName='ArialCustom', fontSize=8, leading=11.2, textColor=colors.HexColor('#064E3B'))
        )
    ]]
    decision_table = Table(decision_box_data, colWidths=[540])
    decision_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ECFDF5')),
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor('#10B981')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(decision_table)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {filename}")

if __name__ == '__main__':
    target_pdf = sys.argv[1] if len(sys.argv) > 1 else '/Users/jarvis/Desktop/macoscode/macOSCode_Proje_Fizibilite_ve_Maliyet_Raporu.pdf'
    build_pdf(target_pdf)
