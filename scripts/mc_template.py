#!/usr/bin/env python3
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
import urllib.request

# macOSCode CLI Version
VERSION = "2.1.0"
VERSION_CODE = 210

# Language Configuration & Persistence (~/.macoscode_lang)
LANG_CONFIG_FILE = os.path.expanduser("~/.macoscode_lang")

def load_persisted_lang():
    if os.path.exists(LANG_CONFIG_FILE):
        try:
            with open(LANG_CONFIG_FILE, "r") as f:
                c = f.read().strip().lower()
                if c in ["en", "tr"]:
                    return c
        except Exception:
            pass
    return "en"

CURRENT_LANG = load_persisted_lang()

def save_persisted_lang(lang):
    global CURRENT_LANG
    CURRENT_LANG = lang
    try:
        with open(LANG_CONFIG_FILE, "w") as f:
            f.write(lang)
    except Exception:
        pass

def txt(tr_str, en_str):
    return en_str if CURRENT_LANG == "en" else tr_str

def t_title(t):
    if CURRENT_LANG == "en" and t.get("title_en"):
        return t.get("title_en")
    return t.get("title", "")

def t_desc(t):
    if CURRENT_LANG == "en" and t.get("desc_en"):
        return t.get("desc_en")
    return t.get("desc", "")

def c_name(c):
    if CURRENT_LANG == "en" and c.get("name_en"):
        return c.get("name_en")
    return c.get("name", "")

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

# 100 TWEAKS DATASET
def _load_tweaks():
    # __EMBEDDED_TWEAKS_PLACEHOLDER__
    _path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tweaks.json")
    if os.path.exists(_path):
        try:
            with open(_path, "r", encoding="utf-8") as _f:
                return json.load(_f)
        except Exception:
            pass
    return []

TWEAKS = _load_tweaks()

# CATEGORIES METADATA
CATEGORIES = [
  {"id": "terminal", "name": "Terminal, Zsh & Kabuk", "name_en": "Terminal, Zsh & Shell", "icon": "💻"},
  {"id": "finder", "name": "Finder & Gelişmiş Dosya Yönetimi", "name_en": "Finder & File Management", "icon": "📁"},
  {"id": "window_dock", "name": "Pencereler, Masaüstü & Dock", "name_en": "Windows, Desktop & Dock", "icon": "🪟"},
  {"id": "keyboard_input", "name": "Klavye, Trackpad & Donanım", "name_en": "Keyboard, Trackpad & Input", "icon": "⌨️"},
  {"id": "dev_security", "name": "Geliştirici, Güvenlik & Sistem", "name_en": "Developer, Security & System", "icon": "⚡"},
  {"id": "tahoe", "name": "macOS Tahoe & Yapay Zeka (AI)", "name_en": "macOS Tahoe & Apple Intelligence", "icon": "🏔️"},
  {"id": "network_power", "name": "Ağ, Güç, Pil & Bakım", "name_en": "Network, Power & Maintenance", "icon": "🔋"}
]

# PRESETS
PRESETS = {
  "dev": {
    "title": "Geliştirici & Mühendis Paketi",
    "title_en": "Developer & Engineer Powerhouse",
    "desc": "Xcode build süresi sayacı, Safari Web Inspector, maksimum tuş tekrar hızı ve Touch ID sudo.",
    "desc_en": "Xcode build duration timer, Safari Web Inspector, lightning key repeat rate, and Touch ID sudo.",
    "ids": ["term-hostname", "term-interactive-comments", "term-touchid-sudo", "find-all-extensions", "find-hidden-files", "find-posix-title", "find-quicklook-text", "key-fast-repeat", "key-disable-press-hold", "dev-xcode-build-duration", "safari-enable-develop-menu", "safari-show-full-url", "dev-textedit-plain-text", "sec-disable-quarantine"]
  },
  "speed": {
    "title": "Ultra Hız & Sıfır Gecikme Paketi",
    "title_en": "Ultra Speed & Zero-Delay Package",
    "desc": "Sıfır Dock gecikmesi, hızlı Mission Control, Suck pencere efekti ve Reduce Motion arayüz hızlandırma.",
    "desc_en": "Zero Dock hover delay, 100ms Mission Control transitions, fluid Suck minimize effect, and Reduce Motion speed.",
    "ids": ["dock-autohide-speed", "dock-suck-effect", "dock-fast-expose-anim", "win-fast-resize", "find-quicklook-fast-zoom", "tahoe-tiling-preview-delay", "tahoe-fast-stage-manager", "tahoe-fast-autohide-menubar", "ui-reduce-motion", "key-fast-repeat"]
  },
  "battery": {
    "title": "Pil Tasarrufu & Donanım Sağlığı",
    "title_en": "Battery Life & Hardware Health",
    "desc": "Klavye aydınlatma zaman aşımı, uykuda ağ uyandırmasını kapatma, %80 şarj sınırı ve düşük güç modu.",
    "desc_en": "Keyboard backlight timeout, disable network sleep wakes, 80% battery charging optimization, and low power mode.",
    "ids": ["hw-keyboard-backlight-dim", "pwr-low-power-mode-battery-only", "pwr-charge-limit-80", "net-wifi-disable-powersave", "net-disable-sleep-on-clamshell", "pwr-fast-hibernation", "sys-clean-sleepimage", "sec-disable-apple-analytics"]
  },
  "tahoe": {
    "title": "macOS Tahoe & AI Özel Paketi",
    "title_en": "macOS Tahoe & Apple Intelligence Suite",
    "desc": "Snap önizleme hızlandırma, kenarlık boşluklarını sıfırlama, yerel Spotlight önceliği ve menü çubuğu sıkıştırma.",
    "desc_en": "Zero-delay window snapping, borderless window tiling, local-first Spotlight search, and compact notch menubar.",
    "ids": ["tahoe-tiling-preview-delay", "tahoe-hide-snap-dividers", "win-remove-tiling-margins", "tahoe-writing-tools-delay", "tahoe-spotlight-local-first", "tahoe-compact-menubar-spacing", "tahoe-mirror-group-notifications", "tahoe-game-mode-auto-boost"]
  }
}

