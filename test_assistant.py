"""
Automated Test Suite for Multilingual Emergency & Safety Assistant
Validates all required test cases from project specification (Section 23, 26).
"""

import sys
import io
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.assistant import EmergencyAssistant


class TestEmergencyAssistant(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assistant = EmergencyAssistant()

    def test_english_medical(self):
        msg = "I need an ambulance immediately"
        result = self.assistant.analyze(msg)
        self.assertTrue(result["success"])
        self.assertEqual(result["language"]["detected"], "English")
        self.assertEqual(result["emergency_type"]["category"], "Medical")
        self.assertEqual(result["urgency"]["level"], "High")

    def test_tamil_fire(self):
        msg = "எங்கள் வீட்டில் தீப்பிடித்துவிட்டது"
        result = self.assistant.analyze(msg)
        self.assertTrue(result["success"])
        self.assertEqual(result["language"]["detected"], "Tamil")
        self.assertEqual(result["emergency_type"]["category"], "Fire")
        self.assertEqual(result["urgency"]["level"], "High")

    def test_tanglish_accident(self):
        msg = "Road la accident aayiduchu, someone badly injured"
        result = self.assistant.analyze(msg)
        self.assertTrue(result["success"])
        self.assertEqual(result["language"]["detected"], "Tanglish")
        self.assertEqual(result["emergency_type"]["category"], "Accident")
        self.assertEqual(result["urgency"]["level"], "High")
        self.assertEqual(result["extracted_information"]["people_injured"], 1)

    def test_tanglish_safety(self):
        msg = "Yaaro enna follow panranga"
        result = self.assistant.analyze(msg)
        self.assertTrue(result["success"])
        self.assertEqual(result["language"]["detected"], "Tanglish")
        # Matches Police / Crime or Personal Safety
        self.assertIn(result["emergency_type"]["category"], ["Police / Crime", "Personal Safety"])
        self.assertEqual(result["urgency"]["level"], "High")

    def test_tamil_natural_disaster(self):
        msg = "எங்கள் பகுதியில் வெள்ளம் ஏற்பட்டுள்ளது"
        result = self.assistant.analyze(msg)
        self.assertTrue(result["success"])
        self.assertEqual(result["language"]["detected"], "Tamil")
        self.assertEqual(result["emergency_type"]["category"], "Natural Disaster")
        self.assertEqual(result["urgency"]["level"], "High")

    def test_information_extraction(self):
        msg = "Road la accident aayiduchu near Thoothukudi bus stand, 2 people injured"
        result = self.assistant.analyze(msg)
        self.assertTrue(result["success"])
        self.assertEqual(result["language"]["detected"], "Tanglish")
        self.assertEqual(result["emergency_type"]["category"], "Accident")
        self.assertEqual(result["urgency"]["level"], "High")
        self.assertEqual(result["extracted_information"]["location"], "Thoothukudi bus stand")
        self.assertEqual(result["extracted_information"]["people_injured"], 2)

    def test_empty_input_handling(self):
        result_empty = self.assistant.analyze("")
        self.assertFalse(result_empty["success"])
        self.assertEqual(result_empty["error"], "Please describe your emergency before analyzing.")

        result_spaces = self.assistant.analyze("   \t  \n  ")
        self.assertFalse(result_spaces["success"])
        self.assertEqual(result_spaces["error"], "Please describe your emergency before analyzing.")


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    unittest.main()
