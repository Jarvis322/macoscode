# 🚀 macOS 100 Power-User Tweaks & Interactive CLI Cheatsheet (2026)

[🇬🇧 English Documentation](README.md) • [🇹🇷 Türkçe Dokümantasyon](README_TR.md)

[![GitHub Pages](https://img.shields.io/badge/Canlı-Web%20Uygulaması-brightgreen?style=for-the-badge&logo=github)](https://jarvis322.github.io/macoscode/)
[![Interactive TUI](https://img.shields.io/badge/İnteraktif-TUI%20%2F%20CLI-purple?style=for-the-badge&logo=gnubash)](scripts/mc)
[![macOS Tahoe Ready](https://img.shields.io/badge/macOS-Tahoe%20%26%20Sequoia-blue?style=for-the-badge&logo=apple)](https://jarvis322.github.io/macoscode/)
[![License: MIT](https://img.shields.io/badge/Lisans-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/Jarvis322/macoscode?style=for-the-badge)](https://github.com/Jarvis322/macoscode/stargazers)

> **Web Uygulaması:** [https://jarvis322.github.io/macoscode/](https://jarvis322.github.io/macoscode/)  
> **Terminal CLI (İnteraktif TUI):** `curl -sSL https://raw.githubusercontent.com/Jarvis322/macoscode/main/scripts/mc | python3`

macOS sistem performansını, pencere yönetimini, Dock/Finder tepkiselliğini ve geliştirici deneyimini en üst seviyeye çıkaran **100 adet doğrulanmış `defaults write` ve Terminal optimizasyonu**.

Gelişmiş **İnteraktif Terminal Arayüzü (TUI/CLI)**, bağımsız tek tıkla **geri alma (revert)** desteği, tek satırlık **Master Setup/Reset** betikleri ve tarayıcıda çalışan **Kişiselleştirilmiş Betik Oluşturucu (Custom Script Builder)** içerir.

---

## ⚡ Hızlı Başlangıç

### 1. 🎛️ İnteraktif Terminal Arayüzü (TUI / CLI)

#### 🍺 Homebrew ile Kurulum:
```bash
brew tap Jarvis322/macoscode
brew install macoscode
```

#### ⚡ Veya Kurulum Yapmadan Anında Çalıştırın:
```bash
curl -sSL https://raw.githubusercontent.com/Jarvis322/macoscode/main/scripts/mc | python3
```

> **İpucu (Alternatif Tek Satırlık Yükleyici):**
> ```bash
> mkdir -p ~/.local/bin && curl -sSL https://raw.githubusercontent.com/Jarvis322/macoscode/main/scripts/mc -o ~/.local/bin/mc && cp ~/.local/bin/mc ~/.local/bin/macoscode && chmod +x ~/.local/bin/mc ~/.local/bin/macoscode
> ```

```bash
mc                     # İnteraktif TUI menüsünü açar
mc --apply-all         # Tüm 100 optimizasyonu tek satırda uygular
mc --revert-all        # Tüm ayarları orijinal fabrika varsayılanına döndürür
mc --status            # Sistemdeki ayarların aktiflik durumunu tarar (System Audit)
mc --preset dev        # Geliştirici optimizasyon paketini uygular (dev | speed | battery | tahoe)
mc --menubar           # Native macOS Menü Çubuğu (Menu Bar) hızlı aç/kapa aracını başlatır (⚡)
mc --search dock       # 'dock' ile ilgili ayarları terminalden arar
mc --lang tr           # Türkçe dilini seçer ve kalıcı yapar (en | tr)
mc --update            # macOSCode CLI aracını en son sürüme günceller
mc --dry-run           # Değişiklik yapmadan komutları önizler
```

---

### 2. ⚡ Native macOS Menü Çubuğu (Menu Bar) Hızlı Aç/Kapa Aracı
Günlük geliştirici ayarlarını (Gizli Dosyalar, Uzantılar, Masaüstü Simgeleri, Reduce Motion, Dock Hızı) doğrudan macOS menü çubuğundaki **⚡** simgesinden tikleyerek yönetmek isterseniz:

* **CLI ile Başlat:** `mc --menubar`
* **Doğrudan Swift ile Çalıştır:** `swift scripts/macoscode-menubar.swift &`
* **SwiftBar / xbar Eklentisi:** `scripts/macoscode.1m.sh` dosyasını SwiftBar eklenti klasörünüze kopyalayın.

---

### 2. Tek Satırlık Hızlı Kurulum & Sıfırlama Betikleri

#### 🚀 Tüm 100 Ayarı Tek Seferde Uygula (Master Setup)
```bash
curl -sSL https://raw.githubusercontent.com/Jarvis322/macoscode/main/scripts/macos-power-setup.sh | bash
```

#### ⏪ Yapılan Tüm Ayarları Orijinal Fabrika Varsayılanına Döndür (Master Reset)
```bash
curl -sSL https://raw.githubusercontent.com/Jarvis322/macoscode/main/scripts/macos-power-revert.sh | bash
```

---

## ✨ Öne Çıkan Özellikler

- 🎛️ **İnteraktif CLI (`mc`):** Terminal üzerinden ok tuşlarıyla gezinme, Space ile toggle, Audit durum raporu ve canlı arama.
- 🚀 **100 İleri Düzey İnce Ayar:** Terminal, Finder, Dock, Klavye/Trackpad, Xcode, Safari, Gizlilik ve Tahoe optimizasyonları.
- 🔐 **Touch ID ile Sudo Onayı:** Terminalde şifre yazma zorunluluğunu kaldırıp parmak iziyle anında yetkilendirme.
- 🏔️ **macOS Tahoe & Apple Intelligence:** Writing Tools gecikme sıfırlama, yerel Spotlight önceliği, iPhone Mirroring bildirim gruplama.
- 📦 **Kişiselleştirilmiş Betik Oluşturucu:** İstediğiniz ayarları seçip tek tıkla özel `custom-macos-setup.sh` (kurulum) ve `custom-macos-revert.sh` (geri alma) betiklerini indirme/kopyalama. Satır içi revert yorumları içerir.
- ⭐ **Favoriler Sistemi:** En sık kullandığınız komutları yerel depolamada saklama.
- 🔍 **Canlı Arama & Akıllı Filtreleme:** `⌘ + K` veya `/` ile anında komut arama ve mobilde yer kaplamayan katlanabilir filtreler.
- 🌐 **Tam İki Dilli Destek:** Web Uygulaması, CLI ve dokümantasyonda anında Türkçe ⟷ İngilizce geçişi.
- 🎨 **Ultra-Premium Glassmorphism:** Apple Tahoe esintili modern koyu tema ve akıcı animasyonlar.

---

## 📂 Kategoriler

1. **💻 Terminal & Kabuk:** Hostname sabitleme, zsh yorum desteği, Touch ID sudo yetkisi, Homebrew telemetri kapatma.
2. **📁 Finder & Dosya Yönetimi:** Tüm dosya uzantılarını gösterme, gizli dosyaları açma, `.DS_Store` engelleme, POSIX başlık yolu, Quick Look metin seçimi.
3. **🪟 Pencere, Masaüstü & Dock:** Sıfır Dock gecikmesi, Suck küçülme efekti, Mission Control gruplama, döşeme kenarlık boşluklarını kaldırma.
4. **⌨️ Klavye, Trackpad & Donanım:** Maksimum tuş tekrar hızı, aksan gecikmesini kaldırma, dokunarak tıklama, 3 parmakla sürükleme.
5. **⚡ Geliştirici, Güvenlik & Sistem:** Xcode build süresi, Safari develop menüsü, açılış gong sesini susturma, JPG ekran görüntüleri, karantina onayını kapatma.
6. **🏔️ macOS Tahoe & AI:** Snap döşeme önizleme hızlandırma, Stage Manager akıcı geçiş, menü çubuğu simge sıkıştırma, Game Mode optimizasyonu.
7. **🔋 Ağ, Güç & Bakım:** Düşük ping Wi-Fi, clamshell uykuyu engelleme, DNS flush, hızlı hibernation, %80 pil koruma tetikleme.

---

## 🛠️ Yerel Çalıştırma

Projeyi yerel ortamınızda görüntülemek için:

```bash
git clone https://github.com/Jarvis322/macoscode.git
cd macoscode
open index.html
```

veya basit bir HTTP sunucusu ile:

```bash
npx serve .
# veya
python3 -m http.server 8000
```

---

## 📄 Lisans

Bu proje [MIT](LICENSE) lisansı altında sunulmaktadır.
Dilediğiniz gibi kullanabilir, özelleştirebilir ve paylaşabilirsiniz.
