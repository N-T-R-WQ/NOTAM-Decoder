from datetime import datetime
import re
import pyttsx3

# --- SPEECH PRONUNCIATION MAPS ---
HOURS_MINS_WORDS = {
    "00": "zero zero", "01": "zero one", "02": "zero two", "03": "zero three",
    "04": "zero four", "05": "zero five", "06": "zero six", "07": "zero seven",
    "08": "zero eight", "09": "zero nine", "10": "ten", "11": "eleven",
    "12": "twelve", "13": "thirteen", "14": "fourteen", "15": "fifteen",
    "16": "sixteen", "17": "seventeen", "18": "eighteen", "19": "nineteen",
    "20": "twenty", "21": "twenty one", "22": "twenty two", "23": "twenty three",
    "24": "twenty four", "25": "twenty five", "26": "twenty six", "27": "twenty seven",
    "28": "twenty eight", "29": "twenty nine", "30": "thirty", "31": "thirty one",
    "32": "thirty two", "33": "thirty three", "34": "thirty four", "35": "thirty five",
    "36": "thirty six", "37": "thirty seven", "38": "thirty eight", "39": "thirty nine",
    "40": "forty", "41": "forty one", "42": "forty two", "43": "forty three",
    "44": "forty four", "45": "forty five", "46": "forty six", "47": "forty seven",
    "48": "forty eight", "49": "forty nine", "50": "fifty", "51": "fifty one",
    "52": "fifty two", "53": "fifty three", "54": "fifty four", "55": "fifty five",
    "56": "fifty six", "57": "fifty seven", "58": "fifty eight", "59": "fifty nine"
}

