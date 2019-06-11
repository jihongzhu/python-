#-*- coding:utf-8 -*-

import sys
import pygame
from settings import *
import random
import time

from functions import draw_cell
from functions import check_events
from Piece import Piece
from gamewall import GameWall
from gamedisplay import GameDisplay
from gamestate import GameState
from gameresource import GameResource

def main():
    # 初始化pygame。启用Pygame必不可少的一步，在程序开始阶段执行。
    pygame.init()
    # 创建屏幕对象（也即窗口对象）
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #分辨率是1200*900
    pygame.display.set_caption("俄罗斯方块") #窗口标题
    # 一直按下某个键，每过100毫秒就引发一个KEYDOWN事件
    #第一个参数是指过 ###ms 后就产生按键事件。第二个参数是指以后每过 ###ms 就产生按键事件
    pygame.key.set_repeat(100, 100)
    # 屏幕背景色
    bg_color = BG_COLOR

    # 生成方块对象

    #game_wall = GameWall(screen)
    #piece = Piece(random.choice(PIECE_TYPES), screen, game_wall)
    game_state = GameState(screen)
    game_resource = GameResource()
    game_resource.play_bg_music()
    # 游戏主循环
    while True:
        # 监视键盘和鼠标事件
        check_events(game_state, game_resource)

        # 填充屏幕背景色
        #screen.fill(bg_color)

        # 设定屏幕背景
        screen.blit(game_resource.load_bg_img(), (0, 0))

        # 绘制直线,网格

        GameDisplay.draw_game_window(screen, game_state, game_resource)

        # 绘制小方块
        # draw_cell(screen, GAME_AREA_LEFT, GAME_AREA_TOP)
        if game_state.piece and not game_state.stopped:
            game_state.piece.paint()

        # 生成方块对象
        if game_state.piece and game_state.piece.is_on_bottom:
            game_state.touch_bottom()

        # 刷新屏幕
        pygame.display.flip()





main()












