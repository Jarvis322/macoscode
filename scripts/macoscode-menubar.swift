#!/usr/bin/env swift
import Cocoa
import Foundation

// MARK: - Shell Execution Helper
@discardableResult
func shell(_ command: String) -> (output: String, exitCode: Int32) {
    let task = Process()
    let pipe = Pipe()
    task.standardOutput = pipe
    task.standardError = pipe
    task.arguments = ["-c", command]
    task.launchPath = "/bin/zsh"
    task.launch()
    task.waitUntilExit()
    let data = pipe.fileHandleForReading.readDataToEndOfFile()
    let output = String(data: data, encoding: .utf8)?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
    return (output, task.terminationStatus)
}

func readBoolDefault(domain: String, key: String) -> Bool {
    let res = shell("defaults read \(domain) \(key) 2>/dev/null")
    if res.exitCode == 0 {
        let val = res.output.lowercased()
        return val == "1" || val == "true" || val == "yes"
    }
    return false
}

func notify(title: String, subtitle: String, message: String) {
    let escapedTitle = title.replacingOccurrences(of: "\"", with: "\\\"")
    let escapedSubtitle = subtitle.replacingOccurrences(of: "\"", with: "\\\"")
    let escapedMessage = message.replacingOccurrences(of: "\"", with: "\\\"")
    let script = "display notification \"\(escapedMessage)\" with title \"\(escapedTitle)\" subtitle \"\(escapedSubtitle)\" sound name \"Glass\""
    _ = shell("osascript -e '\(script)'")
}

