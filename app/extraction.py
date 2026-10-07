"""
Information Extraction Module for Multilingual Emergency & Safety Assistant.
Extracts incident location, injured count, affected count, and key emergency triggers.
Uses regex / rule-based patterns for English, Tamil, and Tanglish.
Strictly returns 'Not detected' when information is absent (no hallucination).
"""

import re
from typing import Dict, List, Any


# Common emergency keywords vocabulary mapped across languages
EMERGENCY_KEYWORDS = [
    # Medical
    "ambulance", "hospital", "doctor", "collapsed", "unconscious", "heart attack",
    "breathing", "bleeding", "blood", "chest pain", "seizure", "poison", "wound",
    "stroke", "clinic", "oxygen", "maruthuvamanai", "aambulans", "mayakkam",
    "raththam", "nenju vali", "uyir", "ill", "sick", "pain",
    "ஆம்புலன்ஸ்", "மருத்துவமனை", "மயக்கம்", "ரத்தம்", "மூச்சு", "மாரடைப்பு", "காயம்",
    
    # Accident
    "accident", "crash", "collision", "hit", "vehicle", "car", "bike", "bus",
    "lorry", "truck", "overturned", "run over", "head on", "speed", "road",
    "aayiduchu", "modhiruchu", "kavunthuruchu", "adi",
    "விபத்து", "மோதியது", "கவிழ்ந்தது", "சாலை", "வாகனம்",
    
    # Fire
    "fire", "blaze", "flames", "burning", "smoke", "explosion", "blast",
    "cylinder", "short circuit", "thee", "theepudichiruchu", "eriyudhu", "puga",
    "தீ", "தீப்பிடித்தது", "நெருப்பு", "புகை", "வெடிப்பு", "சிலிண்டர்",
    
    # Police / Crime
    "police", "theft", "robbery", "stolen", "attacked", "assault", "murder",
    "gun", "knife", "stalker", "follow", "kidnap", "thief", "threat", "fight",
    "thirudan", "kolai", "adi", "bayama", "thiruttu", "panranga",
    "போலீஸ்", "திருட்டு", "தாக்குதல்", "கொலை", "கத்தி", "துப்பாக்கி",
    
    # Personal Safety
    "safety", "harass", "harassment", "abuse", "danger", "unsafe", "stalking",
    "trapped", "help", "alone", "help venum", "kaapathi", "thappikka", "protection",
    "பாதுகாப்பு", "உதவி", "ஆபத்து", "காப்பாற்றுங்கள்", "துன்புறுத்தல்",
    
    # Natural Disaster
    "flood", "earthquake", "cyclone", "storm", "tsunami", "landslide", "heavy rain",
    "drowning", "submerged", "vellam", "mazhai", "puyal", "kaathu", "nilanadukkam",
    "வெள்ளம்", "நிலநடுக்கம்", "புயல்", "மழை", "மண்சரிவு", "சுனாமி"
]


WORD_TO_NUMBER = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "someone": 1, "somebody": 1, "a person": 1, "single person": 1,
    "oru": 1, "oruvar": 1, "oru person": 1, "oruthar": 1,
    "rendu": 2, "irandu": 2, "iruvar": 2,
    "moonu": 3, "moondru": 3, "moovar": 3,
    "naalu": 4, "naangu": 4,
    "anji": 5, "aindhu": 5
}


