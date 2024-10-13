import agentscope
from agentscope.agents import AgentBase
from agentscope.message import Msg
import json
import random

# 初始化 AgentScope 并加载模型配置
model_configs = "../../config/qwen_model_config.json" 
agentscope.init(model_configs=model_configs, project="Gomoku Game")

class BoardAgent(AgentBase):
    def __init__(self, name):
        super().__init__(name=name)
        self.board = [[0 for _ in range(15)] for _ in range(15)]
        self.game_end = False
        self.current_player = 'o'

    def __call__(self, move):
        row, col = move
        if self.is_valid_move(move):
            self.board[row][col] = self.current_player
            if self.check_win(row, col):
                self.game_end = True
                return Msg(self.name, f"Game Over! Player {self.current_player} wins!", role="user")
            if self.check_draw():
                self.game_end = True
                return Msg(self.name, "Game Over! It's a draw!", role="user")
            self.current_player = 'x' if self.current_player == 'o' else 'o'
            return Msg(self.name, "Move accepted", role="user")
        else:
            return Msg(self.name, f"Error: Invalid move {move}", role="user")

    def is_valid_move(self, move):
        row, col = move
        if 0 <= row < 15 and 0 <= col < 15:
            return self.board[row][col] == 0
        return False

    def get_valid_moves(self):
        valid_moves = []
        for i in range(15):
            for j in range(15):
                if self.board[i][j] == 0:
                    valid_moves.append([i, j])
        return valid_moves

    def check_win(self, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for i in range(1, 5):
                r, c = row + i * dr, col + i * dc
                if 0 <= r < 15 and 0 <= c < 15 and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            for i in range(1, 5):
                r, c = row - i * dr, col - i * dc
                if 0 <= r < 15 and 0 <= c < 15 and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False

    def check_draw(self):
        return all(self.board[i][j] != 0 for i in range(15) for j in range(15))

    def board_to_string(self):
        return '\n'.join([''.join(map(str, row)) for row in self.board])

class GomokuAgent(AgentBase):
    SYS_PROMPT_TEMPLATE = """
    You're an aggressive and strategic Gomoku player. Your goal is to win as quickly as possible while preventing your opponent from winning. Play according to these rules and strategies:

    Game Rules:
    1. The Gomoku board is a 15*15 grid. Moves are made by specifying row and column indexes, with [0, 0] marking the top-left corner and [14, 14] indicating the bottom-right corner.
    2. The goal is to be the first player to form an unbroken line of FIVE of your pieces horizontally, vertically, or diagonally. This is the win condition - focus on achieving this!
    3. If the board is completely filled with pieces and no player has formed a row of five, the game is declared a draw.

    Aggressive Strategies:
    1. Winning is top priority! Always look for opportunities to create a line of five pieces.
    2. Block your opponent aggressively. If they have three or four pieces in a row, block them immediately!
    3. Create multiple threats simultaneously. Try to form patterns that give you multiple ways to win.
    4. Control the center of the board when possible, as it offers more winning opportunities.
    5. Be aware of "open" lines (where both ends are open) as they are more valuable than "closed" lines.
    6. IMPORTANT: Prioritize placing your pieces in continuous lines - vertically, horizontally, or diagonally. This strategy increases your chances of winning significantly.

    Note:
    1. Your pieces are represented by '{}', your opponent's by '{}'. 0 represents an empty spot on the board.
    2. Think several moves ahead. Consider both your potential winning moves and your opponent's threats.
    3. Don't waste moves - each placement should either progress your win or hinder your opponent.
    4. Only an unbroken line of five same pieces will win the game. For example, "xxxoxx" is not a win.
    5. Remember, the unbroken line of five can be in any direction: horizontal, vertical, or diagonal.
    6. Always try to extend your existing lines or start new lines in a clear direction (vertical, horizontal, or diagonal).

    Your strategy should be aggressive yet thoughtful. Aim to win quickly by creating continuous lines, but also prevent your opponent from winning at all costs!
    """

    def __init__(self, name, player_symbol, opponent_symbol, model_config_name):
        sys_prompt = f"You are the {name} player ({player_symbol}). " + self.SYS_PROMPT_TEMPLATE.format(player_symbol, opponent_symbol)
        super().__init__(name=name, sys_prompt=sys_prompt, model_config_name=model_config_name)

    def reply(self, x: Msg = None) -> Msg:
        if x is not None:
            self.memory.add(x)

        hint_prompt = """Analyze the board carefully. Respond in the following JSON format:
        {
            "thought": "Detailed analysis of the current situation, your strategy, and reasoning for your move. Explain how your move contributes to forming a continuous line (vertical, horizontal, or diagonal).",
            "move": [row index, column index]
        }
        Make sure your move is aggressive and strategic, aiming to win quickly by creating continuous lines or block your opponent's potential win. Prioritize moves that extend your existing lines or start new lines in a clear direction.
        """

        msg_hint = Msg("system", hint_prompt, role="system")

        prompt = self.model.format(
            self.memory.get_memory(),
            msg_hint,
        )

        response = self.model(prompt)

        try:
            parsed_response = json.loads(response.text)
            if "move" not in parsed_response or "thought" not in parsed_response:
                raise ValueError("Invalid response format")
        except (json.JSONDecodeError, ValueError):
            # 如果无法解析响应，返回一个随机有效移动作为后备方案
            parsed_response = {"move": [random.randint(0, 14), random.randint(0, 14)], "thought": "Random move due to error"}

        self.memory.add(Msg(self.name, json.dumps(parsed_response, ensure_ascii=False), role="assistant"))

        return Msg(self.name, json.dumps(parsed_response, ensure_ascii=False), role="assistant")

def run_gomoku_game():
    board = BoardAgent("Host")
    players = [
        GomokuAgent("Alice", 'o', 'x', "my_qwen_chat"),
        GomokuAgent("Bob", 'x', 'o', "my_qwen_chat")
    ]

    current_player = 0
    while not board.game_end:
        player = players[current_player]
        
        valid_move = False
        attempts = 0
        while not valid_move and attempts < 3:
            # Get the move from the player
            msg = player(Msg("Host", board.board_to_string(), role="user"))
            
            # Parse the response and extract the move
            try:
                response = json.loads(msg.content)
                move = response["move"]
                thought = response["thought"]
                
                # Print the player's response
                print(f"{player.name}: {{")
                print(f'    "thought": "{thought}",')
                print(f'    "move": {move}')
                print("}")

                # Check if the move is valid
                if board.is_valid_move(move):
                    valid_move = True
                else:
                    print(f"Error: Invalid move {move}. The cell is already occupied or out of bounds.")
                    print(f"{player.name}, please choose another move.")
                    attempts += 1
            except (json.JSONDecodeError, KeyError):
                print(f"Error: Invalid response from {player.name}")
                attempts += 1

        if not valid_move:
            # If the AI failed to make a valid move after 3 attempts, make a random valid move
            valid_moves = board.get_valid_moves()
            move = random.choice(valid_moves)
            print(f"{player.name} failed to make a valid move. Making a random move: {move}")

        # Make the move on the board
        result = board(move)
        
        # Print the current board state
        print(f"Host: The current board is as follows:")
        print(board.board_to_string())
        
        if "Game Over" in result.content:
            print(result.content)
            break
        
        # Switch to the other player
        current_player = 1 - current_player
        print(f"{players[current_player].name}, it's your turn.")
        print()

if __name__ == "__main__":
    run_gomoku_game()