import pygame
import sys
from transformers import pipeline

# ==========================
# 1️⃣ Tic-Tac-Toe Logic
# ==========================
class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def make_move(self, row, col, player):
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            return True
        return False

    def is_winner(self, player):
        for row in self.board:
            if all([spot == player for spot in row]): return True
        for col in range(3):
            if all([self.board[r][col] == player for r in range(3)]): return True
        if all([self.board[i][i] == player for i in range(3)]) or \
           all([self.board[i][2 - i] == player for i in range(3)]): return True
        return False

    def is_draw(self):
        return all(self.board[r][c] != ' ' for r in range(3) for c in range(3))

    def minimax(self, is_maximizing, ai_player, human_player, alpha=-float('inf'), beta=float('inf')):
        if self.is_winner(ai_player): return 1
        if self.is_winner(human_player): return -1
        if self.is_draw(): return 0

        if is_maximizing:
            max_score = -float('inf')
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] == ' ':
                        self.board[r][c] = ai_player
                        score = self.minimax(False, ai_player, human_player, alpha, beta)
                        self.board[r][c] = ' '
                        max_score = max(max_score, score)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break
            return max_score
        else:
            min_score = float('inf')
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] == ' ':
                        self.board[r][c] = human_player
                        score = self.minimax(True, ai_player, human_player, alpha, beta)
                        self.board[r][c] = ' '
                        min_score = min(min_score, score)
                        beta = min(beta, score)
                        if beta <= alpha:
                            break
            return min_score

    def best_move(self, ai_player, human_player):
        best_score = -float('inf')
        move = None
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == ' ':
                    self.board[r][c] = ai_player
                    score = self.minimax(False, ai_player, human_player)
                    self.board[r][c] = ' '
                    if score > best_score:
                        best_score = score
                        move = (r, c)
        return move

# ==========================
# 2️⃣ Commentary System
# ==========================
def get_ai_commentary(move, board, human_player='X'):
    """Generate strategic commentary for AI moves."""
    row, col = move
    
    # Check if AI just won
    temp_board = [row[:] for row in board]
    if check_winner_on_board(temp_board, 'O'):
        return f"Victory! AI completes the winning combination at ({row},{col})"
    
    # Check if AI blocked human win
    temp_board = [row[:] for row in board]
    temp_board[row][col] = human_player
    if check_winner_on_board(temp_board, human_player):
        return f"Defensive play! AI blocks your winning move at ({row},{col})"
    
    # Check strategic positions
    if row == 1 and col == 1:
        return "Center control - the most strategic position on the board!"
    
    if (row, col) in [(0,0), (0,2), (2,0), (2,2)]:
        return f"Corner strategy at ({row},{col}) - setting up multiple win paths"
    
    # Check if AI is setting up a fork (multiple winning threats)
    potential_wins = count_potential_wins(board, 'O', move)
    if potential_wins >= 2:
        return f"Fork setup! AI creates multiple winning threats at ({row},{col})"
    
    return f"Strategic positioning at ({row},{col}) - maintaining board control"

def check_winner_on_board(board, player):
    """Check if player has won on given board state."""
    # Rows
    for row in board:
        if all([spot == player for spot in row]):
            return True
    # Columns  
    for col in range(3):
        if all([board[r][col] == player for r in range(3)]):
            return True
    # Diagonals
    if all([board[i][i] == player for i in range(3)]) or \
       all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

def count_potential_wins(board, player, move):
    """Count how many ways player could win after this move."""
    temp_board = [row[:] for row in board]
    temp_board[move[0]][move[1]] = player
    
    wins = 0
    # Check all empty spots for potential wins
    for r in range(3):
        for c in range(3):
            if temp_board[r][c] == ' ':
                temp_board[r][c] = player
                if check_winner_on_board(temp_board, player):
                    wins += 1
                temp_board[r][c] = ' '
    return wins

# ==========================
# 3️⃣ Pygame Setup
# ==========================
pygame.init()
WIDTH, HEIGHT = 300, 400
LINE_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)
LINE_WIDTH = 3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe AI + Strategic Commentary")

def draw_board():
    screen.fill(BG_COLOR)
    pygame.draw.line(screen, LINE_COLOR, (100, 0), (100, 300), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 300), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 100), (300, 100), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (300, 200), LINE_WIDTH)

def draw_marks(game):
    font = pygame.font.SysFont(None, 100)
    for r in range(3):
        for c in range(3):
            mark = game.board[r][c]
            if mark != ' ':
                text = font.render(mark, True, LINE_COLOR)
                screen.blit(text, (c * 100 + 25, r * 100 + 10))

def draw_commentary(text):
    """Draw commentary text at the bottom of the screen."""
    font = pygame.font.SysFont(None, 22)
    words = text.split(' ')
    lines = []
    line = ""
    for word in words:
        if font.size(line + word)[0] < 290:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    for i, line in enumerate(lines):
        rendered = font.render(line.strip(), True, (255, 255, 255))
        screen.blit(rendered, (5, 315 + i * 22))

# ==========================
# 4️⃣ Main Game Loop
# ==========================
def main():
    game = TicTacToe()
    human = 'X'
    ai = 'O'
    current_player = human
    commentary = "Click to make your move!"
    running = True

    while running:
        draw_board()
        draw_marks(game)
        draw_commentary(commentary)
        pygame.display.flip()

        if current_player == human:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // 100
                    row = y // 100
                    
                    # Boundary check
                    if 0 <= row < 3 and 0 <= col < 3:
                        if game.make_move(row, col, human):
                            if game.is_winner(human):
                                commentary = "🏁 Congratulations! You won!"
                                print("🏁 Human wins!")
                                running = False
                            elif game.is_draw():
                                commentary = "🤝 It's a draw! Well played!"
                                print("It's a draw! 🤝")
                                running = False
                            else:
                                current_player = ai
                                commentary = "AI is thinking..."
        else:
            move = game.best_move(ai, human)
            if move:
                game.make_move(move[0], move[1], ai)
                
                # Generate strategic commentary
                commentary = get_ai_commentary(move, game.board, human)
                print(f"💡 AI Commentary: {commentary}")

                if game.is_winner(ai):
                    commentary = "🏁 AI wins! Better luck next time!"
                    print("🏁 AI wins!")
                    running = False
                elif game.is_draw():
                    commentary = "🤝 It's a draw! Well played!"
                    print("It's a draw! 🤝")
                    running = False
                else:
                    current_player = human

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()