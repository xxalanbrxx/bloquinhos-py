# Versão mais organizada do jogo da velha CLI, com a mesma funcionalidade.

class TicTacToe:
    """Main TicTacToe data and operations"""

    def __init__(self):
        self._round = 1
        self._winner = None

        self._turn = 1
        self._running = False

        self._reset_field()

    @property
    def running(self):
        return self._running

    @property
    def turn(self):
        return self._turn

    @property
    def field(self):
        return self._field

    @property
    def winner(self):
        return self._winner

    @property
    def round(self):
        return self._round

    def _reset_field(self):
        assert self._running == False, "The game is not running!"

        self._field = [[0 for cell in range(0, 3)] for row in range(0, 3)]

    def _next_turn(self):
        assert self._running == True, "The game is not running!"

        self._round += 1 

        self._turn = 1 if self._turn == 2 else 2


    def _set_cell(self, row, col, player):
        assert self._field[row][col] == 0, "This cell has already been filled!"

        self._field[row][col] = player

    def _check_gameover(self):
        assert self._running == True, "The game is not running!"

        if self._field[1][1]:

            diagonal_1_win = \
                self._field[0][0] == self._field[1][1] == self._field[2][2]
            
            diagonal_2_win = \
                self._field[0][2] == self._field[1][1] == self._field[2][0]

            if diagonal_1_win or diagonal_2_win:
                self._winner = self._field[1][1]
                self._running = False

                return self

        for row in self._field:

            if row[0] and row[0] == row[1] == row[2]:

                self._winner = row[0]
                self._running = False

                return self

        for i in range(0, 3):

            if self._field[0][i] and \
               self._field[0][i] == self._field[1][i] == self._field[2][i]:

                self._winner = self._field[0][i]
                self._running = False

                return self

        if self._round == 8:
            self._running = False

        return self

    def start_game(self):
        assert self._running == False, \
               "Can't start a game while one is running!"

        self._running = True

        return self

    def play(self, cell):
        col = 0 if cell[0].upper() == "A" \
              else 1 if cell[0].upper() == "B" \
              else 2 if cell[0].upper() == "C" \
              else 4

        row = int(cell[1]) - 1

        self._set_cell(row, col, self._turn)
        self._check_gameover()

        if self._running:
            self._next_turn()

        return self


class GabesT3:
    """TicTacToe CLI front end"""

    def __init__(self, game, player1='X', player2='O', empty_cell=' '):
        self._game = game
        self._p1, self._p2, self._empty = player1, player2, empty_cell

    def get_player_symbol(self, n):
        return self._p1 if n == 1 else self._p2 if n == 2 else self._empty

    def write_game(self):
        g = [ 
            [self.get_player_symbol(c) for c in row]
            for row in self._game.field
        ]

        print(f'''
                  A   B   C
                1 {g[0][0]} | {g[0][1]} | {g[0][2]}
                  - + - + -
                2 {g[1][0]} | {g[1][1]} | {g[1][2]}
                  - + - + -
                3 {g[2][0]} | {g[2][1]} | {g[2][2]}
                ''')

        return self

    def prompt_play(self):
        print(f"{self.get_player_symbol(self._game.turn)}, é a sua vez!")

        try:
            cell = input("Insira uma letra e um número: ")
            self._game.play(cell)

        except (IndexError, AssertionError):
            print("Não dá pra jogar aí!")

        return self

    def get_winner(self):
        if self._game.winner:
            return self.get_player_symbol(self._game.winner)
        else:
            return None

    def tell_winner(self):
        winner = self.get_winner()
        if winner:
            print(f'\n{winner} venceu',
                  f'em {self._game.round} jogadas!')
        else:
            print(f'\nDeu empate! :(')

        return self


    def start(self):
        input("Pressione enter para iniciar...")

        self._game.start_game()

        while self._game.running:
            self.write_game().prompt_play()
                
        self.write_game().tell_winner()
          
        return self


if __name__ == '__main__':
    game = GabesT3(TicTacToe()).start()
