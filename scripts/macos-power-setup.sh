#!/usr/bin/env bash
# ==============================================================================
# 🚀 macOS Ultimate Power-User Setup Script (2026 - Tahoe / Golden Gate Ready)
# Repository: https://github.com/Jarvis322/macoscode
# Web App: https://jarvis322.github.io/macoscode/
# ==============================================================================

set -e

echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║          🚀 macOS 100 Power-User Tweaks & Terminal Optimizer         ║"
echo "║             Tahoe, Sequoia & Golden Gate Ready (2026)                ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Admin yetkisi kontrolü
sudo -v
while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &

echo "⚡ [1/7] Terminal, Zsh ve Kabuk Optimizasyonları Yapılandırılıyor..."
grep -q "setopt INTERACTIVE_COMMENTS" ~/.zshrc 2>/dev/null || echo "setopt INTERACTIVE_COMMENTS" >> ~/.zshrc
defaults write com.apple.Terminal ShowRepresentedURLInTitle -bool false
brew analytics off 2>/dev/null || true
grep -q "HOMEBREW_NO_ANALYTICS" ~/.zprofile 2>/dev/null || echo "export HOMEBREW_NO_ANALYTICS=1" >> ~/.zprofile
if [ -f /etc/pam.d/sudo_local.template ]; then
  sudo sed -e 's/^#auth/auth/' /etc/pam.d/sudo_local.template | sudo tee /etc/pam.d/sudo_local >/dev/null
elif ! grep -q "pam_tid.so" /etc/pam.d/sudo 2>/dev/null; then
  sudo sed -i '' '1s;^;auth       sufficient     pam_tid.so\n;' /etc/pam.d/sudo 2>/dev/null || true
fi

echo "📁 [2/7] Finder ve Gelişmiş Dosya Yönetimi Ayarları Yapılıyor..."
defaults write NSGlobalDomain AppleShowAllExtensions -bool true
defaults write com.apple.finder AppleShowAllFiles -bool true
defaults write com.apple.finder ShowPathbar -bool true
defaults write com.apple.finder ShowStatusBar -bool true
defaults write com.apple.finder NewWindowTarget -string "PfHm"
defaults write com.apple.finder NewWindowTargetPath -string "file://$HOME/"
defaults write com.apple.finder FXDefaultSearchScope -string "SCcf"
defaults write com.apple.finder _FXShowPosixPathInTitle -bool true
defaults write com.apple.finder QLEnableTextSelection -bool true
defaults write com.apple.finder WarnOnEmptyTrash -bool false
defaults write com.apple.finder FXEnableExtensionChangeWarning -bool false
defaults write com.apple.finder FXPreferredViewStyle -string "clmv"
defaults write com.apple.finder AutoExpandSyncFolders -bool true
defaults write com.apple.finder FXEnableRemoveWithoutTrash -bool true
defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true
defaults write com.apple.desktopservices DSDontWriteUSBStores -bool true
defaults write com.apple.NetworkBrowser DisableAirDrop -bool false
defaults write com.apple.NetworkBrowser BrowseAllInterfaces -bool true
defaults write -g QLPanelAnimationDuration -float 0
chflags nohidden ~/Library 2>/dev/null || true
sudo chflags nohidden /Volumes 2>/dev/null || true

echo "🪟 [3/7] Pencereler, Masaüstü ve Dock Ayarları Yapılandırılıyor..."
defaults write com.apple.WindowManager EnableTopDragToRestore -bool true
defaults write com.apple.WindowManager ClickWidgetBackgroundInStageManager -bool true
defaults write com.apple.WindowManager EnableTiledWindowMargins -bool false
defaults write -g NSWindowShouldDragOnGesture -bool true
defaults write com.apple.dock autohide-delay -float 0
defaults write com.apple.dock autohide-time-modifier -float 0.3
defaults write com.apple.dock showhidden -bool true
defaults write com.apple.dock show-recents -bool false
defaults write com.apple.dock expose-group-apps -bool true
defaults write com.apple.dock expose-animation-duration -float 0.1
defaults write com.apple.dock mru-spaces -bool false
defaults write NSGlobalDomain NSWindowResizeTime -float 0.001
defaults write NSGlobalDomain AppleActionOnDoubleClick -string "Fill"
defaults write com.apple.dock wvous-br-corner -int 0
defaults write com.apple.dock mineffect -string "suck"

