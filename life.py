import os
import shutil
import random
import time

class LifeSandbox:
    def __init__(self):
        # Автоматически подстраиваемся под размер окна
        self.width, self.height = shutil.get_terminal_size((80, 24))
        self.height -= 3 # Запас для меню подвала
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.generation = 0
        
    def clear_screen(self):
        # Жесткая очистка, которая сбрасывает буфер прокрутки
        os.system('cls' if os.name == 'nt' else 'clear')

    def randomize(self):
        self.grid = [[1 if random.random() < 0.18 else 0 for _ in range(self.width)] for _ in range(self.height)]
        self.generation = 0

    def update_generation(self):
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                neighbors = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dy == 0 and dx == 0: continue
                        neighbors += self.grid[(y + dy) % self.height][(x + dx) % self.width]
                
                if self.grid[y][x] == 1 and neighbors in [2, 3]:
                    new_grid[y][x] = 1
                elif self.grid[y][x] == 0 and neighbors == 3:
                    new_grid[y][x] = 1
        self.grid = new_grid
        self.generation += 1

    def render(self):
        # Собираем весь экран в одну строку, чтобы не спамить print() и не ломать прокрутку
        output = []
        for row in self.grid:
            output.append("".join("●" if cell else " " for cell in row))
        
        self.clear_screen()
        print("\n".join(output))
        print("=" * self.width)
        print(f" Поколение: {self.generation} | Enter — следующий шаг | 'auto' — запустить поток")
        print(" 'r' — перегенерировать хаос | 'exit' — выход")

if __name__ == "__main__":
    sandbox = LifeSandbox()
    sandbox.randomize()
    
    while True:
        sandbox.render()
        cmd = input(">> ").strip().lower()
        
        if cmd == "exit":
            break
        elif cmd == "r":
            sandbox.randomize()
        elif cmd == "auto":
            print("Запуск авто-симуляции... Нажмите Ctrl+C, чтобы остановить.")
            time.sleep(1)
            try:
                while True:
                    # Обновляем размеры, если окно растянули
                    sandbox.width, sandbox.height = shutil.get_terminal_size((80, 24))
                    sandbox.height -= 3
                    
                    sandbox.update_generation()
                    sandbox.render()
                    time.sleep(0.15) # Ограничиваем скорость, чтобы терминал не зависал
            except KeyboardInterrupt:
                pass # Спокойно возвращаемся в пошаговый режим
        else:
            # Если просто нажал Enter — идет один шаг эволюции
            sandbox.update_generation()