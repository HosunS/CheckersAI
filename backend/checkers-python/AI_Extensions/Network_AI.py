"""
This module houses the NetworkAI which is used just to manage games if the students want to play with others throught the ICS servers.

We are following the javadoc docstring format which is:
@param tag describes the input parameters of the function
@return tag describes what the function returns
@raise tag describes the errors this function can raise
"""

from socket import *
import sys
sys.path.append('../')
from BoardClasses import Move
from time import sleep
import threading


def keep_alive():
    global timer
    timer = threading.Timer(1, keep_alive)
    timer.start()
    serverPort = 12002
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # clientSocket.connect(('syn2-1.ics.uci.edu', serverPort))
    try:
        clientSocket.connect(('syn2-1.ics.uci.edu', serverPort))
    except:
        print("Error: \nConnection lost.")
        timer.cancel()

    sentence = "REQUEST_UPDATE"
    clientSocket.send(sentence.encode())
    result = clientSocket.recv(1024).decode()
    clientSocket.close()
    if result != "OK":
        print("Error: \nConnection lost.")
        timer.cancel()


def end_timer():
    try:
        timer.cancel()
    except:
        pass

class NetworkAI():
    def __init__(self,col,row,p,**kwargs):
        """
        Intializes networkAI
        @param row: no of rows in the board
        @param col: no of columns in the board
        @param p: no of rows to be filled with checker pieces at the start
        @param **kwargs: info to describe the socket connection and 'mode' the AI is in (host or client)
        @return :
        @raise :
        """
        self.topSocket = socket(AF_INET, SOCK_STREAM)
        self.mode = kwargs['mode']
        print(self.mode)
        serverName, serverPort, _ = kwargs['info']
        if self.mode == 'host':
            print("Matching")
            keep_alive() #HeartBeating
            import atexit
            atexit.register(end_timer)
            self.topSocket.bind((serverName, serverPort))
            self.topSocket.listen(1)
            self.topSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            self.connectionSocket, _ = self.topSocket.accept()
            if self.connectionSocket.recv(1024).decode() != 'OK':
                raise SO_ERROR
            else:
                print('OK')
                end_timer()
        else:
            self.topSocket.connect((serverName, serverPort))
            self.topSocket.send("OK".encode())
            print('OK')
    def sent_final_result(self,move):
        """
        Sends result info to the socket
        @param move: 
        @return :
        @raise :
        """
        if self.mode == 'host':
            sentence = str(move).encode()
            self.connectionSocket.send(sentence)
        else:
            sentence = str(move).encode()
            self.topSocket.send(sentence)

    def get_move(self,move):
        """
        get_move function for NetworkAI called from the gameloop in the main module.
        @param move: A Move object describing the move.
        @return res_move: A Move object describing the move manualAI wants to make. This move is a random move from the set of valid moves.
        @raise :
        """

        sleep(0.3)
        #TODO: Combine two branches
        if self.mode == 'host':
            if move.seq:
                print('SENT:', str(move))
                sentence = str(move).encode()
                self.connectionSocket.send(sentence)

            response = self.connectionSocket.recv(1024).decode().rstrip()
            try:
                res_move = Move.from_str(response)
                if not res_move.seq:
                    raise Exception
            except:
                print("You win. Your peer crashed.")
                raise Exception
            print('GET:', res_move)
            return res_move
        else:
            sleep(0.1)
            if move.seq:
                print('SENT:', str(move))
                sentence = str(move).encode()
                self.topSocket.send(sentence)
            response = self.topSocket.recv(1024).decode().rstrip()
            try:
                res_move = Move.from_str(response)
                print(res_move.seq)
                if not res_move.seq:
                    raise Exception
            except:
                print("You win. Your peer crashed.")
                raise Exception
            print('GET:', res_move)
            return res_move

    def __del__(self):
        """
        closes socket connection when networkAI object is destroyed.
        @param :
        @return :
        @raise :
        """
        self.topSocket.close()
        end_timer()
