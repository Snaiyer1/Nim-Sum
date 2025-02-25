import pygame
import random
from functools import reduce

# initialize pygame
pygame.init()

# settings
WIDTH, HEIGHT = 500, 350
BACKGROUND_COLOR = (144, 238, 144)
PLAYER1_COLOR = (220, 20, 60)
PLAYER2_COLOR = (70, 130, 180)
MATCH_COLOR = (255, 240, 0)
BUTTON_COLOR = (139, 136, 248)
BUTTON_HOVER_COLOR = (80, 80, 235)
MATCH_RADIUS = 10
ROW_SPACING = 50
MATCH_SPACING = 30

piles = []
selected = []
player_turn = 1  # player 1 starts by default
computer_first = False  # computer goes first only if the button is clicked
game_over = False

# display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nim")
font = pygame.font.SysFont(None, 30)

# buttons
confirm_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 40, 100, 30)
restart_button = pygame.Rect(WIDTH - 110, 10, 100, 30)
computer_first_button = pygame.Rect(WIDTH - 110, 50, 100, 30)


def generate_piles():
    # random piles
    return [random.randint(1, 7) for _ in range(random.randint(3, 4))]


def draw_matches():
    # game state
    screen.fill(BACKGROUND_COLOR)

    # matches
    y_offset = 50
    for row, count in enumerate(piles):
        for i in range(count):
            x = WIDTH // 2 - (count * MATCH_SPACING // 2) + i * MATCH_SPACING
            y = y_offset + row * ROW_SPACING
            color = PLAYER1_COLOR if (row, i,
                                      1) in selected else PLAYER2_COLOR if (
                                          row, i,
                                          2) in selected else MATCH_COLOR
            pygame.draw.circle(screen, color, (x, y), MATCH_RADIUS, 3 if
                               (row, i, player_turn) in selected else 0)

    # display the player's turn
    if not game_over:
        turn_text = font.render(f"Player {player_turn}'s Turn", True,
                                (255, 255, 255))
    else:
        turn_text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(turn_text, (10, 10))

    # restart button
    pygame.draw.rect(screen, BUTTON_COLOR, restart_button)
    restart_text = font.render("Restart", True, (255, 255, 255))
    screen.blit(restart_text, restart_button.move(10, 5))

    # computer goes first button
    pygame.draw.rect(screen, BUTTON_COLOR, computer_first_button)
    computer_first_text = font.render("Player 2", True, (255, 255, 255))
    screen.blit(computer_first_text, computer_first_button.move(10, 5))

    # confirm choices button
    if selected and not game_over:
        mouse_pos = pygame.mouse.get_pos()
        button_color = BUTTON_HOVER_COLOR if confirm_button.collidepoint(
            mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, confirm_button)
        text = font.render("Confirm", True, (255, 255, 255))
        screen.blit(text, confirm_button.move(10, 5))

    pygame.display.flip()


def player_move():
    # remove matches from selected piles and switch turns
    global selected, piles, player_turn, game_over
    if selected and not game_over:
        row = selected[0][0]
        piles[row] -= len(selected)
        selected = []

        # check if game over
        if all(p == 0 for p in piles):
            show_message(f"Player {player_turn} Loses!")
            game_over = True
        else:
            player_turn = 3 - player_turn  #switch whose turn it is
        draw_matches()


def show_message(message):
    text = font.render(message, True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(2000)


def restart_game():
    # reset game without computer auto playing
    global piles, selected, player_turn, game_over
    piles = generate_piles()
    selected = []
    game_over = False
    player_turn = 1  # player 1 starts by default
    draw_matches()


def start_computer_first():
    # reset game and let the computer have the first move
    global computer_first, player_turn
    restart_game()
    computer_first = True
    player_turn = 2
    computer_move()


def get_nim_sum():
    # XOR sum of the piles
    return reduce(lambda x, y: x ^ y, piles, 0)


def get_optimal_move():
    # optimal strategy
    nim_sum = get_nim_sum()

    # when the nim sum is in the zero state, the player is in a losing position
    if nim_sum == 0:
        max_pile = max(piles)
        return piles.index(max_pile), 1

    # try to find move which leads to nim sum of zero
    for row, pile in enumerate(piles):
        target_pile = pile ^ nim_sum
        if target_pile < pile:
            return row, pile - target_pile  # reduce piles


def computer_move():
    global piles, player_turn, game_over
    if not game_over and player_turn == 2:
        row, count = get_optimal_move()
        piles[row] -= count
        if all(p == 0 for p in piles):
            show_message("Player 2 Wins!")
            game_over = True
        else:
            player_turn = 1
        draw_matches()


def match_clicked(x, y):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    distance = ((mouse_x - x)**2 + (mouse_y - y)**2)**0.5
    return distance <= MATCH_RADIUS


def game_loop():
    global selected, player_turn, computer_first, game_over
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_button.collidepoint(event.pos):
                    restart_game()
                    continue

                if computer_first_button.collidepoint(event.pos):
                    start_computer_first()
                    continue

                if selected and confirm_button.collidepoint(event.pos):
                    player_move()
                    continue

                x_offset = WIDTH // 2
                y_offset = 50
                for row, count in enumerate(piles):
                    for i in range(count):
                        x = x_offset - (count * MATCH_SPACING //
                                        2) + i * MATCH_SPACING
                        y = y_offset + row * ROW_SPACING
                        if match_clicked(x, y):
                            if (row, i, player_turn) in selected:
                                selected.remove((row, i, player_turn))
                            else:
                                if not selected or selected[0][0] == row:
                                    selected.append((row, i, player_turn))
                            draw_matches()

        if player_turn == 2 and not game_over:
            pygame.time.delay(500)
            computer_move()

        draw_matches()
        pygame.display.update()


restart_game()
game_loop()
pygame.quit()
