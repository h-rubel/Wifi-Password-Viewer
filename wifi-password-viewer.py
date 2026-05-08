import subprocess
import time
import os

wifi_data = []


# Clear terminal
def clear():
    os.system('cls')


# 🎨 Colored Signal UI
def signal_ui(signal_text):
    try:
        digits = ''.join([c for c in signal_text if c.isdigit()])

        if not digits:
            return "⚪ Unknown"

        strength = int(digits)

        filled = int(strength / 10)
        empty = 10 - filled
        bar = "█" * filled + "░" * empty

        # ANSI colors
        RESET = "\033[0m"
        GREEN_BG = "\033[42m"
        YELLOW_BG = "\033[43m"
        RED_BG = "\033[41m"
        BLACK = "\033[30m"

        if strength >= 75:
            color = GREEN_BG
            status = "STRONG"
        elif strength >= 40:
            color = YELLOW_BG
            status = "MEDIUM"
        else:
            color = RED_BG
            status = "WEAK"

        return f"{color}{BLACK} {status} | {bar} | {strength}% {RESET}"

    except:
        return "⚪ Unknown"


# 📶 Connected WiFi
def get_connected_wifi():

    ssid = "Unknown"
    signal = "0"

    try:
        result = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'interfaces']
        ).decode('utf-8', errors="ignore")

        for line in result.split('\n'):

            if "SSID" in line and "BSSID" not in line:
                ssid = line.split(":")[-1].strip()

            if "Signal" in line:
                signal = line.split(":")[-1].strip()

    except:
        pass

    return ssid, signal


# 💾 WiFi Profiles
def get_wifi_profiles():

    wifi_data.clear()

    profiles_data = subprocess.check_output(
        ['netsh', 'wlan', 'show', 'profiles']
    ).decode('utf-8', errors="ignore")

    profiles = []

    for line in profiles_data.split('\n'):
        if "All User Profile" in line:
            profile = line.split(":")[-1].strip()
            profiles.append(profile)

    for profile in profiles:

        try:
            results = subprocess.check_output(
                ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']
            ).decode('utf-8', errors="ignore")

            password = "No Password"
            auth = "Unknown"
            cipher = "Unknown"

            for line in results.split('\n'):

                if "Key Content" in line:
                    password = line.split(":")[-1].strip()

                if "Authentication" in line:
                    auth = line.split(":")[-1].strip()

                if "Cipher" in line:
                    cipher = line.split(":")[-1].strip()

            wifi_data.append({
                "ssid": profile,
                "password": password,
                "authentication": auth,
                "cipher": cipher
            })

        except:
            pass


# 📁 Export
def export_passwords():

    with open("wifi_passwords.txt", "w", encoding="utf-8") as file:

        for wifi in wifi_data:

            file.write(f"WiFi Name      : {wifi['ssid']}\n")
            file.write(f"Password       : {wifi['password']}\n")
            file.write(f"Authentication : {wifi['authentication']}\n")
            file.write(f"Cipher         : {wifi['cipher']}\n")
            file.write("-" * 40 + "\n")

    print("\nExported to wifi_passwords.txt")
    time.sleep(2)


# ================= MAIN LOOP =================
while True:

    clear()

    connected_wifi, signal = get_connected_wifi()

    get_wifi_profiles()

    print("==============================")
    print("   WIFI PASSWORD VIEWER ")
    print("==============================\n")

    print(f"📶 Connected WiFi : {connected_wifi}")
    print(f"📊 Signal        : {signal_ui(signal)}\n")

    print("💾 Saved WiFi List:\n")

    for index, wifi in enumerate(wifi_data):

        print(f"[{index}] WiFi Name      : {wifi['ssid']}")
        print(f"     Password       : {wifi['password']}")
        print(f"     Authentication : {wifi['authentication']}")
        print(f"     Cipher         : {wifi['cipher']}")
        print("-" * 40)

    print("\nOptions:")
    print("1. Export Passwords")
    print("2. Exit")

    choice = input("\nEnter choice: ")

    if choice == "1":
        export_passwords()

    elif choice == "2":
        break
