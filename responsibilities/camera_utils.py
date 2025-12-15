import cv2 # OpenCV library for camera operations

def open_camera(camera_index=0):

    cap = cv2.VideoCapture(camera_index)
    #video capture este o clasa din opencv care se ocupa cu capturarea imaginii de la camera
    #camera_index este 0 fiindca este valoarea implicita pentru camera web a laptopului. daca era o camera externa, trebuia =1
    #atribuirea de mai sus returneaza in variabila cap un obiect capturat de la camera web principala cu ajutorul clasei VideoCapture din opencv

    if not cap.isOpened():
        raise RuntimeError("Could not open camera.")
    #isOpen este o metoda a clasei VideoCapture care verifica daca obiectul cap a reusit sa deschida camera
    #cap.isOpen returneaza o valoare de adevart sau fals
    #am pus not in fata pentru a inversa valoarea de adevar si a putea afisa mesajul de eroare
    #raise este folosit pentru a opri programul si a afisa un mesaj de eroare
    #mesajul de eroare va fi afisat in terminal
    #se foloseste RunTimeError pentru o problema care apare in timpul executiei din cauza unor factori externi sau probleme de sistem

    return cap

def read_frame(cap):
    status, frame = cap.read()
    #status este un boolean care indica daca citirea a fost cu succes
    #frame este cadrul citit de la camera - a NumPy arraay care contine pixelii imaginii capturate
    #.read() este o metoda a clasei VideoCapture care citeste un cadru de la camera

    if not status:
        return None
    #daca status este fals, returnam None
    
    # Oglindim imaginea pe orizontala (flip) pentru a fi mai natural
    # flipCode=1 inseamna flip orizontal (ca in oglinda)
    frame = cv2.flip(frame, 1)
    
    return frame

def display_frame(frame, window_name="Rock-Paper-Scissors Game"):
    #se deschide o fereasta cu numele specificat in  OpenCV si se afiseaza frameul capturat mai devreme
    
    # Setam fereastra sa fie resizable (scalabila)
    # cv2.WINDOW_NORMAL permite redimensionarea manuala sau fullscreen
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    cv2.imshow(window_name, frame)
    #se modifica fereastra de fiecare data cand este apelata daca in main se apeleaza impreuna cu cv2.waitKey()
    #imshow este o functie din biblioteca openCV

