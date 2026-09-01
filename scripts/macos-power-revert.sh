#!/usr/bin/env bash
# ==============================================================================
# ⏪ macOS Ultimate Master Revert / Factory Reset Script
# Repository: https://github.com/Jarvis322/macoscode
# Web App: https://jarvis322.github.io/macoscode/
# ==============================================================================

set -e

echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║          ⏪ macOS Master Revert & Factory Reset Script               ║"
echo "║          Yapılan tüm 'defaults write' ayarlarını sıfırlar            ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Admin yetkisi kontrolü
sudo -v
while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &

echo "⚡ [1/7] Sudo Touch ID ve Kabuk Ayarları Sıfırlanıyor..."
sudo rm -f /etc/pam.d/sudo_local 2>/dev/null || true
sudo sed -i '' '/pam_tid.so/d' /etc/pam.d/sudo 2>/dev/null || true
sed -i '' '/setopt INTERACTIVE_COMMENTS/d' ~/.zshrc 2>/dev/null || true
brew analytics on 2>/dev/null || true
sed -i '' '/HOMEBREW_NO_ANALYTICS/d' ~/.zprofile 2>/dev/null || true
defaults delete com.apple.Terminal ShowRepresentedURLInTitle 2>/dev/null || true

echo "📁 [2/7] Finder ve Dosya Ayarları Orijinal Durumuna Döndürülüyor..."
defaults delete NSGlobalDomain AppleShowAllExtensions 2>/dev/null || true
defaults delete com.apple.finder AppleShowAllFiles 2>/dev/null || true
defaults delete com.apple.finder ShowPathbar 2>/dev/null || true
defaults delete com.apple.finder ShowStatusBar 2>/dev/null || true
defaults delete com.apple.finder NewWindowTarget 2>/dev/null || true
defaults delete com.apple.finder NewWindowTargetPath 2>/dev/null || true
defaults delete com.apple.finder FXDefaultSearchScope 2>/dev/null || true
defaults delete com.apple.finder _FXShowPosixPathInTitle 2>/dev/null || true
defaults delete com.apple.finder QLEnableTextSelection 2>/dev/null || true
defaults delete com.apple.finder WarnOnEmptyTrash 2>/dev/null || true
defaults delete com.apple.finder FXEnableExtensionChangeWarning 2>/dev/null || true
defaults delete com.apple.finder FXPreferredViewStyle 2>/dev/null || true
defaults delete com.apple.finder AutoExpandSyncFolders 2>/dev/null || true
defaults delete com.apple.finder FXEnableRemoveWithoutTrash 2>/dev/null || true
defaults delete com.apple.desktopservices DSDontWriteNetworkStores 2>/dev/null || true
defaults delete com.apple.desktopservices DSDontWriteUSBStores 2>/dev/null || true
defaults delete com.apple.NetworkBrowser DisableAirDrop 2>/dev/null || true
defaults delete com.apple.NetworkBrowser BrowseAllInterfaces 2>/dev/null || true
defaults delete -g QLPanelAnimationDuration 2>/dev/null || true
chflags hidden ~/Library 2>/dev/null || true
sudo chflags hidden /Volumes 2>/dev/null || true

echo "🪟 [3/7] Pencereler, Masaüstü ve Dock Ayarları Sıfırlanıyor..."
defaults delete com.apple.WindowManager EnableTopDragToRestore 2>/dev/null || true
defaults delete com.apple.WindowManager ClickWidgetBackgroundInStageManager 2>/dev/null || true
defaults delete com.apple.WindowManager EnableTiledWindowMargins 2>/dev/null || true
defaults delete -g NSWindowShouldDragOnGesture 2>/dev/null || true
defaults delete com.apple.dock autohide-delay 2>/dev/null || true
defaults delete com.apple.dock autohide-time-modifier 2>/dev/null || true
defaults delete com.apple.dock showhidden 2>/dev/null || true
defaults delete com.apple.dock show-recents 2>/dev/null || true
defaults delete com.apple.dock expose-group-apps 2>/dev/null || true
defaults delete com.apple.dock expose-animation-duration 2>/dev/null || true
defaults delete com.apple.dock mru-spaces 2>/dev/null || true
defaults delete NSGlobalDomain NSWindowResizeTime 2>/dev/null || true
defaults delete NSGlobalDomain AppleActionOnDoubleClick 2>/dev/null || true
defaults delete com.apple.dock wvous-br-corner 2>/dev/null || true
defaults delete com.apple.dock static-only 2>/dev/null || true
defaults delete com.apple.dock mineffect 2>/dev/null || true
defaults delete com.apple.finder CreateDesktop 2>/dev/null || true

echo "⌨️ [4/7] Klavye, Trackpad ve Donanım Girdileri Sıfırlanıyor..."
defaults delete NSGlobalDomain KeyRepeat 2>/dev/null || true
defaults delete NSGlobalDomain InitialKeyRepeat 2>/dev/null || true
defaults delete NSGlobalDomain ApplePressAndHoldEnabled 2>/dev/null || true
defaults delete com.apple.AppleMultitouchTrackpad Clicking 2>/dev/null || true
defaults delete com.apple.driver.AppleBluetoothMultitouch.trackpad Clicking 2>/dev/null || true
defaults -currentHost delete NSGlobalDomain com.apple.mouse.tapBehavior 2>/dev/null || true
defaults delete com.apple.AppleMultitouchTrackpad TrackpadThreeFingerDrag 2>/dev/null || true
defaults delete com.apple.driver.AppleBluetoothMultitouch.trackpad TrackpadThreeFingerDrag 2>/dev/null || true
defaults delete NSGlobalDomain NSAutomaticPeriodSubstitutionEnabled 2>/dev/null || true
defaults delete NSGlobalDomain NSAutomaticCapitalizationEnabled 2>/dev/null || true
defaults delete NSGlobalDomain NSAutomaticSpellingCorrectionEnabled 2>/dev/null || true
defaults delete NSGlobalDomain NSAutomaticQuoteSubstitutionEnabled 2>/dev/null || true
defaults delete NSGlobalDomain NSAutomaticDashSubstitutionEnabled 2>/dev/null || true
defaults delete NSGlobalDomain AppleKeyboardUIMode 2>/dev/null || true
defaults delete NSGlobalDomain "com.apple.sound.beep.feedback" 2>/dev/null || true
defaults delete com.apple.helpviewer DevMode 2>/dev/null || true
defaults delete com.apple.BezelServices kDimTime 2>/dev/null || true
defaults delete NSGlobalDomain com.apple.keyboard.fnState 2>/dev/null || true
defaults delete NSGlobalDomain com.apple.swipescrolldirection 2>/dev/null || true

