import unittest
import sys
import os

# Adaugam folderul parinte in path pentru a putea importa modulele din rps/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from responsibilities.gesture_recognition import GestureRecognizer

class TestGestureMapping(unittest.TestCase):

    def setUp(self):
        self.recognizer = GestureRecognizer()

    def test_rock_mapping(self):
        """Testeaza daca pumnul inchis (0 degete) este detectat ca Rock"""
        # Simulam 0 degete intinse
        fingers = {'thumb': False, 'index': False, 'middle': False, 'ring': False, 'pinky': False}
        total = 0
        result = self.recognizer.classify_gesture(fingers, total)
        self.assertEqual(result, "rock")

    def test_rock_mapping_thumb_only(self):
        """Testeaza daca pumnul cu doar degetul mare (1 deget) este tot Rock"""
        fingers = {
            'thumb': True, 'index': False, 'middle': False, 
            'ring': False, 'pinky': False
        }
        total = 1
        
        result = self.recognizer.classify_gesture(fingers, total)
        self.assertEqual(result, "rock")

    def test_paper_mapping(self):
        """Testeaza daca palma deschisa (5 degete) este Paper"""
        fingers = {
            'thumb': True, 'index': True, 'middle': True, 
            'ring': True, 'pinky': True
        }
        total = 5
        
        result = self.recognizer.classify_gesture(fingers, total)
        self.assertEqual(result, "paper")

    def test_paper_mapping_four_fingers(self):
        """Testeaza daca 4 degete (fara thumb) este tot Paper"""
        fingers = {
            'thumb': False, 'index': True, 'middle': True, 
            'ring': True, 'pinky': True
        }
        total = 4
        
        result = self.recognizer.classify_gesture(fingers, total)
        self.assertEqual(result, "paper")

    def test_scissors_mapping(self):
        """Testeaza gestul corect de foarfeca (Index + Middle)"""
        fingers = {
            'thumb': False, 'index': True, 'middle': True, 
            'ring': False, 'pinky': False
        }
        total = 2
        
        result = self.recognizer.classify_gesture(fingers, total)
        self.assertEqual(result, "scissors")

    def test_invalid_gesture(self):
        """Testeaza un gest invalid (ex: Index + Pinky)"""
        # Acesta are total=2, dar nu sunt index+middle, deci ar trebui sa fie None
        # (Conform logicii tale actuale, daca nu e scissors si nu e <=1 sau >=4, returneaza None)
        fingers = {
            'thumb': False, 'index': True, 'middle': False, 
            'ring': False, 'pinky': True
        }
        total = 2
        
        result = self.recognizer.classify_gesture(fingers, total)
        self.assertIsNone(result)

    def tearDown(self):
        self.recognizer.release()

if __name__ == '__main__':
    unittest.main()