# Extensive Australian ICAO Airport & Aviation Dictionary
METAR_NOTAM_DICT = {
    # --- MAJOR INTERNATIONAL & DOMESTIC AIRPORTS ---
    "YSSY": "Sydney Kingsford Smith Airport",
    "YMML": "Melbourne Airport",
    "YBBN": "Brisbane Airport",
    "YPPH": "Perth Airport",
    "YPAD": "Adelaide Airport",
    "YBCG": "Gold Coast Airport",
    "YSCB": "Canberra Airport",
    "YPDN": "Darwin International Airport",
    "YMHB": "Hobart International Airport",
    "YBCS": "Cairns Airport",
    "YBTL": "Townsville Airport",
    "YMCY": "Sunshine Coast Airport",
    "YAMB": "Amberley RAAF Base",
    "YPEA": "Pearce RAAF Base",
    "YSRI": "Richmond RAAF Base",
    "YWLM": "Williamtown RAAF Base",
    "YEDN": "Edinburg RAAF Base",
    
    # --- GENERAL AVIATION & METROPOLITAN SECONDARY ---
    "YSBK": "Bankstown Airport",
    "YMMB": "Moorabbin Airport",
    "YPJT": "Jandakot Airport",
    "YBAF": "Archerfield Airport",
    "YPPF": "Parafield Airport",
    "YCAI": "Camden Airport",
    "YCWH": "Moorabbin / Coldstream",
    "YAVV": "Avalon Airport",
    "YBLN": "Busselton Margaret River Airport",

    # --- REGIONAL NEW SOUTH WALES ---
    "YMDG": "Mudgee Airport",
    "YMAY": "Albury Airport",
    "YWAG": "Wagga Wagga Airport",
    "YSDU": "Dubbo City Regional Airport",
    "YTWN": "Tamworth Regional Airport",
    "YARM": "Armidale Regional Airport",
    "YCFS": "Coffs Harbour Airport",
    "YPKA": "Port Macquarie Airport",
    "YBHI": "Broken Hill Airport",
    "YGLI": "Glen Innes Airport",
    "YGRA": "Grafton Airport",
    "YGTH": "Griffith Airport",
    "YLHI": "Lord Howe Island Airport",
    "YMOR": "Moree Airport",
    "YNAR": "Narrabri Airport",
    "YNRA": "Narrandera Airport",
    "YORG": "Orange Airport",

    # --- REGIONAL VICTORIA ---
    "YBDG": "Bendigo Airport",
    "YBLT": "Ballarat Airport",
    "YMGB": "Gambier Airport",
    "YMHU": "Mount Hotham Airport",
    "YMES": "East Sale RAAF Base",
    "YMNG": "Mangalore Airport",
    "YMLT": "Launceston Airport",
    "YMIA": "Mildura Airport",
    "YSHT": "Shepparton Airport",
    "YWGP": "Wangaratta Airport",

    # --- REGIONAL QUEENSLAND ---
    "YBRK": "Rockhampton Airport",
    "YBMK": "Mackay Airport",
    "YGLA": "Gladstone Airport",
    "YBUD": "Bundaberg Airport",
    "YFRA": "Fraser Coast / Hervey Bay Airport",
    "YHID": "Horn Island Airport",
    "YISA": "Mount Isa Airport",
    "YROM": "Roma Airport",
    "YCHA": "Charleville Airport",
    "YEGP": "Emerald Airport",
    "YLHI": "Hamilton Island Airport",
    "YMKU": "Mackay Airport",
    "YBCV": "Charters Towers Airport",

    # --- REGIONAL WESTERN AUSTRALIA ---
    "YPKG": "Kalgoorlie-Boulder Airport",
    "YPPD": "Port Hedland International Airport",
    "YBMA": "Karratha Airport",
    "YBRM": "Broome International Airport",
    "YPKG": "Esperance Airport",
    "YABA": "Albany Airport",
    "YARG": "Argyle Airport",
    "YPXU": "Exmouth Airport",
    "YNWU": "Paraburdoo Airport",

    # --- REGIONAL SOUTH AUSTRALIA & NT ---
    "YBAS": "Alice Springs Airport",
    "YAYE": "Ayers Rock / Uluru Airport",
    "YKNG": "Kingscote / Kangaroo Island Airport",
    "YPLC": "Port Lincoln Airport",
    "YWHY": "Whyalla Airport",

    # --- NOTAM & TAF TERMINOLOGY ---
    "TAF": "Terminal Area Forecast",
    "TAF3": "TAF3 service active",
    "CAVOK": "CAV OK",
    "RWY": "runway",
    "TWY": "taxiway",
    "CLSD": "closed",
    "WIP": "work in progress",
    "MAINT": "maintenance",
    "WEF": "with effect from",
    "TIL": "until",
    "U/S": "unserviceable",
    "AVBL": "available",
    "UNAVBL": "unavailable",
    "TEMP": "temporary",
    "EST": "estimated",
    "DUE": "due to",
    "HLDG": "holding",
    "LGT": "light",
    "EST": "Eastern Standard Time",
    "SHRA": "showers of rain",
    "SH": "showers of",
    "RA": "rain",
    "DZ": "drizzle",
    "TS": "thunderstorm",
    "FEW": "cloud few at",
    "SCT": "scattered cloud at",
    "BKN": "broken cloud at",
    "OVC": "overcast at",
    "TCU": "towering cumulus",
    "CB": "cumulonimbus",
    "INTER": "Intermittent variations from",
    "TEMPO": "Temporary variations from",
    "RMK": "Remarks:",
}

def format_spoken_time(hhmm_str):
    """Converts '2330' -> 'twenty three thirty'."""
    hh, mm = hhmm_str[:2], hhmm_str[2:]
    return f"{HOURS_MINS_WORDS.get(hh, hh)} {HOURS_MINS_WORDS.get(mm, mm)}"

def spell_out_icao(icao_code):
    """Fallback function to spell out unmapped 4-letter ICAO codes (e.g., YBHI -> Y B H I)."""
    return " ".join(list(icao_code))

def parse_wind(token):
    """Converts wind groups like 31008KT or 28020G35KT into natural spoken English[cite: 1]."""
    match = re.match(r"^(\d{3})(\d{2})(G\d{2})?KT$", token)
    if not match:
        return token
    
    dir_deg, speed_kt, gust = match.groups()
    spoken_dir = " ".join(dir_deg)  # "310" -> "3 1 0"
    
    result = f"Wind {spoken_dir} degrees at {int(speed_kt)} knots"
    if gust:
        result += f" gusting at {int(gust[1:])} knots"
    return result

