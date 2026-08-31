#!/usr/bin/env python3
import json
import os

with open('scripts/tweaks.json', 'r', encoding='utf-8') as f:
    tweaks_data = json.load(f)

script_template = r'''#!/usr/bin/env python3
# ==============================================================================
#  ███╗   ███╗ █████╗  ██████╗ ██████╗ ███████╗ ██████╗ ██████╗ ██████╗ ███████╗
#  ████╗ ████║██╔══██╗██╔════╝██╔═══██╗██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝
#  ██╔████╔██║███████║██║     ██║   ██║███████╗██║     ██║   ██║██║  ██║█████╗  
#  ██║╚██╔╝██║██╔══██║██║     ██║   ██║╚════██║██║     ██║   ██║██║  ██║██╔══╝  
#  ██║ ╚═╝ ██║██║  ██║╚██████╗╚██████╔╝███████║╚██████╗╚██████╔╝██████╔╝███████╗
#  ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
#
#  🚀 macOSCode (mc) - Interactive Terminal UI & macOS Power-User Tool
#  macOS Tahoe & Apple Silicon Power-Tweaks Engine
#  Repository: https://github.com/Jarvis322/macoscode
#  Web App: https://jarvis322.github.io/macoscode/
# ==============================================================================

import sys
import os
import re
import json
import subprocess
import shutil
import time
import argparse

# Reopen /dev/tty if stdin is piped (e.g., curl ... | python3)
if not sys.stdin.isatty():
    try:
        sys.stdin = open('/dev/tty', 'r')
    except Exception:
        pass

# Terminal Colors & Styles (ANSI)
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    
    # Colors
    CYAN = "\033[38;2;56;189;248m"
    BLUE = "\033[38;2;99;102;241m"
    INDIGO = "\033[38;2;79;70;229m"
    PURPLE = "\033[38;2;168;85;247m"
    EMERALD = "\033[38;2;16;185;129m"
    ROSE = "\033[38;2;244;63;94m"
    GOLD = "\033[38;2;251;191;36m"
    GRAY = "\033[38;2;148;163;184m"
    DARK_GRAY = "\033[38;2;100;116;139m"
    WHITE = "\033[38;2;248;250;252m"
    
    # Backgrounds
    BG_CARD = "\033[48;2;15;23;42m"
    BG_CYAN = "\033[48;2;14;116;144m"
    BG_BLUE = "\033[48;2;67;56;202m"
    BG_EMERALD = "\033[48;2;6;95;70m"
    BG_ROSE = "\033[48;2;159;18;57m"

# 100 TWEAKS DATASET
TWEAKS = __TWEAKS_JSON_PLACEHOLDER__

CATEGORIES = [
    {"id": "terminal", "name": "Terminal, Zsh & Kabuk", "icon": "💻"},
    {"id": "finder", "name": "Finder & Dosya Yönetimi", "icon": "📁"},
    {"id": "window_dock", "name": "Pencere, Masaüstü & Dock", "icon": "🪟"},
    {"id": "keyboard_input", "name": "Klavye, Trackpad & Donanım", "icon": "⌨️"},
    {"id": "dev_security", "name": "Geliştirici, Güvenlik & Sistem", "icon": "⚡"},
    {"id": "tahoe", "name": "macOS Tahoe & AI Optimizasyonları", "icon": "🏔️"},
    {"id": "network_power", "name": "Ağ, Güç Yönetimi & Bakım", "icon": "🔋"},
]

PRESETS = {
    "dev": {
        "title": "Geliştirici Güç Paketi (Developer Power Pack)",
        "desc": "Xcode derleme sayacı, Safari geliştirici araçları, sudo Touch ID ve POSIX dosya yolları.",
        "ids": [
            "term-touchid-sudo", "term-interactive-comments", "find-all-extensions",
            "find-hidden-files", "find-posix-title", "find-quicklook-text",
            "dev-xcode-build-duration", "safari-enable-develop-menu", "safari-show-full-url",
            "sys-expand-save-print-panels", "sys-disable-crash-reporter", "sec-disable-quarantine",
            "key-full-keyboard-access", "key-fast-repeat", "key-disable-press-hold"
        ]
    },
    "speed": {
        "title": "Maksimum Hız & 0s Animasyon Paketi (FPS & UI Speed)",
        "desc": "Dock gecikmesini sıfırlama, pencereleri anında boyutlandırma, hızlı klavye tekrarı ve akıcı geçişler.",
        "ids": [
            "dock-autohide-speed", "dock-suck-effect", "dock-fast-expose-anim",
            "dock-no-recent-apps", "win-fast-resize", "find-quicklook-fast-zoom",
            "win-top-drag-restore", "win-remove-tiling-margins", "ui-reduce-motion",
            "key-fast-repeat"
        ]
    },
    "battery": {
        "title": "Pil Tasarrufu & Isı Koruma Paketi (Battery & Thermal Saver)",
        "desc": "Pilde otomatik Düşük Güç Modu, %80 pil sağlığı koruması, Power Nap kapatma ve hızlı uyku.",
        "ids": [
            "pwr-low-power-mode-battery-only", "pwr-charge-limit-80", "pwr-fast-hibernation",
            "sec-disable-apple-analytics", "hw-keyboard-backlight-dim", "find-no-ds-store-network",
            "net-disable-captive-portal"
        ]
    },
    "tahoe": {
        "title": "macOS Tahoe & Apple Intelligence Paketi",
        "desc": "Pencere döşeme önizlemesini hızlandırma, Writing Tools gecikmesini sıfırlama ve yerel Spotlight önceliği.",
        "ids": [
            "tahoe-tiling-preview-delay", "tahoe-hide-snap-dividers", "tahoe-writing-tools-delay",
            "tahoe-spotlight-local-first", "tahoe-mirror-group-notifications", "tahoe-compact-menubar-spacing",
            "tahoe-fast-stage-manager", "tahoe-game-mode-auto-boost", "tahoe-passwords-instant-autofill"
        ]
    }
}

# Raw Key Reader for Interactive TUI
def get_key():
    try:
        import termios, tty
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'A': return 'UP'
                    elif ch3 == 'B': return 'DOWN'
                    elif ch3 == 'C': return 'RIGHT'
                    elif ch3 == 'D': return 'LEFT'
                    elif ch3 == 'H': return 'HOME'
                    elif ch3 == 'F': return 'END'
                    elif ch3 == '3':
                        sys.stdin.read(1) # consume ~
                        return 'DEL'
                return 'ESC'
            elif ch == '\r' or ch == '\n':
                return 'ENTER'
            elif ch == ' ':
                return 'SPACE'
            elif ch == '\x7f' or ch == '\x08':
                return 'BACKSPACE'
            elif ch == '\x03': # Ctrl+C
                return 'CTRL_C'
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    except Exception:
        # Fallback for non-raw environment
        line = sys.stdin.readline().strip()
        return line if line else 'ENTER'

def clear_screen():
    print("\033[2J\033[H", end="")

def print_banner():
    banner = f"""{C.CYAN}{C.BOLD}
  ███╗   ███╗ █████╗  ██████╗ ██████╗ ███████╗ ██████╗ ██████╗ ██████╗ ███████╗
  ████╗ ████║██╔══██╗██╔════╝██╔═══██╗██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝
  ██╔████╔██║███████║██║     ██║   ██║███████╗██║     ██║   ██║██║  ██║█████╗  
  ██║╚██╔╝██║██╔══██║██║     ██║   ██║╚════██║██║     ██║   ██║██║  ██║██╔══╝  
  ██║ ╚═╝ ██║██║  ██║╚██████╗╚██████╔╝███████║╚██████╗╚██████╔╝██████╔╝███████╗
  ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝{C.RESET}
  {C.PURPLE}{C.BOLD}⚡ macOS Interactive Terminal CLI & TUI • 100 Power-Tweaks (v2.0){C.RESET}
  {C.DARK_GRAY}https://github.com/Jarvis322/macoscode • Tahoe & Apple Silicon Ready{C.RESET}
"""
    print(banner)

def refresh_services():
    services = ["Finder", "Dock", "WindowManager", "SystemUIServer", "Spotlight"]
    print(f"\n{C.CYAN}🔄 macOS Sistem servisleri yenileniyor...{C.RESET}")
    for s in services:
        subprocess.run(f"killall {s} 2>/dev/null || true", shell=True)
    time.sleep(0.5)

def run_command(cmd, dry_run=False):
    if dry_run:
        print(f"{C.GRAY}[DRY-RUN]{C.RESET} {cmd}")
        return True
    try:
        res = subprocess.run(cmd, shell=True, check=False)
        return res.returncode == 0
    except Exception as e:
        print(f"{C.ROSE}Hata:{C.RESET} {e}")
        return False

# Audit Check for a tweak
def check_tweak_status(tweak):
    apply_cmd = tweak["apply"]
    # Look for defaults write
    m = re.search(r"defaults write\s+([^\s]+)\s+([^\s]+)\s+(-\w+)\s+(.+)", apply_cmd)
    if m:
        domain, key, vtype, val = m.groups()
        domain = domain.replace('\\', '')
        key = key.replace('"', '').replace("'", "").replace('\\', '')
        val = val.strip().replace('"', '').replace("'", "")
        try:
            res = subprocess.run(f"defaults read {domain} {key} 2>/dev/null", shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                out = res.stdout.strip()
                if vtype == "-bool":
                    target = "1" if val.lower() in ["true", "yes", "1"] else "0"
                    return out.lower() == target or out.lower() == val.lower()
                elif vtype == "-int" or vtype == "-float":
                    return out == val
                return True
            return False
        except Exception:
            return False
    # Check pam_tid.so
    if "pam_tid.so" in apply_cmd:
        try:
            res = subprocess.run("grep -q 'pam_tid.so' /etc/pam.d/sudo 2>/dev/null", shell=True)
            return res.returncode == 0
        except Exception:
            return False
    # Check zsh
    if "INTERACTIVE_COMMENTS" in apply_cmd:
        return False
    return False

# System Audit Dashboard
def run_system_audit():
    clear_screen()
    print_banner()
    print(f"{C.BOLD}{C.CYAN}📊 macOS Sistem Ayarları Denetim Raporu (Audit){C.RESET}")
    print(f"{C.DARK_GRAY}Sisteminizdeki 100 optimizasyonun anlık durumu taranıyor...{C.RESET}\n")

    active_count = 0
    total_count = len(TWEAKS)

    for cat in CATEGORIES:
        cat_tweaks = [t for t in TWEAKS if t["cat"] == cat["id"]]
        print(f"\n{C.BOLD}{cat['icon']} {cat['name']}{C.RESET} {C.DARK_GRAY}({len(cat_tweaks)} Ayar){C.RESET}")
        print("─" * 68)
        for t in cat_tweaks:
            status = check_tweak_status(t)
            if status:
                active_count += 1
                status_badge = f"{C.EMERALD}{C.BOLD}[✔ AKTİF]{C.RESET}"
            else:
                status_badge = f"{C.DARK_GRAY}[  VARSAYILAN  ]{C.RESET}"
            
            title_truncated = t['title'][:44] + "..." if len(t['title']) > 47 else t['title'].ljust(47)
            print(f" {status_badge} {title_truncated} {C.GRAY}[{t['tag']}]{C.RESET}")

    score = int((active_count / total_count) * 100)
    print("\n" + "=" * 68)
    print(f"{C.BOLD}📈 ÖZET: {C.EMERALD}{active_count}{C.RESET}/{total_count} Optimizasyon Aktif ({C.CYAN}%{score} Güç Seviyesi{C.RESET}){C.RESET}")
    print("=" * 68)
    print(f"\n{C.GRAY}Menüye dönmek için herhangi bir tuşa basın...{C.RESET}")
    get_key()

# Batch Apply / Revert
def apply_tweaks_list(tweak_list, mode="apply", dry_run=False):
    action_name = "Uygulanıyor" if mode == "apply" else "Sıfırlanıyor (Revert)"
    color = C.CYAN if mode == "apply" else C.ROSE
    print(f"\n{color}{C.BOLD}🚀 {len(tweak_list)} Ayar {action_name}...{C.RESET}\n")
    
    if not dry_run:
        print(f"{C.GOLD}🔐 Sudo yetkilendirmesi istenebilir...{C.RESET}")
        subprocess.run("sudo -v", shell=True)

    for i, t in enumerate(tweak_list, 1):
        cmd = t["apply"] if mode == "apply" else t["revert"]
        print(f"{C.GRAY}[{i}/{len(tweak_list)}]{C.RESET} {C.BOLD}{t['title']}{C.RESET}")
        if dry_run:
            print(f"   {C.DARK_GRAY}$ {cmd.replace(chr(10), ' && ')}{C.RESET}")
        else:
            run_command(cmd, dry_run=False)

    if not dry_run:
        refresh_services()
        print(f"\n{C.EMERALD}{C.BOLD}✨ İşlem başarıyla tamamlandı! ({len(tweak_list)} Ayar){C.RESET}\n")
    else:
        print(f"\n{C.GOLD}{C.BOLD}✨ [DRY-RUN] Komutlar görüntülendi, sistemde değişiklik yapılmadı.{C.RESET}\n")

# Preset Selector
def run_preset_menu():
    selected_idx = 0
    keys = list(PRESETS.keys())

    while True:
        clear_screen()
        print_banner()
        print(f"{C.BOLD}{C.GOLD}⚡ Hızlı Optimizasyon Paketleri (Presets){C.RESET}\n")

        for idx, k in enumerate(keys):
            p = PRESETS[k]
            cursor = f"{C.CYAN}{C.BOLD}➜{C.RESET}" if idx == selected_idx else " "
            highlight = f"{C.CYAN}{C.BOLD}" if idx == selected_idx else f"{C.WHITE}"
            print(f" {cursor} {highlight}{idx+1}. {p['title']}{C.RESET}")
            print(f"     {C.DARK_GRAY}{p['desc']} ({len(p['ids'])} Ayar){C.RESET}\n")

        print(f"{C.DARK_GRAY}Navigasyon: [↑/↓] Gezin • [Enter] Paketi Seç & Uygula • [r] Paketi Revert Et • [q/Esc] Geri{C.RESET}")

        key = get_key()
        if key in ['UP', 'k']:
            selected_idx = (selected_idx - 1) % len(keys)
        elif key in ['DOWN', 'j']:
            selected_idx = (selected_idx + 1) % len(keys)
        elif key in ['ENTER', 'SPACE']:
            chosen_key = keys[selected_idx]
            chosen_preset = PRESETS[chosen_key]
            tweaks_to_run = [t for t in TWEAKS if t["id"] in chosen_preset["ids"]]
            apply_tweaks_list(tweaks_to_run, mode="apply")
            print(f"\n{C.GRAY}Devam etmek için bir tuşa basın...{C.RESET}")
            get_key()
            break
        elif key == 'r':
            chosen_key = keys[selected_idx]
            chosen_preset = PRESETS[chosen_key]
            tweaks_to_run = [t for t in TWEAKS if t["id"] in chosen_preset["ids"]]
            apply_tweaks_list(tweaks_to_run, mode="revert")
            print(f"\n{C.GRAY}Devam etmek için bir tuşa basın...{C.RESET}")
            get_key()
            break
        elif key in ['q', 'ESC']:
            break

# Interactive Tweak Selector
def run_interactive_selector(category_filter=None):
    if category_filter:
        items = [t for t in TWEAKS if t["cat"] == category_filter]
        cat_obj = next((c for c in CATEGORIES if c["id"] == category_filter), None)
        title = f"{cat_obj['icon']} {cat_obj['name']}" if cat_obj else "Kategori"
    else:
        items = TWEAKS
        title = "Tüm Ayarlar (100-in-1)"

    selected_set = set()
    cursor_idx = 0
    dry_run_mode = False

    while True:
        clear_screen()
        print_banner()
        print(f"{C.BOLD}{C.PURPLE}🎛️ {title}{C.RESET} {C.DARK_GRAY}(Seçili: {len(selected_set)}/{len(items)}){C.RESET}")
        print("─" * 70)

        # Show a window of 10 items
        window_size = 10
        start_idx = max(0, min(cursor_idx - window_size // 2, len(items) - window_size))
        end_idx = min(len(items), start_idx + window_size)

        for idx in range(start_idx, end_idx):
            t = items[idx]
            is_cur = (idx == cursor_idx)
            is_sel = (t["id"] in selected_set)
            
            cursor_mark = f"{C.CYAN}➜{C.RESET}" if is_cur else " "
            check_mark = f"{C.EMERALD}{C.BOLD}[✔]{C.RESET}" if is_sel else f"{C.DARK_GRAY}[ ]{C.RESET}"
            text_style = f"{C.BOLD}{C.WHITE}" if is_cur else f"{C.GRAY}"
            
            tag_badge = f"{C.INDIGO}[{t['tag']}]{C.RESET}"
            title_text = t['title'][:40] + "..." if len(t['title']) > 43 else t['title'].ljust(43)
            print(f" {cursor_mark} {check_mark} {text_style}{title_text}{C.RESET} {tag_badge}")

        # Current Item Detail Card
        cur_tweak = items[cursor_idx]
        print("\n" + f"{C.DARK_GRAY}┌─ Detay ─────────────────────────────────────────────────────────────┐{C.RESET}")
        print(f"{C.DARK_GRAY}│{C.RESET} {C.BOLD}{cur_tweak['title']}{C.RESET}")
        print(f"{C.DARK_GRAY}│{C.RESET} {C.GRAY}{cur_tweak['desc'][:68]}{C.RESET}")
        first_cmd = cur_tweak['apply'].split('\n')[0]
        print(f"{C.DARK_GRAY}│{C.RESET} {C.CYAN}$ {first_cmd[:66]}{C.RESET}")
        print(f"{C.DARK_GRAY}└─────────────────────────────────────────────────────────────────────┘{C.RESET}")

        dry_badge = f"{C.GOLD}[DRY-RUN AÇIK]{C.RESET}" if dry_run_mode else f"{C.DARK_GRAY}[CANLI MOD]{C.RESET}"
        print(f"{C.DARK_GRAY}Navigasyon:{C.RESET} [↑/↓] Gezin • [Space] Seç/Bırak • [a] Tümünü Seç • [d] {dry_badge}")
        print(f"{C.DARK_GRAY}Aksiyonlar:{C.RESET} [Enter] Seçilenleri Uygula • [r] Seçilenleri Sıfırla (Revert) • [q/Esc] Geri")

        key = get_key()
        if key in ['UP', 'k']:
            cursor_idx = (cursor_idx - 1) % len(items)
        elif key in ['DOWN', 'j']:
            cursor_idx = (cursor_idx + 1) % len(items)
        elif key == 'SPACE':
            tid = cur_tweak["id"]
            if tid in selected_set:
                selected_set.remove(tid)
            else:
                selected_set.add(tid)
        elif key == 'a':
            if len(selected_set) == len(items):
                selected_set.clear()
            else:
                selected_set = {t["id"] for t in items}
        elif key == 'd':
            dry_run_mode = not dry_run_mode
        elif key == 'ENTER':
            chosen_tweaks = [t for t in items if t["id"] in selected_set]
            if not chosen_tweaks:
                chosen_tweaks = [cur_tweak]
            apply_tweaks_list(chosen_tweaks, mode="apply", dry_run=dry_run_mode)
            print(f"\n{C.GRAY}Devam etmek için bir tuşa basın...{C.RESET}")
            get_key()
            break
        elif key == 'r':
            chosen_tweaks = [t for t in items if t["id"] in selected_set]
            if not chosen_tweaks:
                chosen_tweaks = [cur_tweak]
            apply_tweaks_list(chosen_tweaks, mode="revert", dry_run=dry_run_mode)
            print(f"\n{C.GRAY}Devam etmek için bir tuşa basın...{C.RESET}")
            get_key()
            break
        elif key in ['q', 'ESC']:
            break

# Category Browser Menu
def run_category_menu():
    selected_idx = 0
    while True:
        clear_screen()
        print_banner()
        print(f"{C.BOLD}{C.CYAN}🎛️  Kategorilere Göre Ayar Gezgini{C.RESET}\n")

        for idx, cat in enumerate(CATEGORIES):
            cat_count = len([t for t in TWEAKS if t["cat"] == cat["id"]])
            cursor = f"{C.CYAN}{C.BOLD}➜{C.RESET}" if idx == selected_idx else " "
            num_styled = f"{C.CYAN}{C.BOLD}[{idx+1}]{C.RESET}" if idx == selected_idx else f"{C.DARK_GRAY}[{idx+1}]{C.RESET}"
            label_styled = f"{C.WHITE}{C.BOLD}{cat['name']}{C.RESET}" if idx == selected_idx else f"{C.GRAY}{cat['name']}{C.RESET}"
            print(f" {cursor} {num_styled} {cat['icon']}  {label_styled} {C.DARK_GRAY}({cat_count} Ayar){C.RESET}")

        print(f"\n{C.DARK_GRAY}Navigasyon: [↑/↓] Gezin • [Enter/Space] Kategoriye Gir • [1-7] Hızlı Tuş • [q/Esc] Geri{C.RESET}")

        key = get_key()
        if key in ['UP', 'k']:
            selected_idx = (selected_idx - 1) % len(CATEGORIES)
        elif key in ['DOWN', 'j']:
            selected_idx = (selected_idx + 1) % len(CATEGORIES)
        elif key in ['ENTER', 'SPACE']:
            chosen_cat = CATEGORIES[selected_idx]["id"]
            run_interactive_selector(category_filter=chosen_cat)
        elif key in ['1', '2', '3', '4', '5', '6', '7']:
            idx = int(key) - 1
            if idx < len(CATEGORIES):
                chosen_cat = CATEGORIES[idx]["id"]
                run_interactive_selector(category_filter=chosen_cat)
        elif key in ['q', 'ESC']:
            break

# Interactive Live Search
def run_search_menu():
    clear_screen()
    print_banner()
    print(f"{C.BOLD}{C.CYAN}🔍  Terminal İçi Ayar Arama{C.RESET}")
    print(f"{C.DARK_GRAY}Aramak istediğiniz anahtar kelimeyi yazın (örn: dock, sudo, finder, tahoe):{C.RESET}\n")
    try:
        query = input(f"{C.BOLD}{C.CYAN}Arama ➜ {C.RESET}").strip().lower()
    except Exception:
        return

    if not query:
        return

    matched = [t for t in TWEAKS if query in t["title"].lower() or query in t["desc"].lower() or query in t["apply"].lower() or query in t["tag"].lower()]
    
    if not matched:
        print(f"\n{C.ROSE}❌ '{query}' ile eşleşen ayar bulunamadı.{C.RESET}")
        time.sleep(1.5)
        return

    # Open selector with matched items
    selected_set = set()
    cursor_idx = 0

    while True:
        clear_screen()
        print_banner()
        print(f"{C.BOLD}{C.CYAN}🔍  '{query}' Arama Sonuçları ({len(matched)} Ayar Bulundu){C.RESET}")
        print("─" * 70)

        for idx, t in enumerate(matched):
            is_cur = (idx == cursor_idx)
            is_sel = (t["id"] in selected_set)
            cursor_mark = f"{C.CYAN}➜{C.RESET}" if is_cur else " "
            check_mark = f"{C.EMERALD}[✔]{C.RESET}" if is_sel else f"{C.DARK_GRAY}[ ]{C.RESET}"
            text_style = f"{C.BOLD}{C.WHITE}" if is_cur else f"{C.GRAY}"
            print(f" {cursor_mark} {check_mark} {text_style}{t['title'][:44]}{C.RESET} {C.DARK_GRAY}[{t['tag']}]{C.RESET}")

        print(f"\n{C.DARK_GRAY}Navigasyon: [↑/↓] • [Space] Seç • [a] Tümünü Seç • [Enter] Uygula • [r] Revert • [q] Geri{C.RESET}")

        key = get_key()
        if key in ['UP', 'k']:
            cursor_idx = (cursor_idx - 1) % len(matched)
        elif key in ['DOWN', 'j']:
            cursor_idx = (cursor_idx + 1) % len(matched)
        elif key == 'SPACE':
            tid = matched[cursor_idx]["id"]
            if tid in selected_set: selected_set.remove(tid)
            else: selected_set.add(tid)
        elif key == 'a':
            if len(selected_set) == len(matched): selected_set.clear()
            else: selected_set = {t["id"] for t in matched}
        elif key == 'ENTER':
            chosen = [t for t in matched if t["id"] in selected_set] or [matched[cursor_idx]]
            apply_tweaks_list(chosen, mode="apply")
            print(f"\n{C.GRAY}Devam etmek için bir tuşa basın...{C.RESET}")
            get_key()
            break
        elif key == 'r':
            chosen = [t for t in matched if t["id"] in selected_set] or [matched[cursor_idx]]
            apply_tweaks_list(chosen, mode="revert")
            print(f"\n{C.GRAY}Devam etmek için bir tuşa basın...{C.RESET}")
            get_key()
            break
        elif key in ['q', 'ESC']:
            break

# Export Custom Bash Scripts
def export_custom_scripts():
    clear_screen()
    print_banner()
    print(f"{C.BOLD}{C.GOLD}📦  Kişiselleştirilmiş Bash Betiği Olarak Kaydet (.sh Export){C.RESET}\n")

    setup_file = "custom-macos-setup.sh"
    revert_file = "custom-macos-revert.sh"

    # Generate Setup
    with open(setup_file, "w", encoding="utf-8") as f:
        f.write(f"#!/usr/bin/env bash\n# macOS Kişiselleştirilmiş Kurulum Betiği (100 Ayar)\nset -e\nsudo -v\n\n")
        for t in TWEAKS:
            f.write(f"# {t['title']}\n# ⏪ Revert: {t['revert']}\n{t['apply']}\n\n")
        f.write("killall Finder Dock WindowManager 2>/dev/null || true\necho '✨ Tamamlandı!'\n")

    # Generate Revert
    with open(revert_file, "w", encoding="utf-8") as f:
        f.write(f"#!/usr/bin/env bash\n# macOS Kişiselleştirilmiş Geri Alma Betiği (100 Ayar)\nset -e\nsudo -v\n\n")
        for t in TWEAKS:
            f.write(f"# {t['title']} (Revert)\n{t['revert']}\n\n")
        f.write("killall Finder Dock WindowManager 2>/dev/null || true\necho '✅ Fabrika varsayılanına döndürüldü!'\n")

    os.chmod(setup_file, 0o755)
    os.chmod(revert_file, 0o755)

    print(f"{C.EMERALD}✔ {setup_file} oluşturuldu.{C.RESET}")
    print(f"{C.EMERALD}✔ {revert_file} oluşturuldu.{C.RESET}")
    print(f"\n{C.CYAN}Bu betikleri doğrudan './{setup_file}' veya './{revert_file}' şeklinde çalıştırabilirsiniz.{C.RESET}")
    print(f"\n{C.GRAY}Menüye dönmek için bir tuşa basın...{C.RESET}")
    get_key()

# Self Installer (mc -> /usr/local/bin or ~/.local/bin)
def install_mc_globally():
    clear_screen()
    print_banner()
    print(f"{C.BOLD}{C.CYAN}⚙️   'mc' Komutunu Global Sisteme Yükle{C.RESET}\n")

    script_path = os.path.abspath(__file__)
    installed = False
    target_dir = "/usr/local/bin"
    target_mc = os.path.join(target_dir, "mc")
    target_macoscode = os.path.join(target_dir, "macoscode")

    try:
        os.makedirs(target_dir, exist_ok=True)
        shutil.copyfile(script_path, target_mc)
        shutil.copyfile(script_path, target_macoscode)
        os.chmod(target_mc, 0o755)
        os.chmod(target_macoscode, 0o755)
        installed = True
        print(f"{C.EMERALD}✔ '{target_mc}' başarıyla kuruldu.{C.RESET}")
        print(f"{C.EMERALD}✔ '{target_macoscode}' başarıyla kuruldu.{C.RESET}")
    except PermissionError:
        print(f"{C.GOLD}🔐 '/usr/local/bin' için yönetici (sudo) izni isteniyor...{C.RESET}")
        res = subprocess.run(f"sudo cp '{script_path}' '{target_mc}' && sudo cp '{script_path}' '{target_macoscode}' && sudo chmod 755 '{target_mc}' '{target_macoscode}'", shell=True)
        if res.returncode == 0:
            installed = True
            print(f"\n{C.EMERALD}✔ '{target_mc}' başarıyla kuruldu.{C.RESET}")
            print(f"{C.EMERALD}✔ '{target_macoscode}' başarıyla kuruldu.{C.RESET}")
        else:
            # Fallback to ~/.local/bin
            user_bin = os.path.expanduser("~/.local/bin")
            os.makedirs(user_bin, exist_ok=True)
            u_mc = os.path.join(user_bin, "mc")
            u_macoscode = os.path.join(user_bin, "macoscode")
            shutil.copyfile(script_path, u_mc)
            shutil.copyfile(script_path, u_macoscode)
            os.chmod(u_mc, 0o755)
            os.chmod(u_macoscode, 0o755)
            installed = True
            print(f"\n{C.EMERALD}✔ '{u_mc}' kullanıcınızın yerel dizinine kuruldu.{C.RESET}")

            # Ensure PATH in zshrc
            zshrc = os.path.expanduser("~/.zshrc")
            path_export = 'export PATH="$HOME/.local/bin:$PATH"'
            try:
                content = open(zshrc).read() if os.path.exists(zshrc) else ""
                if path_export not in content:
                    with open(zshrc, "a") as f:
                        f.write(f"\n# macOSCode mc CLI PATH\n{path_export}\n")
                    print(f"{C.GRAY}ℹ️  ~/.zshrc dosyanıza PATH tanımı eklendi.{C.RESET}")
            except Exception:
                pass

    if installed:
        print(f"\n{C.BOLD}{C.PURPLE}✨ Kurulum tamamlandı! Artık terminalde doğrudan 'mc' veya 'macoscode' yazabilirsiniz! 🚀{C.RESET}")
    else:
        print(f"\n{C.ROSE}❌ Kurulum tamamlanamadı.{C.RESET}")

    print(f"\n{C.GRAY}Menüye dönmek için bir tuşa basın...{C.RESET}")
    get_key()

# Main Interactive TUI Loop
def run_main_tui():
    selected_idx = 0
    menu_items = [
        ("[1]", "🚀", "Master Setup (Tüm 100 Ayarı Tek Tıkla Uygula)", "apply_all"),
        ("[2]", "⏪", "Master Revert (Tüm Ayarları Fabrika Varsayılanına Döndür)", "revert_all"),
        ("[3]", "🎛️ ", "İnteraktif Kategori & Ayar Seçici (TUI)", "categories"),
        ("[4]", "⚡", "Hızlı Paketler (Presets: Developer, Speed, Battery, Tahoe)", "presets"),
        ("[5]", "🔍", "Canlı Arama & Filtreleme (Search by Keyword)", "search"),
        ("[6]", "📊", "Sistem Denetimi & Durum Raporu (System Audit / Status)", "audit"),
        ("[7]", "📦", "Kişiselleştirilmiş Bash Betiği Olarak Kaydet (.sh Export)", "export"),
        ("[8]", "⚙️ ", "'mc' Komutunu Global Sisteme Yükle (Install CLI)", "install"),
        ("[0]", "🚪", "Çıkış (Quit)", "quit")
    ]

    while True:
        clear_screen()
        print_banner()
        print(f"{C.BOLD}{C.WHITE}Lütfen yapmak istediğiniz işlemi seçin:{C.RESET}\n")

        for idx, (num_tag, icon, label, action) in enumerate(menu_items):
            cursor = f"{C.CYAN}{C.BOLD}➜{C.RESET}" if idx == selected_idx else " "
            num_styled = f"{C.CYAN}{C.BOLD}{num_tag}{C.RESET}" if idx == selected_idx else f"{C.DARK_GRAY}{num_tag}{C.RESET}"
            label_styled = f"{C.WHITE}{C.BOLD}{label}{C.RESET}" if idx == selected_idx else f"{C.GRAY}{label}{C.RESET}"
            print(f" {cursor} {num_styled} {icon}  {label_styled}")

        print(f"\n{C.DARK_GRAY}Navigasyon: [↑/↓] Gezin • [Enter/Space] Seç • [1-8/0] Hızlı Tuş • [q] Çıkış{C.RESET}")

        key = get_key()
        if key in ['UP', 'k']:
            selected_idx = (selected_idx - 1) % len(menu_items)
        elif key in ['DOWN', 'j']:
            selected_idx = (selected_idx + 1) % len(menu_items)
        elif key in ['ENTER', 'SPACE']:
            action = menu_items[selected_idx][3]
            handle_action(action)
            if action == 'quit':
                break
        elif key in ['1', '2', '3', '4', '5', '6', '7', '8']:
            idx = int(key) - 1
            handle_action(menu_items[idx][3])
        elif key in ['0', 'q', 'ESC']:
            print(f"\n{C.CYAN}macOSCode ile sisteminiz daima en yüksek performansta! Görüşmek üzere! 👋{C.RESET}\n")
            break

def handle_action(action):
    if action == "apply_all":
        print(f"\n{C.GOLD}Tüm 100 optimizasyon uygulanacak. Onaylıyor musunuz? (e/h):{C.RESET} ", end="")
        choice = get_key()
        if choice.lower() in ['e', 'y', 'ENTER']:
            apply_tweaks_list(TWEAKS, mode="apply")
            print(f"\n{C.GRAY}Devam etmek için bir tuşa basın...{C.RESET}")
            get_key()
    elif action == "revert_all":
        print(f"\n{C.ROSE}Tüm ayarlar Apple fabrika varsayılanına döndürülecek. Onaylıyor musunuz? (e/h):{C.RESET} ", end="")
        choice = get_key()
        if choice.lower() in ['e', 'y', 'ENTER']:
            apply_tweaks_list(TWEAKS, mode="revert")
            print(f"\n{C.GRAY}Devam etmek için bir tuşa basın...{C.RESET}")
            get_key()
    elif action == "categories":
        run_category_menu()
    elif action == "presets":
        run_preset_menu()
    elif action == "search":
        run_search_menu()
    elif action == "audit":
        run_system_audit()
    elif action == "export":
        export_custom_scripts()
    elif action == "install":
        install_mc_globally()

# CLI Main Entry Point
def main():
    parser = argparse.ArgumentParser(
        description="macOSCode (mc) - Interactive Terminal UI & macOS Power-User CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Örnek Kullanımlar:
  mc                     İnteraktif TUI menüsünü açar
  mc --apply-all         Tüm 100 optimizasyonu tek satırda uygular
  mc --revert-all        Tüm ayarları orijinal fabrika varsayılanına döndürür
  mc --status            Sistemdeki ayarların aktiflik durumunu tarar (Audit)
  mc --preset dev        Geliştirici optimizasyon paketini uygular
  mc --search dock       'dock' ile ilgili ayarları arar ve listeler
  mc --install           'mc' komutunu sisteme kalıcı olarak yükler
"""
    )
    parser.add_argument("-a", "--apply-all", action="store_true", help="Tüm 100 ayarı uygula")
    parser.add_argument("-r", "--revert-all", action="store_true", help="Tüm ayarları sıfırla (revert)")
    parser.add_argument("-s", "--status", action="store_true", help="Sistem denetimi ve durum raporu (Audit)")
    parser.add_argument("-p", "--preset", choices=["dev", "speed", "battery", "tahoe"], help="Hızlı optimizasyon paketi çalıştır")
    parser.add_argument("--search", type=str, help="Belirli bir kelimeyi ara")
    parser.add_argument("-d", "--dry-run", action="store_true", help="Komutları çalıştırmadan sadece ekranda göster")
    parser.add_argument("-i", "--install", action="store_true", help="'mc' komutunu /usr/local/bin dizinine yükle")
    parser.add_argument("-t", "--tui", action="store_true", help="İnteraktif TUI modunu başlat")

    args = parser.parse_args()

    # Non-interactive CLI flags
    if args.apply_all:
        apply_tweaks_list(TWEAKS, mode="apply", dry_run=args.dry_run)
    elif args.revert_all:
        apply_tweaks_list(TWEAKS, mode="revert", dry_run=args.dry_run)
    elif args.status:
        run_system_audit()
    elif args.preset:
        chosen = PRESETS[args.preset]
        tweaks_to_run = [t for t in TWEAKS if t["id"] in chosen["ids"]]
        apply_tweaks_list(tweaks_to_run, mode="apply", dry_run=args.dry_run)
    elif args.search:
        q = args.search.lower()
        matched = [t for t in TWEAKS if q in t["title"].lower() or q in t["desc"].lower() or q in t["apply"].lower() or q in t["tag"].lower()]
        print(f"\n{C.CYAN}🔍 '{args.search}' için {len(matched)} ayar bulundu:{C.RESET}\n")
        for i, t in enumerate(matched, 1):
            print(f" {C.BOLD}{i}. {t['title']}{C.RESET} {C.DARK_GRAY}[{t['tag']}]{C.RESET}")
            print(f"    {C.GRAY}{t['desc']}{C.RESET}")
            print(f"    {C.CYAN}$ {t['apply'].replace(chr(10), ' && ')}{C.RESET}\n")
    elif args.install:
        install_mc_globally()
    else:
        # Default: Launch Interactive TUI
        run_main_tui()

if __name__ == "__main__":
    main()
'''

final_script = script_template.replace('__TWEAKS_JSON_PLACEHOLDER__', json.dumps(tweaks_data, ensure_ascii=False, indent=2))

with open('scripts/mc', 'w', encoding='utf-8') as f:
    f.write(final_script)

os.chmod('scripts/mc', 0o755)
print("Successfully generated scripts/mc with 100 tweaks embedded!")
