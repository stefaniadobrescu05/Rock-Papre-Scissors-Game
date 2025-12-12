import random

rock="rock"
paper="paper"
scissors="scissors"
mutari=[rock,paper,scissors]

"generez o alegere random"
def get_computer_move():
    return random.choice(mutari)

"verific daca este mutare valida"
def validate_move(move):
    move=move.lower()
    if move==rock or move==paper or move==scissors:
        return True
    return False

"aleg castigatorul"
def determine_winner(p_move,c_move):
    p_move=p_move.lower()
    c_move=c_move.lower()
    if p_move==c_move:
        return "draw"
    elif (p_move==rock and c_move==scissors) or (p_move==paper and c_move==rock) or (p_move==scissors and c_move==paper):
        return "player"
    else:
        return "computer"
    
"folosesc lower ca sa nu fie case sensitive"