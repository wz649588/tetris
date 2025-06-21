print("Welcome to Tetris!")
import pygame
from game import Game

CELL_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

def main():
    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = Game()

    # Center the board
    TOP_MARGIN = 40
    left_margin = (info.current_w - CELL_SIZE * BOARD_WIDTH) // 2

    move_down_counter = 0
    move_side_counter = 0
    side_delay = 7
    down_delay = 2
    base_auto_drop_delay = 25  # Initial delay (frames)
    min_auto_drop_delay = 3    # Fastest possible
    auto_drop_delay = base_auto_drop_delay
    auto_drop_counter = 0

    while game.is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    old_rotation = game.current_tetromino.rotation
                    game.current_tetromino.rotate()
                    if not game.can_move(0, 0):
                        game.current_tetromino.rotation = old_rotation
                elif event.key == pygame.K_q:
                    game.is_running = False

        keys = pygame.key.get_pressed()
        move_side_counter += 1
        move_down_counter += 1
        auto_drop_counter += 1

        if keys[pygame.K_LEFT] and move_side_counter >= side_delay:
            if game.can_move(0, -1):
                game.current_tetromino.move(0, -1)
            move_side_counter = 0
        elif keys[pygame.K_RIGHT] and move_side_counter >= side_delay:
            if game.can_move(0, 1):
                game.current_tetromino.move(0, 1)
            move_side_counter = 0

        # Soft drop (when holding down)
        if keys[pygame.K_DOWN] and move_down_counter >= down_delay:
            if game.can_move(1, 0):
                game.current_tetromino.move(1, 0)
            move_down_counter = 0

        # Automatic drop (gravity)
        if auto_drop_counter >= auto_drop_delay:
            if game.can_move(1, 0):
                game.current_tetromino.move(1, 0)
            else:
                game.place_tetromino()
            auto_drop_counter = 0

        # Update auto drop delay based on level
        auto_drop_delay = max(base_auto_drop_delay - (game.level - 1) * 4, min_auto_drop_delay)

        if game.flash_timer > 0:
            game.flash_timer -= 1

        draw_board(screen, game, left_margin, TOP_MARGIN)
        pygame.display.flip()
        clock.tick(15)  # FPS

    pygame.quit()

def draw_board(screen, game, left_margin, TOP_MARGIN):
    colors = {
        0: (30, 30, 30),   # Empty
        1: (100, 200, 255),# Placed
        2: (255, 200, 100) # Active
    }
    screen.fill((0, 0, 0))
    display = [row[:] for row in game.board.board]
    if game.current_tetromino:
        shape = game.current_tetromino.get_shape()
        x, y = game.current_tetromino.position
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    xi, yj = x + i, y + j
                    if 0 <= xi < game.board.height and 0 <= yj < game.board.width:
                        display[xi][yj] = 2
    for i, row in enumerate(display):
        for j, cell in enumerate(row):
            pygame.draw.rect(
                screen,
                colors[cell],
                (left_margin + j * CELL_SIZE, TOP_MARGIN + i * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
            )
    # Draw score above the board
    font = pygame.font.SysFont(None, 28)
    score_text = font.render(f"Score: {game.score}", True, (255, 255, 255))
    screen.blit(score_text, (left_margin, 10))

    # Draw level above the board
    level_text = font.render(f"Level: {game.level}", True, (255, 255, 255))
    screen.blit(level_text, (left_margin + 200, 10))

    # Draw next tetromino preview
    preview_x = left_margin + CELL_SIZE * game.board.width + 40
    preview_y = TOP_MARGIN + 40
    font_small = pygame.font.SysFont(None, 24)
    next_text = font_small.render("Next:", True, (255, 255, 255))
    screen.blit(next_text, (preview_x, preview_y - 30))
    next_shape = game.next_tetromino.get_shape()
    for i, row in enumerate(next_shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    (200, 255, 200),
                    (preview_x + j * CELL_SIZE, preview_y + i * CELL_SIZE, CELL_SIZE - 2, CELL_SIZE - 2)
                )
    # Flash effect for Tetris
    if getattr(game, "flash_timer", 0) > 0:
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((255, 255, 0, 80))  # Yellow transparent overlay
        screen.blit(overlay, (0, 0))

# Only run if this is the main script
if __name__ == "__main__":
    main()