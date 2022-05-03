import pygame

pygame.init()

window = pygame.display.set_mode((800, 600))

# Константы для редактирования
game_running = True
game_scene = 'Main menu'
player_turn = 1
grid_created = False
grid_rectangles_list = []
player_1_battleship = []
player_2_battleship = []
player_1_hits = []
player_2_hits = []
player_1_battleship_color = (255, 0, 0)
player_2_battleship_color = (0, 255, 0)
players_same_color = False
valid_done = True
valid_tile_selection = True
custom_tiles_positioning = False
grid_column_size = 7
grid_line_size = 7
size_of_battleship = 4
game_winner = 0
show_own_battleship = False


# Изображения
pygame.display.set_caption("Battleships 1.0.1")
game_icon = pygame.image.load("Resources/Battleships_icon.jpg")
game_background = pygame.image.load("Resources/Battleships_background.png")
button = pygame.image.load("Resources/Battleships_default_button.png")
grid_rectangle = pygame.image.load("Resources/rectangle_transparent.png")


# Создание прямоугольников для кнопок меню
start_button_rect = button.get_rect()
back_button_rect = button.get_rect()
done_button_rect = button.get_rect()
reset_button_rect = button.get_rect()
start_button_rect.topleft = (320, 500) # указание координат верхнего левого угла прямоугольника
back_button_rect.topleft = (0, 0)
done_button_rect.topleft = (650, 430)
reset_button_rect.topleft = (650, 500)



battleship_color_red_button_player_1_rect = pygame.Rect(270, 150, 50, 50) # в скобках координаты x и y, ширина и высота прямоугольника
battleship_color_blue_button_player_1_rect = pygame.Rect(370, 150, 50, 50)
battleship_color_green_button_player_1_rect = pygame.Rect(470, 150, 50, 50)
battleship_color_red_button_player_2_rect = pygame.Rect(270, 350, 50, 50)
battleship_color_blue_button_player_2_rect = pygame.Rect(370, 350, 50, 50)
battleship_color_green_button_player_2_rect = pygame.Rect(470, 350, 50, 50)


# Цвет кнопок меню
color_button1_player_1 = (255, 128, 128)
color_button2_player_1 = (0, 255, 0)
color_button3_player_1 = (0, 0, 255)
color_button1_player_2 = (255, 0, 0)
color_button2_player_2 = (128, 255, 128)
color_button3_player_2 = (0, 0, 255)


# Шрифты, цвета меню и кнопок
big_font = pygame.font.SysFont('roboto', 70)
small_font = pygame.font.SysFont('roboto', 25)

player_1_text = big_font.render('Player 1', True, (255, 255, 255))
player_2_text = big_font.render('Player 2', True, (255, 255, 255))
choose_battleship_color_text = small_font.render('Выбери цвет своего корабля', True, (255, 255, 255)) # Написание инструкции сверху от поля(белого цвета)
same_players_color_text = small_font.render('Игроки должны выбрать разные цвета для своих кораблей!', True,
                                            (255, 0, 0))
start_button_text = small_font.render('Начало игры', True, (255, 255, 255))


# Сцена выбора кораблей начала игры
player_1_turn_text = big_font.render('Ход первого игрока', True, (255, 255, 255))
player_2_turn_text = big_font.render('Ход второго игрока', True, (255, 255, 255))
instructions1_text = small_font.render('Инструкции:  ' + str(size_of_battleship) + ' Поставьте корабль на поле с помощью лкм'

                                                                                    , True,
                                       (255, 255, 255))
instructions2_text = small_font.render(
    'Нажмите лкм, чтобы выбрать место. Если захотите сменить выбор - нажмите reset.',
    True, (255, 255, 255))
instructions3_text = small_font.render('Нажмите лкм, чтобы атаковать поле противника. '
                                       '', True, (255, 255, 255))
instructions4_text = small_font.render('Если вы попадете, линкор противника откроется, если же нет '
                                       'клетка станет белой', True, (255, 255, 255))
instructions5_text = small_font.render(' Не волнуйтесь, ваш корабль неуязвим, если вы попали в него по ошибке.',
                                       True, (255, 255, 255))
back_button_text = small_font.render('Back', True, (255, 255, 255))
done_button_text = small_font.render('Done', True, (255, 255, 255))
reset_button_text = small_font.render('Reset', True, (255, 255, 255))
invalid_done_text = small_font.render('',
                                      True, (255, 0, 0))