def parse_cloud(token):
    """Converts cloud layers like SCT045 into 'scattered cloud at 4500 feet'[cite: 1, 2]."""
    match = re.match(r"^(FEW|SCT|BKN|OVC)(\d{3})(TCU|CB)?$", token)
    if not match:
        return token
    
    cover, alt, cloud_type = match.groups()
    cover_str = METAR_NOTAM_DICT.get(cover, cover)
    alt_feet = int(alt) * 100
    type_str = f" {METAR_NOTAM_DICT.get(cloud_type, cloud_type)}" if cloud_type else ""
    
    return f"{cover_str} {alt_feet} feet{type_str}"

def parse_validity_period(token):
    """Converts TAF validities like 0300/0406 into spoken dates/times[cite: 1]."""
    match = re.match(r"^(\d{2})(\d{2})/(\d{2})(\d{2})$", token)
    if not match:
        return token
    
    start_d, start_h, end_d, end_h = match.groups()
    return f"Effective {start_d} {format_spoken_time(start_h + '00')} to {end_d} {format_spoken_time(end_h + '00')}"

def convert_aviation_text(raw_text):
    """Decodes raw TAF and NOTAM blocks into plain English for TTS speech[cite: 1, 2]."""
    lines = raw_text.strip().split("\n")
    processed_lines = []

    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
            
        words = line_clean.split()
        translated_words = []

        for word in words:
            clean = word.strip(",.:;/()")
            upper = clean.upper()

            # 1. Expand known airport codes and terms
            if upper in METAR_NOTAM_DICT:
                translated_words.append(METAR_NOTAM_DICT[upper])
            # 2. Dynamic handling for unmapped Australian ICAO codes (starts with Y and 4 letters)
            elif re.match(r"^Y[A-Z]{3}$", upper):
                translated_words.append(f"Airport {spell_out_icao(upper)}")
            # 3. Time blocks like FM030500
            elif re.match(r"^FM\d{6}$", upper):
                day, time_str = upper[2:4], upper[4:]
                translated_words.append(f"From {day} {format_spoken_time(time_str)}")
            # 4. 10-digit dates (YYMMDDHHMM or MMDDHHMM)
            elif re.match(r"^\d{10}$", clean):
                try:
                    dt = datetime.strptime(clean, "%y%m%d%H%M")
                    translated_words.append(f"{dt.strftime('%B %d')} {format_spoken_time(dt.strftime('%H%M'))}")
                except ValueError:
                    translated_words.append(clean)
            # 5. Parse Wind (e.g. 31008KT)
            elif re.match(r"^\d{3}\d{2}(G\d{2})?KT$", upper):
                translated_words.append(parse_wind(upper))
            # 6. Parse Clouds (e.g. SCT045 or FEW060TCU)
            elif re.match(r"^(FEW|SCT|BKN|OVC)\d{3}(TCU|CB)?$", upper):
                translated_words.append(parse_cloud(upper))
            # 7. TAF Validity Period (e.g. 0300/0406)
            elif re.match(r"^\d{4}/\d{4}$", upper):
                translated_words.append(parse_validity_period(upper))
            # 8. Visibility (9999 or 5000 meters)
            elif upper == "9999":
                translated_words.append("visibility 10 kilometers or more")
            elif re.match(r"^\d{4}$", upper) and not upper.endswith("Z"):
                translated_words.append(f"visibility {clean} meters")
            # 9. Time with Zulu stamp (e.g. 022322Z)
            elif re.match(r"^\d{6}Z$", upper):
                day, time_str = upper[:2], upper[2:6]
                translated_words.append(f"at {day} {format_spoken_time(time_str)} Zulu")
            # 10. Temperature / QNH indicators
            elif upper in ["T", "Q"]:
                translated_words.append("Temperature" if upper == "T" else "QNH")
            else:
                translated_words.append(word)

        processed_lines.append(" ".join(translated_words))

    return "\n".join(processed_lines)

def speak_text(text):
    """Plays converted text through local Text-to-Speech audio engine."""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"(Audio playback error: {e})")

# --- SAMPLE RUN ---
if __name__ == "__main__":
    sample_input = """
TAF YSSY 022322Z 0300/0406
31008KT CAVOK
FM030500 33014KT 9999 SHRA SCT045
"""
    decoded = convert_aviation_text(sample_input)
    print("\n--- DECODED BRIEFING ---")
    print(decoded)
    speak_text(decoded)
