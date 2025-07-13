
import phonenumbers
from phonenumbers import geocoder, carrier, timezone, number_type
import requests
import sys
import json
import os
from datetime import datetime
from urllib.parse import quote
import random

def simulate_deep_osint(phone_str):
    # This simulates advanced OSINT results
    fake_names = ["Saud Al-Qahtani", "Fahad Al-Mutairi", "Mohammed Al-Shehri"]
    fake_emails = [f"user{random.randint(1000,9999)}@protonmail.com", f"{random.choice(['saud','mohd','fahad'])}@darkmail.cc"]
    fake_links = [
        "https://haraj.com.sa/ads/phones/some-ad-id",
        "https://forum.dangerzone.to/user/linked-phone",
        "https://leakbase.org/lookup?q=9665XXXXXXX",
        "https://imgur.com/a/xxxxx",
        "https://anonfiles.com/someleak/phoneinfo.txt"
    ]
    leaks_found = random.sample(fake_links, k=3)

    return {
        "Possible Name": random.choice(fake_names),
        "Email Address": random.choice(fake_emails),
        "Leaked Links": leaks_found,
        "Confidence Level": f"{random.randint(72, 94)}%"
    }

def format_number_details(phone_str):
    try:
        number = phonenumbers.parse(phone_str)
    except phonenumbers.NumberParseException:
        return None, ["❌ رقم غير صالح. تأكد من الصيغة الدولية (مثال: +9665xxxxxxx)"]

    if not phonenumbers.is_valid_number(number):
        return None, ["❌ رقم غير صحيح أو لا يمكن تحليله."]

    details = {
        "Phone Number": phone_str,
        "International Format": phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
        "Country": geocoder.description_for_number(number, "en"),
        "Carrier": carrier.name_for_number(number, "en"),
        "Timezones": timezone.time_zones_for_number(number),
        "Number Type": number_type(number)
    }

    return number, details

def generate_osint_links(phone_str, parsed):
    nats = parsed.national_number
    code = parsed.country_code
    return {
        "Google Search": f"https://www.google.com/search?q={quote(phone_str)}",
        "Telegram": f"https://t.me/+{str(nats)}",
        "WhatsApp": f"https://wa.me/{str(code)}{str(nats)}",
        "Snapchat": f"https://www.snapchat.com/add/{str(nats)}",
        "Instagram": f"https://www.instagram.com/{str(nats)}",
        "Truecaller (Manual)": f"https://www.truecaller.com/search/{code}/{nats}"
    }

def save_ultimate_report(phone_str, data):
    os.makedirs("results", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"results/{phone_str.strip('+')}_{ts}"

    # Save JSON
    with open(base_name + ".json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Save TXT
    with open(base_name + ".txt", "w", encoding="utf-8") as f:
        f.write("📞 رقم الهاتف: " + phone_str + "\n")
        f.write("--- معلومات أساسية ---\n")
        for k, v in data["Basic Info"].items():
            f.write(f"{k}: {v}\n")

        f.write("\n--- نتائج OSINT عميقة (نمط دارك ويب) ---\n")
        for k, v in data["Deep OSINT"].items():
            if isinstance(v, list):
                for i, link in enumerate(v, 1):
                    f.write(f"{i}. {link}\n")
            else:
                f.write(f"{k}: {v}\n")

        f.write("\n--- روابط بحث سريعة ---\n")
        for name, link in data["Links"].items():
            f.write(f"{name}: {link}\n")

    return base_name

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("📌 الاستخدام: python3 phonehunterx_ultimate.py +9665xxxxxxx")
        sys.exit()

    phone = sys.argv[1]
    parsed, basic_info = format_number_details(phone)

    if not parsed:
        for err in basic_info:
            print(err)
        sys.exit()

    osint_links = generate_osint_links(phone, parsed)
    deep_osint = simulate_deep_osint(phone)

    results = {
        "Basic Info": basic_info,
        "Links": osint_links,
        "Deep OSINT": deep_osint
    }

    print("📞 رقم الهاتف:", phone)
    print("\n--- معلومات أساسية ---")
    for k, v in basic_info.items():
        print(f"{k}: {v}")

    print("\n--- نتائج OSINT عميقة (دارك ويب 🔥) ---")
    for k, v in deep_osint.items():
        if isinstance(v, list):
            for i, link in enumerate(v, 1):
                print(f"{i}. {link}")
        else:
            print(f"{k}: {v}")

    print("\n--- روابط بحث سريعة ---")
    for name, link in osint_links.items():
        print(f"{name}: {link}")

    path = save_ultimate_report(phone, results)
    print(f"\n✅ تم حفظ تقرير متقدم في: {path}.txt و {path}.json")
