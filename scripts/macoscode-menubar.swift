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
        
        // Header
        let titleItem = NSMenuItem(title: "🚀 macOSCode Power Tweaks", action: nil, keyEquivalent: "")
        titleItem.attributedTitle = NSAttributedString(
            string: "🚀 macOSCode Power Tweaks",
            attributes: [.font: NSFont.boldSystemFont(ofSize: 13)]
        )
        menu.addItem(titleItem)
        
        let subtitleItem = NSMenuItem(title: "Hızlı Ayarlar & Sistem Optimizasyonu", action: nil, keyEquivalent: "")
        subtitleItem.attributedTitle = NSAttributedString(
            string: "Hızlı Ayarlar & Sistem Optimizasyonu",
            attributes: [.font: NSFont.systemFont(ofSize: 11), .foregroundColor: NSColor.secondaryLabelColor]
        )
        menu.addItem(subtitleItem)
        menu.addItem(NSMenuItem.separator())
        
        // 1. Hidden Files
        let hiddenFilesActive = readBoolDefault(domain: "com.apple.finder", key: "AppleShowAllFiles")
        let hiddenItem = NSMenuItem(
            title: "Gizli Dosyaları Göster (.dotfiles)",
            action: #selector(toggleHiddenFiles),
            keyEquivalent: "h"
        )
        hiddenItem.target = self
        hiddenItem.state = hiddenFilesActive ? .on : .off
        menu.addItem(hiddenItem)
        
        // 2. File Extensions
        let extActive = readBoolDefault(domain: "NSGlobalDomain", key: "AppleShowAllExtensions")
        let extItem = NSMenuItem(
            title: "Tüm Dosya Uzantılarını Göster (.json, .env)",
            action: #selector(toggleExtensions),
            keyEquivalent: "e"
        )
        extItem.target = self
        extItem.state = extActive ? .on : .off
        menu.addItem(extItem)
        
        // 3. Desktop Icons
        let desktopIconsRes = shell("defaults read com.apple.finder CreateDesktop 2>/dev/null")
        let desktopIconsHidden = (desktopIconsRes.exitCode == 0 && desktopIconsRes.output == "0")
        let desktopItem = NSMenuItem(
            title: "Masaüstü Simgelerini Göster",
            action: #selector(toggleDesktopIcons),
            keyEquivalent: "d"
        )
        desktopItem.target = self
        desktopItem.state = desktopIconsHidden ? .off : .on
        menu.addItem(desktopItem)
        
        // 4. Dock Autohide Delay
        let dockDelayRes = shell("defaults read com.apple.dock autohide-delay 2>/dev/null")
        let dockZeroDelay = (dockDelayRes.exitCode == 0 && dockDelayRes.output == "0")
        let dockItem = NSMenuItem(
            title: "Dock Sıfır Gecikmeli Hızlı Açılış",
            action: #selector(toggleDockSpeed),
            keyEquivalent: ""
        )
        dockItem.target = self
        dockItem.state = dockZeroDelay ? .on : .off
        menu.addItem(dockItem)
        
        // 5. Reduce Motion
        let motionActive = readBoolDefault(domain: "com.apple.universalaccess", key: "reduceMotion")
        let motionItem = NSMenuItem(
            title: "Hareketi Azalt (Reduce Motion Hızlandırma)",
            action: #selector(toggleReduceMotion),
            keyEquivalent: ""
        )
        motionItem.target = self
        motionItem.state = motionActive ? .on : .off
        menu.addItem(motionItem)
        
        // 6. Quick Look Text Selection
        let qlActive = readBoolDefault(domain: "com.apple.finder", key: "QLEnableTextSelection")
        let qlItem = NSMenuItem(
            title: "Quick Look Önizlemede Metin Seçimi",
            action: #selector(toggleQLText),
            keyEquivalent: ""
        )
        qlItem.target = self
        qlItem.state = qlActive ? .on : .off
        menu.addItem(qlItem)
        
        // 7. Gatekeeper Quarantine Prompt
        let quarantineRes = shell("defaults read com.apple.LaunchServices LSQuarantine 2>/dev/null")
        let quarantineDisabled = (quarantineRes.exitCode == 0 && quarantineRes.output == "0")
        let quarantineItem = NSMenuItem(
            title: "İndirilen Dosya Karantina Uyarısını Atla",
            action: #selector(toggleQuarantine),
            keyEquivalent: ""
        )
        quarantineItem.target = self
        quarantineItem.state = quarantineDisabled ? .on : .off
        menu.addItem(quarantineItem)
        
        menu.addItem(NSMenuItem.separator())
        
        // Actions Header
        let actionsLabel = NSMenuItem(title: "Hızlı İşlemler (Actions)", action: nil, keyEquivalent: "")
        actionsLabel.attributedTitle = NSAttributedString(
            string: "⚡ Hızlı Araçlar",
            attributes: [.font: NSFont.boldSystemFont(ofSize: 11), .foregroundColor: NSColor.secondaryLabelColor]
        )
        menu.addItem(actionsLabel)
        
        // Flush DNS
        let flushItem = NSMenuItem(title: "🧹 DNS Önbelleğini Temizle (Flush DNS)", action: #selector(flushDNS), keyEquivalent: "")
        flushItem.target = self
        menu.addItem(flushItem)
        
        // Open mc in Terminal
        let openMcItem = NSMenuItem(title: "🎛️ Terminal'de 'mc' TUI Başlat", action: #selector(openTerminalMC), keyEquivalent: "t")
        openMcItem.target = self
        menu.addItem(openMcItem)
        
        // Open Web App
        let openWebItem = NSMenuItem(title: "🌐 macOSCode Web Sitesini Aç", action: #selector(openWebSite), keyEquivalent: "w")
        openWebItem.target = self
        menu.addItem(openWebItem)
        
        menu.addItem(NSMenuItem.separator())
        
        // Refresh & Quit
        let refreshItem = NSMenuItem(title: "🔄 Menüyü Yenile", action: #selector(refreshClicked), keyEquivalent: "r")
        refreshItem.target = self
        menu.addItem(refreshItem)
        
        let quitItem = NSMenuItem(title: "❌ Menü Bar Aracını Kapat", action: #selector(quitApp), keyEquivalent: "q")
        quitItem.target = self
        menu.addItem(quitItem)
        
        statusItem.menu = menu
    }
    
    // MARK: - Actions
    @objc func toggleHiddenFiles() {
        let current = readBoolDefault(domain: "com.apple.finder", key: "AppleShowAllFiles")
        if current {
            shell("defaults delete com.apple.finder AppleShowAllFiles && killall Finder")
        } else {
            shell("defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder")
        }
        refreshMenu()
    }
    
    @objc func toggleExtensions() {
        let current = readBoolDefault(domain: "NSGlobalDomain", key: "AppleShowAllExtensions")
        if current {
            shell("defaults delete NSGlobalDomain AppleShowAllExtensions && killall Finder")
        } else {
            shell("defaults write NSGlobalDomain AppleShowAllExtensions -bool true && killall Finder")
        }
        refreshMenu()
    }
    
    @objc func toggleDesktopIcons() {
        let currentRes = shell("defaults read com.apple.finder CreateDesktop 2>/dev/null")
        let isHidden = (currentRes.exitCode == 0 && currentRes.output == "0")
        if isHidden {
            shell("defaults delete com.apple.finder CreateDesktop && killall Finder")
        } else {
            shell("defaults write com.apple.finder CreateDesktop -bool false && killall Finder")
        }
        refreshMenu()
    }
    
    @objc func toggleDockSpeed() {
        let dockDelayRes = shell("defaults read com.apple.dock autohide-delay 2>/dev/null")
        let isZero = (dockDelayRes.exitCode == 0 && dockDelayRes.output == "0")
        if isZero {
            shell("defaults delete com.apple.dock autohide-delay && defaults delete com.apple.dock autohide-time-modifier && killall Dock")
        } else {
            shell("defaults write com.apple.dock autohide-delay -float 0 && defaults write com.apple.dock autohide-time-modifier -float 0.3 && killall Dock")
        }
        refreshMenu()
    }
    
    @objc func toggleReduceMotion() {
        let current = readBoolDefault(domain: "com.apple.universalaccess", key: "reduceMotion")
        if current {
            shell("defaults delete com.apple.universalaccess reduceMotion 2>/dev/null || true")
        } else {
            shell("defaults write com.apple.universalaccess reduceMotion -bool true")
        }
        refreshMenu()
    }
    
    @objc func toggleQLText() {
        let current = readBoolDefault(domain: "com.apple.finder", key: "QLEnableTextSelection")
        if current {
            shell("defaults delete com.apple.finder QLEnableTextSelection && killall Finder")
        } else {
            shell("defaults write com.apple.finder QLEnableTextSelection -bool true && killall Finder")
        }
        refreshMenu()
    }
    
    @objc func toggleQuarantine() {
        let quarantineRes = shell("defaults read com.apple.LaunchServices LSQuarantine 2>/dev/null")
        let isDisabled = (quarantineRes.exitCode == 0 && quarantineRes.output == "0")
        if isDisabled {
            shell("defaults delete com.apple.LaunchServices LSQuarantine 2>/dev/null || true")
        } else {
            shell("defaults write com.apple.LaunchServices LSQuarantine -bool false")
        }
        refreshMenu()
    }
    
    @objc func flushDNS() {
        _ = shell("sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder 2>/dev/null || true")
        let alert = NSAlert()
        alert.messageText = "DNS Önbelleği Temizlendi"
        alert.informativeText = "Yerel macOS DNS önbelleği ve mDNSResponder başarıyla sıfırlandı."
        alert.alertStyle = .informational
        alert.runModal()
    }
    
    @objc func openTerminalMC() {
        let appleScript = """
        tell application "Terminal"
            activate
            do script "mc || python3 ~/Desktop/macoscode/scripts/mc"
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
