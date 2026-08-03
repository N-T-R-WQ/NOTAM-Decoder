from datetime import datetime
import re
import pyttsx3

# Number to words dictionary for natural time pronunciation
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

# Dictionary of Australian Airports, FIRs, and NOTAM Terms
NOTAM_DICT = {
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
    "YSBK": "Bankstown Airport",
    "YMMB": "Moorabbin Airport",
    "YPJT": "Jandakot Airport",
    "YBAF": "Archerfield Airport",
    "YPPF": "Parafield Airport",
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
    "CAVOK": "CAV OK",  # Converts CAVOK so speech engine says "CAV OK"
}

def format_spoken_time(hhmm_str):
    """Converts a 4-digit time string like '2330' into 'twenty three thirty'."""
    hh = hhmm_str[:2]
    mm = hhmm_str[2:]
    
    spoken_hh = HOURS_MINS_WORDS.get(hh, hh)
    spoken_mm = HOURS_MINS_WORDS.get(mm, mm)
    
    return f"{spoken_hh} {spoken_mm}"

def parse_time_input(token):
    """Converts times like 2330, 2330Z, 0800UTC into spoken two-number format."""
    clean = token.rstrip("Zz").upper()
    
    if re.match(r"^\d{4}$", clean):
        spoken = format_spoken_time(clean)
        return f"{spoken} U T C" if token.upper().endswith("Z") else spoken

    return token

def expand_notam_date(token):
    """Converts YYMMDDHHMM or YYMMDDHHMMZ into plain text date and spoken time."""
    clean_token = token.rstrip("Zz")
    if not re.match(r"^\d{10}$", clean_token):
        return token

    try:
        dt = datetime.strptime(clean_token, "%y%m%d%H%M")
        date_str = dt.strftime("%B %d, %Y")
        time_str = dt.strftime("%H%M")
        spoken_time = format_spoken_time(time_str)
        return f"{date_str} at {spoken_time} U T C"
    except ValueError:
        return token

def expand_runway(token):
    """Expands runway codes like '16R/34L' into 'Runway 16 Right / 34 Left'."""
    pattern = r"^(\d{2}[LCR]?)(/(\d{2}[LCR]?))?$"
    match = re.match(pattern, token, re.IGNORECASE)
    if not match:
        return token

    def format_rwy(code):
        num = code[:2]
        side = {"L": " Left", "R": " Right", "C": " Center"}.get(code[2:].upper(), "")
        return f"{num}{side}"

    rwy1 = format_rwy(match.group(1))
    if match.group(3):
        return f"Runway {rwy1} / {format_rwy(match.group(3))}"
    return f"Runway {rwy1}"

def convert_notam(raw_text):
    text = re.sub(r"\b[A-E]\)", "", raw_text)
    words = text.split()
    translated = []

    for word in words:
        clean = word.strip(",.:;/()")
        upper = clean.upper()

        if upper in NOTAM_DICT:
            translated.append(NOTAM_DICT[upper])
        elif re.match(r"^\d{10}Z?$", clean, re.IGNORECASE):
            translated.append(expand_notam_date(clean))
        elif re.match(r"^\d{4}Z?$", upper):
            translated.append(parse_time_input(clean))
        elif re.match(r"^\d{2}[LCR]?(/\d{2}[LCR]?)?$", upper):
            translated.append(expand_runway(upper))
        else:
            translated.append(word)

    return " ".join(translated)

def speak_text(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"(Audio playback unavailable: {e})")

if __name__ == "__main__":
    sample = "A) YSSY B) 2608032330 E) WX CAVOK RWY 16R CLSD WEF 2330Z"
    result = convert_notam(sample)
    
    print("\n--- CONVERTED TEXT FOR SPEECH ---")
    print(result)
    
    print("\n🔊 Playing Audio...")
    speak_text(result)
