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
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=None, body_color=None) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объекта. Должен быть переопределён в наследниках."""
        raise NotImplementedError(
            'Method must be implemented in subclass'
        )


class Apple(GameObject):
    """Класс яблока.
    Отвечает за генерацию и отрисовку яблока.
    """

    def __init__(self) -> None:
        position = self.randomize_position()
        super().__init__(position, APPLE_COLOR)

    def randomize_position(self):
        """Возвращает случайную позицию яблока."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return x, y

    def respawn(self, snake_position):
        """Перемещает яблоко в новое случайное место, исключая координаты змейки."""
        while True:
            new_pos = self.randomize_position()
            if new_pos not in snake_position:
                self.position = new_pos
                break

    def draw(self):
        """Метод отрисовки яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс змейки.
    Отвечает за хранение позиций тела, обработку движения и столкновений.
    """

    def __init__(self, next_direction=None) -> None:
        super().__init__(body_color=SNAKE_COLOR)
        # По тз требуется именно поле positionS.
        # Смысла дублировать positions в super.position не вижу.
        self.positions = [BOARD_CENTER]
        self.length = BASE_SNAKE_LENGTH
        self.direction = RIGHT
        self.next_direction = next_direction

    def draw(self):
        """Метод отрисовки змейки."""
        for pos in self.positions:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def move(self):
        """Перемещает змейку в текущем направлении."""
        x, y = self.get_head_position()
        x = (x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        y = (y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT

        if (x, y) in self.positions:
            self.reset()
            return

        self.positions.insert(0, (x, y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def update_direction(self):
        """Применяет новое направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние после столкновения."""
        self.length = BASE_SNAKE_LENGTH
        self.positions = [BOARD_CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
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
    """Основной цикл игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.respawn(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