def draw_ui_elements(
    frame,
    score=None,
    instruction="Press C to capture | Q to quit",
    detection_status=None,   # None / "ok" / "fail" - colors ROI
    detected_gesture=None,  # "rock" / "paper" / "scissors" / None - gestul detectat in timp real
    winner=None, #"player" / "computer" / "draw"
    player_move=None,  # "rock" / "paper" / "scissors" - ce a facut jucatorul
    computer_move=None,  # "rock" / "paper" / "scissors" - ce a facut computerul
    roi=((160, 120), (480, 440)),  # ((x1,y1),(x2,y2)),  rectangle where user should place hand
    #region of interest -  cu coordonatele pentru punctul din stanga sus, respectiv din dreapta jos
):
    #adauga elemente de interfata peste frame

    if frame is None:
        return None
    
    h, w = frame.shape[:2]
    #in variable se pun intaltimea si latimea frameului
    #un frame are caracteritica .shape care returneaza un tuplu cu dimensiunile sale: (height, width, channels)
    #[:2] este folosit pentru a lua dor primele 2 valori din tuplu

    #Top bar
    bar_h = 90
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, bar_h), (0, 0, 0), -1)
    #(0,0) coord pct stanga sus iar (w,bar_h) coord pct dreapta jos, cu w - latimea imaginii si bar_h inltimea data de noi
    #codul de culoare este negreu in format BGR - asta foloseste openCV
    #-1 pentru thickness inseamna ca se umple dreptunghiul

    frame = cv2.addWeighted(overlay, 0.45, frame, 0.55, 0)
    #addweighted suprapune doua imagini cu o anumita transparenta
    #dupa formula result = overlay * 0.45 + frame * 0.55 + 0
    #0.45, 0.55 sunt coeficientii de transparenta pentru fiecare imagine, care adunate trebuie sa dea 1
    
    #Score
    if score is None:
        score = {"player": 0, "computer": 0, "draws": 0}
        
    score_text = f"Player: {score.get('player', 0)}  |  Computer: {score.get('computer', 0)}  |  Draw: {score.get('draws', 0)}"
    #se creeaza textul afisat, iar valorile sunt luate din dictionar cu metoda specifica de dictionar .get
    #f permite sa se insereze variabile direct in string

    cv2.putText(frame, score_text, (15, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    #se adauga textul pe frame, in poztitia (15,32), cu fontul specificat, marimea 0.8, culoarea alba (BGR) si grosimea 2

    #Instruction (word-wrapped to stay inside window)
    if instruction:
        max_width = w - 30  # 15px padding on both sides
        words = instruction.split()
        lines = []
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.7
        thickness = 2
        current = ""
        for word in words:
            test = (current + " " + word).strip()
            size = cv2.getTextSize(test, font, scale, thickness)[0]
            if size[0] <= max_width or not current:
                current = test
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)

        y = 50  # start inside the top bar
        line_h = int(cv2.getTextSize("Ag", font, scale, thickness)[0][1] * 1.4)
        for line in lines[:3]:  # cap to 3 lines to keep within bar
            cv2.putText(frame, line, (15, y), font, scale, (230, 230, 230), thickness)
            y += line_h

    #ROI rectangle
    (x1, y1), (x2, y2) = roi
    #se extrag coordonatele din tuplul dat ca parametru si se pun in niste variabile care vor fi folosite mai tarziu in functii specifice openCV

    if detection_status == "ok":
        roi_color = (0, 255, 0)      # green
        status_text = "Detected gesture"
    elif detection_status == "fail":
        roi_color = (0, 0, 255)      # red
        status_text = "No gesture detected"
    else:
        roi_color = (255, 255, 0)    # cyan/yellow-ish
        status_text = "Place hand in box"
    #detection_status este decis ce valoare are in main, in functie de rezultatul primit de la gesture_recognition

    cv2.rectangle(frame, (x1, y1), (x2, y2), roi_color, 3)
    #pt valori pozitive [1, 5+] se decide cat de groasa va fi bordura chenarului, iar pentru -1 se umple tot chenarul cu acaea culoare
    cv2.putText(frame, status_text, (x1, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, roi_color, 2)

    # Afisam gestul detectat in timp real in coltu din dreapta sus
    if detected_gesture is not None:
        # Pozitie top-right
        real_time_text = f"Detected: {detected_gesture.upper()}"
        text_size = cv2.getTextSize(real_time_text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
        text_x = w - text_size[0] - 15
        text_y = bar_h + 40
        
        # Background pentru text (pentru citibilitate)
        cv2.rectangle(frame, (text_x - 5, text_y - 25), (w - 10, text_y + 5), (0, 0, 0), -1)
        cv2.putText(frame, real_time_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    elif detection_status == "fail":
        # Afisam mesaj de eroare cand nu detecteaza
        error_text = "Invalid Gesture"
        text_size = cv2.getTextSize(error_text, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)[0]
        text_x = w - text_size[0] - 15
        text_y = bar_h + 40
        
        # Background pentru text
        cv2.rectangle(frame, (text_x - 5, text_y - 25), (w - 10, text_y + 5), (0, 0, 0), -1)
        cv2.putText(frame, error_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    y_info = bar_h + 30
    
    # Afisam mutarile jucatorului si computerului daca exista (in zona de jos, la stanga si dreapta)
    if player_move is not None and computer_move is not None:
        # Afisam mutarea jucatorului pe stanga jos
        player_text = f"You: {player_move.upper()}"
        # Background pentru text cu padding
        player_text_size = cv2.getTextSize(player_text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
        padding = 15
        cv2.rectangle(frame, (10, h - 160), (10 + player_text_size[0] + 2*padding, h - 70), (50, 50, 50), -1)
        cv2.putText(frame, player_text, (10 + padding, h - 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (100, 200, 255), 3)  # Orange
        
        # Afisam mutarea computerului pe dreapta jos
        computer_text = f"Computer: {computer_move.upper()}"
        computer_text_size = cv2.getTextSize(computer_text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
        cv2.rectangle(frame, (w - 10 - computer_text_size[0] - 2*padding, h - 160), (w - 10, h - 70), (50, 50, 50), -1)
        cv2.putText(frame, computer_text, (w - 10 - computer_text_size[0] - padding, h - 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 100, 100), 3)  # Cyan
    
    if winner is not None:
        if winner == "player":
            result_text = "You Win!"
            result_color = (0, 255, 0)  # Green
        elif winner == "computer":
            result_text = "Computer Wins!"
            result_color = (0, 0, 255)  # Red
        else:
            result_text = "It's a Draw!"
            result_color = (255, 255, 0)  # Cyan
        
        # Afisam rezultatul in centru, sus
        text_size = cv2.getTextSize(result_text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
        text_x = (w - text_size[0]) // 2
        text_y = bar_h + 60
        
        # Background pentru text
        cv2.rectangle(frame, (text_x - 10, text_y - 35), (text_x + text_size[0] + 10, text_y + 10), (0, 0, 0), -1)
        cv2.putText(frame, result_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, result_color, 3)

    return frame

def get_keypress(delay=1):
        #delay ul este in milisecunde
        #scopul functiei este de a detecta ce tasta a fost apasata in fereastara si sa o returneze 
        #partea de interpretare si creare a unei actiuni in functie de tasta apasata se face in main cu niste if uri in fct de ce retuneaza fct asta

        key = cv2.waitKey(delay) & 0xFF

        if key == 255:
            return None
        
        return chr(key)

def close_camera(cap):
    
    if cap is not None:
        cap.release()
    #da release la camera ca sa poata fi folosita corect la alte rulari sau de alte aplicatii
    #destroy inchide toate ferestrele create de openCV

    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Mini test for camera_utils.py only (no other files needed)

    cap = open_camera()
    score = {"player": 0, "computer": 0, "draw": 0}

    show_help = False
    detection_status = None
    player_move = None
    computer_move = None
    winner = None

    try:
        while True:
            frame = read_frame(cap)
            if frame is None:
                continue

            instruction = "C: simulate capture | H: help | Q: quit"
            if show_help:
                instruction = "Help: Put hand in the box. Later we detect gestures. Press H to hide."

            # Simulate detection feedback when pressing C
            frame = draw_ui_elements(
                frame,
                score=score,
                instruction=instruction,
                detection_status=detection_status,
                winner=winner,
            )

            display_frame(frame)

            key = get_keypress()
            if key is None:
                continue

            key = key.lower()

            if key == "q":
                break

            if key == "h":
                show_help = not show_help

            if key == "c":
                # Fake "capture" result (since gesture_recognition isn't ready yet)
                detection_status = "ok"
                player_move = "rock"
                computer_move = "paper"
                winner = "computer"
                score["computer"] += 1

    finally:
        close_camera(cap)
