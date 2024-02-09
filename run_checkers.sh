#!/bin/bash

AI_RUNNER="AI_Runner.py"

WHITE="/home/songhn/171/Checkers_Student-master/Tools/Sample_AIs/Poor_AI/main.py"

BLACK="/home/songhn/171/Checkers_Student-master/src/checkers-python/main.py"

player1_wins=0
ties=0
GAMES_TO_PLAY=5

for (( i=1; i<=GAMES_TO_PLAY; i++ ))
do
    echo "Game $i of $GAMES_TO_PLAY"
    # Run the game and capture the output
    output=$(python3 "$AI_RUNNER" 8 8 3 l "$BLACK" "$WHITE")

    echo "$output"

    # Check if Player 1 is the winner
    if [[ "$output" == *"player 1 wins"* ]]; then
        ((player1_wins++))
    elif [[ "$output" == *"Tie"* ]]; then
        ((ties++))
    fi
    echo "Player 1 won $player1_wins out of $i games and $ties were ties."
done
echo "Player 1 won $player1_wins out of $GAMES_TO_PLAY games and $ties were ties."