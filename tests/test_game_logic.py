import unittest
import sys
"ca sa pot lucra cu path-uri"
import os
"pt acces la setarile interpretorului"

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'responsibilities')))
"importez modulul pe care vreau sa-l testez"

from responsibilities import game_logic

class TestGameLogic(unittest.TestCase):

    def testValidateMove(self):
        "cu assertTrue verific daca expreisa din paranteza e adevarata"
        "nu este case sensitive"
        self.assertTrue(game_logic.validate_move("rock"))
        self.assertTrue(game_logic.validate_move("paper"))
        self.assertTrue(game_logic.validate_move("scissors"))

        self.assertFalse(game_logic.validate_move(""))
        self.assertFalse(game_logic.validate_move("cuvant"))

    def testWinnerPlayerWins(self):
        self.assertEqual(game_logic.determine_winner("rock","scissors"), "player")    
        self.assertEqual(game_logic.determine_winner("paper","rock"), "player")    
        self.assertEqual(game_logic.determine_winner("scissors","paper"), "player")

    def testWinnerComputerWins(self):
        self.assertEqual(game_logic.determine_winner("scissors","rock"), "computer")    
        self.assertEqual(game_logic.determine_winner("rock","paper"), "computer")    
        self.assertEqual(game_logic.determine_winner("paper","scissors"), "computer")

    def testDraw(self):
        self.assertEqual(game_logic.determine_winner("rock","rock"), "draw")
        self.assertEqual(game_logic.determine_winner("paper","paper"), "draw")
        self.assertEqual(game_logic.determine_winner("scissors","scissors"), "draw")

    "folosesc unittest ca sa pot sa testez individual functiile, fara sa depinda de alte fisiere"
    if __name__ == '__main__':
        unittest.main()
    "Dacă rulez acest fișier direct, execută toate testele pe care le găsești în el."