echo "⌨️ [4/7] Klavye, Trackpad ve Donanım Girdileri Hızlandırılıyor..."
defaults write NSGlobalDomain KeyRepeat -int 1
defaults write NSGlobalDomain InitialKeyRepeat -int 10
defaults write NSGlobalDomain ApplePressAndHoldEnabled -bool false
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad Clicking -bool true
defaults write com.apple.AppleMultitouchTrackpad Clicking -bool true
defaults -currentHost write NSGlobalDomain com.apple.mouse.tapBehavior -int 1 2>/dev/null || true
defaults write com.apple.AppleMultitouchTrackpad TrackpadThreeFingerDrag -bool true
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad TrackpadThreeFingerDrag -bool true
defaults write NSGlobalDomain NSAutomaticPeriodSubstitutionEnabled -bool false
defaults write NSGlobalDomain NSAutomaticCapitalizationEnabled -bool false
defaults write NSGlobalDomain NSAutomaticSpellingCorrectionEnabled -bool false
defaults write NSGlobalDomain NSAutomaticQuoteSubstitutionEnabled -bool false
defaults write NSGlobalDomain NSAutomaticDashSubstitutionEnabled -bool false
defaults write NSGlobalDomain AppleKeyboardUIMode -int 3
defaults write NSGlobalDomain "com.apple.sound.beep.feedback" -int 0
defaults write com.apple.helpviewer DevMode -bool true
defaults write com.apple.BezelServices kDimTime -int 10 2>/dev/null || true

echo "⚡ [5/7] Geliştirici, Güvenlik ve Sistem İnce Ayarları..."
defaults write com.apple.dt.Xcode ShowBuildOperationDuration -bool true
defaults write com.apple.LaunchServices LSQuarantine -bool false
defaults write com.apple.Safari IncludeDevelopMenu -bool true
defaults write com.apple.Safari WebKitDeveloperExtrasEnabledPreferenceKey -bool true
defaults write com.apple.Safari com.apple.Safari.ContentPageGroupIdentifier.WebKit2DeveloperExtrasEnabled -bool true
defaults write com.apple.Safari ShowFullURLInSmartSearchField -bool true
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode -bool true
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode2 -bool true
defaults write NSGlobalDomain PMPrintingExpandedStateForPrint -bool true
defaults write NSGlobalDomain PMPrintingExpandedStateForPrint2 -bool true
defaults write com.apple.CrashReporter DialogType -string "none"
defaults write com.apple.BluetoothAudioAgent "Apple Bitpool Min (editable)" -int 40
defaults write com.apple.screensaver askForPassword -int 1
defaults write com.apple.screensaver askForPasswordDelay -int 0
defaults write com.apple.screencapture type -string "jpg"
defaults write com.apple.screencapture disable-shadow -bool true
mkdir -p ~/Pictures/Screenshots
defaults write com.apple.screencapture location ~/Pictures/Screenshots
defaults write com.apple.notificationcenterui dndDisplayNotifications -bool false

echo "🏔️ [6/7] macOS Tahoe & Apple Intelligence Optimizasyonları..."
defaults write com.apple.WindowManager TilingWindowPreviewDelay -float 0
defaults write com.apple.WindowManager ShowTilingSnapDividers -bool false
defaults write com.apple.ScreenContinuity AutoGroupPhoneNotifications -bool true
defaults write com.apple.ScreenContinuity MirrorDoNotDisturbState -bool true
defaults write NSGlobalDomain WritingToolsShowDelay -float 0
defaults write com.apple.Spotlight DirectMathEvaluation -bool true
defaults write com.apple.Spotlight LookupServerDisableRemoteQueries -bool true
defaults -currentHost write -globalDomain NSStatusItemSpacing -int 6 2>/dev/null || true
defaults -currentHost write -globalDomain NSStatusItemSelectionPadding -int 4 2>/dev/null || true
defaults write com.apple.Passwords AutoFillDisplayDelay -float 0
defaults write com.apple.Passwords EnableFastTouchIDAuthentication -bool true
defaults write com.apple.backgroundtaskmanagement SuppressServiceAlerts -bool true
defaults write com.apple.WindowManager AppSwitcherAnimationDuration -float 0.1
defaults write com.apple.gameoverlay EnableGameModeAutoBoost -bool true
defaults write com.apple.WindowManager AutoRestoreStageLayout -bool true

echo "🔄 [7/7] Sistem Servisleri Yeniden Başlatılıyor..."
killall Finder 2>/dev/null || true
killall Dock 2>/dev/null || true
killall WindowManager 2>/dev/null || true
killall SystemUIServer 2>/dev/null || true
killall Spotlight 2>/dev/null || true

echo ""
echo "✨ Tebrikler! 100 power-user macOS optimizasyonu başarıyla tamamlandı."
echo "💡 İpucu: Bazı değişikliklerin tam olarak aktif olması için oturumu kapatıp açabilir veya bilgisayarı yeniden başlatabilirsiniz."
echo ""
