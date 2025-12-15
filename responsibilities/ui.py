import cv2

def draw_ui_elements(
    frame,
    score=None,
    instruction="Press C to capture | Q to quit",
    detection_status=None,   # None / "ok" / "fail" - colors ROI
    detected_gesture=None,   # "rock" / "paper" / "scissors" / None - gestul detectat in timp real
    winner=None,             # "player" / "computer" / "draw" / None
    player_move=None,        # NU mai desenam mutarile (raman ca parametru ca sa nu crape alte apeluri)
    computer_move=None,      # folosit doar in mesajul de rezultat (nu desenam mutarea separat jos)
    roi=((160, 120), (480, 440)),  # ((x1,y1),(x2,y2))
):
    """
    Adauga elemente de interfata peste frame
    """
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
    #se adauga textul pe frame, in poztitia (15,26), cu fontul specificat, marimea 0.6, culoarea alba (BGR) si grosimea 2

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

    # IMPORTANT: NU mai afisam mutarile jucatorului si computerului (player_move / computer_move) separat jos
    # (blocul ala a fost scos intentionat)

    # Afisam rezultatul rundei dupa ce apesi C (cand winner nu mai e None)
    if winner is not None:
        if winner == "player":
            base_text = "You Win!"
            result_color = (0, 255, 0)  # Green
        elif winner == "computer":
            base_text = "You Lose!"
            result_color = (0, 0, 255)  # Red
        else:
            base_text = "It's a Draw!"
            result_color = (255, 255, 0)  # Cyan

        # Adaugam si alegerea computerului in acelasi text (ca sa nu incarcam ecranul cu alte box-uri)
        if computer_move is not None:
            result_text = f"{base_text} (Computer: {computer_move.upper()})"
        else:
            result_text = base_text  # fallback daca nu a fost setat in main

        # Pozitie: centru, SUB top bar, ca sa nu se suprapuna cu scor/instructiuni
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 1.15  # putin mai mic pentru ca textul e mai lung acum
        thickness = 3

        text_size = cv2.getTextSize(result_text, font, scale, thickness)[0]
        text_x = (w - text_size[0]) // 2
        text_y = bar_h + 110  # sub top bar, suficient de jos ca sa nu loveasca "Detected: ..."

        # Background pentru text
        cv2.rectangle(
            frame,
            (text_x - 14, text_y - text_size[1] - 16),
            (text_x + text_size[0] + 14, text_y + 14),
            (0, 0, 0),
            -1
        )
        cv2.putText(frame, result_text, (text_x, text_y), font, scale, result_color, thickness)

    return frame