game_over_text = big_font.render('Игра закончена!', True, (255, 255, 255))
game_winner_text = []



pygame.display.set_icon(game_icon) # назначение иконки игры, ссылаясь на константу с изображением сверху


# Функции
def create_grid():
    global grid_rectangles_list # назначение глобальной переменной
    grid_rectangle_element = grid_rectangle.get_rect()
    grid_rectangle_element.topleft = (80, 150)
    grid_rectangles_list.append(grid_rectangle_element)
    for i in range(0, grid_line_size):
        if i == 0:
            for j in range(1, grid_column_size): # отрисовка поля 7x7 через цикл
                grid_rectangle_new_element = grid_rectangle.get_rect()
                grid_rectangle_new_element.topleft = grid_rectangles_list[j - 1].topright
                grid_rectangles_list.append(grid_rectangle_new_element)
        else:
            for j in range(0, grid_column_size):
                grid_rectangle_new_element = grid_rectangle.get_rect()
                grid_rectangle_new_element.topleft = grid_rectangles_list[grid_line_size * (i - 1) + j].bottomleft
                grid_rectangles_list.append(grid_rectangle_new_element)


def draw_grid():
    global grid_rectangles_list
    global grid_created
    if not grid_created:
        create_grid()
        grid_created = True
    else:
        for grid_element in grid_rectangles_list:
            window.blit(grid_rectangle, grid_element)


def is_game_over(): # проверка на победителя и сцена окончания игры
    global game_winner, game_winner_text
    if player_turn == 1:
        for rect in player_1_battleship:
            if rect not in player_2_hits:
                return False
        game_winner = 2
    elif player_turn == 2:
        for rect in player_2_battleship:
            if rect not in player_1_hits:
                return False
        game_winner = 1
    game_winner_text = small_font.render('Игрок ' + str(game_winner) + ' Победил. Нажмите back, чтобы '
                                                                        'сыграть снова', True, (255, 255, 255))
    return True


def check_is_tile_selection_valid(player_number, element_to_check):
    if not custom_tiles_positioning:
        if player_number == 1:
            if len(player_1_battleship) == 1:
                for rect in player_1_battleship:
                    if rect.x == element_to_check.x and (
                            rect.y + 60 == element_to_check.y or rect.y - 60 == element_to_check.y):
                        return True
                    if rect.y == element_to_check.y and (
                            rect.x + 80 == element_to_check.x or rect.x - 80 == element_to_check.x):
                        return True
                return False
            elif len(player_1_battleship) > 1:
                is_vertical = False
                is_horizontal = False
                if element_to_check.x == player_1_battleship[0].x and element_to_check.x == player_1_battleship[1].x:
                    is_vertical = True
                    is_horizontal = False
                elif element_to_check.y == player_1_battleship[0].y and element_to_check.y == player_1_battleship[1].y:
                    is_vertical = False
                    is_horizontal = True
                for rect in player_1_battleship:
                    if is_vertical:
                        if rect.y + 60 == element_to_check.y or rect.y - 60 == element_to_check.y:
                            return True
                    elif is_horizontal:
                        if rect.x + 80 == element_to_check.x or rect.x - 80 == element_to_check.x:
                            return True
                return False

        elif player_number == 2:
            if len(player_2_battleship) == 1:
                for rect in player_2_battleship:
                    if rect.x == element_to_check.x and (
                            rect.y + 60 == element_to_check.y or rect.y - 60 == element_to_check.y):
                        return True
                    if rect.y == element_to_check.y and (
                            rect.x + 80 == element_to_check.x or rect.x - 80 == element_to_check.x):
                        return True
                return False
            elif len(player_2_battleship) > 1:
                is_vertical = False
                is_horizontal = False
                if element_to_check.x == player_2_battleship[0].x and element_to_check.x == player_2_battleship[1].x:
                    is_vertical = True
                    is_horizontal = False
                elif element_to_check.y == player_2_battleship[0].y and element_to_check.y == player_2_battleship[1].y:
                    is_vertical = False
                    is_horizontal = True
                for rect in player_2_battleship:
                    if is_vertical:
                        if rect.y + 60 == element_to_check.y or rect.y - 60 == element_to_check.y:
                            return True
                    elif is_horizontal:
                        if rect.x + 80 == element_to_check.x or rect.x - 80 == element_to_check.x:
                            return True
                return False
    else:
        if player_number == 1:
            for rect in player_1_battleship:
                if rect.x == element_to_check.x and (
                        rect.y + 60 == element_to_check.y or rect.y - 60 == element_to_check.y):
                    return True
                if rect.y == element_to_check.y and (
                        rect.x + 80 == element_to_check.x or rect.x - 80 == element_to_check.x):
                    return True
            return False
        elif player_number == 2:
            for rect in player_2_battleship:
                if rect.x == element_to_check.x and (
                        rect.y + 60 == element_to_check.y or rect.y - 60 == element_to_check.y):
                    return True
                if rect.y == element_to_check.y and (
                        rect.x + 80 == element_to_check.x or rect.x - 80 == element_to_check.x):
                    return True
            return False


