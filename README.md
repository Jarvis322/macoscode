# 🚀 macOS 100 Power-User Tweaks & Interactive CLI Cheatsheet (2026)

[🇬🇧 English Documentation](README.md) • [🇹🇷 Türkçe Dokümantasyon](README_TR.md)

[![GitHub Pages](https://img.shields.io/badge/Live-Web%20App-brightgreen?style=for-the-badge&logo=github)](https://jarvis322.github.io/macoscode/)
[![Interactive TUI](https://img.shields.io/badge/Interactive-TUI%20%2F%20CLI-purple?style=for-the-badge&logo=gnubash)](scripts/mc)
[![macOS Tahoe Ready](https://img.shields.io/badge/macOS-Tahoe%20%26%20Sequoia-blue?style=for-the-badge&logo=apple)](https://jarvis322.github.io/macoscode/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/Jarvis322/macoscode?style=for-the-badge)](https://github.com/Jarvis322/macoscode/stargazers)

> **Live Web Application:** [https://jarvis322.github.io/macoscode/](https://jarvis322.github.io/macoscode/)  
> **Terminal CLI (Interactive TUI):** `curl -sSL https://raw.githubusercontent.com/Jarvis322/macoscode/main/scripts/mc | python3`

A curated, battle-tested collection of **100 verified `defaults write` and Terminal optimizations** to elevate macOS system performance, window management, Dock/Finder responsiveness, battery health, and developer ergonomics.

Includes an **Interactive Terminal UI (TUI/CLI)** with instant self-update capabilities, standalone **1-click revert commands**, 1-line **Master Setup/Reset** scripts, and an in-browser **Custom Bash Script Generator** with inline revert comments.

---

## ⚡ Quick Start

### 1. 🎛️ Interactive Terminal UI (TUI / CLI)

#### 🍺 Install via Homebrew:
```bash
brew tap Jarvis322/macoscode
brew install macoscode
```

#### ⚡ Or Run Instantly Without Installing:
```bash
curl -sSL https://raw.githubusercontent.com/Jarvis322/macoscode/main/scripts/mc | python3
```

> **Tip (Alternative 1-Line Installer):**
> ```bash
> mkdir -p ~/.local/bin && curl -sSL https://raw.githubusercontent.com/Jarvis322/macoscode/main/scripts/mc -o ~/.local/bin/mc && cp ~/.local/bin/mc ~/.local/bin/macoscode && chmod +x ~/.local/bin/mc ~/.local/bin/macoscode
> ```

```bash
mc                     # Launch interactive TUI menu
mc --apply-all         # Apply all 100 optimizations in a single command
mc --revert-all        # Restore all settings to Apple factory defaults
mc --status            # Scan system configuration status (Audit Report)
mc --preset dev        # Run optimization suites (dev | speed | battery | tahoe)
mc --menubar           # Launch native macOS Menu Bar companion toggle app (⚡)
mc --search dock       # Search tweaks matching keyword in terminal
mc --lang en           # Set active language preference (en | tr)
mc --update            # Self-update 'mc' CLI to the latest GitHub release
mc --dry-run           # Preview commands without executing changes
```

---

### 2. ⚡ Native macOS Menu Bar Companion App
Prefer toggling daily developer tweaks (Hidden Files, File Extensions, Desktop Icons, Reduce Motion, Dock Speed) right from your macOS status bar?

* **Launch via CLI:** `mc --menubar`
* **Or Run Directly in Swift:** `swift scripts/macoscode-menubar.swift &`
* **SwiftBar / xbar Plugin:** Simply copy `scripts/macoscode.1m.sh` to your SwiftBar plugins folder.

---

### 2. 1-Line Master Setup & Reset Scripts

#### 🚀 Apply All 100 Optimizations at Once (Master Setup)
```bash
curl -sSL https://raw.githubusercontent.com/Jarvis322/macoscode/main/scripts/macos-power-setup.sh | bash
```

#### ⏪ Restore All Settings to Apple Factory Defaults (Master Reset)
```bash
curl -sSL https://raw.githubusercontent.com/Jarvis322/macoscode/main/scripts/macos-power-revert.sh | bash
```

---

## ✨ Key Features

- 🎛️ **Interactive CLI (`mc`):** Arrow-key navigation, Space toggle selection, System Audit health checks, and live keyword search.
- 🔄 **Self-Updating Engine:** Seamless `mc --update` checks GitHub releases and upgrades local binaries with version locking.
- 🚀 **100 Verified Power-User Tweaks:** Curated for Terminal, Finder, Dock, Keyboard/Trackpad, Xcode, Safari, Privacy, and macOS Tahoe.
- 🔐 **Touch ID for Sudo:** Instant biometric authentication in terminal without typing passwords.
- 🏔️ **macOS Tahoe & Apple Intelligence:** Writing Tools delay removal, local-first Spotlight search, and iPhone Mirroring notification grouping.
- 📦 **Custom Script Generator:** Select any tweak combination on the web app to download personalized `custom-macos-setup.sh` and `custom-macos-revert.sh` scripts.
- ⭐ **Favorites System:** Bookmark your most-used commands locally in browser storage.
- 🔍 **Live Search & Smart Filtering:** `⌘ + K` or `/` hotkeys to search commands with collapsible tag filters.
- 🌐 **Full Bilingual Support:** Instant Turkish ⟷ English localization across the Web App, CLI, and Documentation.
- 🎨 **Ultra-Premium Glassmorphic UI:** Inspired by macOS Tahoe aesthetics with responsive cards, micro-interactions, and dark mode.

---

## 📂 Categories

1. **💻 Terminal & Shell:** Persistent hostname, Zsh comment parsing, Touch ID sudo authorization, disable Homebrew analytics.
2. **📁 Finder & File Management:** Show all file extensions, reveal hidden files, disable `.DS_Store` on USB/network shares, POSIX window paths, Quick Look text selection.
3. **🪟 Windows, Desktop & Dock:** Zero Dock delay, fluid Suck minimize animation, Mission Control window grouping, borderless window tiling.
4. **⌨️ Keyboard, Trackpad & Input:** Maximum key repeat rate, disable accent menu delays, tap-to-click, three-finger drag.
5. **⚡ Developer, Security & System:** Xcode build timers, Safari Web Inspector, mute startup chime, JPG screenshots, disable quarantine popups.
6. **🏔️ macOS Tahoe & AI:** Snap tiling preview speed, Stage Manager transition acceleration, notch menubar compression, Game Mode boost.
7. **🔋 Network, Power & Maintenance:** Low-latency Wi-Fi, prevent clamshell sleep, instant DNS flush, fast hibernation, 80% charge limit optimization.

---

## 🛠️ Local Development

To run the web application locally:

```bash
git clone https://github.com/Jarvis322/macoscode.git
cd macoscode
open index.html
```

or with any static HTTP server:

```bash
npx serve .
# or
python3 -m http.server 8000
```

---

## 📄 License

This project is open-source under the [MIT](LICENSE) License.  
Feel free to use, customize, and share!
