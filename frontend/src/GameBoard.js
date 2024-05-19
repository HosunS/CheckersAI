import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import './GameBoard.css';

const socket = io.connect('http://localhost:5000');

const GameBoard = () => {
    const [board, setBoard] = useState([]);
    const [isGameRunning, setIsGameRunning] = useState(false);

    useEffect(() => {
        socket.on('game_update', (data) => {
            const newBoard = data.message.split('\n').filter(line => line.length > 0 && line !== '----------------------');
            setBoard(newBoard);
        });

        socket.on('game_over', (data) => {
            alert(data.message);
            setIsGameRunning(false);
        });

        return () => {
            socket.disconnect();
        };
    }, []);

    const startGame = () => {
        if (!isGameRunning) {
            socket.emit('start_game');
            setIsGameRunning(true);
        }
    };

    const renderCell = (cellContent, rowIndex, cellIndex) => {
        const isBlackCell = (rowIndex + cellIndex) % 2 === 1;
        const cellClass = isBlackCell ? 'cell black-cell' : 'cell red-cell';

        switch (cellContent) {
            case 'b': return <div className={`${cellClass} black-piece`} />;
            case 'B': return <div className={`${cellClass} black-king`} />;
            case 'w': return <div className={`${cellClass} red-piece`} />;
            case 'W': return <div className={`${cellClass} red-king`} />;
            default: return <div className={cellClass} />;
        }
    };

    return (
        <div className="game-container">
            <h1 className="game-title">Checkers AI Game</h1>
            <button className="start-button" onClick={startGame} disabled={isGameRunning}>Start Game</button>
            <div className="board">
                {board.map((row, rowIndex) => (
                    <div key={rowIndex} className="board-row">
                        {row.split(' ').map((cell, cellIndex) => (
                            <div key={cellIndex} className="board-cell">
                                {renderCell(cell, rowIndex, cellIndex)}
                            </div>
                        ))}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default GameBoard;