def draw_main_menu_scene():
    window.blit(player_1_text, (300, 50))
    window.blit(player_2_text, (300, 250))
    window.blit(button, start_button_rect)
    window.blit(start_button_text, (345, 520))
    window.blit(choose_battleship_color_text, (275, 110))
    window.blit(choose_battleship_color_text, (275, 310))
    if players_same_color:
        window.blit(same_players_color_text, (150, 570))

    pygame.draw.rect(window, color_button1_player_1, battleship_color_red_button_player_1_rect)
    pygame.draw.rect(window, color_button2_player_1, battleship_color_green_button_player_1_rect)
    pygame.draw.rect(window, color_button3_player_1, battleship_color_blue_button_player_1_rect)
    pygame.draw.rect(window, color_button1_player_2, battleship_color_red_button_player_2_rect)
    pygame.draw.rect(window, color_button2_player_2, battleship_color_green_button_player_2_rect)
    pygame.draw.rect(window, color_button3_player_2, battleship_color_blue_button_player_2_rect)


def draw_choosing_battleships_scene():
    draw_grid()
    window.blit(instructions1_text, (50, 100))
    window.blit(instructions2_text, (50, 120))
    window.blit(button, back_button_rect)
    window.blit(button, done_button_rect)
    window.blit(button, reset_button_rect)
    window.blit(back_button_text, (50, 20))
    window.blit(done_button_text, (700, 450))
    window.blit(reset_button_text, (700, 520))
    if player_turn == 1:
        window.blit(player_1_turn_text, (250, 30))
        for rect in player_1_battleship:
            battleship_tile = pygame.Rect(rect.x + 20, rect.y + 10, 40, 40)
            pygame.draw.rect(window, player_1_battleship_color, battleship_tile)
    elif player_turn == 2:
        window.blit(player_2_turn_text, (250, 30))
        for rect in player_2_battleship:
            battleship_tile = pygame.Rect(rect.x + 20, rect.y + 10, 40, 40)
            pygame.draw.rect(window, player_2_battleship_color, battleship_tile)
    if not valid_done:
        window.blit(invalid_done_text, (200, 580))