def get_key():
    try:
        import termios
        import tty
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
                return 'ESC'
            elif ch == '\r' or ch == '\n':
                return 'ENTER'
            elif ch == ' ':
                return 'SPACE'
            elif ch == '\x7f' or ch == '\x08':
                return 'BACKSPACE'
            elif ch == '\x03':
                return 'CTRL_C'
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    except Exception:
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
  {C.PURPLE}{C.BOLD}⚡ macOS Interactive Terminal CLI & TUI • 100 Power-Tweaks (v{VERSION}){C.RESET}
  {C.DARK_GRAY}https://github.com/Jarvis322/macoscode • Build {VERSION_CODE} • Tahoe & Apple Silicon{C.RESET}
"""
    print(banner)

def refresh_services():
    services = ["Finder", "Dock", "WindowManager", "SystemUIServer", "Spotlight"]
    msg = txt("macOS Sistem servisleri yenileniyor...", "Restarting macOS system services...")
    print(f"\n{C.CYAN}🔄 {msg}{C.RESET}")
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
        err_msg = txt("Hata:", "Error:")
        print(f"{C.ROSE}{err_msg}{C.RESET} {e}")
        return False

# Audit Check for a tweak
def check_tweak_status(tweak):
    apply_cmd = tweak["apply"]
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
    if "pam_tid.so" in apply_cmd:
        try:
            res = subprocess.run("grep -q 'pam_tid.so' /etc/pam.d/sudo /etc/pam.d/sudo_local 2>/dev/null", shell=True)
            return res.returncode == 0
        except Exception:
            return False
    if "INTERACTIVE_COMMENTS" in apply_cmd:
        try:
            res = subprocess.run("grep -q 'setopt INTERACTIVE_COMMENTS' ~/.zshrc 2>/dev/null", shell=True)
            return res.returncode == 0
        except Exception:
            return False
    if "HOMEBREW_NO_ANALYTICS" in apply_cmd:
        try:
            res = subprocess.run("grep -q 'HOMEBREW_NO_ANALYTICS' ~/.zprofile ~/.zshrc 2>/dev/null", shell=True)
            return res.returncode == 0
        except Exception:
            return False
    return False

# System Audit Dashboard
def run_system_audit(interactive=True):
    if interactive:
        clear_screen()
        print_banner()
    title_msg = txt("macOS Sistem Ayarları Denetim Raporu (Audit)", "macOS System Configuration Audit Report")
    desc_msg = txt("Sisteminizdeki 100 optimizasyonun anlık durumu taranıyor...", "Scanning active state for all 100 power-user optimizations...")
    print(f"{C.BOLD}{C.CYAN}📊 {title_msg}{C.RESET}")
    print(f"{C.DARK_GRAY}{desc_msg}{C.RESET}\n")

    active_count = 0
    total_count = len(TWEAKS)

    for cat in CATEGORIES:
        cat_tweaks = [t for t in TWEAKS if t["cat"] == cat["id"]]
        cat_suffix = txt("Ayar", "Tweaks")
        print(f"\n{C.BOLD}{cat['icon']} {c_name(cat)}{C.RESET} {C.DARK_GRAY}({len(cat_tweaks)} {cat_suffix}){C.RESET}")
        print("─" * 68)
        for t in cat_tweaks:
            status = check_tweak_status(t)
            if status:
                active_count += 1
                status_lbl = txt("AKTİF", "ACTIVE")
                status_badge = f"{C.EMERALD}{C.BOLD}[✔ {status_lbl}]{C.RESET}"
            else:
                def_lbl = txt("VARSAYILAN", "DEFAULT ")
                status_badge = f"{C.DARK_GRAY}[  {def_lbl}  ]{C.RESET}"
            
            title = t_title(t)
            title_truncated = title[:44] + "..." if len(title) > 47 else title.ljust(47)
            print(f" {status_badge} {title_truncated} {C.GRAY}[{t['tag']}]{C.RESET}")

    score = int((active_count / total_count) * 100)
    print("\n" + "=" * 68)
    summary_label = txt("ÖZET", "SUMMARY")
    power_label = txt("Güç Seviyesi", "Power Level")
    opt_label = txt("Optimizasyon Aktif", "Optimizations Active")
    print(f"{C.BOLD}📈 {summary_label}: {C.EMERALD}{active_count}{C.RESET}/{total_count} {opt_label} ({C.CYAN}%{score} {power_label}{C.RESET}){C.RESET}")
    print("=" * 68)
    if interactive:
        back_msg = txt("Menüye dönmek için herhangi bir tuşa basın...", "Press any key to return to menu...")
        print(f"\n{C.GRAY}{back_msg}{C.RESET}")
        get_key()

# Batch Apply / Revert
def apply_tweaks_list(tweak_list, mode="apply", dry_run=False):
    action_name = txt("Uygulanıyor", "Applying") if mode == "apply" else txt("Sıfırlanıyor (Revert)", "Reverting to Factory Defaults")
    color = C.CYAN if mode == "apply" else C.ROSE
    count_suffix = txt("Ayar", "Tweaks")
    print(f"\n{color}{C.BOLD}🚀 {len(tweak_list)} {count_suffix} {action_name}...{C.RESET}\n")
    
    if not dry_run:
        sudo_msg = txt("Sudo yetkilendirmesi istenebilir...", "Administrator (sudo) authorization may be requested...")
        print(f"{C.GOLD}🔐 {sudo_msg}{C.RESET}")
        subprocess.run("sudo -v", shell=True)

    for i, t in enumerate(tweak_list, 1):
        cmd = t["apply"] if mode == "apply" else t["revert"]
        print(f"{C.GRAY}[{i}/{len(tweak_list)}]{C.RESET} {C.BOLD}{t_title(t)}{C.RESET}")
        if dry_run:
            print(f"   {C.DARK_GRAY}$ {cmd.replace(chr(10), ' && ')}{C.RESET}")
        else:
            run_command(cmd, dry_run=False)

    if not dry_run:
        refresh_services()
        done_msg = txt("İşlem başarıyla tamamlandı!", "Operation completed successfully!")
        print(f"\n{C.EMERALD}{C.BOLD}✨ {done_msg} ({len(tweak_list)} {count_suffix}){C.RESET}\n")
    else:
        dry_msg = txt("Komutlar görüntülendi, sistemde değişiklik yapılmadı.", "Commands previewed, no changes were applied to system.")
        print(f"\n{C.GOLD}{C.BOLD}✨ [DRY-RUN] {dry_msg}{C.RESET}\n")

# Preset Selector
def run_preset_menu():
    selected_idx = 0
    keys = list(PRESETS.keys())

    while True:
        clear_screen()
        print_banner()
        preset_hdr = txt("Hızlı Optimizasyon Paketleri (Presets)", "Quick Optimization Presets")
        print(f"{C.BOLD}{C.GOLD}⚡ {preset_hdr}{C.RESET}\n")

        for idx, k in enumerate(keys):
            p = PRESETS[k]
            p_title = p.get("title_en") if CURRENT_LANG == "en" else p.get("title")
            p_desc = p.get("desc_en") if CURRENT_LANG == "en" else p.get("desc")
            cursor = f"{C.CYAN}{C.BOLD}➜{C.RESET}" if idx == selected_idx else " "
            highlight = f"{C.CYAN}{C.BOLD}" if idx == selected_idx else f"{C.WHITE}"
            count_suffix = txt("Ayar", "Tweaks")
            print(f" {cursor} {highlight}{idx+1}. {p_title}{C.RESET}")
            print(f"     {C.DARK_GRAY}{p_desc} ({len(p['ids'])} {count_suffix}){C.RESET}\n")

        nav_msg = txt("Navigasyon: [↑/↓] Gezin • [Enter] Paketi Seç & Uygula • [r] Paketi Revert Et • [q/Esc] Geri", "Navigation: [↑/↓] Navigate • [Enter] Apply Preset • [r] Revert Preset • [q/Esc] Back")
        print(f"{C.DARK_GRAY}{nav_msg}{C.RESET}")

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
            cont_msg = txt("Devam etmek için bir tuşa basın...", "Press any key to continue...")
            print(f"\n{C.GRAY}{cont_msg}{C.RESET}")
            get_key()
            break
        elif key == 'r':
            chosen_key = keys[selected_idx]
            chosen_preset = PRESETS[chosen_key]
            tweaks_to_run = [t for t in TWEAKS if t["id"] in chosen_preset["ids"]]
            apply_tweaks_list(tweaks_to_run, mode="revert")
            cont_msg = txt("Devam etmek için bir tuşa basın...", "Press any key to continue...")
            print(f"\n{C.GRAY}{cont_msg}{C.RESET}")
            get_key()
            break
        elif key in ['q', 'ESC']:
            break

# Interactive Tweak Selector
def run_interactive_selector(category_filter=None):
    if category_filter:
        items = [t for t in TWEAKS if t["cat"] == category_filter]
        cat_obj = next((c for c in CATEGORIES if c["id"] == category_filter), None)
        title = f"{cat_obj['icon']} {c_name(cat_obj)}" if cat_obj else txt("Kategori", "Category")
    else:
        items = TWEAKS
        title = txt("Tüm Ayarlar (100-in-1)", "All Power Tweaks (100-in-1)")

    selected_set = set()
    cursor_idx = 0
    dry_run_mode = False

    while True:
        clear_screen()
        print_banner()
        sel_label = txt("Seçili", "Selected")
        print(f"{C.BOLD}{C.PURPLE}🎛️  {title}{C.RESET} {C.DARK_GRAY}({sel_label}: {len(selected_set)}/{len(items)}){C.RESET}")
        print("─" * 70)

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
            title_str = t_title(t)
            title_text = title_str[:40] + "..." if len(title_str) > 43 else title_str.ljust(43)
            print(f" {cursor_mark} {check_mark} {text_style}{title_text}{C.RESET} {tag_badge}")

        # Current Item Detail Card
        cur_tweak = items[cursor_idx]
        det_lbl = txt("Detay & Önizleme", "Detail & Preview")
        print("\n" + f"{C.DARK_GRAY}┌─ {det_lbl} ───────────────────────────────────────────────┐{C.RESET}")
        print(f"{C.DARK_GRAY}│{C.RESET} {C.BOLD}{t_title(cur_tweak)}{C.RESET}")
        print(f"{C.DARK_GRAY}│{C.RESET} {C.GRAY}{t_desc(cur_tweak)[:68]}{C.RESET}")
        first_cmd = cur_tweak['apply'].split('\n')[0]
        print(f"{C.DARK_GRAY}│{C.RESET} {C.CYAN}$ {first_cmd[:66]}{C.RESET}")
        print(f"{C.DARK_GRAY}└─────────────────────────────────────────────────────────────────────┘{C.RESET}")

        dry_on = txt("DRY-RUN AÇIK", "DRY-RUN ON")
        live_on = txt("CANLI MOD", "LIVE MODE")
        dry_badge = f"{C.GOLD}[{dry_on}]{C.RESET}" if dry_run_mode else f"{C.DARK_GRAY}[{live_on}]{C.RESET}"
        nav_1 = txt("Navigasyon:", "Navigation:")
        nav_2 = txt("Gezin", "Navigate")
        nav_3 = txt("Seç/Bırak", "Toggle")
        nav_4 = txt("Tümünü Seç", "Select All")
        act_1 = txt("Aksiyonlar:", "Actions:")
        act_2 = txt("Uygula", "Apply Selected")
        act_3 = txt("Sıfırla (Revert)", "Revert Selected")
        act_4 = txt("Geri", "Back")
        print(f"{C.DARK_GRAY}{nav_1}{C.RESET} [↑/↓] {nav_2} • [Space] {nav_3} • [a] {nav_4} • [d] {dry_badge}")
        print(f"{C.DARK_GRAY}{act_1}{C.RESET} [Enter] {act_2} • [r] {act_3} • [q/Esc] {act_4}")

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
            cont_msg = txt("Devam etmek için bir tuşa basın...", "Press any key to continue...")
            print(f"\n{C.GRAY}{cont_msg}{C.RESET}")
            get_key()
            break
        elif key == 'r':
            chosen_tweaks = [t for t in items if t["id"] in selected_set]
            if not chosen_tweaks:
                chosen_tweaks = [cur_tweak]
            apply_tweaks_list(chosen_tweaks, mode="revert", dry_run=dry_run_mode)
            cont_msg = txt("Devam etmek için bir tuşa basın...", "Press any key to continue...")
            print(f"\n{C.GRAY}{cont_msg}{C.RESET}")
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
        cat_hdr = txt("Kategorilere Göre Ayar Gezgini", "Browse by Category")
        print(f"{C.BOLD}{C.CYAN}🎛️  {cat_hdr}{C.RESET}\n")

        for idx, cat in enumerate(CATEGORIES):
            cat_count = len([t for t in TWEAKS if t["cat"] == cat["id"]])
            cursor = f"{C.CYAN}{C.BOLD}➜{C.RESET}" if idx == selected_idx else " "
            num_styled = f"{C.CYAN}{C.BOLD}[{idx+1}]{C.RESET}" if idx == selected_idx else f"{C.DARK_GRAY}[{idx+1}]{C.RESET}"
            cat_label = c_name(cat)
            label_styled = f"{C.WHITE}{C.BOLD}{cat_label}{C.RESET}" if idx == selected_idx else f"{C.GRAY}{cat_label}{C.RESET}"
            count_suffix = txt("Ayar", "Tweaks")
            print(f" {cursor} {num_styled} {cat['icon']}  {label_styled} {C.DARK_GRAY}({cat_count} {count_suffix}){C.RESET}")

        nav_cat = txt("Navigasyon: [↑/↓] Gezin • [Enter/Space] Kategoriye Gir • [1-7] Hızlı Tuş • [q/Esc] Geri", "Navigation: [↑/↓] Navigate • [Enter/Space] Enter Category • [1-7] Direct Key • [q/Esc] Back")
        print(f"\n{C.DARK_GRAY}{nav_cat}{C.RESET}")

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
    search_hdr = txt("Terminal İçi Ayar Arama", "Live Terminal Tweak Search")
    search_sub = txt("Aramak istediğiniz anahtar kelimeyi yazın (örn: dock, sudo, finder, tahoe):", "Enter search query keyword (e.g. dock, sudo, finder, battery, tahoe):")
    print(f"{C.BOLD}{C.CYAN}🔍  {search_hdr}{C.RESET}")
    print(f"{C.DARK_GRAY}{search_sub}{C.RESET}\n")
    search_prompt = txt("Arama", "Search")
    try:
        query = input(f"{C.BOLD}{C.CYAN}{search_prompt} ➜ {C.RESET}").strip().lower()
    except Exception:
        return

    if not query:
        return

    matched = [t for t in TWEAKS if query in t["title"].lower() or query in t.get("title_en", "").lower() or query in t["desc"].lower() or query in t.get("desc_en", "").lower() or query in t["apply"].lower() or query in t["tag"].lower()]
    
    if not matched:
        no_res = txt(f"'{query}' ile eşleşen ayar bulunamadı.", f"No tweaks found matching '{query}'.")
        print(f"\n{C.ROSE}❌ {no_res}{C.RESET}")
        time.sleep(1.5)
        return

    selected_set = set()
    cursor_idx = 0

    while True:
        clear_screen()
        print_banner()
        res_hdr = txt(f"'{query}' Arama Sonuçları ({len(matched)} Ayar Bulundu)", f"'{query}' Search Results ({len(matched)} Tweaks Found)")
        print(f"{C.BOLD}{C.CYAN}🔍  {res_hdr}{C.RESET}")
        print("─" * 70)

        for idx, t in enumerate(matched):
            is_cur = (idx == cursor_idx)
            is_sel = (t["id"] in selected_set)
            cursor_mark = f"{C.CYAN}➜{C.RESET}" if is_cur else " "
            check_mark = f"{C.EMERALD}[✔]{C.RESET}" if is_sel else f"{C.DARK_GRAY}[ ]{C.RESET}"
            text_style = f"{C.BOLD}{C.WHITE}" if is_cur else f"{C.GRAY}"
            print(f" {cursor_mark} {check_mark} {text_style}{t_title(t)[:44]}{C.RESET} {C.DARK_GRAY}[{t['tag']}]{C.RESET}")

        nav_search = txt("Navigasyon: [↑/↓] • [Space] Seç • [a] Tümünü Seç • [Enter] Uygula • [r] Revert • [q] Geri", "Navigation: [↑/↓] • [Space] Toggle • [a] All • [Enter] Apply • [r] Revert • [q] Back")
        print(f"\n{C.DARK_GRAY}{nav_search}{C.RESET}")

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
            cont_msg = txt("Devam etmek için bir tuşa basın...", "Press any key to continue...")
            print(f"\n{C.GRAY}{cont_msg}{C.RESET}")
            get_key()
            break
        elif key == 'r':
            chosen = [t for t in matched if t["id"] in selected_set] or [matched[cursor_idx]]
            apply_tweaks_list(chosen, mode="revert")
            cont_msg = txt("Devam etmek için bir tuşa basın...", "Press any key to continue...")
            print(f"\n{C.GRAY}{cont_msg}{C.RESET}")
            get_key()
            break
        elif key in ['q', 'ESC']:
            break

# Export Custom Bash Scripts
def export_custom_scripts():
    clear_screen()
    print_banner()
    exp_hdr = txt("Kişiselleştirilmiş Bash Betiği Olarak Kaydet (.sh Export)", "Export Customized Bash Setup/Reset Scripts (.sh)")
    print(f"{C.BOLD}{C.GOLD}📦  {exp_hdr}{C.RESET}\n")

    setup_file = "custom-macos-setup.sh"
    revert_file = "custom-macos-revert.sh"

    # Generate Setup
    with open(setup_file, "w", encoding="utf-8") as f:
        f.write(f"#!/usr/bin/env bash\n# macOS Power-User Setup Script ({len(TWEAKS)} Tweaks)\n# Repository: https://github.com/Jarvis322/macoscode\nset -e\nsudo -v\n\n")
        for t in TWEAKS:
            f.write(f"# {t_title(t)}\n# Revert: {t['revert']}\n{t['apply']}\n\n")
        f.write("killall Finder Dock WindowManager 2>/dev/null || true\necho '✨ Setup complete!'\n")

    # Generate Revert
    with open(revert_file, "w", encoding="utf-8") as f:
        f.write(f"#!/usr/bin/env bash\n# macOS Power-User Revert Script ({len(TWEAKS)} Tweaks)\n# Repository: https://github.com/Jarvis322/macoscode\nset -e\nsudo -v\n\n")
        for t in TWEAKS:
            f.write(f"# {t_title(t)} (Revert)\n{t['revert']}\n\n")
        f.write("killall Finder Dock WindowManager 2>/dev/null || true\necho '✅ Restored to Apple factory defaults!'\n")

    os.chmod(setup_file, 0o755)
    os.chmod(revert_file, 0o755)

    created_lbl = txt("oluşturuldu.", "created successfully.")
    print(f"{C.EMERALD}✔ {setup_file} {created_lbl}{C.RESET}")
    print(f"{C.EMERALD}✔ {revert_file} {created_lbl}{C.RESET}")
    run_msg = txt(f"Bu betikleri doğrudan ./{setup_file} veya ./{revert_file} şeklinde çalıştırabilirsiniz.", f"You can run these scripts directly via ./{setup_file} or ./{revert_file}")
    print(f"\n{C.CYAN}{run_msg}{C.RESET}")
    back_msg = txt("Menüye dönmek için bir tuşa basın...", "Press any key to return to menu...")
    print(f"\n{C.GRAY}{back_msg}{C.RESET}")
    get_key()

# Launch Swift Menu Bar Companion App
def launch_menubar_app(interactive=True):
    if interactive:
        clear_screen()
        print_banner()
        title_lbl = txt("macOS Menu Bar Aracını Başlat", "Launch macOS Menu Bar Companion App")
        print(f"{C.BOLD}{C.CYAN}🖥️   {title_lbl}{C.RESET}\n")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    swift_script = os.path.join(script_dir, "macoscode-menubar.swift")

    msg = txt("Menu Bar aracı (⚡) menü çubuğunuzda arka planda başlatılıyor...", "Starting Menu Bar companion app (⚡) in your top status bar...")
    if interactive:
        print(f"{C.EMERALD}{msg}{C.RESET}\n")

    try:
        subprocess.Popen(f"swift '{swift_script}' >/dev/null 2>&1 &", shell=True)
        ok_msg = txt("✔ Menu Bar aracı başarıyla çalıştırıldı! Ekranınızın sağ üst köşesindeki ⚡ simgesine tıklayarak ayarları anında açıp kapatabilirsiniz.", "✔ Menu Bar companion app launched! Click the ⚡ icon in your top right menu bar to toggle tweaks with live checkmarks.")
        if interactive:
            print(f"{C.BOLD}{C.PURPLE}✨ {ok_msg}{C.RESET}")
            back_msg = txt("Menüye dönmek için bir tuşa basın...", "Press any key to return to menu...")
            print(f"\n{C.GRAY}{back_msg}{C.RESET}")
            get_key()
        else:
            print(f"{C.EMERALD}{ok_msg}{C.RESET}")
    except Exception as e:
        err_msg = txt("Hata:", "Error:")
        print(f"{C.ROSE}{err_msg} {e}{C.RESET}")

# Self Installer (mc -> /usr/local/bin or ~/.local/bin)
def install_mc_globally():
    clear_screen()
    print_banner()
    title_lbl = txt("'mc' Komutunu Global Sisteme Yükle", "Install 'mc' Command Globally")
    print(f"{C.BOLD}{C.CYAN}⚙️   {title_lbl}{C.RESET}\n")

    script_path = os.path.abspath(__file__)
    installed = False
    target_dir = "/usr/local/bin"
    target_mc = os.path.join(target_dir, "mc")
    target_macoscode = os.path.join(target_dir, "macoscode")
    installed_lbl = txt("başarıyla kuruldu.", "installed successfully.")

    try:
        os.makedirs(target_dir, exist_ok=True)
        shutil.copyfile(script_path, target_mc)
        shutil.copyfile(script_path, target_macoscode)
        os.chmod(target_mc, 0o755)
        os.chmod(target_macoscode, 0o755)
        installed = True
        print(f"{C.EMERALD}✔ '{target_mc}' {installed_lbl}{C.RESET}")
        print(f"{C.EMERALD}✔ '{target_macoscode}' {installed_lbl}{C.RESET}")
    except PermissionError:
        perm_msg = txt("'/usr/local/bin' için yönetici (sudo) izni isteniyor...", "Admin (sudo) permission requested for '/usr/local/bin'...")
        print(f"{C.GOLD}🔐 {perm_msg}{C.RESET}")
        res = subprocess.run(f"sudo mkdir -p '{target_dir}' && sudo cp '{script_path}' '{target_mc}' && sudo cp '{script_path}' '{target_macoscode}' && sudo chmod 755 '{target_mc}' '{target_macoscode}'", shell=True)
        if res.returncode == 0:
            installed = True
            print(f"\n{C.EMERALD}✔ '{target_mc}' {installed_lbl}{C.RESET}")
            print(f"{C.EMERALD}✔ '{target_macoscode}' {installed_lbl}{C.RESET}")
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
            local_lbl = txt("kullanıcınızın yerel dizinine kuruldu.", "installed to your local user directory.")
            print(f"\n{C.EMERALD}✔ '{u_mc}' {local_lbl}{C.RESET}")

            # Ensure PATH in zshrc
            zshrc = os.path.expanduser("~/.zshrc")
            path_export = 'export PATH="$HOME/.local/bin:$PATH"'
            try:
                content = open(zshrc).read() if os.path.exists(zshrc) else ""
                if path_export not in content:
                    with open(zshrc, "a") as f:
                        f.write(f"\n# macOSCode mc CLI PATH\n{path_export}\n")
                    path_lbl = txt("dosyanıza PATH tanımı eklendi.", "PATH export added to ~/.zshrc.")
                    print(f"{C.GRAY}ℹ️  ~/.zshrc {path_lbl}{C.RESET}")
            except Exception:
                pass

    if installed:
        comp_msg = txt("Kurulum tamamlandı! Artık terminalde doğrudan 'mc' veya 'macoscode' yazabilirsiniz! 🚀", "Installation complete! You can now run 'mc' or 'macoscode' anywhere! 🚀")
        print(f"\n{C.BOLD}{C.PURPLE}✨ {comp_msg}{C.RESET}")
    else:
        fail_msg = txt("Kurulum tamamlanamadı.", "Installation failed.")
        print(f"\n{C.ROSE}❌ {fail_msg}{C.RESET}")

    back_msg = txt("Menüye dönmek için bir tuşa basın...", "Press any key to return to menu...")
    print(f"\n{C.GRAY}{back_msg}{C.RESET}")
    get_key()

# Self Updater (Fetch latest mc from GitHub and update local binaries)
def update_mc(interactive=True, force=False):
    if interactive:
        clear_screen()
        print_banner()
    upd_hdr = txt("'mc' Sürüm ve Güncelleme Denetimi (Self-Update)", "'mc' Version & Self-Update Checker")
    print(f"{C.BOLD}{C.CYAN}🔄  {upd_hdr}{C.RESET}\n")
    cur_lbl = txt("Mevcut Sürüm:", "Current Local Version:")
    print(f"{cur_lbl} {C.BOLD}{C.EMERALD}v{VERSION}{C.RESET} (Build {VERSION_CODE})")
    query_lbl = txt("GitHub üzerindeki en son sürüm sorgulanıyor...", "Querying latest release from GitHub...")
    print(f"{C.GRAY}{query_lbl}{C.RESET}\n")
    
    url = "https://raw.githubusercontent.com/Jarvis322/macoscode/main/scripts/mc"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'macOSCode-CLI-Updater'})
        with urllib.request.urlopen(req, timeout=12) as response:
            if response.status != 200:
                http_err = txt("Güncelleme indirilemedi: HTTP", "Failed to fetch update: HTTP")
                print(f"\n{C.ROSE}❌ {http_err} {response.status}{C.RESET}")
                if interactive:
                    cont_msg = txt("Devam etmek için bir tuşa basın...", "Press any key to continue...")
                    print(f"\n{C.GRAY}{cont_msg}{C.RESET}")
                    get_key()
                return
            new_code = response.read().decode('utf-8')
    except Exception as e:
        conn_err = txt("Bağlantı hatası:", "Connection error:")
        print(f"\n{C.ROSE}❌ {conn_err} {e}{C.RESET}")
        if interactive:
            cont_msg = txt("Devam etmek için bir tuşa basın...", "Press any key to continue...")
            print(f"\n{C.GRAY}{cont_msg}{C.RESET}")
            get_key()
        return

    if "#!/usr/bin/env python3" not in new_code or len(new_code) < 1000:
        inv_err = txt("İndirilen dosya geçerli bir macOSCode betiği değil.", "Downloaded content is not a valid macOSCode script.")
        print(f"\n{C.ROSE}❌ {inv_err}{C.RESET}")
        if interactive:
            cont_msg = txt("Devam etmek için bir tuşa basın...", "Press any key to continue...")
            print(f"\n{C.GRAY}{cont_msg}{C.RESET}")
            get_key()
        return

    # Extract remote version
    rem_ver_match = re.search(r'VERSION\s*=\s*["\']([0-9a-zA-Z\.]+)["\']', new_code)
    rem_code_match = re.search(r'VERSION_CODE\s*=\s*(\d+)', new_code)
    
    remote_version = rem_ver_match.group(1) if rem_ver_match else "unknown"
    remote_vcode = int(rem_code_match.group(1)) if rem_code_match else 0

    latest_lbl = txt("En Son GitHub Sürümü:", "Latest GitHub Release:")
    print(f"{latest_lbl} {C.BOLD}{C.CYAN}v{remote_version}{C.RESET} (Build {remote_vcode})\n")

    if remote_vcode > 0 and remote_vcode <= VERSION_CODE and not force:
        up_to_date = txt(f"Zaten en güncel sürümü (v{VERSION}) kullanıyorsunuz!", f"You are already running the latest version (v{VERSION})!")
        print(f"{C.EMERALD}✔ {up_to_date}{C.RESET}")
        if interactive:
            force_prompt = txt("Yine de zorla yeniden yüklemek ister misiniz? (e/h):", "Do you still want to force reinstall? (y/n):")
            print(f"\n{C.GOLD}{force_prompt}{C.RESET} ", end="")
            choice = get_key()
            if choice.lower() not in ['e', 'y']:
                return
        else:
            return

    if remote_vcode > VERSION_CODE:
        avail_msg = txt("Yeni bir sürüm bulundu:", "New version available:")
        print(f"{C.GOLD}🚀 {avail_msg} {C.ROSE}v{VERSION}{C.GOLD} ➜ {C.EMERALD}v{remote_version}{C.RESET}")
        apply_msg = txt("Güncelleme uygulanıyor...", "Applying update...")
        print(f"{C.CYAN}{apply_msg}{C.RESET}\n")

    targets = []
    current_script = os.path.abspath(__file__)
    targets.append(current_script)

    for candidate in [
        "/usr/local/bin/mc",
        "/usr/local/bin/macoscode",
        os.path.expanduser("~/.local/bin/mc"),
        os.path.expanduser("~/.local/bin/macoscode")
    ]:
        if os.path.exists(candidate) and candidate not in targets:
            targets.append(candidate)

    updated_any = False
    temp_path = f"/tmp/mc_update_{int(time.time())}.py"
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(new_code)
    os.chmod(temp_path, 0o755)

    for target in targets:
        try:
            shutil.copyfile(temp_path, target)
            os.chmod(target, 0o755)
            upd_str = txt("güncellendi", "updated")
            print(f"{C.EMERALD}✔ '{target}' {upd_str} (v{remote_version}).{C.RESET}")
            updated_any = True
        except PermissionError:
            sudo_req = txt("güncellemesi için yönetici (sudo) izni isteniyor...", "update requires administrator (sudo) privileges...")
            print(f"{C.GOLD}🔐 '{target}' {sudo_req}{C.RESET}")
            res = subprocess.run(f"sudo cp '{temp_path}' '{target}' && sudo chmod 755 '{target}'", shell=True)
            if res.returncode == 0:
                sudo_upd = txt("güncellendi (sudo ile).", "updated (with sudo).")
                print(f"{C.EMERALD}✔ '{target}' {sudo_upd} (v{remote_version}){C.RESET}")
                updated_any = True
            else:
                fail_upd = txt("güncellenemedi.", "failed to update.")
                print(f"{C.ROSE}❌ '{target}' {fail_upd}{C.RESET}")
        except Exception as e:
            err_upd = txt("güncellenirken hata:", "update error:")
            print(f"{C.ROSE}❌ '{target}' {err_upd} {e}{C.RESET}")

    try:
        os.remove(temp_path)
    except Exception:
        pass

    if updated_any:
        succ_msg = txt(f"Başarılı! 'mc' v{remote_version} (Build {remote_vcode}) sürümüne yükseltildi! 🚀", f"Success! 'mc' upgraded to v{remote_version} (Build {remote_vcode})! 🚀")
        print(f"\n{C.BOLD}{C.PURPLE}🎉 {succ_msg}{C.RESET}")
    else:
        warn_msg = txt("Hedef dosyalar güncellenemedi.", "Target files could not be updated.")
        print(f"\n{C.GOLD}⚠️ {warn_msg}{C.RESET}")

    if interactive:
        back_msg = txt("Menüye dönmek için bir tuşa basın...", "Press any key to return to menu...")
        print(f"\n{C.GRAY}{back_msg}{C.RESET}")
        get_key()

# Main Interactive TUI Loop
def run_main_tui():
    selected_idx = 0

    while True:
        menu_items = [
            ("[1]", "🚀", txt("Master Setup (Tüm 100 Ayarı Tek Tıkla Uygula)", "Master Setup (Apply All 100 Optimizations)"), "apply_all"),
            ("[2]", "⏪", txt("Master Revert (Tüm Ayarları Fabrika Varsayılanına Döndür)", "Master Revert (Restore All to Apple Defaults)"), "revert_all"),
            ("[3]", "🎛️ ", txt("İnteraktif Kategori & Ayar Seçici (TUI)", "Interactive Category & Tweak Selector"), "categories"),
            ("[4]", "⚡", txt("Hızlı Paketler (Presets: Developer, Speed, Battery, Tahoe)", "Quick Presets (Developer, Speed, Battery, Tahoe)"), "presets"),
            ("[5]", "🔍", txt("Canlı Arama & Filtreleme (Search by Keyword)", "Live Search & Keyword Filter"), "search"),
            ("[6]", "📊", txt("Sistem Denetimi & Durum Raporu (System Audit / Status)", "System Audit & Health Status Report"), "audit"),
            ("[7]", "📦", txt("Kişiselleştirilmiş Bash Betiği Olarak Kaydet (.sh Export)", "Export Customized Bash Scripts (.sh)"), "export"),
            ("[8]", "⚙️ ", txt("'mc' Komutunu Global Sisteme Yükle (Install CLI)", "Install 'mc' CLI Globally"), "install"),
            ("[9]", "🖥️ ", txt("Menu Bar Hızlı Ayar Aracını Başlat (Menu Bar Companion)", "Launch Menu Bar Quick Toggle App"), "menubar"),
            ("[U]", "🔄", txt("'mc' Aracını Güncelle (Self-Update from GitHub)", "Self-Update 'mc' from GitHub"), "update"),
            ("[L]", "🌐", txt("Dili Değiştir / Switch Language: 🇹🇷 Türkçe ➜ 🇬🇧 English", "Switch Language / Dili Değiştir: 🇬🇧 English ➜ 🇹🇷 Türkçe"), "toggle_lang"),
            ("[0]", "🚪", txt("Çıkış (Quit)", "Quit"), "quit")
        ]

        clear_screen()
        print_banner()
        action_prompt = txt("Lütfen yapmak istediğiniz işlemi seçin:", "Please choose an action:")
        print(f"{C.BOLD}{C.WHITE}{action_prompt}{C.RESET}\n")

        for idx, (num_tag, icon, label, action) in enumerate(menu_items):
            cursor = f"{C.CYAN}{C.BOLD}➜{C.RESET}" if idx == selected_idx else " "
            num_styled = f"{C.CYAN}{C.BOLD}{num_tag}{C.RESET}" if idx == selected_idx else f"{C.DARK_GRAY}{num_tag}{C.RESET}"
            label_styled = f"{C.WHITE}{C.BOLD}{label}{C.RESET}" if idx == selected_idx else f"{C.GRAY}{label}{C.RESET}"
            print(f" {cursor} {num_styled} {icon}  {label_styled}")

        nav_main = txt("Navigasyon: [↑/↓] Gezin • [Enter/Space] Seç • [1-9/U/L/0] Hızlı Tuş • [q] Çıkış", "Navigation: [↑/↓] Navigate • [Enter/Space] Select • [1-9/U/L/0] Direct Key • [q] Quit")
        print(f"\n{C.DARK_GRAY}{nav_main}{C.RESET}")

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
        elif key in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            idx = int(key) - 1
            handle_action(menu_items[idx][3])
        elif key in ['u', 'U']:
            handle_action("update")
        elif key in ['m', 'M']:
            handle_action("menubar")
        elif key in ['l', 'L']:
            handle_action("toggle_lang")
        elif key in ['0', 'q', 'ESC']:
            bye_msg = txt("macOSCode ile sisteminiz daima en yüksek performansta! Görüşmek üzere! 👋", "Keep your Mac tuned with macOSCode! See you next time! 👋")
            print(f"\n{C.CYAN}{bye_msg}{C.RESET}\n")
            break

def handle_action(action):
    if action == "apply_all":
        apply_prompt = txt("Tüm 100 optimizasyon uygulanacak. Onaylıyor musunuz? (e/h):", "All 100 optimizations will be applied. Continue? (y/n):")
        print(f"\n{C.GOLD}{apply_prompt}{C.RESET} ", end="")
        ans = input().strip().lower()
        if ans in ["e", "evet", "y", "yes"]:
            apply_tweaks_list(TWEAKS, mode="apply")
    elif action == "revert_all":
        revert_prompt = txt("DİKKAT: Tüm ayarlar Apple fabrika varsayılanına döndürülecek. Devam edilsin mi? (e/h):", "WARNING: All settings will revert to Apple factory defaults. Continue? (y/n):")
        print(f"\n{C.ROSE}{revert_prompt}{C.RESET} ", end="")
        ans = input().strip().lower()
        if ans in ["e", "evet", "y", "yes"]:
            apply_tweaks_list(TWEAKS, mode="revert")
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
    elif action == "menubar":
        launch_menubar_app(interactive=True)
    elif action == "update":
        update_mc(interactive=True)
    elif action == "toggle_lang":
        new_lang = "tr" if CURRENT_LANG == "en" else "en"
        save_persisted_lang(new_lang)

# CLI Main Entry Point
def main():
    global CURRENT_LANG
    parser = argparse.ArgumentParser(
        description=f"macOSCode (mc) v{VERSION} - Interactive Terminal UI & macOS Power-User CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""Examples / Örnekler:
  mc                     Launch interactive TUI menu / İnteraktif TUI menüsünü açar
  mc --apply-all         Apply all 100 tweaks in 1-line / Tüm 100 optimizasyonu uygular
  mc --revert-all        Restore all settings to Apple factory defaults / Tüm ayarları sıfırlar
  mc --status            Scan system for active tweaks status / Sistem denetimi (Audit)
  mc --preset dev        Apply developer presets (dev | speed | battery | tahoe)
  mc --menubar           Launch Swift Menu Bar companion app / Menü çubuğu aracını başlatır
  mc --search dock       Search and list tweaks matching "dock"
  mc --lang en           Set active language to English / Turkish (en | tr)
  mc --install           Install "mc" command globally / Sisteme kalıcı kurar
  mc --update            Self-update "mc" CLI from GitHub / GitHub'dan günceller
  mc --version           Show version info (v{VERSION})
"""
    )
    parser.add_argument("-v", "--version", action="version", version=f"macOSCode CLI (mc) v{VERSION} (Build {VERSION_CODE})")
    parser.add_argument("-a", "--apply-all", action="store_true", help=txt("Tüm 100 ayarı uygula", "Apply all 100 optimizations"))
    parser.add_argument("-r", "--revert-all", action="store_true", help=txt("Tüm ayarları sıfırla (revert)", "Restore all settings to Apple factory defaults"))
    parser.add_argument("-s", "--status", action="store_true", help=txt("Sistem denetimi ve durum raporu (Audit)", "Run system configuration audit"))
    parser.add_argument("-p", "--preset", choices=["dev", "speed", "battery", "tahoe"], help=txt("Hızlı optimizasyon paketi çalıştır", "Run preset suite"))
    parser.add_argument("-m", "--menubar", action="store_true", help=txt("macOS Menü Bar hızlı ayar aracını başlat", "Launch macOS Menu Bar companion app"))
    parser.add_argument("--search", type=str, help=txt("Belirli bir kelimeyi ara", "Search tweaks by keyword"))
    parser.add_argument("-l", "--lang", choices=["en", "tr"], help=txt("Dili ayarla (en: English, tr: Türkçe)", "Set CLI language (en: English, tr: Turkish)"))
    parser.add_argument("-d", "--dry-run", action="store_true", help=txt("Komutları çalıştırmadan sadece ekranda göster", "Preview commands without applying"))
    parser.add_argument("-i", "--install", action="store_true", help=txt("'mc' komutunu global sisteme yükle", "Install 'mc' globally to PATH"))
    parser.add_argument("-u", "--update", action="store_true", help=txt("'mc' aracını GitHub'dan en son sürüme güncelle", "Self-update 'mc' to latest GitHub release"))
    parser.add_argument("-f", "--force", action="store_true", help=txt("Sürüm aynı olsa bile güncellemeyi zorla", "Force reinstall during update"))
    parser.add_argument("-t", "--tui", action="store_true", help=txt("İnteraktif TUI modunu başlat", "Launch interactive TUI mode"))

    args = parser.parse_args()

    if args.lang:
        save_persisted_lang(args.lang)

    # Non-interactive CLI flags
    if args.apply_all:
        apply_tweaks_list(TWEAKS, mode="apply", dry_run=args.dry_run)
    elif args.revert_all:
        apply_tweaks_list(TWEAKS, mode="revert", dry_run=args.dry_run)
    elif args.status:
        run_system_audit(interactive=False)
    elif args.menubar:
        launch_menubar_app(interactive=False)
    elif args.preset:
        chosen = PRESETS[args.preset]
        tweaks_to_run = [t for t in TWEAKS if t["id"] in chosen["ids"]]
        apply_tweaks_list(tweaks_to_run, mode="apply", dry_run=args.dry_run)
    elif args.search:
        q = args.search.lower()
        matched = [t for t in TWEAKS if q in t["title"].lower() or q in t.get("title_en", "").lower() or q in t["desc"].lower() or q in t.get("desc_en", "").lower() or q in t["apply"].lower() or q in t["tag"].lower()]
        found_msg = txt(f"'{args.search}' için {len(matched)} ayar bulundu:", f"Found {len(matched)} tweaks matching '{args.search}':")
        print(f"\n{C.CYAN}🔍 {found_msg}{C.RESET}\n")
        for i, t in enumerate(matched, 1):
            print(f" {C.BOLD}{i}. {t_title(t)}{C.RESET} {C.DARK_GRAY}[{t['tag']}]{C.RESET}")
            print(f"    {C.GRAY}{t_desc(t)}{C.RESET}")
            print(f"    {C.CYAN}$ {t['apply'].replace(chr(10), ' && ')}{C.RESET}\n")
    elif args.install:
        install_mc_globally()
    elif args.update:
        update_mc(interactive=False, force=args.force)
    else:
        # Default: Launch Interactive TUI
        run_main_tui()

if __name__ == "__main__":
    main()
