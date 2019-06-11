#-*- coding:utf-8 -*-

from settings import *
from gamedisplay import GameDisplay
import pygame

class Piece(object):
    def __init__(self, shape, screen, gamewall):
        self.x = 4
        self.y = 0

        # 值为一个字符。S,  I，J，L，O，T，Z等字母中的一个
        self.shape = shape
        # 翻转了几次，决定方块的姿态
        self.turn_times = 0
        # 到达底部了吗？
        self.is_on_bottom = False

        # 屏幕对象。绘制方块的方法会用到。
        self.screen = screen

        self.game_wall = gamewall

    def paint(self):
        shape_template = PIECES[self.shape]
        shape_turn = shape_template[self.turn_times]

        for r in range(len(shape_turn)):
            for c in range(len(shape_turn[0])):
                if shape_turn[r][c] == 'O':
                    self.draw_cell(self.y + r, self.x + c)

    def draw_cell(self, row, column):
        GameDisplay.draw_cell(self.screen, row, column, PIECE_COLORS[self.shape])

    def move_right(self):
        '''方块向右移动1个单元格'''
        if self.can_move_right():
            self.x += 1

    def move_left(self):
        '''方块向左移动1个单元格'''
        if self.can_move_left():
            self.x -= 1

    def move_up(self):
        '''方块向上移动1个单元格'''
        if self.can_move_up():
            self.y -= 1

    def move_down(self):
        '''方块向下移动1格。如果到达了底部，设置is_on_bottom属性为True.'''
        if self.can_move_down():
            self.y += 1
        else:
            self.is_on_bottom = True

    def can_move_right(self):
        shape_mtx = PIECES[self.shape][self.turn_times]

        for r in range(len(shape_mtx)):
            for c in range(len(shape_mtx[0])):
                if shape_mtx[r][c] == 'O':
                    if (self.x + c >= COLUMN_NUM - 1) \
                            or (self.game_wall.is_wall(self.y + r, self.x + c + 1)):
                        return False
        return True

    def can_move_left(self):
        shape_mtx = PIECES[self.shape][self.turn_times]

        for r in range(len(shape_mtx)):
            for c in range(len(shape_mtx[0])):
                if shape_mtx[r][c] == 'O':
                    if (self.x + c <= 0)\
                            or (self.game_wall.is_wall(self.y + r, self.x + c - 1)):
                        return False
        return True

    def can_move_up(self):
        shape_mtx = PIECES[self.shape][self.turn_times]

        for r in range(len(shape_mtx)):
            for c in range(len(shape_mtx[0])):
                if shape_mtx[r][c] == 'O':
                    if self.y + r <= 0:
                        return False
        return True

    def can_move_down(self):
        shape_mtx = PIECES[self.shape][self.turn_times]

        for r in range(len(shape_mtx)):
            for c in range(len(shape_mtx[0])):
                if shape_mtx[r][c] == 'O':
                    if (self.y + r >= LINE_NUM - 1)\
                            or (self.game_wall.is_wall(self.y + r + 1, self.x + c)):
                        return False
        return True

    def turn(self):
        shape_list_len = len(PIECES[self.shape])
        if self.can_turn():
            self.turn_times = (self.turn_times + 1) % shape_list_len

    def can_turn(self):
        shape_list_len = len(PIECES[self.shape])
        turn_times = (self.turn_times + 1) % shape_list_len
        self.shape_mtx = PIECES[self.shape][turn_times]

        for r in range(len(self.shape_mtx)):
            for c in range(len(self.shape_mtx[0])):
                if self.shape_mtx[r][c] == 'O':
                    if ((self.x + c < 0 or self.x + c >= COLUMN_NUM) or
                        (self.y + r < 0 or self.y + r >= LINE_NUM) or
                        (self.game_wall.is_wall(self.y + r, self.x + c))):
                        return False
        return True

    def fall_down(self):
        while not self.is_on_bottom:
            self.move_down()

    def hit_wall(self):
        shape_mtx = PIECES[self.shape][self.turn_times]
        for r in range(len(shape_mtx)):
            for c in range(len(shape_mtx[0])):
                if shape_mtx[r][c] == 'O':
                    if self.game_wall.is_wall(self.y + r, self.x + c):
                        return True
        return False
