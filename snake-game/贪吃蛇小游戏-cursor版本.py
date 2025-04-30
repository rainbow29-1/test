import tkinter as tk
import random

class Snake:
    def __init__(self, color, initial_pos, control_keys):
        self.body = [initial_pos]
        self.direction = "Right"
        self.color = color
        self.control_keys = control_keys
        self.score = 0
        self.growing = False

    def move(self):
        moves = {"Right": [20, 0], "Left": [-20, 0], "Up": [0, -20], "Down": [0, 20]}
        head = [self.body[0][0] + moves[self.direction][0], self.body[0][1] + moves[self.direction][1]]
        self.body.insert(0, head)
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def check_collision(self, other_snake):
        head = self.body[0]
        return (not (0 <= head[0] < 400 and 0 <= head[1] < 400) or
                head in self.body[1:] or
                head in other_snake.body)

    def change_direction(self, new_dir):
        opposite_dirs = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
        if opposite_dirs.get(new_dir) != self.direction:
            self.direction = new_dir

    def reset(self, initial_pos):
        self.body = [initial_pos]
        self.direction = "Right"
        self.score = 0
        self.growing = False

class Game:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("双人贪吃蛇")
        self.window.resizable(False, False)
        
        self.canvas = tk.Canvas(self.window, width=400, height=400, bg="black")
        self.canvas.pack()
        
        self.snake1 = Snake("#4CAF50", [100, 100], {"Left": "Left", "Right": "Right", "Up": "Up", "Down": "Down"})
        self.snake2 = Snake("#FF5722", [300, 300], {"Left": "a", "Right": "d", "Up": "w", "Down": "s"})
        
        self.food_pos = [0, 0]
        self.game_paused = False
        self.game_active = True
        
        self.generate_food()
        self.window.bind("<Key>", self.on_key_press)
        self.update()
        self.window.mainloop()

    def generate_food(self):
        while True:
            x = random.randrange(20, 360, 20)
            y = random.randrange(20, 360, 20)
            self.food_pos = [x, y]
            if self.food_pos not in self.snake1.body and self.food_pos not in self.snake2.body:
                break

    def game_over(self):
        self.game_active = False
        self.canvas.create_text(200, 180, text="游戏结束!", fill="white", font=("Arial", 24))
        self.canvas.create_text(200, 220, text="按空格键重新开始", fill="white", font=("Arial", 16))

    def reset_game(self):
        self.game_active = True
        self.game_paused = False
        self.snake1.reset([100, 100])
        self.snake2.reset([300, 300])
        self.generate_food()

    def toggle_pause(self):
        self.game_paused = not self.game_paused

    def on_key_press(self, event):
        if event.keysym == "space":
            if not self.game_active:
                self.reset_game()
            else:
                self.toggle_pause()
            return
            
        if not self.game_active or self.game_paused:
            return
            
        for snake in [self.snake1, self.snake2]:
            if event.keysym in snake.control_keys.values():
                new_direction = [k for k, v in snake.control_keys.items() if v == event.keysym][0]
                snake.change_direction(new_direction)

    def update(self):
        if not self.game_active or self.game_paused:
            self.window.after(100, self.update)
            return
            
        for snake in [self.snake1, self.snake2]:
            snake.move()
            
        if self.snake1.check_collision(self.snake2) or self.snake2.check_collision(self.snake1):
            self.game_over()
            self.window.after(100, self.update)
            return
        
        for snake in [self.snake1, self.snake2]:
            if snake.body[0] == self.food_pos:
                snake.growing = True
                snake.score += 1
                self.generate_food()
        
        self.canvas.delete("all")
        
        for snake, score_pos in [(self.snake1, 50), (self.snake2, 350)]:
            for segment in snake.body:
                self.canvas.create_rectangle(segment[0], segment[1],
                                          segment[0] + 20, segment[1] + 20,
                                          fill=snake.color)
            self.canvas.create_text(score_pos, 10, text=f"蛇{1 if snake==self.snake1 else 2}得分: {snake.score}", fill="white")
        
        self.canvas.create_oval(self.food_pos[0], self.food_pos[1],
                              self.food_pos[0] + 20, self.food_pos[1] + 20,
                              fill="red")
        
        if self.game_paused:
            self.canvas.create_text(200, 200, text="游戏暂停", fill="white", font=("Arial", 24))
        
        self.window.after(100, self.update)

if __name__ == "__main__":
    Game()
