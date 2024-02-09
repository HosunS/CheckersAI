import subprocess

def run_game(ai_runner, black_ai, white_ai):
    # Start the external AI program
    process = subprocess.Popen(
        ['python3', ai_runner, '8', '8', '3', 'l', black_ai, white_ai],
        stdout=subprocess.PIPE,
        universal_newlines=True  # For Python < 3.7 compatibility
    )

    # Print output in real-time
    for line in process.stdout:
        print(line, end="")

    process.stdout.close()
    return_code = process.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, process.args)

def main():
    ai_runner = "AI_Runner.py"
    white_ai = "/home/songhn/171/Checkers_Student-master/Tools/Sample_AIs/Poor_AI/main.py"
    black_ai = "/home/songhn/171/Checkers_Student-master/src/checkers-python/main.py"
    games_to_play = 4
    player1_wins = 0
    ties = 0

    for i in range(1, games_to_play + 1):
        print("Game {} of {}".format(i, games_to_play))
        output = run_game(ai_runner, black_ai, white_ai)
        print(output)

        if output == "player 1 wins":
            player1_wins += 1
        elif output == "Tie":
            ties += 1

    print("Player 1 won {} out of {} games and {} were ties.".format(player1_wins, games_to_play, ties))


if __name__ == "__main__":
    main()
