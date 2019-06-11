#-*- coding:utf-8 -*-
import sys
import pygame
from settings import *

def draw_cell(screen, left, top):
    '''绘制单元格，也即绘制小方块'''
    '''
    left: 单元格离窗口左边界的距离。单位是像素。
    top: 单元格离窗口上边界的距离。
    '''
    cell_left_top = (left, top)#小方块的左上角坐标点
    cell_width_height = (CELL_WIDTH, CELL_WIDTH)#小方块的宽度和高度
    cell_rect = pygame.Rect(cell_left_top, cell_width_height)
    pygame.draw.rect(screen, CELL_COLOR, cell_rect)


def check_events(game_state, game_resource):
    '''捕捉和处理键盘按键事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            on_key_down(event, game_state, game_resource)
        elif event.type == pygame.USEREVENT:
            if game_state.piece:
                game_state.piece.move_down()


def on_key_down(event, game_state, game_resource):
    if event.key == pygame.K_q:
        sys.exit()
    elif not game_state.paused and event.key == pygame.K_DOWN:
        if game_state.piece:
            print("向下按键被按下")
            game_state.piece.move_down()
    elif not game_state.paused and event.key == pygame.K_UP:
        if game_state.piece:
            print("向上按键被按下")
            game_state.piece.turn()
            # piece.move_up()
    elif not game_state.paused and event.key == pygame.K_RIGHT:
        if game_state.piece:
            print("向右按键被按下")
            game_state.piece.move_right()
    elif not game_state.paused and event.key == pygame.K_LEFT:
        if game_state.piece:
            print("向左按键被按下")
            game_state.piece.move_left()
    elif not game_state.paused and event.key == pygame.K_f:
        if game_state.piece:
            if game_state.piece:
                game_state.piece.fall_down()
    elif (event.key == pygame.K_s and game_state.stopped) \
            or event.key == pygame.K_r:
        game_state.start_game()
    #elif event.key == pygame.K_r:
       # game_state.start_game()#按r键强制重新开始游戏
    elif event.key == pygame.K_p and not game_state.stopped:
        if game_state.paused:
            game_state.resume_game()
        else:
            game_state.pause_game()
    elif event.key == pygame.K_m:
        game_resource.pause_bg_music()





