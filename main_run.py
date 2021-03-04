# -*- coding: utf-8 -*-
import sys
import random
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from main_ui import Ui_MainWindow

data = {'/\\': '>', '>': '\\/', '\\/': '<', '<': '/\\', '||': '=', '=': '||'}
BOARD = [[0 for _ in range(10)] for __ in range(10)]
ENEMY_BOARD = [[0 for _ in range(10)] for ___ in range(10)]

FONT = QtGui.QFont()
FONT.setPointSize(12)
FONT.setBold(True)
FONT.setWeight(75)


class Game(QMainWindow, Ui_MainWindow):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.ship = ''
        self.type_ship = 0
        self.board = []
        self.enemy_board = []
        self.list_ships = [0, 0, 0, 0]
        self.list_ship_enemy = [0, 0, 0, 0]
        self.game_status = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Морской бой')

        for i in range(len(BOARD)):
            list_ = []
            for j in range(len(BOARD[i])):
                list_.append(self.gridLayout.itemAtPosition(i + 1, j + 1).widget())
            self.board.append(list_)

        self.set_visible_start_menu()
        self.set_visible_enemy_board(False)

        self.pushButton.clicked.connect(self.get_one_ship)
        self.pushButton_302.clicked.connect(self.get_two_ship)
        self.pushButton_301.clicked.connect(self.get_three_ship)
        self.pushButton_303.clicked.connect(self.get_four_ship)
        self.pushButton_304.clicked.connect(self.rotate)
        self.pushButton_101.clicked.connect(self.clear_board)
        self.buttonGroup.buttonClicked.connect(self.button_clicked)

        self.buttonGroup_2.buttonClicked.connect(self.enemy_button_clicked)

        self.action_2.triggered.connect(self.start_game_bot)
        self.action_3.triggered.connect(self.defeat)
        self.action_4.triggered.connect(self.info)
        self.action.triggered.connect(self.play_other_user)

        self.action_3.setEnabled(False)

    def play_other_user(self):
        message_window = QMessageBox(self)
        message_window.setFont(FONT)
        message_window.setText('В ближайшем будешем будет доступна игра по сети!')
        message_window.setWindowTitle('Функция недоступна')
        message_window.exec()

    def info(self):
        message_window = QMessageBox(self)
        message_window.setFont(FONT)
        message_window.setText('Бла-бла-бла\nПрочитай сам в интернете!')
        message_window.setWindowTitle('Правила игры')
        message_window.exec()

    def defeat(self):
        message_window = QMessageBox(self)
        message_window.setFont(FONT)
        message_window.setText('Поражение! Вы сдались!')
        message_window.setWindowTitle('Итоги игры')
        message_window.exec()
        self.end_game()

    def enemy_button_clicked(self, btn):
        for x in range(len(self.enemy_board)):
            list_btn = self.enemy_board[x]
            if btn in list_btn:
                y = list_btn.index(btn)
                text_btn = self.enemy_board[x][y].text()
                if text_btn not in ['.', 'X']:
                    if ENEMY_BOARD[x][y] == 0 or ENEMY_BOARD[x][y] == -1:
                        self.enemy_board[x][y].setText('.')
                    else:
                        self.enemy_board[x][y].setText('X')
                        ENEMY_BOARD[x][y] = 5
                        if not self.check_game_status():
                            return
                else:
                    return
                break

        if self.check_game_status():
            message_window = QMessageBox(self)
            message_window.setFont(FONT)
            message_window.setText('Победа! Вы уничтожили все корабли противника!')
            message_window.setWindowTitle('Итоги игры')
            message_window.exec()
            self.game_status = 0

        again_shot = True
        while again_shot:
            x, y = random.randint(0, 9), random.randint(0, 9)
            text_btn = self.board[x][y].text()
            if text_btn not in ['.', 'X']:
                if BOARD[x][y] == 0 or BOARD[x][y] == -1:
                    self.board[x][y].setText('.')
                    again_shot = False
                else:
                    self.board[x][y].setText('X')
                    BOARD[x][y] = 5

        if self.check_game_status() and self.game_status == 1:
            message_window = QMessageBox(self)
            message_window.setFont(FONT)
            message_window.setText('Поражение! Все ваши корабли были уничтожены!')
            message_window.setWindowTitle('Итоги игры')
            message_window.exec()
            self.game_status = 0

        if self.game_status == 0:
            self.end_game()
            self.action_3.setEnabled(False)

    def end_game(self):
        self.set_visible_enemy_board(False)
        self.set_visible_start_menu()
        self.clear_board()
        self.clear_enemy_board()


    def check_game_status(self):
        win_rate = 0
        for line in ENEMY_BOARD:
            win_rate += line.count(5)
        if win_rate == 20:
            return True

        win_rate = 0
        for line in BOARD:
            win_rate += line.count(5)
        if win_rate == 20:
            return True

        return False

    def create_random_enemy_board(self):
        for i in range(len(BOARD)):
            list_ = []
            for j in range(len(BOARD[i])):
                list_.append(self.gridLayout_3.itemAtPosition(i + 1, j + 1).widget())
            self.enemy_board.append(list_)

        self.list_ship_enemy = [0, 0, 0, 0]

        self.get_four_ship()
        [self.rotate() for _ in range(random.randint(0, 4))]
        while self.list_ship_enemy[self.type_ship - 1] != 1:
            x, y = random.randint(0, 9), random.randint(0, 9)
            self.place_ship(x, y, enemy=True)

        self.get_three_ship()
        [self.rotate() for _ in range(random.randint(0, 4))]
        while self.list_ship_enemy[self.type_ship - 1] != 2:
            x, y = random.randint(0, 9), random.randint(0, 9)
            self.place_ship(x, y, enemy=True)

        self.get_two_ship()
        [self.rotate() for _ in range(random.randint(0, 4))]
        while self.list_ship_enemy[self.type_ship - 1] != 3:
            x, y = random.randint(0, 9), random.randint(0, 9)
            self.place_ship(x, y, enemy=True)

        self.get_one_ship()
        [self.rotate() for _ in range(random.randint(0, 4))]
        while self.list_ship_enemy[self.type_ship - 1] != 4:
            x, y = random.randint(0, 9), random.randint(0, 9)
            self.place_ship(x, y, enemy=True)

    def start_game_bot(self):
        if sum(self.list_ships) == 10:
            self.game_status = 1
            self.action_3.setEnabled(True)
            self.set_visible_enemy_board()
            self.set_visible_start_menu(False)
            self.create_random_enemy_board()

        else:
            message_window = QMessageBox(self)
            message_window.setFont(FONT)
            message_window.setText('Для начала игры расставьте все корабли на своём поле!')
            message_window.setWindowTitle('Морской бой')
            message_window.exec()

    def clear_enemy_board(self):
        global ENEMY_BOARD
        ENEMY_BOARD = [[0 for _ in range(10)] for __ in range(10)]
        [[self.enemy_board[x][y].setText('') for x in range(len(self.enemy_board))] for y in range(len(self.enemy_board))]
        self.list_ship_enemy = [0, 0, 0, 0]

    def clear_board(self):
        global BOARD
        BOARD = [[0 for _ in range(10)] for __ in range(10)]
        [[self.board[x][y].setText('') for x in range(len(self.board))] for y in range(len(self.board))]
        self.ship = ''
        self.list_ships = [0, 0, 0, 0]
        self.pushButton.setEnabled(False)
        self.ship = ''
        self.label_44.setText('')

        self.pushButton_302.setEnabled(True)
        self.pushButton_301.setEnabled(True)
        self.pushButton_303.setEnabled(True)
        self.pushButton.setEnabled(True)

    def set_visible_enemy_board(self, visible=True):
        self.label_42.setVisible(visible)
        for i in range(len(BOARD) + 1):
            for j in range(len(BOARD[0]) + 1):
                widget = self.gridLayout_3.itemAtPosition(i, j)
                if widget:
                    widget.widget().setVisible(visible)

    def set_visible_start_menu(self, visible=True):
        for i in range(3):
            for j in range(2):
                widget = self.gridLayout_2.itemAtPosition(i, j)
                if widget:
                    widget.widget().setVisible(visible)
        self.label_43.setVisible(visible)
        self.label_44.setVisible(visible)
        self.pushButton_304.setVisible(visible)
        self.pushButton_101.setVisible(visible)

    def button_clicked(self, btn):
        if self.ship and self.game_status != 1:
            for x in range(len(self.board)):
                list_btn = self.board[x]
                if btn in list_btn:
                    y = list_btn.index(btn)
                    self.place_ship(x, y)
                    break

    def check_coord(self, x, y):
        if 0 <= x < len(self.board) and 0 <= y < len(self.board):
            return True
        return False

    def check_place_ship(self, x, y, sign_x, sign_y, len_ship, enemy):
        if sign_x != 0:
            num = x
            sign = sign_x
        else:
            num = y
            sign = sign_y
        for i in range(len_ship):
            if not (0 <= num + i * sign < len(self.board)):
                return False
            else:
                x_board, y_board = x + i * sign_x, y + i * sign_y
                if self.check_coord(x_board, y_board):
                    if enemy:
                        if ENEMY_BOARD[x_board][y_board] != 0:
                            return False
                    else:
                        if BOARD[x_board][y_board] != 0:
                            return False

        return True

    def create_neighbour(self, x, y, board):
        steps = [(0, 1), (1, 0), (1, 1), (-1, -1), (-1, 0), (0, -1), (-1, 1), (1, -1)]
        for step_x, step_y in steps:
            new_x, new_y = x + step_x, y + step_y
            if self.check_coord(new_x, new_y):
                if board[new_x][new_y] == 0:
                    board[new_x][new_y] = -1

    def place_ship(self, x, y, enemy=False):
        sign_x, sign_y = 0, 0
        if '+' in self.ship:
            list_ship = self.ship.split('+')
            if '<' in list_ship:
                sign_y = 1
            else:
                sign_y = -1
                list_ship = list_ship[::-1]
        else:
            list_ship = self.ship.split('\n')
            if '\\/' in list_ship:
                sign_x = -1
                list_ship = list_ship[::-1]
            else:
                sign_x = 1

        if self.check_place_ship(x, y, sign_x, sign_y, len(list_ship), enemy):
            for i in range(len(list_ship)):
                if not enemy:
                    self.board[x + i * sign_x][y + i * sign_y].setText(list_ship[i])
                    BOARD[x + i * sign_x][y + i * sign_y] = self.type_ship
                    self.create_neighbour(x + i * sign_x, y + i * sign_y, BOARD)
                else:
                    # self.enemy_board[x + i * sign_x][y + i * sign_y].setText(list_ship[i])
                    ENEMY_BOARD[x + i * sign_x][y + i * sign_y] = self.type_ship
                    self.create_neighbour(x + i * sign_x, y + i * sign_y, ENEMY_BOARD)
            if not enemy:
                self.list_ships[self.type_ship - 1] += 1
                if self.list_ships[0] == 4 and self.pushButton.isEnabled():
                    self.pushButton.setEnabled(False)
                    self.ship = ''
                    self.label_44.setText('')
                if self.list_ships[1] == 3 and self.pushButton_302.isEnabled():
                    self.pushButton_302.setEnabled(False)
                    self.ship = ''
                    self.label_44.setText('')
                if self.list_ships[2] == 2 and self.pushButton_301.isEnabled():
                    self.pushButton_301.setEnabled(False)
                    self.ship = ''
                    self.label_44.setText('')
                if self.list_ships[3] == 1 and self.pushButton_303.isEnabled():
                    self.pushButton_303.setEnabled(False)
                    self.ship = ''
                    self.label_44.setText('')
            else:
                self.list_ship_enemy[self.type_ship - 1] += 1

    def rotate(self):
        if self.ship:
            new_ship = []
            if_enter = True
            right = False
            top = True

            if '+' in self.ship:
                space = '+'
            else:
                space = '\n'

            for piece in self.ship.split(space):
                piece_ship = data[piece]
                if piece_ship == '=':
                    if_enter = False
                if piece_ship == '>' or piece_ship == '<':
                    right = True
                if piece_ship == '\\/' or piece_ship == '/\\':
                    top = False
                new_ship.append(piece_ship)
            if if_enter:
                if top:
                    self.ship = '\n'.join(new_ship[::-1])
                else:
                    self.ship = '\n'.join(new_ship)
            else:
                if right:
                    self.ship = '+'.join(new_ship[::-1])
                else:
                    self.ship = '+'.join(new_ship)

            self.label_44.setText(self.ship.replace('+', ''))

    def get_one_ship(self):
        self.ship = '/\\'
        self.type_ship = 1
        self.label_44.setText(self.ship)

    def get_two_ship(self):
        self.ship = '/\\\n||'
        self.type_ship = 2
        self.label_44.setText(self.ship)

    def get_three_ship(self):
        self.ship = '/\\\n||\n||'
        self.type_ship = 3
        self.label_44.setText(self.ship)

    def get_four_ship(self):
        self.ship = '/\\\n||\n||\n||'
        self.type_ship = 4
        self.label_44.setText(self.ship)


if __name__ == '__main__':
    app = QApplication([])
    game = Game()
    game.show()
    sys.exit(app.exec_())
