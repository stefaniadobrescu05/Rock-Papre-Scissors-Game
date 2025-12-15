import cv2
import mediapipe as mp

class GestureRecognizer:
    """
    Clasa pentru recunoasterea gesturilor de mana (rock, paper, scissors)
    Foloseste MediaPipe pentru detectia mainii si a landmark-urilor
    """
    
    def __init__(self):
        # Initializare MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,      # False pentru video stream
            max_num_hands=1,               # Detectam doar o mana
            min_detection_confidence=0.7,  # Confidence minim pentru detectie
            min_tracking_confidence=0.5    # Confidence minim pentru tracking
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def count_extended_fingers(self, hand_landmarks):
        """
        Numara cate degete sunt intinse
        Returneaza un dictionar cu informatii despre fiecare deget
        """
        # Landmark indices pentru varf degete si articulatii
        # 0=wrist, 4=thumb_tip, 8=index_tip, 12=middle_tip, 16=ring_tip, 20=pinky_tip
        
        fingers_extended = {
            'thumb': False,
            'index': False,
            'middle': False,
            'ring': False,
            'pinky': False
        }
        
        # Extragem coordonatele landmark-urilor
        landmarks = hand_landmarks.landmark
        
        # Verificam degetul mare (thumb) - logica diferita pt ca se misca lateral
        # Comparam pozitia tip-ului cu ip-ul (inter-phalangeal joint)
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]
        
        # Thumb extended daca tip-ul este mai la dreapta/stanga decat ip
        # (depinde de orientarea mainii - verificam distanta)
        if abs(thumb_tip.x - thumb_ip.x) > abs(thumb_ip.x - thumb_mcp.x):
            fingers_extended['thumb'] = True
        
        # Verificam celelalte degete - comparam y-ul tip-ului cu pip-ul
        # (y scade cand degetul merge in sus pe ecran)
        finger_tips = [8, 12, 16, 20]  # index, middle, ring, pinky
        finger_pips = [6, 10, 14, 18]  # PIP joints (Proximal Interphalangeal)
        finger_names = ['index', 'middle', 'ring', 'pinky']
        
        for tip_id, pip_id, name in zip(finger_tips, finger_pips, finger_names):
            tip = landmarks[tip_id]
            pip = landmarks[pip_id]
            
            # Degetul e intins daca varful e mai sus decat articulatia PIP
            if tip.y < pip.y:
                fingers_extended[name] = True
        
        # Numar total degete intinse
        total_extended = sum(fingers_extended.values())
        
        return fingers_extended, total_extended
    
    def classify_gesture(self, fingers_extended, total_extended):
        """
        Clasifica gestul bazat pe degetele intinse
        
        Rock: Pumn inchis - 0 degete intinse sau doar degetul mare
        Paper: Palma deschisa - toate degetele intinse (5)
        Scissors: Index si middle intinse - exact 2 degete intinse si acestea sunt index+middle
        """
        
        # Paper: 4-5 degete intinse (cu sau fara degetul mare)
        if total_extended >= 4:
            return "paper"
        
        # Scissors: index si middle intinse, restul stranse
        if (total_extended == 2 and 
            fingers_extended['index'] and 
            fingers_extended['middle'] and
            not fingers_extended['ring'] and
            not fingers_extended['pinky']):
            return "scissors"
        
        # Rock: 0-1 degete intinse (pumn inchis, posibil cu degetul mare vizibil)
        if total_extended <= 1:
            return "rock"
        
        # Daca nu se potriveste cu niciunul, returnam None
        return None
    
    def detect_gesture(self, frame, roi=None):
        """
        Detecteaza gestul in frame
        
        Args:
            frame: Frame-ul de la camera (NumPy array)
            roi: Region of Interest - tuplu ((x1,y1),(x2,y2)) optional
        
        Returns:
            gesture: "rock", "paper", "scissors" sau None
            status: "ok" daca a detectat, "fail" daca nu
            annotated_frame: Frame cu desenate landmark-urile
        """
        
        if frame is None:
            return None, "fail", frame
        
        # Facem o copie pentru a nu modifica frame-ul original
        annotated_frame = frame.copy()
        
        # Daca avem ROI, extragem doar acea regiune pentru procesare
        if roi is not None:
            (x1, y1), (x2, y2) = roi
            roi_frame = frame[y1:y2, x1:x2]
        else:
            roi_frame = frame
            x1, y1 = 0, 0
        
        # Convertim BGR (OpenCV) la RGB (MediaPipe)
        rgb_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2RGB)
        
        # Procesam cu MediaPipe
        results = self.hands.process(rgb_frame)
        
        # Verificam daca s-a detectat o mana
        if results.multi_hand_landmarks:
            # Luam prima mana detectata
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Desenam landmark-urile pe frame
            # Ajustam coordonatele daca avem ROI
            if roi is not None:
                # Cream un obiect pentru desenat in ROI
                for landmark in hand_landmarks.landmark:
                    # Convertim coordonatele relative la coordonate absolute in ROI
                    h, w = roi_frame.shape[:2]
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    # Desenam un cerc mic pentru fiecare landmark
                    cv2.circle(annotated_frame, (x1 + cx, y1 + cy), 5, (0, 255, 0), -1)
                
                # Desenam si conexiunile
                self.mp_draw.draw_landmarks(
                    roi_frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
                annotated_frame[y1:y2, x1:x2] = roi_frame
            else:
                # Desenam direct pe frame complet
                self.mp_draw.draw_landmarks(
                    annotated_frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
            
            # Numaram degetele intinse
            fingers_extended, total_extended = self.count_extended_fingers(hand_landmarks)
            
            # Clasificam gestul
            gesture = self.classify_gesture(fingers_extended, total_extended)
            
            if gesture is not None:
                return gesture, "ok", annotated_frame
            else:
                return None, "fail", annotated_frame
        
        # Nu s-a detectat nicio mana
        return None, "fail", annotated_frame
    
    def release(self):
        """
        Elibereaza resursele MediaPipe
        """
        self.hands.close()


# Functie helper pentru a fi folosita direct din alte module
def create_recognizer():
    """
    Creeaza si returneaza o instanta de GestureRecognizer
    """
    return GestureRecognizer()


if __name__ == "__main__":
    # Test pentru gesture_recognition.py
    print("Testing gesture recognition...")
    print("Make sure you have a camera connected!")
    print("\nGesture guide:")
    print("- ROCK: Closed fist")
    print("- PAPER: Open palm (all fingers extended)")
    print("- SCISSORS: Index and middle finger extended in V shape")
    print("\nPress Q to quit\n")
    
    # Importam camera_utils pentru test
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    
    try:
        from camera_utils import open_camera, read_frame, display_frame, get_keypress, close_camera
        
        cap = open_camera()
        recognizer = create_recognizer()
        
        # ROI pentru testare
        roi = ((160, 120), (480, 440))
        
        while True:
            frame = read_frame(cap)
            if frame is None:
                continue
            
            # Detectam gestul
            gesture, status, annotated_frame = recognizer.detect_gesture(frame, roi=roi)
            
            # Desenam ROI
            (x1, y1), (x2, y2) = roi
            color = (0, 255, 0) if status == "ok" else (0, 0, 255)
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            
            # Afisam gestul detectat
            if gesture:
                text = f"Detected: {gesture.upper()}"
                cv2.putText(annotated_frame, text, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            else:
                text = "Place hand in box"
                cv2.putText(annotated_frame, text, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            display_frame(annotated_frame, "Gesture Recognition Test")
            
            key = get_keypress()
            if key and key.lower() == 'q':
                break
        
        recognizer.release()
        close_camera(cap)
        print("\nTest completed!")
        
    except ImportError:
        print("Error: Could not import camera_utils")
        print("Make sure camera_utils.py exists in the responsibilities folder")
    except Exception as e:
        print(f"Error during test: {e}")