def draw_game_started_scene():
    draw_grid()
    game_over = is_game_over()
    window.blit(button, back_button_rect)
    window.blit(back_button_text, (50, 20))
    if not game_over:
        window.blit(instructions3_text, (50, 80))
        window.blit(instructions4_text, (50, 100))
        window.blit(instructions5_text, (50, 120))
        if player_turn == 1:
            window.blit(player_1_turn_text, (250, 30))
            if show_own_battleship:
                for rect in player_1_battleship:
                    if rect in player_1_hits and rect not in player_2_battleship:
                        player_1_hits.remove(rect)
                    if rect not in player_1_hits:
                        battleship_tile = pygame.Rect(rect.x + 20, rect.y + 10, 40, 40)
                        pygame.draw.rect(window, player_1_battleship_color, battleship_tile)
                for rect in player_1_hits:
                    if rect in player_2_battleship:
                        if rect not in player_1_battleship:
                            battleship_tile = pygame.Rect(rect.x + 20, rect.y + 10, 40, 40)
                            pygame.draw.rect(window, player_2_battleship_color, battleship_tile)
                        else:
                            battleship2_tile = pygame.Rect(rect.x + 10, rect.y + 15, 30, 30)
                            pygame.draw.rect(window, player_2_battleship_color, battleship2_tile)
                            battleship1_tile = pygame.Rect(rect.x + 45, rect.y + 15, 30, 30)
                            pygame.draw.rect(window, player_1_battleship_color, battleship1_tile)
                    if rect not in player_2_battleship:
                        if rect not in player_1_battleship:
                            battleship_tile = pygame.Rect(rect.x + 20, rect.y + 10, 40, 40)
                            pygame.draw.rect(window, (255, 255, 255), battleship_tile)
            elif not show_own_battleship:
                for rect in player_1_hits:
                    if rect in player_2_battleship:
                        battleship_tile = pygame.Rect(rect.x + 20, rect.y + 10, 40, 40)
                        pygame.draw.rect(window, player_2_battleship_color, battleship_tile)
                    else:
                        battleship_tile = pygame.Rect(rect.x + 20, rect.y + 10, 40, 40)
                        pygame.draw.rect(window, (255, 255, 255), battleship_tile)
        elif player_turn == 2:
            window.blit(player_2_turn_text, (250, 30))
            if show_own_battleship:
                for rect in player_2_battleship:
                    if rect in player_2_hits and rect not in player_1_battleship:
                        player_2_hits.remove(rect)
                    if rect not in player_2_hits:
                        battleship_tile = pygame.Rect(rect.x + 20, rect.y + 10, 40, 40)
                        pygame.draw.rect(window, player_2_battleship_color, battleship_tile)

                for rect in player_2_hits:
                    if rect in player_1_battleship:
                        if rect not in player_2_battleship:
                            battleship_tile = pygame.Rect(rect.x + 20, rect.y + 10, 40, 40)
                            pygame.draw.rect(window, player_1_battleship_color, battleship_tile)
                        else:
                            battleship1_tile = pygame.Rect(rect.x + 10, rect.y + 15, 30, 30)
                            pygame.draw.rect(window, player_1_battleship_color, battleship1_tile)
                            battleship2_tile = pygame.Rect(rect.x + 45, rect.y + 15, 30, 30)
                            pygame.draw.rect(window, player_2_battleship_color, battleship2_tile)
                    if rect not in player_1_battleship:
                        if rect not in player_2_battleship:
                            battleship_tile = pygame.Rect(rect.x + 20, rect.y + 10, 40, 40)
                            pygame.draw.rect(window, (255, 255, 255), battleship_tile)
            elif not show_own_battleship:
                for rect in player_2_hits:
                    if rect in player_1_battleship:
                        battleship_tile = pygame.Rect(rect.x + 20, rect.y + 10, 40, 40)
                        pygame.draw.rect(window, player_1_battleship_color, battleship_tile)
                    else:
                        battleship_tile = pygame.Rect(rect.x + 20, rect.y + 10, 40, 40)
                        pygame.draw.rect(window, (255, 255, 255), battleship_tile)
    elif game_over:
        window.blit(game_over_text, (250, 30))
        window.blit(game_winner_text, (150, 100))
        for rect in player_1_battleship:
            if rect not in player_2_battleship:
                battleship_tile = pygame.Rect(rect.x + 20, rect.y + 10, 40, 40)
                pygame.draw.rect(window, player_1_battleship_color, battleship_tile)
            else:
                battleship1_tile = pygame.Rect(rect.x + 10, rect.y + 15, 30, 30)
                pygame.draw.rect(window, player_1_battleship_color, battleship1_tile)
                battleship2_tile = pygame.Rect(rect.x + 45, rect.y + 15, 30, 30)
                pygame.draw.rect(window, player_2_battleship_color, battleship2_tile)
        for rect in player_2_battleship:
            if rect not in player_1_battleship:
                battleship_tile = pygame.Rect(rect.x + 20, rect.y + 10, 40, 40)
                pygame.draw.rect(window, player_2_battleship_color, battleship_tile)