echo "⚡ [5/7] Geliştirici ve Sistem Ayarları Orijinale Alınıyor..."
defaults delete com.apple.dt.Xcode ShowBuildOperationDuration 2>/dev/null || true
defaults delete com.apple.LaunchServices LSQuarantine 2>/dev/null || true
defaults delete com.apple.Safari IncludeDevelopMenu 2>/dev/null || true
defaults delete com.apple.Safari WebKitDeveloperExtrasEnabledPreferenceKey 2>/dev/null || true
defaults delete com.apple.Safari com.apple.Safari.ContentPageGroupIdentifier.WebKit2DeveloperExtrasEnabled 2>/dev/null || true
defaults delete com.apple.Safari ShowFullURLInSmartSearchField 2>/dev/null || true
defaults delete NSGlobalDomain NSNavPanelExpandedStateForSaveMode 2>/dev/null || true
defaults delete NSGlobalDomain NSNavPanelExpandedStateForSaveMode2 2>/dev/null || true
defaults delete NSGlobalDomain PMPrintingExpandedStateForPrint 2>/dev/null || true
defaults delete NSGlobalDomain PMPrintingExpandedStateForPrint2 2>/dev/null || true
defaults delete com.apple.CrashReporter DialogType 2>/dev/null || true
defaults delete com.apple.BluetoothAudioAgent "Apple Bitpool Min (editable)" 2>/dev/null || true
defaults delete com.apple.screensaver askForPassword 2>/dev/null || true
defaults delete com.apple.screensaver askForPasswordDelay 2>/dev/null || true
defaults delete com.apple.screencapture type 2>/dev/null || true
defaults delete com.apple.screencapture disable-shadow 2>/dev/null || true
defaults delete com.apple.screencapture location 2>/dev/null || true
defaults delete com.apple.notificationcenterui dndDisplayNotifications 2>/dev/null || true

echo "🏔️ [6/7] macOS Tahoe ve Apple Intelligence Ayarları Temizleniyor..."
defaults delete com.apple.WindowManager TilingWindowPreviewDelay 2>/dev/null || true
defaults delete com.apple.WindowManager ShowTilingSnapDividers 2>/dev/null || true
defaults delete com.apple.ScreenContinuity AutoGroupPhoneNotifications 2>/dev/null || true
defaults delete com.apple.ScreenContinuity MirrorDoNotDisturbState 2>/dev/null || true
defaults delete NSGlobalDomain WritingToolsShowDelay 2>/dev/null || true
defaults delete com.apple.Spotlight DirectMathEvaluation 2>/dev/null || true
defaults delete com.apple.Spotlight LookupServerDisableRemoteQueries 2>/dev/null || true
defaults -currentHost delete -globalDomain NSStatusItemSpacing 2>/dev/null || true
defaults -currentHost delete -globalDomain NSStatusItemSelectionPadding 2>/dev/null || true
defaults delete com.apple.Passwords AutoFillDisplayDelay 2>/dev/null || true
defaults delete com.apple.Passwords EnableFastTouchIDAuthentication 2>/dev/null || true
defaults delete com.apple.backgroundtaskmanagement SuppressServiceAlerts 2>/dev/null || true
defaults delete com.apple.WindowManager AppSwitcherAnimationDuration 2>/dev/null || true
defaults delete com.apple.gameoverlay EnableGameModeAutoBoost 2>/dev/null || true
defaults delete com.apple.WindowManager HideDesktop 2>/dev/null || true
defaults delete com.apple.WindowManager AutoRestoreStageLayout 2>/dev/null || true
defaults delete NSGlobalDomain _HIHideMenuBar 2>/dev/null || true
defaults delete NSGlobalDomain MenuBarShowDelay 2>/dev/null || true
defaults delete com.apple.CoreMedia.AVCapture EnableNeuralProcessingOverride 2>/dev/null || true
defaults delete com.apple.Spotlight LookupServerPrioritizeDefinitions 2>/dev/null || true

echo "🔋 Donanım ve Güç Ayarları Fabrika Varsayılanına Sıfırlanıyor..."
sudo pmset -a restoredefaults 2>/dev/null || true
sudo nvram AutoBoot=%03 2>/dev/null || true
sudo nvram StartupMute=%00 2>/dev/null || true

echo "🔄 [7/7] Sistem Servisleri Varsayılanlarla Yeniden Başlatılıyor..."
killall Finder 2>/dev/null || true
killall Dock 2>/dev/null || true
killall WindowManager 2>/dev/null || true
killall SystemUIServer 2>/dev/null || true
killall Spotlight 2>/dev/null || true

echo ""
echo "✅ Sistem tamamen macOS orijinal fabrika ayarlarına döndürüldü!"
echo ""
