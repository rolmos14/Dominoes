import random


class Dominoes:
    """
    A class to represent Dominoes game.

    ...

    Attributes:
        initial_pieces : list
            contains all the 28 unique domino pieces
        stock_pieces : list
            contains the current stock pieces of the game.
            Initially there are 28 pieces which are used for the game. At the beginning of the game, 7 pieces go to
            Computer player (computer_pieces) and another 7 go to Player (player_pieces). Then players can get pieces
            from stock when they cannot continue playing with their pieces.
            It is stored as nested lists, one per piece.
        computer_pieces : list
            contains the current pieces of the Computer player.
            It is stored as nested lists, one per piece.
        player_pieces : list
            contains the current pieces of the Player.
            It is stored as nested lists, one per piece.
        domino_snake : list
            contains the current status of the game.
            It is stored as nested lists, one per piece.
        status : str
            stores the next turn 'player'/'computer' or the end-game condition 'player_wins'/'computer_wins'/'draw'.
    """
    initial_pieces = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
                      [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6],
                      [2, 2], [2, 3], [2, 4], [2, 5], [2, 6],
                      [3, 3], [3, 4], [3, 5], [3, 6],
                      [4, 4], [4, 5], [4, 6],
                      [5, 5], [5, 6],
                      [6, 6]]

    def __init__(self):
        """The constructor to initialize the object."""
        self.stock_pieces = self.initial_pieces
        self.computer_pieces = []
        self.player_pieces = []
        self.domino_snake = []
        self.status = ''

    def new_game(self):
        """Shuffles the stock pieces and then splits the pieces between players and the stock."""
        random.shuffle(self.stock_pieces)  # shuffle stock pieces
        self.computer_pieces = random.sample(self.stock_pieces, 7)  # take 7 for Computer player
        self.stock_pieces = [piece for piece in self.stock_pieces
                             if piece not in self.computer_pieces]  # update stock
        self.player_pieces = random.sample(self.stock_pieces, 7)  # take 7 for Player
        self.stock_pieces = [piece for piece in self.stock_pieces
                             if piece not in self.player_pieces]  # update stock, 14 remain in stock

    def start_game(self):
        """
        Determines the starting piece and updates the game accordingly.
        If starting piece cannot be determined it returns False.

        Return:
            possible : bool
                True if starting piece has been determined, False if not
        """
        possible = False
        double_pieces = [[6, 6], [5, 5], [4, 4], [3, 3], [2, 2], [1, 1], [0, 0]]
        for double in double_pieces:
            if double in self.computer_pieces:
                # Computer starts. Remove the piece from computer and place it in the snake.
                self.computer_pieces.remove(double)
                self.domino_snake.append(double)
                self.status = "player"
                possible = True
                break
            elif double in self.player_pieces:
                # Player starts. Remove the piece from player and place it in the snake.
                self.player_pieces.remove(double)
                self.domino_snake.append(double)
                self.status = "computer"
                possible = True
                break
        return possible

    def move(self):
        """Makes the move from player or computer and switches turn."""
        # If it's player's turn
        if self.status == "player":
            # Wait for valid move
            while True:
                try:
                    player_move = int(input())
                    if abs(player_move) > len(self.player_pieces):
                        raise ValueError
                    if self.move_is_legal(self.player_pieces[abs(player_move) - 1], player_move):
                        break  # valid and legal move
                    print("Illegal move. Please try again.")
                except ValueError:
                    print("Invalid input. Please try again.")
            # Apply the move
            self.apply_move(self.player_pieces, player_move)
            self.status = "computer"  # switch turn
        # If it's computer's turn
        else:  # self.status == "computer"
            # Wait for Enter from player
            input()
            # Choose piece based on AI
            computer_move = self.ai_move()
            # Apply the move
            self.apply_move(self.computer_pieces, computer_move)
            self.status = "player"  # switch turn

    def ai_move(self):
        """
        Determines the move to be performed by computer, taking into account computer pieces and snake pieces.

        Return:
            move : int
                move to be performed by computer
        """
        # Count number of 0's, 1's... and 6's in computer hand and in the snake
        number_count = []  # list where number is the index and the value is the count of that number
        for num in range(7):
            count = 0
            # Count appearances in computer pieces
            count = len([number for piece in self.computer_pieces for number in piece if num == number])
            # Count appearances in domino snake
            count += len([number for piece in self.domino_snake for number in piece if num == number])
            number_count.append(count)
        # Each piece in computer hand receives a score equal to the sum of appearances of its numbers
        piece_score = []  # list where index is the position of the piece and value the score
        for piece in self.computer_pieces:
            piece_score.append(number_count[piece[0]] + number_count[piece[1]])
        # Try to play the piece with the highest score
        for _ in range(len(piece_score)):
            piece_index = piece_score.index(max(piece_score))
            piece_score[piece_index] = -1  # -1 for pieces already checked
            # Check if piece can be placed at left end of domino snake
            if self.move_is_legal(self.computer_pieces[piece_index], -1):
                return - (piece_index + 1)
            # Check if piece can be placed at right end of domino snake
            if self.move_is_legal(self.computer_pieces[piece_index], 1):
                return piece_index + 1
        # If no piece can be played, pick from stock
        return 0

    def move_is_legal(self, piece, move):
        """
        Verifies if a move is legal.
        A move is legal if at least one of the numbers of the piece matches
        the number at the corresponding end of the domino snake.
        A pick from the stock is always legal.

        Parameters:
            piece : list
                list containing the two numbers of the piece
            move : int
                move to perform

        Return:
            legal : bool
                True if move is legal, otherwise False

        """
        # Verify at left end of domino snake
        if move < 0 and self.domino_snake[0][0] in piece:
            return True
        # Verify at right end of domino snake
        if move > 0 and self.domino_snake[-1][1] in piece:
            return True
        if move == 0:
            return True
        return False

    def apply_move(self, pieces, move):
        """
        Applies the move for the specified player pieces.

        Parameters:
            pieces : list
                list of pieces of the player that is making the move
            move : int
                move to perform
        """
        if move < 0:  # piece to the left of the snake
            self.domino_snake.insert(0, pieces.pop(abs(move) - 1))
            # Check orientation of piece to match numbers
            if self.domino_snake[0][1] != self.domino_snake[1][0]:
                self.domino_snake[0] = self.domino_snake[0][::-1]
        elif move > 0:  # piece to the right of the snake
            self.domino_snake.append(pieces.pop(move - 1))
            # Check orientation of piece to match numbers
            if self.domino_snake[-1][0] != self.domino_snake[-2][1]:
                self.domino_snake[-1] = self.domino_snake[-1][::-1]
        else:  # move == 0, pick from stock
            if len(self.stock_pieces) > 0:
                pieces.append(self.stock_pieces.pop())

    def game_over(self):
        """Checks for end-game conditions and updates status accordingly."""
        if len(self.player_pieces) == 0:
            self.status = "player_wins"
        elif len(self.computer_pieces) == 0:
            self.status = "computer_wins"
        else:
            left_end = self.domino_snake[0][0]
            right_end = self.domino_snake[len(self.domino_snake) - 1][1]
            # If numbers on the ends are identical
            if left_end == right_end:
                # And appear within the snake 8 times, it's a draw
                if len([piece for piece in self.domino_snake if left_end in piece]) >= 8:
                    self.status = "draw"

    def __str__(self):
        """
        Return a representation of the current status of the game.
        """
        header = 70 * '='
        stock = "Stock size: " + str(len(self.stock_pieces))
        computer = "Computer pieces: " + str(len(self.computer_pieces))
        snake = ""
        if len(self.domino_snake) > 6:
            # If snake is long, show it compacted
            snake = self.domino_snake[0].__str__() + self.domino_snake[1].__str__() + \
                    self.domino_snake[2].__str__() + "..." + self.domino_snake[-3].__str__() + \
                    self.domino_snake[-2].__str__() + self.domino_snake[-1].__str__()
        else:
            # Show it entirely
            for piece in self.domino_snake:
                snake += piece.__str__()
        player = "Your pieces:\n"
        for i in range(len(self.player_pieces)):
            player += f"{i + 1}:{self.player_pieces[i]}\n"
        status = "Status: "
        if self.status == "player":
            status += "It's your turn to make a move. Enter your command."
        elif self.status == "computer":
            status += "Computer is about to make a move. Press Enter to continue..."
        elif self.status == "player_wins":
            status += "The game is over. You won!"
        elif self.status == "computer_wins":
            status += "The game is over. The computer won!"
        elif self.status == "draw":
            status += "The game is over. It's a draw!"
        return "\n".join([header, stock, computer, "", snake, "", player, status])


dominoes = Dominoes()

# Crate a new game and start it
while True:
    dominoes.new_game()
    if dominoes.start_game():
        break

# Game loop
while True:
    print(dominoes)
    if dominoes.status not in ("player", "computer"):
        break  # game over
    dominoes.move()
    dominoes.game_over()
