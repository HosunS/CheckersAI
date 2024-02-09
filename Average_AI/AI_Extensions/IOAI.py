import sys
sys.path.append("../")
from AI_Extensions.Communicator import Communicator
from BoardClasses import Move


def get_prefix(ai):
    if ai.endswith('.exe'):
        ai = './'+ai
    elif ai.endswith('.py') or ai.endswith('.pyc') :
        ai = 'python3 '+ai
    elif ai.endswith('.jar'):
        ai = 'java -jar ' + ai

    return ai


class IOAI():
    def __init__(self,col,row,p,**kwargs):
        command = kwargs['ai_path']
        command = get_prefix(command)
        command = command + " " + str(col) + " " + str(row) + " " + str(p) + " " + " t"
        self.communicator = Communicator(command,kwargs['time'])

    def get_move(self,move):
        self.communicator.send(str(move).encode())
        ai_move,err = self.communicator.recv(return_stderr=True)
        if len(err) > 1:
            print("exception")
            raise Exception(err.decode())
        ai_move = ai_move.decode().split("\n")[-1].rstrip()
        return Move.from_str(ai_move)

    def close(self):
        self.communicator.close()