def extract_location(text: str) -> str:
    """
    Extracts location mentioned in English, Tamil, or Tanglish.
    Looks for spatial prepositions, landmarks, and Tamil location markers.
    """
    if not text:
        return "Not detected"

    # Pattern 1: Prepositions in English / Tanglish (near, at, opposite to, behind, close to, next to, etc.)
    # Example: "near Thoothukudi bus stand, 2 people injured"
    prep_pattern = re.search(
        r"(?:near|at|opposite to|opposite|close to|behind|next to|in front of|towards|around)\s+([A-Za-z0-9\u0B80-\u0BFF\s,'\-]+?)(?=[,\.\?!]|\s+(?:\d+\s*(?:people|persons|injured)|someone\b|urgently\b|please\b|help\b)|$)",
        text,
        re.IGNORECASE
    )
    if prep_pattern:
        loc = prep_pattern.group(1).strip()
        loc = re.sub(r"^(?:the|a|an)\s+", "", loc, flags=re.IGNORECASE).strip()
        # Avoid generic false positives like 'my home', 'here', 'my area'
        if len(loc) >= 3 and loc.lower() not in ["my home", "my house", "my room", "here", "my area"]:
            return loc

    # Pattern 2: Landmark with proper noun / place name
    # e.g. "Thoothukudi bus stand", "Anna Nagar signal", "Tambaram railway station"
    landmark_pattern = re.search(
        r"([A-Za-z\u0B80-\u0BFF][A-Za-z0-9\u0B80-\u0BFF\s]{1,30}?\s*(?:bus stand|railway station|hospital|school|college|bridge|junction|signal|flyover|toll gate|highway|street|bazaar|market|temple|church|mosque|lake|beach|park|hall|பஸ் நிலையம்|பேருந்து நிலையம்|ரயில் நிலையம்|மருத்துவமனை|பள்ளி|கல்லூரி|பாலம்|சந்திப்பு))",
        text,
        re.IGNORECASE
    )
    if landmark_pattern:
        loc = landmark_pattern.group(1).strip()
        if len(loc) >= 3:
            return loc

    # Pattern 3: Tanglish suffix (e.g. "bus stand pakkatula", "signal kitta", "school munnadi")
    tanglish_suffix = re.search(
        r"([A-Za-z0-9\s]{2,30}?)\s+(?:pakkatula|kitta|munnadi|la|kithey)",
        text,
        re.IGNORECASE
    )
    if tanglish_suffix:
        loc = tanglish_suffix.group(1).strip()
        if len(loc) >= 3 and not loc.lower() in ["road", "street", "car", "bike"]:
            return loc

    # Pattern 4: Tamil markers (e.g. "... அருகில்", "... பகுதியில்", "... எதிரில்")
    tamil_pattern = re.search(
        r"([\u0B80-\u0BFF\s]{2,35}?)\s+(?:அருகில்|பகுதியில்|முன்பு|பக்கத்தில்|எதிரில்|நோக்கி)",
        text
    )
    if tamil_pattern:
        loc = tamil_pattern.group(1).strip()
        tamil_stop_words = ["எங்கள்", "நமது", "என்", "இந்த", "அந்த", "ஒரு"]
        if loc in tamil_stop_words:
            loc = ""
        else:
            # Strip leading pronouns if present (e.g. "எங்கள் சென்னை பகுதியில்" -> "சென்னை")
            for sw in tamil_stop_words:
                if loc.startswith(sw + " "):
                    loc = loc[len(sw) + 1:].strip()
        if len(loc) >= 3 and loc not in tamil_stop_words:
            return loc

    # Pattern 5: In / near English place (e.g. "in Chennai", "near my school")
    gen_pattern = re.search(
        r"(?:near|in|at)\s+([A-Z][a-zA-Z0-9\s]+?)(?=[,\.\?!]|\s+and|\s+with|$)",
        text
    )
    if gen_pattern:
        loc = gen_pattern.group(1).strip()
        if len(loc) >= 3:
            return loc

    return "Not detected"