# Игровой цикл
while game_running:
    window.fill((0, 0, 0))
    window.blit(game_background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if game_scene == 'Main menu':
                players_same_color = False
                if start_button_rect.collidepoint(x, y):
                    if player_1_battleship_color == player_2_battleship_color:
                        players_same_color = True
                    else:
                        player_turn = 1
                        game_scene = 'Choosing battleships'
                        players_same_color = False
                if battleship_color_red_button_player_1_rect.collidepoint(x, y):
                    player_1_battleship_color = (255, 0, 0)
                    color_button1_player_1 = (255, 128, 128)
                    color_button2_player_1 = (0, 255, 0)
                    color_button3_player_1 = (0, 0, 255)
                if battleship_color_green_button_player_1_rect.collidepoint(x, y):
                    player_1_battleship_color = (0, 255, 0)
                    color_button1_player_1 = (255, 0, 0)
                    color_button2_player_1 = (128, 255, 128)
                    color_button3_player_1 = (0, 0, 255)
                if battleship_color_blue_button_player_1_rect.collidepoint(x, y):
                    player_1_battleship_color = (0, 0, 255)
                    color_button1_player_1 = (255, 0, 0)
                    color_button2_player_1 = (0, 255, 0)
                    color_button3_player_1 = (128, 128, 255)
                if battleship_color_red_button_player_2_rect.collidepoint(x, y):
                    player_2_battleship_color = (255, 0, 0)
                    color_button1_player_2 = (255, 128, 128)
                    color_button2_player_2 = (0, 255, 0)
                    color_button3_player_2 = (0, 0, 255)
                if battleship_color_green_button_player_2_rect.collidepoint(x, y):
                    player_2_battleship_color = (0, 255, 0)
                    color_button1_player_2 = (255, 0, 0)
                    color_button2_player_2 = (128, 255, 128)
                    color_button3_player_2 = (0, 0, 255)
                if battleship_color_blue_button_player_2_rect.collidepoint(x, y):
                    player_2_battleship_color = (0, 0, 255)
                    color_button1_player_2 = (255, 0, 0)
                    color_button2_player_2 = (0, 255, 0)
                    color_button3_player_2 = (128, 128, 255)
            elif game_scene == 'Choosing battleships':
                if back_button_rect.collidepoint(x, y):
                    game_scene = 'Main menu'
                    player_1_battleship = []
                    player_2_battleship = []
                elif done_button_rect.collidepoint(x, y):
                    if player_turn == 1:
                        if len(player_1_battleship) == size_of_battleship:
                            player_turn = 2
                            valid_done = True
                        else:
                            valid_done = False
                    elif player_turn == 2:
                        if len(player_2_battleship) == size_of_battleship:
                            game_scene = 'Game Started'
                            player_turn = 1
                            valid_done = True
                        else:
                            valid_done = False
                elif reset_button_rect.collidepoint(x, y):
                    if player_turn == 1:
                        player_1_battleship = []
                    elif player_turn == 2:
                        player_2_battleship = []
                else:
                    for element in grid_rectangles_list:
                        if element.collidepoint(x, y):
                            valid_tile_selection = True
                            if player_turn == 1:
                                if element not in player_1_battleship:
                                    if size_of_battleship > len(player_1_battleship) > 0:
                                        if check_is_tile_selection_valid(1, element):
                                            player_1_battleship.append(element)
                                        else:
                                            valid_tile_selection = False
                                    elif len(player_1_battleship) == 0:
                                        player_1_battleship.append(element)

                            elif player_turn == 2:
                                if element not in player_2_battleship:
                                    if size_of_battleship > len(player_2_battleship) > 0:
                                        if check_is_tile_selection_valid(2, element):
                                            player_2_battleship.append(element)
                                        else:
                                            valid_tile_selection = False
                                    elif len(player_2_battleship) == 0:
                                        player_2_battleship.append(element)
                        valid_done = True
            elif game_scene == 'Game Started':
                if back_button_rect.collidepoint(x, y):
                    game_scene = 'Main menu'
                    game_winner = 0
                    player_1_battleship = []
                    player_2_battleship = []
                    player_1_hits = []
                    player_2_hits = []
                else:
                    for element in grid_rectangles_list:
                        if not is_game_over():
                            if element.collidepoint(x, y):
                                if player_turn == 1:
                                    player_1_hits.append(element)
                                    player_turn = 2
                                elif player_turn == 2:
                                    player_2_hits.append(element)
                                    player_turn = 1

    if game_scene == 'Main menu':
        draw_main_menu_scene()
    if game_scene == 'Choosing battleships':
        draw_choosing_battleships_scene()
    if game_scene == 'Game Started':
        draw_game_started_scene()
    pygame.display.update()

