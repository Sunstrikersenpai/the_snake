from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

BOARD_CENTER = (
    (SCREEN_WIDTH // GRID_SIZE // 2) * GRID_SIZE,
    (SCREEN_HEIGHT // GRID_SIZE // 2) * GRID_SIZE,
)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)
BASE_SNAKE_LENGTH = 1

# Скорость движения змейки:
SPEED = 7

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    def __init__(self, position, body_color) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):
    def __init__(self) -> None:
        position = self._randomize_position()
        super().__init__(position, APPLE_COLOR)

    def _randomize_position(self):
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (x, y)

    def respawn(self):
        self.position = self._randomize_position()

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self, next_direction=None) -> None:
        super().__init__(position=BOARD_CENTER, body_color=SNAKE_COLOR)
        self.position = [self.position]
        self.length = BASE_SNAKE_LENGTH
        self.last = None
        self.direction = RIGHT
        self.next_direction = next_direction

    def draw(self):
        for position in self.position:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        x, y = self.get_head_position()
        x = (x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        y = (y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        if (x,y) in self.position:
            self.reset()
            return
        self.position.insert(0, (x, y))
        if len(self.position) > self.length:
            self.last = self.position[len(self.position) - 1]
            self.position.pop()

    def get_head_position(self):
        return self.position[0]

    def reset(self):
        self.length = BASE_SNAKE_LENGTH
        self.position = [BOARD_CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


# Функция обработки действий пользователя
def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # 1. Обработка ввода
        handle_keys(snake)

        # 2. Обновление направления
        snake.update_direction()

        # 3. Движение змейки
        snake.move()

        # 4. Проверка — съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            
            print("HEAD:", snake.get_head_position())
            print("APPLE:", apple.position)
            print("LENGTH:", snake.length)
            print("SEGMENTS:", len(snake.position))
            snake.length += 1
            apple.respawn()
            print("HEAD:", snake.get_head_position())
            print("APPLE:", apple.position)
            print("LENGTH:", snake.length)
            print("SEGMENTS:", len(snake.position))

        # 5. Перерисовка поля
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
    

        # 6. Обновление окна
        pygame.display.update()


if __name__ == "__main__":
    main()