def extract_injured_count(text: str) -> Any:
    """
    Extracts the number of injured people.
    Returns integer count or 'Not detected'.
    """
    if not text:
        return "Not detected"

    # Case 1: Numeric digits + injury indicators
    # e.g. "2 people injured", "3 persons hurt", "injured: 2", "1 person hospitalized", "1 person unconscious"
    num_pattern = re.search(
        r"(\d+)\s*(?:person|people|persons|individuals|patient|patients|men|women|kids|children|passengers|members|per|பேர்|நபர்கள்)?\s*(?:badly\s+)?(?:injured|hurt|wounded|hospitalized|bleeding|unconscious|காயம்|படுகாயம்)",
        text,
        re.IGNORECASE
    )
    if num_pattern:
        return int(num_pattern.group(1))

    # Case 2: Injury word followed by digits (e.g. "injured 2", "casualties 3")
    reverse_pattern = re.search(
        r"(?:injured|hurt|casualties|hospitalized|காயம்)\s*(?:count|persons|people)?\s*[:\-\s]\s*(\d+)",
        text,
        re.IGNORECASE
    )
    if reverse_pattern:
        return int(reverse_pattern.group(1))

    # Case 3: Word numbers (e.g. "someone badly injured", "two people injured", "oruvarukku kaayam")
    for word, count in WORD_TO_NUMBER.items():
        pattern = rf"\b{re.escape(word)}\b\s*(?:is\s+|was\s+)?(?:badly\s+)?(?:injured|hurt|wounded|hospitalized|காயம்|படுகாயம்|adi|kaayam)"
        if re.search(pattern, text, re.IGNORECASE):
            return count

    # Case 4: General mention of "someone injured" or "person injured"
    if re.search(r"(?:someone|somebody|a person|one person)\s+(?:badly\s+)?(?:injured|hurt|bleeding|collapsed)", text, re.IGNORECASE):
        return 1

    # Case 5: Tamil words
    if re.search(r"(?:ஒருவர்|ஒருத்தர்)\s+(?:காயம்|படுகாயம்)", text):
        return 1
    if re.search(r"(?:இருவர்|இரண்டு பேர்)\s+(?:காயம்|படுகாயம்)", text):
        return 2

    return "Not detected"


def extract_affected_count(text: str) -> Any:
    """
    Extracts the number of people affected / trapped / stranded.
    """
    if not text:
        return "Not detected"

    num_pattern = re.search(
        r"(\d+)\s*(?:people|persons|residents|families|villagers|students|per|பேர்)?\s*(?:trapped|stranded|affected|missing|suffering|சிக்கியுள்ளனர்|பாதிக்கப்பட்டுள்ளனர்)",
        text,
        re.IGNORECASE
    )
    if num_pattern:
        return int(num_pattern.group(1))

    for word, count in WORD_TO_NUMBER.items():
        pattern = rf"\b{re.escape(word)}\b\s*(?:people|persons)?\s*(?:trapped|stranded|affected|missing)"
        if re.search(pattern, text, re.IGNORECASE):
            return count

    return "Not detected"


def extract_keywords(text: str) -> List[str]:
    """
    Extracts detected emergency keywords present in the text.
    """
    if not text:
        return []

    lower_text = text.lower()
    detected = []
    
    for kw in EMERGENCY_KEYWORDS:
        # Match as word boundary or exact substring
        if re.search(rf"\b{re.escape(kw)}\b", lower_text) or kw in lower_text:
            if kw not in detected:
                detected.append(kw)
                
    return detected[:8]  # Limit to most relevant 8 keywords


def extract_emergency_information(text: str) -> Dict[str, Any]:
    """
    Runs the complete information extraction suite.
    """
    return {
        "location": extract_location(text),
        "people_injured": extract_injured_count(text),
        "people_affected": extract_affected_count(text),
        "keywords": extract_keywords(text)
    }


if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    test_cases = [
        "Road la accident aayiduchu near Thoothukudi bus stand, 2 people injured",
        "எங்கள் வீட்டில் தீப்பிடித்துவிட்டது",
        "I need an ambulance immediately, 1 person unconscious near City Hospital",
        "Yaaro enna follow panranga",
        "எங்கள் பகுதியில் வெள்ளம் ஏற்பட்டுள்ளது, 5 பேர் சிக்கியுள்ளனர்",
        "Road la accident aayiduchu, someone badly injured"
    ]
    for tc in test_cases:
        print(f"\n--- Input: {tc} ---")
        res = extract_emergency_information(tc)
        print("Location:", res["location"])
        print("People Injured:", res["people_injured"])
        print("People Affected:", res["people_affected"])
        print("Keywords:", res["keywords"])
