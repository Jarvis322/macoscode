# 🚀 macOS 100 Power-User Tweaks & Terminal Cheatsheet (2026)

[![GitHub Pages](https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge&logo=github)](https://jarvis322.github.io/macoscode/)
[![macOS Tahoe Ready](https://img.shields.io/badge/macOS-Tahoe%20%26%20Sequoia-blue?style=for-the-badge&logo=apple)](https://jarvis322.github.io/macoscode/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/Jarvis322/macoscode?style=for-the-badge)](https://github.com/Jarvis322/macoscode/stargazers)

> **Canlı Web Uygulaması:** [https://jarvis322.github.io/macoscode/](https://jarvis322.github.io/macoscode/)

macOS sistem performansını, pencere yönetimini, Dock/Finder tepkiselliğini ve geliştirici deneyimini en üst seviyeye çıkaran **100 adet doğrulanmış `defaults write` ve Terminal optimizasyonu**.

Her bir ayar için **bağımsız tek tıkla geri alma (revert)** desteği, tek satırlık **Master Setup/Reset** betikleri ve tarayıcıda çalışan **Kişiselleştirilmiş Betik Oluşturucu (Custom Script Builder)** içerir.

---

## ⚡ Hızlı Başlangıç (Tek Satır Kurulum)

### 1. Tüm 100 Ayarı Tek Seferde Uygula (Master Setup)
```bash
curl -sSL https://raw.githubusercontent.com/Jarvis322/macoscode/main/scripts/macos-power-setup.sh | bash
```

### 2. Yapılan Tüm Ayarları Orijinal Fabrika Varsayılanına Döndür (Master Reset)
```bash
curl -sSL https://raw.githubusercontent.com/Jarvis322/macoscode/main/scripts/macos-power-revert.sh | bash
```

---

## ✨ Öne Çıkan Özellikler

- 🚀 **100 İleri Düzey İnce Ayar:** Terminal, Finder, Dock, Klavye/Trackpad, Xcode, Safari, Gizlilik ve Tahoe optimizasyonları.
- 🔐 **Touch ID ile Sudo Onayı:** Terminalde şifre yazma zorunluluğunu kaldırıp parmak iziyle anında yetkilendirme.
- 🏔️ **macOS Tahoe & Apple Intelligence:** Writing Tools gecikme sıfırlama, yerel Spotlight önceliği, iPhone Mirroring bildirim gruplama.
- 📦 **Kişiselleştirilmiş Betik Oluşturucu:** İstediğiniz ayarları seçip tek tıkla özel `custom-macos-setup.sh` indirme/kopyalama.
- ⭐ **Favoriler Sistemi:** En sık kullandığınız komutları yerel depolamada saklama.
- 🔍 **Canlı Arama & Filtreleme:** `⌘ + K` veya `/` ile anında komut arama ve etiket filtreleme.
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
