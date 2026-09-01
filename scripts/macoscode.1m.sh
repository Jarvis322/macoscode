#!/usr/bin/env bash
# <swiftbar.name>macOSCode Quick Tweaks</swiftbar.name>
# <swiftbar.version>v2.0</swiftbar.version>
# <swiftbar.author>Jarvis322</swiftbar.author>
# <swiftbar.author.github>Jarvis322</swiftbar.author.github>
# <swiftbar.desc>Quick toggle macOS tweaks from your menu bar</swiftbar.desc>
# <swiftbar.dependencies>bash</swiftbar.dependencies>

echo "⚡"
echo "---"
echo "🚀 macOSCode Power Tweaks | href=https://jarvis322.github.io/macoscode/ font=bold"
echo "---"

# Hidden Files
SHOW_ALL=$(defaults read com.apple.finder AppleShowAllFiles 2>/dev/null)
if [ "$SHOW_ALL" = "1" ] || [ "$SHOW_ALL" = "true" ]; then
    echo "✓ Gizli Dosyaları Göster | bash='defaults delete com.apple.finder AppleShowAllFiles && killall Finder' terminal=false refresh=true"
else
    echo "✗ Gizli Dosyaları Göster | bash='defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder' terminal=false refresh=true"
fi

# Extensions
SHOW_EXT=$(defaults read NSGlobalDomain AppleShowAllExtensions 2>/dev/null)
if [ "$SHOW_EXT" = "1" ] || [ "$SHOW_EXT" = "true" ]; then
    echo "✓ Tüm Dosya Uzantılarını Göster | bash='defaults delete NSGlobalDomain AppleShowAllExtensions && killall Finder' terminal=false refresh=true"
else
    echo "✗ Tüm Dosya Uzantılarını Göster | bash='defaults write NSGlobalDomain AppleShowAllExtensions -bool true && killall Finder' terminal=false refresh=true"
fi

# Desktop Icons
SHOW_DESK=$(defaults read com.apple.finder CreateDesktop 2>/dev/null)
if [ "$SHOW_DESK" = "0" ] || [ "$SHOW_DESK" = "false" ]; then
    echo "✗ Masaüstü Simgelerini Göster | bash='defaults delete com.apple.finder CreateDesktop && killall Finder' terminal=false refresh=true"
else
    echo "✓ Masaüstü Simgelerini Göster | bash='defaults write com.apple.finder CreateDesktop -bool false && killall Finder' terminal=false refresh=true"
fi

# Reduce Motion
RED_MOT=$(defaults read com.apple.universalaccess reduceMotion 2>/dev/null)
if [ "$RED_MOT" = "1" ] || [ "$RED_MOT" = "true" ]; then
    echo "✓ Hareketi Azalt (Reduce Motion) | bash='defaults delete com.apple.universalaccess reduceMotion' terminal=false refresh=true"
else
    echo "✗ Hareketi Azalt (Reduce Motion) | bash='defaults write com.apple.universalaccess reduceMotion -bool true' terminal=false refresh=true"
fi

# Quick Look Text Selection
QL_TXT=$(defaults read com.apple.finder QLEnableTextSelection 2>/dev/null)
if [ "$QL_TXT" = "1" ] || [ "$QL_TXT" = "true" ]; then
    echo "✓ Quick Look Metin Seçimi | bash='defaults delete com.apple.finder QLEnableTextSelection && killall Finder' terminal=false refresh=true"
else
    echo "✗ Quick Look Metin Seçimi | bash='defaults write com.apple.finder QLEnableTextSelection -bool true && killall Finder' terminal=false refresh=true"
fi

echo "---"
echo "🧹 DNS Önbelleğini Temizle | bash='sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder' terminal=true refresh=true"
echo "🎛️ Terminal'de mc TUI Aç | bash='open -a Terminal' terminal=false"
echo "🌐 macOSCode Web Sitesini Aç | href=https://jarvis322.github.io/macoscode/"
