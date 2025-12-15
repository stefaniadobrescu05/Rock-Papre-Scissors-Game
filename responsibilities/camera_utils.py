import cv2  # OpenCV library for camera operations
from ui import draw_ui_elements


def open_camera(camera_index=0):

    cap = cv2.VideoCapture(camera_index)
    # video capture este o clasa din opencv care se ocupa cu capturarea imaginii de la camera
    # camera_index este 0 fiindca este valoarea implicita pentru camera web a laptopului. daca era o camera externa, trebuia =1
    # atribuirea de mai sus returneaza in variabila cap un obiect capturat de la camera web principala cu ajutorul clasei VideoCapture din opencv

    if not cap.isOpened():
        raise RuntimeError("Could not open camera.")
    # isOpen este o metoda a clasei VideoCapture care verifica daca obiectul cap a reusit sa deschida camera
    # cap.isOpen returneaza o valoare de adevart sau fals
    # am pus not in fata pentru a inversa valoarea de adevar si a putea afisa mesajul de eroare
    # raise este folosit pentru a opri programul si a afisa un mesaj de eroare
    # mesajul de eroare va fi afisat in terminal
    # se foloseste RunTimeError pentru o problema care apare in timpul executiei din cauza unor factori externi sau probleme de sistem

    return cap


def read_frame(cap):
    status, frame = cap.read()
    # status este un boolean care indica daca citirea a fost cu succes
    # frame este cadrul citit de la camera - a NumPy array care contine pixelii imaginii capturate
    # .read() este o metoda a clasei VideoCapture care citeste un cadru de la camera

    if not status:
        return None
    # daca status este fals, returnam None

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
    # se modifica fereastra de fiecare data cand este apelata daca in main se apeleaza impreuna cu cv2.waitKey()
    # imshow este o functie din biblioteca openCV


def get_keypress(delay=1):
    #delay ul este in milisecunde
    #scopul functiei este de a detecta ce tasta a fost apasata in fereastara si sa o returneze
    #partea de interpretare si creare a unei actiuni in functie de tasta apasata se face in main cu niste if uri in fct de ce retuneaza fct asta

    key = cv2.waitKey(delay) & 0xFF

    if key == 255:
        return None

    return chr(key).lower()  # returnam direct lowercase ca sa fie mai simplu in main


def close_camera(cap):
    """
    Elibereaza camera si inchide toate ferestrele OpenCV
    
    Args:
        cap: Obiectul VideoCapture de inchis
    """
    if cap is not None:
        cap.release()
    # da release la camera ca sa poata fi folosita corect la alte rulari sau de alte aplicatii
    # destroy inchide toate ferestrele create de openCV

    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Mini test for camera_utils.py only (no other files needed)

    cap = open_camera()

    score = {"player": 0, "computer": 0, "draws": 0}
    #IMPORTANT: in ui.py se foloseste cheia "draws", deci o pastram asa ca sa se afiseze corect

    show_help = False
    detection_status = None

    # NU mai avem nevoie sa tinem player_move/computer_move/winner aici daca nu vrem sa apara textul dupa C

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
                detected_gesture=None,
                #IMPORTANT: nu trimitem winner/player_move/computer_move -> asa nu se mai afiseaza acele bucati de text
            )

            display_frame(frame)

            key = get_keypress()
            if key is None:
                continue

            if key == "q":
                break

            if key == "h":
                show_help = not show_help

            if key == "c":
                # Fake "capture" result (since gesture_recognition isn't ready yet)
                detection_status = "ok"
                score["computer"] += 1

    finally:
        close_camera(cap)
