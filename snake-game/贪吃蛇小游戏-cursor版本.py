# ... existing code ...

class Snake:
    def __init__(self, color, initial_pos, control_keys):
        self.body = [initial_pos]
        self.direction = "Right"
        self.color = color
        self.control_keys = control_keys
        self.score = 0


    def move(self):
        moves = {
            "Right": [20, 0],
            "Left": [-20, 0],
            "Up": [0, -20],
            "Down
        }
        head = [self.body[0][0] + moves[self.direction][0],
                self.body[0][1] + moves[self.direction][1]]
        self.body.insert(0, head)
        self.body.pop()

    def check_collision(self, other_snake):
        head = self.body[0]
        # 检查墙壁碰撞
        if not (0 <= head[0] < 400 and 0 <= head[1] < 400):
            return True
        # 检查自身碰撞
        if head in self.body[1:]:
            return True
        # 检查与其他蛇碰撞
        if head in other_snake.body:
            return True
        return False

    def change_direction(self, new_dir):
        opposite_dirs = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
        if opposite_dirs.get(new_dir) != self.direction:
            self.direction = new_dir

# 创建两条蛇
snake1 = Snake("#4CAF50", [100, 50], {
    "Left": "Left", "Right": "Right", "Up": "Up", "Down": "Down"
})
snake2 = Snake("#FF5722", [300, 50], {
    "Left": "a", "Right": "d", "Up": "w", "Down": "s"
})

def on_key_press(event):
    for snake in [snake1, snake2]:
        if event.keysym in snake.control_keys.values():
            new_direction = [k for k, v in snake.control_keys.items() if v == event.keysym][0]
            snake.change_direction(new_direction)

def update():
    # 移动蛇
    for snake in [snake1, snake2]:
        snake.move()
        
    # 检查碰撞
    if snake1.check_collision(snake2) or snake2.check_collision(snake1):
        game_over()
        return
    
    # 检查食物
    for snake in [snake1, snake2]:
        if snake.body[0] == food_pos:
            snake.body.append(snake.body[-1])
            snake.score += 1
            generate_food()
    
    # 更新画布
    canvas.delete("all")
    
    # 绘制蛇和分数
    for snake, score_pos in [(snake1, 50), (snake2, 350)]:
        for segment in snake.body:
            canvas.create_rectangle(segment[0], segment[1],
                                  segment[0] + 20, segment[1] + 20,
                                  fill=snake.color)
        canvas.create_text(score_pos, 10, text=f"蛇{1 if snake==snake1 else 2}得分: {snake.score}", fill="white")
    
    # 绘制食物
    canvas.create_oval(food_pos[0], food_pos[1],
                      food_pos[0] + 20, food_pos[1] + 20,
                      fill="red")
    
    window.after(100, update)
# ... existing code ...
