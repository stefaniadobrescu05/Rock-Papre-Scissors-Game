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
    return frame

def display_frame(frame, window_name="Rock-Paper-Scissors Game"):
    #se deschide o fereasta cu numele specificat in  OpenCV si se afiseaza frameul capturat mai devreme

    cv2.imshow(window_name, frame)
    #se modifica fereastra de fiecare data cand este apelata daca in main se apeleaza impreuna cu cv2.waitKey()
    #imshow este o functie din biblioteca openCV

def draw_ui_elements(
    frame,
    score=None,
    instruction="Press C to capture | Q to quit",
    detection_status=None,   # None / "ok" / "fail" - colors ROI
    winner=None, #"player" / "computer" / "draw" 
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

    score_text = f"Player: {score.get("player", 0)}  |  Computer: {score.get("computer", 0)}  |  Draws: {score.get("draws", 0)}"
    #se creeaza textul afisat, iar valorile sunt luate din dictionar cu metoda specifica de dictionar .get
    #f permite sa se insereze variabile direct in string

    cv2.putText(frame, score_text, (15, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    #se adauga textul pe frame, in poztitia (15,32), cu fontul specificat, marimea 0.8, culoarea alba (BGR) si grosimea 2

    #Instruction
    cv2.putText(frame, instruction, (15, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (230, 230, 230), 2)

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

    y_info = bar_h + 30
    if winner is not None:
        if winner == "player":
            result_text = "You Win!"
        elif winner == "computer":
            result_text = "Computer Wins!"
        else:
            result_text = "It's a Draw!"
        
        cv2.putText(frame, result_text, (15, y_info + 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        return frame

def get_keypress():
    pass

def close_camera(camera):
    pass