// MARK: - Menu Bar App Delegate
class MenuBarAppDelegate: NSObject, NSApplicationDelegate {
    var statusItem: NSStatusItem!
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.accessory)
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        
        if let button = statusItem.button {
            button.title = "⚡"
            button.toolTip = "macOSCode Quick Tweaks & Optimizer"
        }
        
        refreshMenu()
    }
    
    func refreshMenu() {
        let menu = NSMenu()
        menu.autoenablesItems = false
        
        // Count active tweaks
        var activeCount = 0
        var totalCount = 0
        
        func track(_ active: Bool) {
            totalCount += 1
            if active { activeCount += 1 }
        }
        
        // Preliminary checks for live counts
        let hiddenActive = readBoolDefault(domain: "com.apple.finder", key: "AppleShowAllFiles"); track(hiddenActive)
        let extActive = readBoolDefault(domain: "NSGlobalDomain", key: "AppleShowAllExtensions"); track(extActive)
        let posixActive = readBoolDefault(domain: "com.apple.finder", key: "_FXShowPosixPathInTitle"); track(posixActive)
        let qlActive = readBoolDefault(domain: "com.apple.finder", key: "QLEnableTextSelection"); track(qlActive)
        let dsActive = readBoolDefault(domain: "com.apple.desktopservices", key: "DSDontWriteNetworkStores"); track(dsActive)
        let warnTrash = readBoolDefault(domain: "com.apple.finder", key: "WarnOnEmptyTrash")
        let warnTrashDisabled = (shell("defaults read com.apple.finder WarnOnEmptyTrash 2>/dev/null").output == "0"); track(warnTrashDisabled)
        let warnExtDisabled = (shell("defaults read com.apple.finder FXEnableExtensionChangeWarning 2>/dev/null").output == "0"); track(warnExtDisabled)
        
        let deskIconsRes = shell("defaults read com.apple.finder CreateDesktop 2>/dev/null")
        let deskIconsHidden = (deskIconsRes.exitCode == 0 && deskIconsRes.output == "0"); track(deskIconsHidden)
        let dockDelayRes = shell("defaults read com.apple.dock autohide-delay 2>/dev/null")
        let dockFast = (dockDelayRes.exitCode == 0 && dockDelayRes.output == "0"); track(dockFast)
        let suckActive = (shell("defaults read com.apple.dock mineffect 2>/dev/null").output.contains("suck")); track(suckActive)
        let noTileMargins = (shell("defaults read com.apple.WindowManager EnableTiledWindowMargins 2>/dev/null").output == "0"); track(noTileMargins)
        let stageDeskActive = readBoolDefault(domain: "com.apple.WindowManager", key: "ClickWidgetBackgroundInStageManager"); track(stageDeskActive)
        let reduceMotionActive = readBoolDefault(domain: "com.apple.universalaccess", key: "reduceMotion"); track(reduceMotionActive)
        let topDragActive = readBoolDefault(domain: "com.apple.WindowManager", key: "EnableTopDragToRestore"); track(topDragActive)
        let noRecents = (shell("defaults read com.apple.dock show-recents 2>/dev/null").output == "0"); track(noRecents)
        
        let keyRepeatFast = (shell("defaults read NSGlobalDomain KeyRepeat 2>/dev/null").output == "1"); track(keyRepeatFast)
        let pressHoldOff = (shell("defaults read NSGlobalDomain ApplePressAndHoldEnabled 2>/dev/null").output == "0"); track(pressHoldOff)
        let tapToClick = readBoolDefault(domain: "com.apple.driver.AppleBluetoothMultitouch.trackpad", key: "Clicking"); track(tapToClick)
        let threeFinger = readBoolDefault(domain: "com.apple.AppleMultitouchTrackpad", key: "TrackpadThreeFingerDrag"); track(threeFinger)
        let autocorrectOff = (shell("defaults read NSGlobalDomain NSAutomaticSpellingCorrectionEnabled 2>/dev/null").output == "0"); track(autocorrectOff)
        let volumeBeepOff = (shell("defaults read NSGlobalDomain com.apple.sound.beep.feedback 2>/dev/null").output == "0"); track(volumeBeepOff)
        
        let xcodeDuration = readBoolDefault(domain: "com.apple.dt.Xcode", key: "ShowBuildOperationDuration"); track(xcodeDuration)
        let safariDevelop = readBoolDefault(domain: "com.apple.Safari", key: "IncludeDevelopMenu"); track(safariDevelop)
        let safariFullUrl = readBoolDefault(domain: "com.apple.Safari", key: "ShowFullURLInSmartSearchField"); track(safariFullUrl)
        let quarantineOff = (shell("defaults read com.apple.LaunchServices LSQuarantine 2>/dev/null").output == "0"); track(quarantineOff)
        let crashDialogOff = (shell("defaults read com.apple.CrashReporter DialogType 2>/dev/null").output == "none"); track(crashDialogOff)
        let bitpoolBoost = (shell("defaults read com.apple.BluetoothAudioAgent \"Apple Bitpool Min (editable)\" 2>/dev/null").output == "40"); track(bitpoolBoost)
        let expandPanels = readBoolDefault(domain: "NSGlobalDomain", key: "NSNavPanelExpandedStateForSaveMode"); track(expandPanels)
        
        let wifiPowersaveOff = (shell("defaults read /Library/Preferences/SystemConfiguration/com.apple.airport.opp.plist WiFiPowerManagement 2>/dev/null").output == "0"); track(wifiPowersaveOff)
        let neverSleepAc = (shell("pmset -g custom 2>/dev/null | grep -E '^AC Power:' -A 10 | grep 'sleep[[:space:]]+0'").exitCode == 0); track(neverSleepAc)
        let clamshellNoSleep = (shell("pmset -g | grep 'disablesleep[[:space:]]+1'").exitCode == 0); track(clamshellNoSleep)
        let startupMute = (shell("nvram StartupMute 2>/dev/null").output.contains("%01")); track(startupMute)
        
        let snapZeroDelay = (shell("defaults read com.apple.WindowManager TilingWindowPreviewDelay 2>/dev/null").output == "0"); track(snapZeroDelay)
        let noSnapDividers = (shell("defaults read com.apple.WindowManager ShowTilingSnapDividers 2>/dev/null").output == "0"); track(noSnapDividers)
        let spotLocalFirst = (shell("defaults read com.apple.Spotlight LookupServerDisableRemoteQueries 2>/dev/null").output == "1"); track(spotLocalFirst)
        let spotDirectMath = readBoolDefault(domain: "com.apple.Spotlight", key: "DirectMathEvaluation"); track(spotDirectMath)
        let compactMenubar = (shell("defaults -currentHost read -globalDomain NSStatusItemSpacing 2>/dev/null").output == "6"); track(compactMenubar)
        let writingToolsFast = (shell("defaults read NSGlobalDomain WritingToolsShowDelay 2>/dev/null").output == "0"); track(writingToolsFast)

        // HEADER
        let titleItem = NSMenuItem(title: "🚀 macOSCode Power Optimizer", action: nil, keyEquivalent: "")
        titleItem.attributedTitle = NSAttributedString(
            string: "🚀 macOSCode Power Optimizer",
            attributes: [.font: NSFont.boldSystemFont(ofSize: 13)]
        )
        menu.addItem(titleItem)
        
        let pct = totalCount > 0 ? Int((Double(activeCount) / Double(totalCount)) * 100) : 0
        let statusText = "📊 Durum: \(activeCount)/\(totalCount) Ayar Aktif (%\(pct) Güç)"
        let subtitleItem = NSMenuItem(title: statusText, action: nil, keyEquivalent: "")
        subtitleItem.attributedTitle = NSAttributedString(
            string: statusText,
            attributes: [.font: NSFont.systemFont(ofSize: 11), .foregroundColor: NSColor.systemTeal]
        )
        menu.addItem(subtitleItem)
        menu.addItem(NSMenuItem.separator())

        // 📁 SUBMENU 1: FINDER & DOSYA YÖNETİMİ
        let finderMenu = NSMenu()
        finderMenu.autoenablesItems = false
        
        addToggle(to: finderMenu, title: "Gizli Dosyaları Göster (.dotfiles)", state: hiddenActive, action: #selector(toggleHiddenFiles))
        addToggle(to: finderMenu, title: "Tüm Dosya Uzantılarını Göster (.json, .env)", state: extActive, action: #selector(toggleExtensions))
        addToggle(to: finderMenu, title: "Finder Başlığında Tam Dosya Yolu (POSIX)", state: posixActive, action: #selector(togglePosixPath))
        addToggle(to: finderMenu, title: "Quick Look Önizlemede Metin Seçimi", state: qlActive, action: #selector(toggleQLText))
        addToggle(to: finderMenu, title: "Ağ ve USB'ye .DS_Store Yazılmasını Engelle", state: dsActive, action: #selector(toggleDSStore))
        addToggle(to: finderMenu, title: "Çöp Kutusunu Boşaltırken Uyarıyı Kapat", state: warnTrashDisabled, action: #selector(toggleWarnTrash))
        addToggle(to: finderMenu, title: "Uzantı Değiştirme Uyarısını Kapat", state: warnExtDisabled, action: #selector(toggleWarnExt))
        
        let finderParent = NSMenuItem(title: "📁 Finder & Gelişmiş Dosya Yönetimi", action: nil, keyEquivalent: "")
        finderParent.submenu = finderMenu
        menu.addItem(finderParent)

        // 🪟 SUBMENU 2: PENCERELER, MASAÜSTÜ & DOCK
        let winDockMenu = NSMenu()
        winDockMenu.autoenablesItems = false
        
        addToggle(to: winDockMenu, title: "Masaüstü Simgelerini Gizle (Temiz Masaüstü)", state: deskIconsHidden, action: #selector(toggleDesktopIcons))
        addToggle(to: winDockMenu, title: "Dock Sıfır Gecikmeli Hızlı Açılış", state: dockFast, action: #selector(toggleDockSpeed))
        addToggle(to: winDockMenu, title: "Pencereleri 'Suck' Efektiyle Küçült", state: suckActive, action: #selector(toggleSuckEffect))
        addToggle(to: winDockMenu, title: "Pencere Döşeme Kenar Boşluklarını Kaldır", state: noTileMargins, action: #selector(toggleTilingMargins))
        addToggle(to: winDockMenu, title: "Stage Manager'da Masaüstünü Görünür Tut", state: stageDeskActive, action: #selector(toggleStageManagerDesktop))
        addToggle(to: winDockMenu, title: "Hareketi Azalt (Reduce Motion Hızlandırma)", state: reduceMotionActive, action: #selector(toggleReduceMotion))
        addToggle(to: winDockMenu, title: "Büyütülmüş Pencereyi Üstten Çekerek Geri Al", state: topDragActive, action: #selector(toggleTopDrag))
        addToggle(to: winDockMenu, title: "Dock'taki Son Kullanılan Uygulamaları Gizle", state: noRecents, action: #selector(toggleDockRecents))
        
        let winDockParent = NSMenuItem(title: "🪟 Pencereler, Masaüstü & Dock", action: nil, keyEquivalent: "")
        winDockParent.submenu = winDockMenu
        menu.addItem(winDockParent)

        // ⌨️ SUBMENU 3: KLAVYE, TRACKPAD & GİRDİ
        let inputMenu = NSMenu()
        inputMenu.autoenablesItems = false
        
        addToggle(to: inputMenu, title: "Maksimum Tuş Tekrar Hızı ve Min Gecikme", state: keyRepeatFast, action: #selector(toggleKeyRepeat))
        addToggle(to: inputMenu, title: "Aksan Menüsü Yerine Doğrudan Tuş Tekrarı", state: pressHoldOff, action: #selector(togglePressAndHold))
        addToggle(to: inputMenu, title: "Trackpad Dokunarak Tıklama (Tap to Click)", state: tapToClick, action: #selector(toggleTapToClick))
        addToggle(to: inputMenu, title: "Trackpad Üç Parmakla Sürükleme", state: threeFinger, action: #selector(toggleThreeFinger))
        addToggle(to: inputMenu, title: "Otomatik Nokta, Büyük Harf ve Düzeltmeyi Kapat", state: autocorrectOff, action: #selector(toggleAutocorrect))
        addToggle(to: inputMenu, title: "Ses Seviyesi Değişirken Çıkan Bip Sesini Kapat", state: volumeBeepOff, action: #selector(toggleVolumeBeep))
        
        let inputParent = NSMenuItem(title: "⌨️ Klavye, Trackpad & Donanım Girdileri", action: nil, keyEquivalent: "")
        inputParent.submenu = inputMenu
        menu.addItem(inputParent)

        // ⚡ SUBMENU 4: GELİŞTİRİCİ, GÜVENLİK & SİSTEM
        let devMenu = NSMenu()
        devMenu.autoenablesItems = false
        
        addToggle(to: devMenu, title: "Xcode Derleme Süresi Sayacı (Build Duration)", state: xcodeDuration, action: #selector(toggleXcodeDuration))
        addToggle(to: devMenu, title: "Safari Geliştirici Menüsü ve Web Inspector", state: safariDevelop, action: #selector(toggleSafariDevelop))
        addToggle(to: devMenu, title: "Safari Adres Çubuğunda Tam URL Göster", state: safariFullUrl, action: #selector(toggleSafariFullUrl))
        addToggle(to: devMenu, title: "İndirilen Dosyalarda Karantina Uyarısını Atla", state: quarantineOff, action: #selector(toggleQuarantine))
        addToggle(to: devMenu, title: "Çökme Raporu (Crash Reporter) Pencerelerini Kapat", state: crashDialogOff, action: #selector(toggleCrashReporter))
        addToggle(to: devMenu, title: "Bluetooth Yüksek Ses Kalitesi (Bitpool 40)", state: bitpoolBoost, action: #selector(toggleBluetoothBitpool))
        addToggle(to: devMenu, title: "Kayıt ve Yazdırma Pencerelerini Genişletilmiş Aç", state: expandPanels, action: #selector(toggleExpandPanels))
        
        let devParent = NSMenuItem(title: "⚡ Geliştirici, Güvenlik & Sistem", action: nil, keyEquivalent: "")
        devParent.submenu = devMenu
        menu.addItem(devParent)

        // 🔋 SUBMENU 5: AĞ, GÜÇ & DONANIM
        let powerMenu = NSMenu()
        powerMenu.autoenablesItems = false
        
        addToggle(to: powerMenu, title: "Wi-Fi Güç Tasarrufunu Kapat (Düşük Ping/Jitter)", state: wifiPowersaveOff, action: #selector(toggleWifiPowerSave))
        addToggle(to: powerMenu, title: "Prizde İken Uykuyu Engelle (Never Sleep)", state: neverSleepAc, action: #selector(toggleAcNeverSleep))
        addToggle(to: powerMenu, title: "Kapak Kapalıyken Uyumayı Engelle (Clamshell)", state: clamshellNoSleep, action: #selector(toggleClamshellSleep))
        addToggle(to: powerMenu, title: "Mac Başlangıç Sesini (Startup Chime) Sustur", state: startupMute, action: #selector(toggleStartupMute))
        
        let powerParent = NSMenuItem(title: "🔋 Ağ, Güç Yönetimi & Donanım", action: nil, keyEquivalent: "")
        powerParent.submenu = powerMenu
        menu.addItem(powerParent)

        // 🏔️ SUBMENU 6: MACOS TAHOE & AI
        let tahoeMenu = NSMenu()
        tahoeMenu.autoenablesItems = false
        
        addToggle(to: tahoeMenu, title: "Pencere Döşeme Snap Önizleme Gecikmesini Sıfırla", state: snapZeroDelay, action: #selector(toggleSnapDelay))
        addToggle(to: tahoeMenu, title: "Döşenen Pencereler Arasındaki Ayırıcı Çizgiyi Kaldır", state: noSnapDividers, action: #selector(toggleSnapDividers))
        addToggle(to: tahoeMenu, title: "Spotlight'ta Web Yerine Yerel Dosyalara Öncelik Ver", state: spotLocalFirst, action: #selector(toggleSpotlightLocalFirst))
        addToggle(to: tahoeMenu, title: "Spotlight Matematik Formüllerini Doğrudan Çözsün", state: spotDirectMath, action: #selector(toggleSpotlightDirectMath))
        addToggle(to: tahoeMenu, title: "Menü Çubuğu Simgelerini Sıkıştır (Notch Modu)", state: compactMenubar, action: #selector(toggleCompactMenubar))
        addToggle(to: tahoeMenu, title: "Yazma Araçları (Writing Tools) Gecikmesini Sıfırla", state: writingToolsFast, action: #selector(toggleWritingToolsDelay))
        
        let tahoeParent = NSMenuItem(title: "🏔️ macOS Tahoe & Apple Intelligence", action: nil, keyEquivalent: "")
        tahoeParent.submenu = tahoeMenu
        menu.addItem(tahoeParent)

        menu.addItem(NSMenuItem.separator())

        // 🛠️ SUBMENU 7: HIZLI SİSTEM ARAÇLARI
        let toolsMenu = NSMenu()
        toolsMenu.autoenablesItems = false
        
        toolsMenu.addItem(NSMenuItem(title: "🧹 DNS Önbelleğini Temizle (Flush DNS)", action: #selector(actionFlushDNS), keyEquivalent: ""))
        toolsMenu.addItem(NSMenuItem(title: "📶 Wi-Fi Modülünü Yeniden Başlat", action: #selector(actionRestartWifi), keyEquivalent: ""))
        toolsMenu.addItem(NSMenuItem(title: "🎧 Bluetooth Servisini Yeniden Başlat", action: #selector(actionRestartBluetooth), keyEquivalent: ""))
        toolsMenu.addItem(NSMenuItem(title: "💾 SSD Sleep Image Dosyasını Temizle", action: #selector(actionCleanSleepImage), keyEquivalent: ""))
        toolsMenu.addItem(NSMenuItem.separator())
        toolsMenu.addItem(NSMenuItem(title: "🚀 Tüm 100 Ayarı Uygula (Master Setup)", action: #selector(actionApplyAll), keyEquivalent: ""))
        toolsMenu.addItem(NSMenuItem(title: "⏪ Tümünü Fabrika Ayarlarına Döndür (Master Reset)", action: #selector(actionRevertAll), keyEquivalent: ""))
        
        for item in toolsMenu.items { item.target = self }
        
        let toolsParent = NSMenuItem(title: "🛠️ Hızlı Sistem Araçları & Bakım", action: nil, keyEquivalent: "")
        toolsParent.submenu = toolsMenu
        menu.addItem(toolsParent)

        // DIRECT ACCESS ITEMS
        let openMcItem = NSMenuItem(title: "🎛️ Terminal'de 'mc' TUI Başlat", action: #selector(openTerminalMC), keyEquivalent: "t")
        openMcItem.target = self
        menu.addItem(openMcItem)
        
        let openWebItem = NSMenuItem(title: "🌐 macOSCode Web Sitesini Aç", action: #selector(openWebSite), keyEquivalent: "w")
        openWebItem.target = self
        menu.addItem(openWebItem)
        
        menu.addItem(NSMenuItem.separator())
        
        // REFRESH & QUIT
        let refreshItem = NSMenuItem(title: "🔄 Durumu Yenile", action: #selector(refreshClicked), keyEquivalent: "r")
        refreshItem.target = self
        menu.addItem(refreshItem)
        
        let quitItem = NSMenuItem(title: "❌ Menü Bar Aracını Kapat", action: #selector(quitApp), keyEquivalent: "q")
        quitItem.target = self
        menu.addItem(quitItem)
        
        statusItem.menu = menu
    }
    
    private func addToggle(to menu: NSMenu, title: String, state: Bool, action: Selector) {
        let item = NSMenuItem(title: title, action: action, keyEquivalent: "")
        item.target = self
        item.state = state ? .on : .off
        menu.addItem(item)
    }
    
    // MARK: - Toggle Handlers
    @objc func toggleHiddenFiles() {
        let current = readBoolDefault(domain: "com.apple.finder", key: "AppleShowAllFiles")
        if current {
            shell("defaults delete com.apple.finder AppleShowAllFiles && killall Finder")
            notify(title: "Finder", subtitle: "Gizli Dosyalar Gizlendi", message: "Nokta ile başlayan gizli sistem dosyaları artık gizli.")
        } else {
            shell("defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder")
            notify(title: "Finder", subtitle: "Gizli Dosyalar Görünür", message: ".dotfiles ve gizli proje dizinleri görünür yapıldı.")
        }
        refreshMenu()
    }
    
    @objc func toggleExtensions() {
        let current = readBoolDefault(domain: "NSGlobalDomain", key: "AppleShowAllExtensions")
        if current {
            shell("defaults delete NSGlobalDomain AppleShowAllExtensions && killall Finder")
            notify(title: "Finder", subtitle: "Uzantı Görünümü Sıfırlandı", message: "Dosya uzantıları macOS varsayılanına döndürüldü.")
        } else {
            shell("defaults write NSGlobalDomain AppleShowAllExtensions -bool true && killall Finder")
            notify(title: "Finder", subtitle: "Tüm Uzantılar Görünür", message: "Finder'da .json, .env, .png vb. tüm uzantılar açık.")
        }
        refreshMenu()
    }
    
    @objc func togglePosixPath() {
        let current = readBoolDefault(domain: "com.apple.finder", key: "_FXShowPosixPathInTitle")
        if current {
            shell("defaults delete com.apple.finder _FXShowPosixPathInTitle && killall Finder")
            notify(title: "Finder", subtitle: "Başlık Yolu Kapatıldı", message: "Pencere başlığı standart ada döndü.")
        } else {
            shell("defaults write com.apple.finder _FXShowPosixPathInTitle -bool true && killall Finder")
            notify(title: "Finder", subtitle: "POSIX Yolu Aktif", message: "Finder başlığında tam dosya yolu (/Users/...) gösteriliyor.")
        }
        refreshMenu()
    }
    
    @objc func toggleQLText() {
        let current = readBoolDefault(domain: "com.apple.finder", key: "QLEnableTextSelection")
        if current {
            shell("defaults delete com.apple.finder QLEnableTextSelection && killall Finder")
            notify(title: "Quick Look", subtitle: "Metin Seçimi Kapatıldı", message: "Hızlı Bakış önizlemelerinde metin seçimi kapatıldı.")
        } else {
            shell("defaults write com.apple.finder QLEnableTextSelection -bool true && killall Finder")
            notify(title: "Quick Look", subtitle: "Metin Seçimi Aktif", message: "Boşluk tuşu ile açılan önizlemelerde metinler kopyalanabilir.")
        }
        refreshMenu()
    }
    
    @objc func toggleDSStore() {
        let current = readBoolDefault(domain: "com.apple.desktopservices", key: "DSDontWriteNetworkStores")
        if current {
            shell("defaults delete com.apple.desktopservices DSDontWriteNetworkStores; defaults delete com.apple.desktopservices DSDontWriteUSBStores")
            notify(title: "Depolama", subtitle: ".DS_Store Engeli Kaldırıldı", message: "Ağ ve USB sürücülere .DS_Store yazımına izin verildi.")
        } else {
            shell("defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true; defaults write com.apple.desktopservices DSDontWriteUSBStores -bool true")
            notify(title: "Depolama", subtitle: ".DS_Store Engellendi", message: "Harici USB ve ağ paylaşımlarına .DS_Store dosyası yazılmayacak.")
        }
        refreshMenu()
    }
    
    @objc func toggleWarnTrash() {
        let current = (shell("defaults read com.apple.finder WarnOnEmptyTrash 2>/dev/null").output == "0")
        if current {
            shell("defaults delete com.apple.finder WarnOnEmptyTrash && killall Finder")
            notify(title: "Finder", subtitle: "Çöp Uyarısı Aktif", message: "Çöp boşaltılırken onay penceresi gösterilecek.")
        } else {
            shell("defaults write com.apple.finder WarnOnEmptyTrash -bool false && killall Finder")
            notify(title: "Finder", subtitle: "Çöp Uyarısı Kapatıldı", message: "Çöp boşaltırken onay kutusu sorulmadan temizlenecek.")
        }
        refreshMenu()
    }
    
    @objc func toggleWarnExt() {
        let current = (shell("defaults read com.apple.finder FXEnableExtensionChangeWarning 2>/dev/null").output == "0")
        if current {
            shell("defaults delete com.apple.finder FXEnableExtensionChangeWarning && killall Finder")
            notify(title: "Finder", subtitle: "Uzantı Uyarısı Aktif", message: "Uzantı değiştirilirken uyarı penceresi gösterilecek.")
        } else {
            shell("defaults write com.apple.finder FXEnableExtensionChangeWarning -bool false && killall Finder")
            notify(title: "Finder", subtitle: "Uzantı Uyarısı Kapatıldı", message: "Dosya uzantıları uyarısız anında değiştirilecek.")
        }
        refreshMenu()
    }
    
    @objc func toggleDesktopIcons() {
        let currentRes = shell("defaults read com.apple.finder CreateDesktop 2>/dev/null")
        let isHidden = (currentRes.exitCode == 0 && currentRes.output == "0")
        if isHidden {
            shell("defaults delete com.apple.finder CreateDesktop && killall Finder")
            notify(title: "Masaüstü", subtitle: "Simgeler Görünür", message: "Masaüstü dosyaları ve disk ikonları görünür yapıldı.")
        } else {
            shell("defaults write com.apple.finder CreateDesktop -bool false && killall Finder")
            notify(title: "Masaüstü", subtitle: "Simgeler Gizlendi", message: "Masaüstü temizlendi (ekran paylaşımı modu aktif).")
        }
        refreshMenu()
    }
    
    @objc func toggleDockSpeed() {
        let dockDelayRes = shell("defaults read com.apple.dock autohide-delay 2>/dev/null")
        let isZero = (dockDelayRes.exitCode == 0 && dockDelayRes.output == "0")
        if isZero {
            shell("defaults delete com.apple.dock autohide-delay && defaults delete com.apple.dock autohide-time-modifier && killall Dock")
            notify(title: "Dock", subtitle: "Animasyon Sıfırlandı", message: "Dock açılış hızı fabrika varsayılanına döndürüldü.")
        } else {
            shell("defaults write com.apple.dock autohide-delay -float 0 && defaults write com.apple.dock autohide-time-modifier -float 0.3 && killall Dock")
            notify(title: "Dock", subtitle: "Sıfır Gecikme Aktif", message: "Fare kenara geldiğinde Dock anında gecikmesiz açılacak.")
        }
        refreshMenu()
    }
    
    @objc func toggleSuckEffect() {
        let current = (shell("defaults read com.apple.dock mineffect 2>/dev/null").output.contains("suck"))
        if current {
            shell("defaults delete com.apple.dock mineffect && killall Dock")
            notify(title: "Dock", subtitle: "Genie Efektine Dönüldü", message: "Pencereler klasik Genie dalga efektiyle küçülecek.")
        } else {
            shell("defaults write com.apple.dock mineffect -string 'suck' && killall Dock")
            notify(title: "Dock", subtitle: "Suck Efekti Aktif", message: "Pencereler akıcı 'Suck' animasyonuyla küçülecek.")
        }
        refreshMenu()
    }
    
    @objc func toggleTilingMargins() {
        let current = (shell("defaults read com.apple.WindowManager EnableTiledWindowMargins 2>/dev/null").output == "0")
        if current {
            shell("defaults delete com.apple.WindowManager EnableTiledWindowMargins && killall WindowManager")
            notify(title: "Pencereler", subtitle: "Döşeme Kenarlıkları Aktif", message: "Yan yana döşenen pencereler arasında boşluk bırakılacak.")
        } else {
            shell("defaults write com.apple.WindowManager EnableTiledWindowMargins -bool false && killall WindowManager")
            notify(title: "Pencereler", subtitle: "Sıfır Kenar Boşluğu (Borderless)", message: "Döşenen pencereler tam kenardan kenara oturacak.")
        }
        refreshMenu()
    }
    
    @objc func toggleStageManagerDesktop() {
        let current = readBoolDefault(domain: "com.apple.WindowManager", key: "ClickWidgetBackgroundInStageManager")
        if current {
            shell("defaults delete com.apple.WindowManager ClickWidgetBackgroundInStageManager && killall WindowManager")
            notify(title: "Stage Manager", subtitle: "Masaüstü Gizleme Varsayılan", message: "Stage Manager aktifken masaüstü gizlenecek.")
        } else {
            shell("defaults write com.apple.WindowManager ClickWidgetBackgroundInStageManager -bool true && killall WindowManager")
            notify(title: "Stage Manager", subtitle: "Masaüstü Her Zaman Görünür", message: "Stage Manager'da masaüstü widget ve simgeleri görünür tutuluyor.")
        }
        refreshMenu()
    }
    
    @objc func toggleReduceMotion() {
        let current = readBoolDefault(domain: "com.apple.universalaccess", key: "reduceMotion")
        if current {
            shell("defaults delete com.apple.universalaccess reduceMotion 2>/dev/null || true")
            notify(title: "Arayüz", subtitle: "Animasyonlar Açık", message: "macOS standart kaydırma ve büyüme animasyonları devrede.")
        } else {
            shell("defaults write com.apple.universalaccess reduceMotion -bool true")
            notify(title: "Arayüz", subtitle: "Hareketi Azalt Aktif (Ultra Hızlı)", message: "Tüm sistem geçişleri anlık crossfade hızına alındı.")
        }
        refreshMenu()
    }
    
    @objc func toggleTopDrag() {
        let current = readBoolDefault(domain: "com.apple.WindowManager", key: "EnableTopDragToRestore")
        if current {
            shell("defaults delete com.apple.WindowManager EnableTopDragToRestore && killall WindowManager")
            notify(title: "Pencereler", subtitle: "Üstten Çekme Kapatıldı", message: "Büyütülmüş pencere üst çubuğundan çekilince boyutu korunur.")
        } else {
            shell("defaults write com.apple.WindowManager EnableTopDragToRestore -bool true && killall WindowManager")
            notify(title: "Pencereler", subtitle: "Üstten Çekerek Geri Yükle Aktif", message: "Büyütülmüş pencere üstten aşağı çekilince orijinal boyutuna döner.")
        }
        refreshMenu()
    }
    
    @objc func toggleDockRecents() {
        let current = (shell("defaults read com.apple.dock show-recents 2>/dev/null").output == "0")
        if current {
            shell("defaults delete com.apple.dock show-recents && killall Dock")
            notify(title: "Dock", subtitle: "Son Kullanılanlar Açık", message: "Dock sağında son açılan uygulamalar listelenecek.")
        } else {
            shell("defaults write com.apple.dock show-recents -bool false && killall Dock")
            notify(title: "Dock", subtitle: "Son Kullanılanlar Gizlendi", message: "Dock sadeleştirildi, son kullanılanlar alanı kaldırıldı.")
        }
        refreshMenu()
    }
    
    @objc func toggleKeyRepeat() {
        let current = (shell("defaults read NSGlobalDomain KeyRepeat 2>/dev/null").output == "1")
        if current {
            shell("defaults delete NSGlobalDomain KeyRepeat; defaults delete NSGlobalDomain InitialKeyRepeat")
            notify(title: "Klavye", subtitle: "Tuş Hızı Sıfırlandı", message: "Klavye tekrar hızı standart ayarlara döndü.")
        } else {
            shell("defaults write NSGlobalDomain KeyRepeat -int 1; defaults write NSGlobalDomain InitialKeyRepeat -int 10")
            notify(title: "Klavye", subtitle: "Maksimum Hız Aktif", message: "Geliştiriciler için ışık hızında tuş tekrarı ayarlandı.")
        }
        refreshMenu()
    }
    
    @objc func togglePressAndHold() {
        let current = (shell("defaults read NSGlobalDomain ApplePressAndHoldEnabled 2>/dev/null").output == "0")
        if current {
            shell("defaults delete NSGlobalDomain ApplePressAndHoldEnabled")
            notify(title: "Klavye", subtitle: "Aksan Menüsü Açık", message: "Harfe basılı tutunca aksan menüsü (é, è) açılacak.")
        } else {
            shell("defaults write NSGlobalDomain ApplePressAndHoldEnabled -bool false")
            notify(title: "Klavye", subtitle: "Doğrudan Tekrar Aktif", message: "Harfe basılı tutulduğunda anında tuş tekrarı (aaaa) yapılacak.")
        }
        refreshMenu()
    }
    
    @objc func toggleTapToClick() {
        let current = readBoolDefault(domain: "com.apple.driver.AppleBluetoothMultitouch.trackpad", key: "Clicking")
        if current {
            shell("defaults delete com.apple.driver.AppleBluetoothMultitouch.trackpad Clicking 2>/dev/null; defaults delete com.apple.AppleMultitouchTrackpad Clicking 2>/dev/null; defaults -currentHost delete NSGlobalDomain com.apple.mouse.tapBehavior 2>/dev/null; defaults delete NSGlobalDomain com.apple.mouse.tapBehavior 2>/dev/null || true")
            notify(title: "Trackpad", subtitle: "Dokunarak Tıklama Kapatıldı", message: "Değişikliğin donanıma tam yansıması için oturumu kapatıp açabilirsiniz.")
        } else {
            shell("defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad Clicking -bool true; defaults write com.apple.AppleMultitouchTrackpad Clicking -bool true; defaults -currentHost write NSGlobalDomain com.apple.mouse.tapBehavior -int 1; defaults write NSGlobalDomain com.apple.mouse.tapBehavior -int 1")
            notify(title: "Trackpad", subtitle: "Dokunarak Tıklama Diske Yazıldı", message: "macOS donanım sürücüsünün algılaması için oturumu kapatıp açmanız (Log out) gerekir.")
        }
        refreshMenu()
    }
    
    @objc func toggleThreeFinger() {
        let current = readBoolDefault(domain: "com.apple.AppleMultitouchTrackpad", key: "TrackpadThreeFingerDrag")
        if current {
            shell("defaults delete com.apple.AppleMultitouchTrackpad TrackpadThreeFingerDrag; defaults delete com.apple.driver.AppleBluetoothMultitouch.trackpad TrackpadThreeFingerDrag")
            notify(title: "Trackpad", subtitle: "Üç Parmak Sürükleme Kapatıldı", message: "Üç parmakla sürükleme devre dışı bırakıldı.")
        } else {
            shell("defaults write com.apple.AppleMultitouchTrackpad TrackpadThreeFingerDrag -bool true; defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad TrackpadThreeFingerDrag -bool true")
            notify(title: "Trackpad", subtitle: "Üç Parmak Sürükleme Aktif", message: "Pencereleri üç parmakla doğrudan sürükleyebilirsiniz.")
        }
        refreshMenu()
    }
    
    @objc func toggleAutocorrect() {
        let current = (shell("defaults read NSGlobalDomain NSAutomaticSpellingCorrectionEnabled 2>/dev/null").output == "0")
        if current {
            shell("defaults delete NSGlobalDomain NSAutomaticSpellingCorrectionEnabled; defaults delete NSGlobalDomain NSAutomaticPeriodSubstitutionEnabled; defaults delete NSGlobalDomain NSAutomaticCapitalizationEnabled")
            notify(title: "Metin Girişi", subtitle: "Otomatik Düzeltme Açık", message: "macOS otomatik yazım düzeltmeleri devreye alındı.")
        } else {
            shell("defaults write NSGlobalDomain NSAutomaticSpellingCorrectionEnabled -bool false; defaults write NSGlobalDomain NSAutomaticPeriodSubstitutionEnabled -bool false; defaults write NSGlobalDomain NSAutomaticCapitalizationEnabled -bool false")
            notify(title: "Metin Girişi", subtitle: "Otomatik Düzeltmeler Kapatıldı", message: "Kodlama yaparken kelimelerin ve noktaların bozulması engellendi.")
        }
        refreshMenu()
    }
    
    @objc func toggleVolumeBeep() {
        let current = (shell("defaults read NSGlobalDomain com.apple.sound.beep.feedback 2>/dev/null").output == "0")
        if current {
            shell("defaults delete NSGlobalDomain com.apple.sound.beep.feedback")
            notify(title: "Ses", subtitle: "Bip Sesi Açık", message: "Ses tuşlarına basıldığında geri bildirim sesi çalacak.")
        } else {
            shell("defaults write NSGlobalDomain 'com.apple.sound.beep.feedback' -int 0")
            notify(title: "Ses", subtitle: "Bip Sesi Kapatıldı", message: "Ses seviyesi değişirken çıkan bip sesi susturuldu.")
        }
        refreshMenu()
    }
    
    @objc func toggleXcodeDuration() {
        let current = readBoolDefault(domain: "com.apple.dt.Xcode", key: "ShowBuildOperationDuration")
        if current {
            shell("defaults delete com.apple.dt.Xcode ShowBuildOperationDuration 2>/dev/null || true")
            notify(title: "Xcode", subtitle: "Derleme Sayacı Kapatıldı", message: "Xcode başlığında build süresi gizlendi.")
        } else {
            shell("defaults write com.apple.dt.Xcode ShowBuildOperationDuration -bool true")
            notify(title: "Xcode", subtitle: "Derleme Sayacı Aktif", message: "Xcode'da projenin kaç saniyede build edildiği gösteriliyor.")
        }
        refreshMenu()
    }
    
    @objc func toggleSafariDevelop() {
        let current = readBoolDefault(domain: "com.apple.Safari", key: "IncludeDevelopMenu")
        if current {
            shell("defaults delete com.apple.Safari IncludeDevelopMenu 2>/dev/null; defaults delete com.apple.Safari WebKitDeveloperExtrasEnabledPreferenceKey 2>/dev/null; defaults delete com.apple.Safari com.apple.Safari.ContentPageGroupIdentifier.WebKit2DeveloperExtrasEnabled 2>/dev/null || true")
            notify(title: "Safari", subtitle: "Geliştirici Menüsü Kapatıldı", message: "Develop menüsü gizlendi.")
        } else {
            shell("defaults write com.apple.Safari IncludeDevelopMenu -bool true; defaults write com.apple.Safari WebKitDeveloperExtrasEnabledPreferenceKey -bool true; defaults write com.apple.Safari com.apple.Safari.ContentPageGroupIdentifier.WebKit2DeveloperExtrasEnabled -bool true")
            notify(title: "Safari", subtitle: "Geliştirici Menüsü & Inspector Açık", message: "Develop menüsü ve Web Inspector aktif edildi.")
        }
        refreshMenu()
    }
    
    @objc func toggleSafariFullUrl() {
        let current = readBoolDefault(domain: "com.apple.Safari", key: "ShowFullURLInSmartSearchField")
        if current {
            shell("defaults delete com.apple.Safari ShowFullURLInSmartSearchField 2>/dev/null || true")
            notify(title: "Safari", subtitle: "Alan Adı Görünümü", message: "Safari adres çubuğunda sadece alan adı gösterilecek.")
        } else {
            shell("defaults write com.apple.Safari ShowFullURLInSmartSearchField -bool true")
            notify(title: "Safari", subtitle: "Tam URL Yolu Aktif", message: "Safari akıllı arama çubuğunda tam URL (https://.../path) açık.")
        }
        refreshMenu()
    }
    
    @objc func toggleQuarantine() {
        let current = (shell("defaults read com.apple.LaunchServices LSQuarantine 2>/dev/null").output == "0")
        if current {
            shell("defaults delete com.apple.LaunchServices LSQuarantine 2>/dev/null || true")
            notify(title: "Güvenlik", subtitle: "Karantina Uyarısı Açık", message: "İnternetten indirilen araçlarda onay sorulacak.")
        } else {
            shell("defaults write com.apple.LaunchServices LSQuarantine -bool false")
            notify(title: "Güvenlik", subtitle: "Karantina Uyarısı Kapatıldı", message: "'İnternetten indirildi açılsın mı?' sorusu atlanacak.")
        }
        refreshMenu()
    }
    
    @objc func toggleCrashReporter() {
        let current = (shell("defaults read com.apple.CrashReporter DialogType 2>/dev/null").output == "none")
        if current {
            shell("defaults delete com.apple.CrashReporter DialogType 2>/dev/null || true")
            notify(title: "Sistem", subtitle: "Çökme Raporu Diyalogları Açık", message: "Uygulama çökünce hata kutusu gösterilecek.")
        } else {
            shell("defaults write com.apple.CrashReporter DialogType -string 'none'")
            notify(title: "Sistem", subtitle: "Çökme Rapor Pencereleri Kapatıldı", message: "Çökme pencereleri yerine sessiz arka plan günlüğü tutulacak.")
        }
        refreshMenu()
    }
    
    @objc func toggleBluetoothBitpool() {
        let current = (shell("defaults read com.apple.BluetoothAudioAgent \"Apple Bitpool Min (editable)\" 2>/dev/null").output == "40")
        if current {
            shell("defaults delete com.apple.BluetoothAudioAgent \"Apple Bitpool Min (editable)\" 2>/dev/null || true")
            notify(title: "Ses", subtitle: "Bluetooth Bitpool Sıfırlandı", message: "Standart Bluetooth ses kalitesine dönüldü.")
        } else {
            shell("defaults write com.apple.BluetoothAudioAgent \"Apple Bitpool Min (editable)\" -int 40")
            notify(title: "Ses", subtitle: "Bluetooth Yüksek Bitrate Aktif", message: "AAC/SBC kulaklık ve hoparlör aktarım kalitesi en üste sabitlendi.")
        }
        refreshMenu()
    }
    
    @objc func toggleExpandPanels() {
        let current = readBoolDefault(domain: "NSGlobalDomain", key: "NSNavPanelExpandedStateForSaveMode")
        if current {
            shell("defaults delete NSGlobalDomain NSNavPanelExpandedStateForSaveMode 2>/dev/null; defaults delete NSGlobalDomain NSNavPanelExpandedStateForSaveMode2 2>/dev/null; defaults delete NSGlobalDomain PMPrintingExpandedStateForPrint 2>/dev/null || true")
            notify(title: "Pencereler", subtitle: "Kayıt Pencereleri Kompakt", message: "Kayıt diyalogları standart boyutta açılacak.")
        } else {
            shell("defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode -bool true; defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode2 -bool true; defaults write NSGlobalDomain PMPrintingExpandedStateForPrint -bool true; defaults write NSGlobalDomain PMPrintingExpandedStateForPrint2 -bool true")
            notify(title: "Pencereler", subtitle: "Genişletilmiş Pencereler Aktif", message: "Kayıt ve yazdırma pencerelerinde klasör ağacı otomatik açık gelecek.")
        }
        refreshMenu()
    }
    
    @objc func toggleWifiPowerSave() {
        let current = (shell("defaults read /Library/Preferences/SystemConfiguration/com.apple.airport.opp.plist WiFiPowerManagement 2>/dev/null").output == "0")
        if current {
            shell("sudo defaults delete /Library/Preferences/SystemConfiguration/com.apple.airport.opp.plist WiFiPowerManagement 2>/dev/null || true")
            notify(title: "Wi-Fi", subtitle: "Güç Tasarrufu Açık", message: "Kablosuz kart standart güç moduna alındı.")
        } else {
            shell("sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.airport.opp.plist WiFiPowerManagement -bool false")
            notify(title: "Wi-Fi", subtitle: "Güç Tasarrufu Kapatıldı (Düşük Ping)", message: "SSH ve online oyunlarda paket gecikmesi/jitter engellendi.")
        }
        refreshMenu()
    }
    
    @objc func toggleAcNeverSleep() {
        let current = (shell("pmset -g custom 2>/dev/null | grep -E '^AC Power:' -A 10 | grep 'sleep[[:space:]]+0'").exitCode == 0)
        if current {
            shell("sudo pmset -c sleep 10")
            notify(title: "Güç", subtitle: "Prizde Uyku Açık", message: "Adaptör takılıyken 10 dk sonra uykuya geçecek.")
        } else {
            shell("sudo pmset -c sleep 0")
            notify(title: "Güç", subtitle: "Uykusuz Mod Aktif (Amphetamine)", message: "Prizde iken arka plan indirme ve işlemler asla uyumayacak.")
        }
        refreshMenu()
    }
    
    @objc func toggleClamshellSleep() {
        let current = (shell("pmset -g | grep 'disablesleep[[:space:]]+1'").exitCode == 0)
        if current {
            shell("sudo pmset -a disablesleep 0")
            notify(title: "Güç", subtitle: "Kapak Uyku Modu Açık", message: "Kapak kapatılınca MacBook uykuya geçecek.")
        } else {
            shell("sudo pmset -a disablesleep 1")
            notify(title: "Güç", subtitle: "Kapak Kapalıyken Çalışma Aktif", message: "Kapak kapalıyken indirme ve render işlemleri kesilmeyecek.")
        }
        refreshMenu()
    }
    
    @objc func toggleStartupMute() {
        let current = (shell("nvram StartupMute 2>/dev/null").output.contains("%01"))
        if current {
            shell("sudo nvram StartupMute=%00")
            notify(title: "Donanım", subtitle: "Başlangıç Sesi Açık", message: "Mac açılışında gong sesi çalacak.")
        } else {
            shell("sudo nvram StartupMute=%01")
            notify(title: "Donanım", subtitle: "Başlangıç Sesi Susturuldu", message: "Mac açılış ve yeniden başlatma gong sesi kapatıldı.")
        }
        refreshMenu()
    }
    
    @objc func toggleSnapDelay() {
        let current = (shell("defaults read com.apple.WindowManager TilingWindowPreviewDelay 2>/dev/null").output == "0")
        if current {
            shell("defaults delete com.apple.WindowManager TilingWindowPreviewDelay && killall WindowManager")
            notify(title: "Tahoe", subtitle: "Snap Önizleme Gecikmesi Standart", message: "Pencere kenar önizleme süresi sıfırlandı.")
        } else {
            shell("defaults write com.apple.WindowManager TilingWindowPreviewDelay -float 0 && killall WindowManager")
            notify(title: "Tahoe", subtitle: "Sıfır Gecikmeli Snap Önizleme", message: "Pencereler ekran kenarına yaklaştırılınca anında yapışacak.")
        }
        refreshMenu()
    }
    
    @objc func toggleSnapDividers() {
        let current = (shell("defaults read com.apple.WindowManager ShowTilingSnapDividers 2>/dev/null").output == "0")
        if current {
            shell("defaults delete com.apple.WindowManager ShowTilingSnapDividers && killall WindowManager")
            notify(title: "Tahoe", subtitle: "Ayırıcı Çizgiler Açık", message: "Döşenen pencereler arasında gri ayırıcı çizgi gösterilecek.")
        } else {
            shell("defaults write com.apple.WindowManager ShowTilingSnapDividers -bool false && killall WindowManager")
            notify(title: "Tahoe", subtitle: "Ayırıcı Çizgiler Kaldırıldı", message: "Pencereler arasında temiz, çizgisiz görünüm sağlandı.")
        }
        refreshMenu()
    }
    
    @objc func toggleSpotlightLocalFirst() {
        let current = (shell("defaults read com.apple.Spotlight LookupServerDisableRemoteQueries 2>/dev/null").output == "1")
        if current {
            shell("defaults delete com.apple.Spotlight LookupServerDisableRemoteQueries 2>/dev/null; killall Spotlight")
            notify(title: "Spotlight", subtitle: "Web Önerileri Açık", message: "Spotlight aramalarında internet önerileri gösterilecek.")
        } else {
            shell("defaults write com.apple.Spotlight LookupServerDisableRemoteQueries -bool true && killall Spotlight")
            notify(title: "Spotlight", subtitle: "Yerel Öncelikli Arama", message: "Web aramaları kapatıldı, yerel dosya ve projelere öncelik verildi.")
        }
        refreshMenu()
    }
    
    @objc func toggleSpotlightDirectMath() {
        let current = readBoolDefault(domain: "com.apple.Spotlight", key: "DirectMathEvaluation")
        if current {
            shell("defaults delete com.apple.Spotlight DirectMathEvaluation 2>/dev/null; killall Spotlight")
            notify(title: "Spotlight", subtitle: "Matematik Çözücü Standart", message: "Spotlight standart hesaplayıcı moduna döndü.")
        } else {
            shell("defaults write com.apple.Spotlight DirectMathEvaluation -bool true && killall Spotlight")
            notify(title: "Spotlight", subtitle: "Anında Matematik Çözücü", message: "Spotlight formül ve döviz hesaplamalarını anında öne çıkaracak.")
        }
        refreshMenu()
    }
    
    @objc func toggleCompactMenubar() {
        let current = (shell("defaults -currentHost read -globalDomain NSStatusItemSpacing 2>/dev/null").output == "6")
        if current {
            shell("defaults -currentHost delete -globalDomain NSStatusItemSpacing 2>/dev/null; defaults -currentHost delete -globalDomain NSStatusItemSelectionPadding 2>/dev/null; killall SystemUIServer")
            notify(title: "Menü Çubuğu", subtitle: "Standart Boşluk", message: "Menü çubuğu simgeleri fabrika aralığına döndü.")
        } else {
            shell("defaults -currentHost write -globalDomain NSStatusItemSpacing -int 6; defaults -currentHost write -globalDomain NSStatusItemSelectionPadding -int 4; killall SystemUIServer")
            notify(title: "Menü Çubuğu", subtitle: "Kompakt Mod Aktif (Notch Optimizasyonu)", message: "Menü çubuğu ikon boşlukları sıkıştırılarak daha çok simge sığdırıldı.")
        }
        refreshMenu()
    }
    
    @objc func toggleWritingToolsDelay() {
        let current = (shell("defaults read NSGlobalDomain WritingToolsShowDelay 2>/dev/null").output == "0")
        if current {
            shell("defaults delete NSGlobalDomain WritingToolsShowDelay 2>/dev/null || true")
            notify(title: "Apple Intelligence", subtitle: "Yazma Araçları Standart", message: "Yazma araçları menü gecikmesi sıfırlandı.")
        } else {
            shell("defaults write NSGlobalDomain WritingToolsShowDelay -float 0")
            notify(title: "Apple Intelligence", subtitle: "Sıfır Gecikmeli Yazma Araçları", message: "Metin seçildiğinde Apple Intelligence menüsü anında açılacak.")
        }
        refreshMenu()
    }
    
    // MARK: - Actions
    @objc func actionFlushDNS() {
        _ = shell("sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder 2>/dev/null || true")
        notify(title: "macOSCode", subtitle: "🧹 DNS Önbelleği Temizlendi", message: "Yerel DNS önbelleği ve mDNSResponder servisi başarıyla sıfırlandı.")
    }
    
    @objc func actionRestartWifi() {
        _ = shell("networksetup -setairportpower en0 off && sleep 1 && networksetup -setairportpower en0 on 2>/dev/null || true")
        notify(title: "macOSCode", subtitle: "📶 Wi-Fi Yeniden Başlatıldı", message: "Kablosuz ağ kartı kapatılıp tekrar devreye alındı.")
    }
    
    @objc func actionRestartBluetooth() {
        _ = shell("sudo pkill bluetoothd 2>/dev/null || true")
        notify(title: "macOSCode", subtitle: "🎧 Bluetooth Yeniden Başlatıldı", message: "Bluetooth arka plan servisi (bluetoothd) sıfırlandı.")
    }
    
    @objc func actionCleanSleepImage() {
        _ = shell("sudo rm -f /var/vm/sleepimage 2>/dev/null || true")
        notify(title: "macOSCode", subtitle: "💾 Sleep Image Temizlendi", message: "Dahili SSD'de uyku bellek dosyası silinerek alan açıldı.")
    }
    
    @objc func actionApplyAll() {
        _ = shell("mc --apply-all 2>/dev/null || true")
        notify(title: "macOSCode", subtitle: "🚀 Master Setup Tamamlandı", message: "Tüm 100 power-user optimizasyonu başarıyla uygulandı!")
        refreshMenu()
    }
    
    @objc func actionRevertAll() {
        _ = shell("mc --revert-all 2>/dev/null || true")
        notify(title: "macOSCode", subtitle: "⏪ Fabrika Ayarlarına Dönüldü", message: "Tüm ayarlar orijinal Apple varsayılanına döndürüldü.")
        refreshMenu()
    }
    
    @objc func openTerminalMC() {
        let appleScript = """
        tell application "Terminal"
            activate
            do script "mc"
        end tell
        """
        if let script = NSAppleScript(source: appleScript) {
            var error: NSDictionary?
            script.executeAndReturnError(&error)
        }
    }
    
    @objc func openWebSite() {
        if let url = URL(string: "https://jarvis322.github.io/macoscode/") {
            NSWorkspace.shared.open(url)
        }
    }
    
    @objc func refreshClicked() {
        refreshMenu()
        notify(title: "macOSCode", subtitle: "🔄 Durum Güncellendi", message: "Tüm sistem ayarlarının canlı durumları yenilendi.")
    }
    
    @objc func quitApp() {
        NSApp.terminate(nil)
    }
}

// MARK: - Main Application Run
let app = NSApplication.shared
let delegate = MenuBarAppDelegate()
app.delegate = delegate
app.run()
