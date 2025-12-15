"""
Rock-Paper-Scissors Game with Hand Gesture Recognition
Main application file that ties together camera, gesture recognition, and game logic
"""

import sys
import os
import time

# Add responsibilities folder to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'responsibilities'))

from camera_utils import (
    open_camera,
    read_frame,
    display_frame,
    draw_ui_elements,
    get_keypress,
    close_camera
)
from gesture_recognition import create_recognizer
from game_logic import get_computer_move, determine_winner


class RockPaperScissorsGame:
    """
    Clasa principala pentru jocul Rock-Paper-Scissors cu recunoastere de gesturi
    """
    
    def __init__(self):
        """Initializeaza jocul"""
        self.camera = None
        self.recognizer = None
        self.score = {
            "player": 0,
            "computer": 0,
            "draws": 0
        }
        
        # ROI (Region of Interest) - locul unde trebuie sa puna mana jucatorul
        self.roi = ((160, 120), (480, 440))
        
        # Game state
        self.game_active = True
        self.waiting_for_capture = True
        self.last_gesture = None
        self.last_result = None
        self.last_player_move = None
        self.last_computer_move = None
        self.last_result_time = 0
        self.result_display_duration = 2.0  # Afisam rezultatul 2 secunde
        
        # Help state
        self.show_help = False
    
    def initialize(self):
        """Deschide camera si initializeaza gesture recognizer"""
        try:
            print("Opening camera...")
            self.camera = open_camera()
            
            print("Initializing gesture recognizer...")
            self.recognizer = create_recognizer()
            
            print("Game initialized successfully!")
            return True
        except Exception as e:
            print(f"Error initializing game: {e}")
            return False
    
    def process_frame(self):
        """
        Proceseaza un cadru de la camera
        Returns: True daca jocul continua, False daca trebuie sa se inchida
        """
        # Citim un cadru de la camera
        frame = read_frame(self.camera)
        if frame is None:
            return True
        
        # Detectam gestul in cadrul curent
        gesture, detection_status, frame_with_landmarks = self.recognizer.detect_gesture(
            frame,
            roi=self.roi
        )
        
        # Stocam gestul detectat
        self.last_gesture = gesture
        
        # Verifica daca trebuie sa resetam rezultatul anterior (a trecut prea mult timp)
        current_time = time.time()
        if self.last_result and (current_time - self.last_result_time) > self.result_display_duration:
            self.last_result = None
            self.waiting_for_capture = True
        
        # Determinam statusul detectiei
        if detection_status == "ok" and gesture:
            detection_display = "ok"
        elif detection_status == "ok":
            detection_display = "fail"
        else:
            detection_display = None
        
        # Cream instructiuni pentru utilizator
        if self.show_help:
            instruction = "Help: Put your hand in the box and press C to play. Press H to hide."
        elif self.waiting_for_capture:
            instruction = "Press C to play | H for help | Q to quit"
        else:
            instruction = "Gesture detected! Processing... | Q to quit"
        
        # Desenam elementele UI pe frame
        # Afisam mutarile doar daca inca nu s-a trecut prea mult timp de la rezultat
        show_moves = False
        if self.last_result and (current_time - self.last_result_time) < self.result_display_duration:
            show_moves = True
        
        ui_frame = draw_ui_elements(
            frame_with_landmarks,
            score=self.score,
            instruction=instruction,
            detection_status=detection_display,
            detected_gesture=gesture,  # Afisam gestul detectat in timp real
            winner=self.last_result if show_moves else None,
            player_move=self.last_player_move if show_moves else None,
            computer_move=self.last_computer_move if show_moves else None,
            roi=self.roi
        )
        
        # Afisam frame-ul
        display_frame(ui_frame)
        
        # Citim inputul de la tastatura
        key = get_keypress(delay=30)  # 30ms delay
        
        if key is not None:
            key = key.lower()
            
            # Q pentru quit
            if key == 'q':
                return False
            
            # H pentru help
            if key == 'h':
                self.show_help = not self.show_help
            
            # C pentru capture/play
            if key == 'c':
                if gesture and self.waiting_for_capture:
                    self.play_round(gesture)
        
        return True
    
    def play_round(self, player_move):
        """
        Joaca o runda a jocului
        
        Args:
            player_move: Gestul detectat de la jucator ("rock", "paper", "scissors")
        """
        # Generam mutarea computerului
        computer_move = get_computer_move()
        
        # Determinam castigatorul
        winner = determine_winner(player_move, computer_move)
        
        # Actualizam scorul
        if winner == "player":
            self.score["player"] += 1
        elif winner == "computer":
            self.score["computer"] += 1
        else:
            self.score["draws"] += 1
        
        # Stocam mutarile pentru afisare
        self.last_player_move = player_move
        self.last_computer_move = computer_move
        
        # Stocam rezultatul pentru afisare
        self.last_result = winner
        self.last_result_time = time.time()
        self.waiting_for_capture = False
        
        # Afisam in consola
        print(f"\n{'='*50}")
        print(f"Round Result:")
        print(f"Player: {player_move.upper()}")
        print(f"Computer: {computer_move.upper()}")
        print(f"Winner: {winner.upper()}")
        print(f"Score - Player: {self.score['player']} | Computer: {self.score['computer']} | Draws: {self.score['draws']}")
        print(f"{'='*50}\n")
    
    def run(self):
        """
        Ruleaza bucla principala a jocului
        """
        print("\n" + "="*50)
        print("Welcome to Rock-Paper-Scissors with Hand Gesture Recognition!")
        print("="*50)
        print("\nControls:")
        print("  C - Capture gesture and play a round")
        print("  H - Toggle help text")
        print("  Q - Quit the game")
        print("\nGesture Guide:")
        print("  ROCK     - Closed fist")
        print("  PAPER    - Open palm (all fingers extended)")
        print("  SCISSORS - Index and middle finger in V shape")
        print("\n" + "="*50 + "\n")
        
        if not self.initialize():
            return
        
        try:
            while self.game_active:
                if not self.process_frame():
                    self.game_active = False
        
        except KeyboardInterrupt:
            print("\n\nGame interrupted by user!")
        
        except Exception as e:
            print(f"\n\nError during gameplay: {e}")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Elibereaza resursele si inchide aplicatia"""
        print("\nCleaning up...")
        
        if self.recognizer:
            self.recognizer.release()
        
        if self.camera:
            close_camera(self.camera)
        
        print("\nFinal Score:")
        print(f"  Player:   {self.score['player']}")
        print(f"  Computer: {self.score['computer']}")
        print(f"  Draws:    {self.score['draws']}")
        print("\nThanks for playing!")


def main():
    """Punct de intrare al programului"""
    game = RockPaperScissorsGame()
    game.run()


if __name__ == "__main__":
    main()
