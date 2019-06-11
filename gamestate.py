#-*- coding:utf-8 -*-

import random
from settings import *
from Piece import Piece
from gamewall import GameWall
import pygame
import time

class GameState():
    def __init__(self, screen):
        self.screen = screen
        # 墙体对象
        self.wall = GameWall(screen)
        # 当前方块
        self.piece = None
        # 1000ms，定时器时间间隔
        self.timer_interval = TIMER_INTERVAL #1000ms

        #self.set_timer(self.timer_interval) #启动定时器

        self.game_score = 0
        self.stopped = True # 游戏停止了吗？
        self.paused = False
        self.session_count = 0
        self.next_piece = None
        self.difficulty = 1

    def set_timer(self, timer_interval):
        self.game_timer = pygame.time.set_timer(pygame.USEREVENT,
                            timer_interval)

    def stop_timer(self):
        # 传入0表示清除定时器
        pygame.time.set_timer(pygame.USEREVENT, 0)

    def add_score(self, score):
        self.game_score += score
        difficulty = self.game_score // DIFFICULTY_LEVEL_INTERVAL + 1
        if difficulty > self.difficulty:
            self.difficulty += 1
            self.timer_interval -= TIMER_DECREASE_VALUE
            pygame.time.set_timer(pygame.USEREVENT, self.timer_interval)

    def start_game(self):
        self.stopped = False
        self.set_timer(TIMER_INTERVAL)
        self.timer_interval = TIMER_INTERVAL
        #self.piece = Piece(random.choice(PIECE_TYPES), self.screen, self.wall)

        # 生成第一个方块。此时self.piece=None, self.next_piece引用下一方块对象。
        self.piece = self.new_piece()
        # 生成第二个方块，此时self.piece引用当前方块对象。
        self.piece = self.new_piece()

        self.session_count += 1
        self.wall.clear()
        self.game_score = 0
        self.paused = False
        # 每次游戏，使用不同的随机数序列
        random.seed(int(time.time()))

    def pause_game(self):
        '''暂停游戏'''
        pygame.time.set_timer(pygame.USEREVENT, 0) #传入0表示清除定时器
        self.paused = True

    def resume_game(self):
        '''继续游戏'''
        self.set_timer(self.timer_interval)
        self.paused = False

    def touch_bottom(self):
        if not self.stopped:
            self.wall.add_to_wall(self.piece)

        self.add_score(self.wall.eliminate_lines())
        #print(self.game_score)

        for c in range(COLUMN_NUM):
            if self.wall.is_wall(0, c):
                self.stopped = True
                break
        if not self.stopped:
            #self.piece = Piece(random.choice(PIECE_TYPES), self.screen, self.wall)
            self.piece = self.new_piece()
            if self.piece.hit_wall():
                self.stopped = True
        else:
            self.stop_timer()

    def new_piece(self):
        self.piece = self.next_piece
        self.next_piece = Piece(random.choice(PIECE_TYPES), self.screen, self.wall)

        return self.piece
