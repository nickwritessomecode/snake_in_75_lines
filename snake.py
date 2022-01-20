import tkinter as tk
from collections import deque
import random

class Game:
    FIELD_SIZE = 17

    def __init__(self):
        self.snake = deque([(Game.FIELD_SIZE//2, Game.FIELD_SIZE//2 + x) for x in range(8)])
        self.space = [(r, c) for r in range(Game.FIELD_SIZE) for c in range(Game.FIELD_SIZE)]
        self.direction = (0, 0)
        self.moves = deque()
        self.apple_eaten = 0
        self.game_over = False
        self.reset_apple()
            
    def reset_apple(self):
        self.apple = random.choice(list(set(self.space) - set(self.snake)))
    
    def move(self, dr, dc):
        if self.game_over:
            self.__init__()
        elif (-dr, -dc) != self.direction:
            self.moves.append((dr, dc))

    def advance(self):
        if self.moves:
            self.direction = self.moves.popleft()            

        new_head = tuple(sum(x)%Game.FIELD_SIZE for x in zip(self.snake[-1], self.direction))
        
        if new_head not in self.snake:
            self.snake.append(new_head)
            if new_head == self.apple:
                self.apple_eaten += 1
                self.reset_apple()
            else:
                self.snake.popleft()
        elif new_head != self.snake[-1]:
            self.game_over = True

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.game = Game()
        self.create_widgets()
        self.update_clock()
    
    def update_clock(self):
        self.game.advance()
        self.update()
        self.master.after(80, self.update_clock)

    def create_widgets(self):
        CELL_SIZE = 55
        self.status_msg = tk.Entry(self, highlightthickness = 0, width=10, 
                                         font=("Courier", 36), bg='#578A34')
        self.status_msg.pack(side="top", fill='x')
        
        self.canvas = tk.Canvas(self, height=CELL_SIZE*self.game.FIELD_SIZE, 
                                      width=CELL_SIZE*self.game.FIELD_SIZE)
        self.canvas.bind('<Up>', lambda _: self.game.move(-1, 0))
        self.canvas.bind('<Left>', lambda _: self.game.move(0, -1))
        self.canvas.bind('<Down>', lambda _: self.game.move(1, 0))
        self.canvas.bind('<Right>', lambda _: self.game.move(0, 1))
        self.canvas.focus_set()
        self.canvas.pack()
        self.rectangles = {(r, c): 
            self.canvas.create_rectangle(c*CELL_SIZE, r*CELL_SIZE, 
                    (c+1)*CELL_SIZE, (r+1)*CELL_SIZE, width=0)
                for r, c in self.game.space
        }

    def update(self):
        for r, c in self.game.space:
            fill_color = '#AAD751' if (r + c) % 2 == 0 else '#A2D149'
            if (r, c) in self.game.snake:
                fill_color = 'blue' if (r, c) == self.game.snake[-1] else '#426FE3'
            elif (r, c) == self.game.apple:
                fill_color = 'red'

            self.canvas.itemconfig(self.rectangles[(r, c)], fill=fill_color)
        
        self.status_msg.delete(0, tk.END)
        self.status_msg.insert(tk.END, "🍎:" + str(self.game.apple_eaten) + (" GAME OVER" if self.game.game_over else ""))

        
root = tk.Tk()
app = Application(master=root)
app.mainloop()
