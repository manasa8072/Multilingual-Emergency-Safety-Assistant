"""
Emergency Response Generation Module.
Provides safe, predefined, deterministic response templates based on Emergency Type and Urgency.

Safety Rule (Section 25):
The system must NEVER claim that emergency services or first responders have been dispatched.
It must direct the user to contact local emergency services immediately.
"""

from typing import Dict, Any


SAFE_RESPONSE_TEMPLATES = {
    ("Medical", "High"): (
        "Medical emergency detected. Please seek immediate medical assistance and call emergency medical services (108 / 112)."
    ),
    ("Accident", "High"): (
        "Serious accident detected. Please contact emergency services immediately and ensure you are in a safe location."
    ),
    ("Fire", "High"): (
        "Fire emergency detected. Move to a safe location and contact fire emergency services (101 / 112) immediately."
    ),
    ("Police / Crime", "High"): (
        "Possible security emergency detected. Move to a safe location and contact the police (100 / 112) immediately."
    ),
    ("Personal Safety", "High"): (
        "Personal safety emergency detected. Move to a safe place and seek assistance or call emergency support (112 / 1091)."
    ),
    ("Natural Disaster", "High"): (
        "Natural disaster emergency detected. Move to a safe area and follow local emergency instructions and disaster helplines."
    ),
    
    # Medium Urgency Templates
    ("Medical", "Medium"): (
        "Medical concern detected. Monitor the situation carefully and consult a doctor or healthcare center if condition worsens."
    ),
    ("Accident", "Medium"): (
        "Incident or minor collision reported. Ensure everyone is in a safe location away from active traffic and exchange information if safe."
    ),
    ("Fire", "Medium"): (
        "Potential fire or smoke concern detected. Stay alert, keep fire extinguishers ready, and evacuate immediately if smoke spreads."
    ),
    ("Police / Crime", "Medium"): (
        "Non-critical security concern reported. Stay in a well-lit, populated area and report details to local law enforcement."
    ),
    ("Personal Safety", "Medium"): (
        "Personal safety concern noted. Stay in public areas, inform a trusted contact or friend, and contact local authorities if you feel unsafe."
    ),
    ("Natural Disaster", "Medium"): (
        "Weather or environmental advisory detected. Stay indoors, avoid waterlogged areas, and follow official local forecasts."
    ),
}

EMERGENCY_CONTACT_DIRECTORY = {
    "National Emergency Hotline": "112",
    "Police Helpline": "100",
    "Fire Service": "101",
    "Ambulance / Medical": "108",
    "Women Safety Helpline": "1091",
    "Disaster Management": "1077"
}


def generate_emergency_response(emergency_type: str, urgency: str) -> Dict[str, Any]:
    """
    Generates safe recommended actions and helplines.
    """
    key = (emergency_type, urgency)
    
    # Default fallback template
    default_resp = (
        f"{emergency_type} incident detected with {urgency} urgency. "
        "Please prioritize your personal safety and contact local emergency services immediately."
    )
    
    recommended_action = SAFE_RESPONSE_TEMPLATES.get(key, default_resp)
    
    return {
        "recommended_action": recommended_action,
        "disclaimer": "This system is an AI assistance prototype and does not automatically dispatch emergency responders. Please dial local emergency numbers (112 / 108 / 100 / 101) directly.",
        "emergency_contacts": EMERGENCY_CONTACT_DIRECTORY
    }
