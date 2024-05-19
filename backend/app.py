from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
import subprocess
import shlex

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
socketio = SocketIO(app, cors_allowed_origins="*")
BLACK_PATH = "/Users/hosun/Desktop/CheckersAI/backend/checkers-python/main.py"
WHITE_PATH = "/Users/hosun/Desktop/CheckersAI/backend/Sample_AIs/Random_AI/main.py"

def run_ai_game():
    command = f"python3 -u AI_Runner.py 8 8 3 l {BLACK_PATH} {WHITE_PATH}"
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, text=True, bufsize=1)

    board_lines = []
    final_board_state = ""
    skip_header = True

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            line = output.strip()
            print(f"AI Output: {line}")
            
            if any(line.startswith(f"{i} ") for i in range(8)) or line == '----------------------':
                if skip_header and any(line.startswith(f"{i} ") for i in range(8)):
                    skip_header = False
                    continue

                if line != '----------------------':
                    board_lines.append(' '.join(line.split()[1:]))
                else:
                    board_lines.append(line)
                    board_state = '\n'.join(board_lines)
                    final_board_state = board_state
                    socketio.emit('game_update', {'message': board_state}, broadcast=True)
                    skip_header = True
                    board_lines = []

            if "Player 1 Wins" in line or "Player 2 Wins" in line or "Tie" in line:
                board_lines.append(line)
                final_board_state = '\n'.join(board_lines)
                socketio.emit('game_update', {'message': final_board_state}, broadcast=True)
                socketio.emit('game_over', {'message': line}, broadcast=True)
                break

@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('start_game')
def on_start_game():
    print(f"Starting game with {BLACK_PATH} and {WHITE_PATH}")
    run_ai_game()
    print("Game over emitted")

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == '__main__':
    socketio.run(app, debug=True)
