import React, { useEffect, useRef, useState } from 'react';
import { PlayCircle, RotateCw, ArrowLeft, ArrowRight, ArrowDown } from 'lucide-react';

// Cores permitidas
const COLORS = {
  RED: '#ef4444',
  GREEN: '#22c55e',
  BLUE: '#3b82f6',
};

// Peças do Tetris usando apenas as cores especificadas
const TETROMINOS = {
  I: {
    shape: [[1, 1, 1, 1]],
    color: COLORS.RED,
  },
  O: {
    shape: [
      [1, 1],
      [1, 1],
    ],
    color: COLORS.GREEN,
  },
  T: {
    shape: [
      [0, 1, 0],
      [1, 1, 1],
    ],
    color: COLORS.BLUE,
  },
  L: {
    shape: [
      [1, 0],
      [1, 0],
      [1, 1],
    ],
    color: COLORS.RED,
  },
};

const CANVAS_WIDTH = 300;
const CANVAS_HEIGHT = 600;
const BLOCK_SIZE = 30;

// Move function declarations outside useEffect
const createEmptyBoard = () => {
  return Array(20).fill(null).map(() => Array(10).fill(null));
};

const createNewPiece = () => {
  const pieces = Object.keys(TETROMINOS);
  const randomPiece = pieces[Math.floor(Math.random() * pieces.length)] as keyof typeof TETROMINOS;
  return {
    shape: TETROMINOS[randomPiece].shape,
    color: TETROMINOS[randomPiece].color,
    x: 3,
    y: 0,
  };
};

const TetrisGame: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [gameStarted, setGameStarted] = useState(false);
  const [score, setScore] = useState(0);

  // Som de sucesso ao completar uma linha
  const successSound = new Audio('https://assets.mixkit.co/active_storage/sfx/2000/2000-preview.mp3');

  useEffect(() => {
    if (!gameStarted) return;

    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    if (!canvas || !ctx) return;

    let currentPiece = createNewPiece();
    let board = createEmptyBoard();
    let animationFrameId: number;
    let lastDropTime = 0;
    const dropInterval = 1000; // 1 segundo entre quedas

    const draw = () => {
      // Limpar canvas
      ctx.fillStyle = '#fff';
      ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

      // Desenhar grade
      ctx.strokeStyle = '#ddd';
      for (let i = 0; i < CANVAS_WIDTH; i += BLOCK_SIZE) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, CANVAS_HEIGHT);
        ctx.stroke();
      }
      for (let i = 0; i < CANVAS_HEIGHT; i += BLOCK_SIZE) {
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(CANVAS_WIDTH, i);
        ctx.stroke();
      }

      // Desenhar peça atual
      drawPiece();

      // Desenhar peças fixas
      drawBoard();
    };

    const drawPiece = () => {
      currentPiece.shape.forEach((row, y) => {
        row.forEach((value, x) => {
          if (value) {
            ctx.fillStyle = currentPiece.color;
            ctx.fillRect(
              (currentPiece.x + x) * BLOCK_SIZE,
              (currentPiece.y + y) * BLOCK_SIZE,
              BLOCK_SIZE - 1,
              BLOCK_SIZE - 1
            );
          }
        });
      });
    };

    const drawBoard = () => {
      board.forEach((row, y) => {
        row.forEach((value, x) => {
          if (value) {
            ctx.fillStyle = value;
            ctx.fillRect(
              x * BLOCK_SIZE,
              y * BLOCK_SIZE,
              BLOCK_SIZE - 1,
              BLOCK_SIZE - 1
            );
          }
        });
      });
    };

    const checkCollision = () => {
      return currentPiece.shape.some((row, dy) => {
        return row.some((value, dx) => {
          if (!value) return false;
          const newX = currentPiece.x + dx;
          const newY = currentPiece.y + dy;
          return (
            newX < 0 ||
            newX >= 10 ||
            newY >= 20 ||
            (newY >= 0 && board[newY][newX])
          );
        });
      });
    };

    const mergePiece = () => {
      currentPiece.shape.forEach((row, y) => {
        row.forEach((value, x) => {
          if (value) {
            const boardY = currentPiece.y + y;
            if (boardY >= 0) {
              board[boardY][currentPiece.x + x] = currentPiece.color;
            }
          }
        });
      });
    };

    const checkLines = () => {
      let linesCleared = 0;
      board.forEach((row, y) => {
        if (row.every(cell => cell !== null)) {
          board.splice(y, 1);
          board.unshift(Array(10).fill(null));
          linesCleared++;
          successSound.play();
        }
      });
      if (linesCleared > 0) {
        setScore(prev => prev + (linesCleared * 100));
      }
    };

    const movePieceDown = () => {
      currentPiece.y++;
      if (checkCollision()) {
        currentPiece.y--;
        mergePiece();
        checkLines();
        currentPiece = createNewPiece();
        if (checkCollision()) {
          setGameStarted(false);
        }
      }
    };

    const rotatePiece = () => {
      const rotated = currentPiece.shape[0].map((_, i) =>
        currentPiece.shape.map(row => row[i]).reverse()
      );
      const previousShape = currentPiece.shape;
      currentPiece.shape = rotated;
      if (checkCollision()) {
        currentPiece.shape = previousShape;
      }
    };

    const handleKeyDown = (e: KeyboardEvent) => {
      switch (e.key) {
        case 'ArrowLeft':
          currentPiece.x--;
          if (checkCollision()) currentPiece.x++;
          break;
        case 'ArrowRight':
          currentPiece.x++;
          if (checkCollision()) currentPiece.x--;
          break;
        case 'ArrowDown':
          movePieceDown();
          break;
        case 'ArrowUp':
          rotatePiece();
          break;
      }
    };

    const gameLoop = (timestamp: number) => {
      if (timestamp - lastDropTime > dropInterval) {
        movePieceDown();
        lastDropTime = timestamp;
      }

      draw();
      animationFrameId = requestAnimationFrame(gameLoop);
    };

    window.addEventListener('keydown', handleKeyDown);
    animationFrameId = requestAnimationFrame(gameLoop);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      cancelAnimationFrame(animationFrameId);
    };
  }, [gameStarted]);

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <canvas
          ref={canvasRef}
          width={CANVAS_WIDTH}
          height={CANVAS_HEIGHT}
          className="border-2 border-gray-200"
        />
        <div className="mt-4 flex justify-between items-center">
          <div className="text-2xl font-bold text-indigo-600">
            Pontos: {score}
          </div>
          {!gameStarted && (
            <button
              onClick={() => setGameStarted(true)}
              className="flex items-center gap-2 bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors"
            >
              <PlayCircle size={24} />
              Começar Jogo
            </button>
          )}
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow-lg">
        <h2 className="text-xl font-bold text-center mb-4">Como Jogar</h2>
        <div className="grid grid-cols-2 gap-4">
          <div className="flex items-center gap-2">
            <ArrowLeft size={24} className="text-gray-600" />
            <span>Mover para esquerda</span>
          </div>
          <div className="flex items-center gap-2">
            <ArrowRight size={24} className="text-gray-600" />
            <span>Mover para direita</span>
          </div>
          <div className="flex items-center gap-2">
            <ArrowDown size={24} className="text-gray-600" />
            <span>Mover para baixo</span>
          </div>
          <div className="flex items-center gap-2">
            <RotateCw size={24} className="text-gray-600" />
            <span>Girar peça (↑)</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TetrisGame;