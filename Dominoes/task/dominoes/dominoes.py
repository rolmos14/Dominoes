import random


class Dominoes:
    """
    A class to represent Dominoes game.

    ...

    Attributes:
        initial_pieces : list
            contains all the 28 unique dominoe pieces
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
            stores the next turn 'player' or 'computer'.
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

    def __str__(self):
        """
        Return a representation of the current status of the game.
        """
        header = 70 * '='
        stock = "Stock size: " + str(len(self.stock_pieces))
        computer = "Computer pieces: " + str(len(self.computer_pieces))
        snake = self.domino_snake[0].__str__()
        player = "Your pieces:\n"
        for i in range(len(self.player_pieces)):
            player += f"{i + 1}:{self.player_pieces[i]}\n"
        status = "Status: " + ("It's your turn to make a move. Enter your command." if self.status == "player" else \
                                "Computer is about to make a move. Press Enter to continue... ")
        return "\n".join([header, stock, computer, "", snake, "", player, status])


dominoes = Dominoes()

while True:
    dominoes.new_game()
    if dominoes.start_game():
        break

print(dominoes)
