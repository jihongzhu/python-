#-*- coding:utf-8 -*-

from settings import *
import pygame


class GameDisplay(object):
    @staticmethod
    def draw_cell(screen, row, column, color):
        '''第y行x列的格子里填充color颜色。一种方块对应一种颜色。'''
        cell_position = (column * CELL_WIDTH + GAME_AREA_LEFT + 1,
                          row * CELL_WIDTH + GAME_AREA_TOP + 1)

        cell_width_height = (CELL_WIDTH - 2, CELL_WIDTH - 2)

        cell_rect = pygame.Rect(cell_position, cell_width_height)

        pygame.draw.rect(screen, color, cell_rect)

    @staticmethod
    def draw_game_window(screen, game_state, game_resource):
        '''绘制游戏区域'''
        # pygame.draw.line(screen, (0, 0, 0), (100, 100), (200, 200))
        # 绘制一条线。第二个参数(0, 0, 0)决定颜色是黑色。起点坐标是(100, 100)，终点是(200, 200)

        """
        for i in range(20):
            pygame.draw.line(screen, EDGE_COLOR, (GAME_AREA_LEFT, GAME_AREA_TOP + (i * CELL_WIDTH)),
                             (GAME_AREA_LEFT + GAME_AREA_WIDTH, GAME_AREA_TOP + (i * CELL_WIDTH)))

        # 绘制底部边界线
        pygame.draw.line(screen, EDGE_COLOR, (GAME_AREA_LEFT, GAME_AREA_TOP + 20 * CELL_WIDTH),
                         (GAME_AREA_LEFT + GAME_AREA_WIDTH, GAME_AREA_TOP + 20 * CELL_WIDTH))
        # 绘制左侧边界线
        for i in range(10):
            pygame.draw.line(screen, EDGE_COLOR, (GAME_AREA_LEFT + (i * CELL_WIDTH), GAME_AREA_TOP),
                             (GAME_AREA_LEFT + (i * CELL_WIDTH), GAME_AREA_TOP + 20 * CELL_WIDTH))
        # 绘制右侧边界线
        pygame.draw.line(screen, EDGE_COLOR, (GAME_AREA_LEFT + 10 * CELL_WIDTH, GAME_AREA_TOP),
                         (GAME_AREA_LEFT + 10 * CELL_WIDTH, GAME_AREA_TOP + 20 * CELL_WIDTH))
        """
        GameDisplay.draw_border(screen, GAME_AREA_WIDTH - EDGE_WIDTH, GAME_AREA_TOP, LINE_NUM, COLUMN_NUM)

        GameDisplay.draw_wall(game_state.wall)
        GameDisplay.draw_score(screen, game_state.game_score)
        GameDisplay.draw_difficulty_level(screen, game_state.difficulty)
        GameDisplay.draw_mannual(screen)
        GameDisplay.draw_next_piece(screen, game_state.next_piece)

        #游戏结束图片显示
        if game_state.stopped:
            if game_state.session_count > 0:
                GameDisplay.draw_gameover(screen, game_resource)

        #游戏开始图片显示
        if game_state.stopped and not game_state.session_count:
            GameDisplay.draw_start_prompt(screen, game_resource)
        #游戏暂停图片显示
        if game_state.paused:
            GameDisplay.draw_pause_prompt(screen, game_resource)


    @staticmethod
    def draw_score(screen, score):
        '''绘制游戏得分'''
        score_label_font = pygame.font.SysFont('simhei', 28)#换成'arial'，无法显示中文。

        score_label_surface = score_label_font.render(u'得分: ', False, SCORE_LABEL_COLOR)
        score_label_position = (GAME_AREA_LEFT + COLUMN_NUM * CELL_WIDTH + MARGIN_WIDTH, GAME_AREA_TOP + 5 * CELL_WIDTH)
        screen.blit(score_label_surface, score_label_position)

        score_font = pygame.font.SysFont('arial', 36)
        score_surface = score_font.render(str(score), False, SCORE_COLOR)
        score_label_width = score_label_surface.get_width()
        score_position = (score_label_position[0] + score_label_width + 20, score_label_position[1])
        screen.blit(score_surface, score_position)



    @staticmethod
    def draw_wall(game_wall):
        '''绘制墙体'''
        for r in range(LINE_NUM):
            for c in range(COLUMN_NUM):
                if game_wall.area[r][c] != WALL_BLANK_LABEL:
                    GameDisplay.draw_cell(game_wall.screen, r, c, PIECE_COLORS[game_wall.area[r][c]])

    @staticmethod
    def draw_next_piece(screen, next_piece):
        '''绘制下一方块'''
        # 绘制边框
        start_x = GAME_AREA_LEFT + COLUMN_NUM * CELL_WIDTH + MARGIN_WIDTH

        start_y = GAME_AREA_TOP
        GameDisplay.draw_border(screen, start_x, start_y, 4, 4)

        if next_piece:
            start_x += EDGE_WIDTH
            start_y += EDGE_WIDTH
            cells = []  #cells变量存储姿态矩阵中有砖块的单元格
            # 扫描姿态矩阵，得出有砖块的单元格
            shape_template = PIECES[next_piece.shape]
            shape_turn = shape_template[next_piece.turn_times]
            for r in range(len(shape_turn)):
                for c in range(len(shape_turn[0])):
                    if shape_turn[r][c] == 'O':
                        cells.append((c, r, PIECE_COLORS[next_piece.shape]))

            max_c = max([cell[0] for cell in cells])
            min_c = min([cell[0] for cell in cells])
            start_x += round((4 - (max_c - min_c + 1)) / 2 * CELL_WIDTH)
            max_r = max([cell[1] for cell in cells])
            min_r = min([cell[1] for cell in cells])
            start_y += round((4 - (max_r - min_r + 1)) / 2 * CELL_WIDTH)

            # 绘制方块
            for cell in cells:
                color = cell[2]
                #left_top = (start_x + cell[0] * CELL_WIDTH, start_y + cell[1] * CELL_WIDTH)
                left_top = (start_x + (cell[0] - min_c) * CELL_WIDTH,
                            start_y + (cell[1] - min_r) * CELL_WIDTH)

                GameDisplay.draw_cell_rect(screen, left_top, color)

    @staticmethod
    def draw_start_prompt(screen, game_resource):
        start_tip_position = (GAME_AREA_LEFT + 1 * CELL_WIDTH,
                              GAME_AREA_TOP + 10 * CELL_WIDTH)
        screen.blit(game_resource.load_newgame_img(), start_tip_position)

    @staticmethod
    def draw_pause_prompt(screen, game_resource):
        '''显示游戏暂停'''
        pause_position = (GAME_AREA_LEFT + 1 * CELL_WIDTH,
                          GAME_AREA_TOP + 9 * CELL_WIDTH)
        screen.blit(game_resource.load_pausing_img(), pause_position)

        resume_tip_position = (GAME_AREA_LEFT + CELL_WIDTH / 2,
                               GAME_AREA_TOP + 11 * CELL_WIDTH)
        screen.blit(game_resource.load_continue_img(), resume_tip_position)

    @staticmethod

    def draw_gameover(screen, game_resource):
        gameover_position = (GAME_AREA_LEFT + 3 * CELL_WIDTH,
                          GAME_AREA_TOP + 9 * CELL_WIDTH)
        screen.blit(game_resource.load_gameover_img(), gameover_position)

        resume_tip_position = (GAME_AREA_LEFT + 2 * CELL_WIDTH,
                               GAME_AREA_TOP + 11 * CELL_WIDTH)
        screen.blit(game_resource.load_newgame_img(), resume_tip_position)

    @staticmethod
    def draw_border(screen, start_x, start_y, line_num, column_num):
        top_border = pygame.Rect(start_x, start_y, 2 * EDGE_WIDTH + column_num * CELL_WIDTH, EDGE_WIDTH)
        pygame.draw.rect(screen, EDGE_COLOR, top_border)

        left_border = pygame.Rect(start_x, start_y, EDGE_WIDTH, 2 * EDGE_WIDTH + line_num * CELL_WIDTH)
        pygame.draw.rect(screen, EDGE_COLOR, left_border)

        right_border = pygame.Rect(start_x + EDGE_WIDTH + column_num * CELL_WIDTH, start_y, EDGE_WIDTH,
                                   2 * EDGE_WIDTH + line_num * CELL_WIDTH)
        pygame.draw.rect(screen, EDGE_COLOR, right_border)

        bottom_border = pygame.Rect(start_x, start_y + EDGE_WIDTH + line_num * CELL_WIDTH,
                                    2 * EDGE_WIDTH + column_num * CELL_WIDTH, EDGE_WIDTH)
        pygame.draw.rect(screen, EDGE_COLOR, bottom_border)


    @staticmethod
    def draw_cell_rect(screen, left_top_anchor, color):
        left_top_anchor = (left_top_anchor[0] + 1, left_top_anchor[1] + 1)
        cell_width_height = (CELL_WIDTH - 2, CELL_WIDTH - 2)
        cell_rect = pygame.Rect(left_top_anchor, cell_width_height)
        pygame.draw.rect(screen, color, cell_rect)

    @staticmethod
    def draw_difficulty_level(screen, level):
        '''绘制游戏难度级别'''
        level_label_font = pygame.font.SysFont('simhei', 28) # 换成'arial'，无法显示中文。

        level_label_surface = level_label_font.render(u'难度: ', False, SCORE_LABEL_COLOR)
        level_label_position = (GAME_AREA_LEFT + COLUMN_NUM * CELL_WIDTH + MARGIN_WIDTH, GAME_AREA_TOP + 8 * CELL_WIDTH)
        screen.blit(level_label_surface, level_label_position)

        level_font = pygame.font.SysFont('arial', 36)
        level_surface = level_font.render(str(level), False, SCORE_COLOR)
        level_label_width = level_label_surface.get_width()
        level_position = (level_label_position[0] + level_label_width + 20, level_label_position[1])
        screen.blit(level_surface, level_position)

    @staticmethod
    def draw_mannual(screen):
        base_position_x = 40
        base_position_y = GAME_AREA_TOP + 40
        title_font = pygame.font.SysFont('simhei', 28)
        title_surface = title_font.render(u'玩法：', True, TITLE_COLOR)
        title_position = (base_position_x, base_position_y)
        screen.blit(title_surface, title_position)

        base_position_y += 60
        gamectrl_label_font = pygame.font.SysFont('simhei', 24)
        gamectrl_label_surface = gamectrl_label_font.render(u'游戏控制', True, TITLE_COLOR)
        gamectrl_label_position = (base_position_x, base_position_y)
        screen.blit(gamectrl_label_surface, gamectrl_label_position)

        base_position_y += 40
        man_font = pygame.font.SysFont('simhei', 20)
        man_down_surface = man_font.render(u'开始：s字母键；退出：q字母键', False, HANZI_COLOR)
        man_down_position = (base_position_x, base_position_y)
        screen.blit(man_down_surface, man_down_position)

        base_position_y += 40
        # man_font = pygame.font.SysFont('stkaiti', 20)
        man_pause_surface = man_font.render(u'暂停/继续：p字母键', False, HANZI_COLOR)
        man_pause_position = (base_position_x, base_position_y)
        screen.blit(man_pause_surface, man_pause_position)

        base_position_y += 40
        # man_font = pygame.font.SysFont('stkaiti', 20)
        man_restart_surface = man_font.render(u'重玩：r字母键', False, HANZI_COLOR)
        man_restart_position = (base_position_x, base_position_y)
        screen.blit(man_restart_surface, man_restart_position)

        base_position_y += 40
        # man_font = pygame.font.SysFont('stkaiti', 20)
        man_music_surface = man_font.render(u'暂停/继续播放音乐：m字母键', False, HANZI_COLOR)
        man_music_position = (base_position_x, base_position_y)
        screen.blit(man_music_surface, man_music_position)

        base_position_y += 60
        # gamectrl_label_font = pygame.font.SysFont('stkaiti', 24)
        gamectrl_label_surface = gamectrl_label_font.render(u'方块控制', True, TITLE_COLOR)
        gamectrl_label_position = (base_position_x, base_position_y)
        screen.blit(gamectrl_label_surface, gamectrl_label_position)

        base_position_y += 40
        # man_font = pygame.font.SysFont('stkaiti', 20)
        man_down_surface = man_font.render(u'翻转：上方向键；下移：下方向键', False, HANZI_COLOR)
        man_down_position = (base_position_x, base_position_y)
        screen.blit(man_down_surface, man_down_position)

        base_position_y += 40
        man_move_surface = man_font.render(u'左移：左方向键；右移：右方向键', False, HANZI_COLOR)
        man_move_position = (base_position_x, base_position_y)
        screen.blit(man_move_surface, man_move_position)

        base_position_y += 40
        man_speed_surface = man_font.render(u'快速到底：f字母键', False, HANZI_COLOR)
        man_speed_position = (base_position_x, base_position_y)
        screen.blit(man_speed_surface, man_speed_position)



