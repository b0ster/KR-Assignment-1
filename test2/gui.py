import tkinter as tk

from tkinter import messagebox as msg
from . import style
from . import helpers
from time import sleep, perf_counter


class Sudoku:
  def __init__(self):
    self.window = tk.Tk()
    self.window.title("Sudoku Solver")
    self.window.protocol("WM_DELETE_WINDOW", self.kill_window)
    self.window.geometry("550x610")
    self.window.resizable(False, False)
    self.elapsed_time = 0
    self.is_operating = True
    self.level = "easy"
    self.text_ids = [[0]*9 for _ in range(9)]
    
    menubar = tk.Menu(self.window)
    level = tk.Menu(menubar, tearoff=0)
    level.add_command(label="Easy", command=self.easy)
    level.add_command(label="Difficult", command=self.difficult)
    menubar.add_cascade(label="Level", menu=level)
    self.window.config(menu=menubar)

    # canvas
    self.canvas = tk.Canvas(self.window, **style.canvas)
    self.canvas.pack(side=tk.TOP, fill=tk.BOTH)
    self.canvas.update()
    self.width = self.canvas.winfo_width()
    self.height = self.canvas.winfo_height()
    self.step_x, self.step_y = self.width/9, self.height/9

    frame = tk.Frame(self.window, bg="#f4f4f4")
    frame.pack(side=tk.TOP)
    
    self.generate_button = tk.Button(frame, text="Generate", command=self.generate, **style.btn)
    self.generate_button.grid(ipadx=15, pady=6, row=0, column=0)
    self.button_hover(self.generate_button)
    
    self.run_button = tk.Button(frame, text="Solve", command=self.solve, **style.btn)
    self.run_button.grid(ipadx=15, padx=30, pady=6, row=0, column=1)
    self.button_hover(self.run_button)
    
    self.reset_button = tk.Button(frame, text="Reset", command=self.reset, **style.btn)
    self.reset_button.grid(ipadx=15, pady=6, row=0, column=2)
    self.button_hover(self.reset_button)
    
    var = tk.DoubleVar()
    self.speed = tk.Scale(frame, variable=var, **style.scale)
    self.speed.grid(ipadx=80, row=1, column=0, columnspan=2)
    self.speed.set(50)

    tk.Label(frame, text="Runtime:", font="Arial 13").grid(row=1, column=2)
    self.runtime = tk.Label(frame, text='00:00', font="Arial 13")
    self.runtime.grid(row=1, column=3)
    
    
    self.draw_lines()
    self.board = helpers.generate_board()
    self.write_given_numbers()

    self.window.mainloop()

  def kill_window(self):
    self.window.destroy()
    
  def on_enter(self, event, btn):
    btn['background'] = '#333333'

  def on_leave(self, event, btn):
    btn['background'] = '#444444'
  
  def button_hover(self, button):
    button.bind("<Enter>", lambda event, btn=button: self.on_enter(event, btn))
    button.bind("<Leave>", lambda event, btn=button: self.on_leave(event, btn))
    
  def easy(self):
    self.level = "easy"
    self.generate()
    
  def difficult(self):
    self.level = "difficult"
    self.generate()
    
  def draw_lines(self):
    # draw x lines
    y = self.step_y
    while y <= self.height:
      x = 0
      thic = (round(y/self.step_y) % 3 == 0) and 3 or 1
      while x <= self.width:
        self.canvas.create_line(x, y, x+3.5, y, width=thic)
        self.canvas.update()
        x += 3.5
      y += self.step_y
    
    # draw y lines
    x = self.step_x
    while x <= self.width:
      y = 0
      thic = (round(x/self.step_x) % 3 == 0) and 3 or 1
      while y <= self.height:
        self.canvas.create_line(x, y, x, y+3.5, width=thic)
        self.canvas.update()
        y += 3.5
      x += self.step_x
  
  def write_given_numbers(self):
    y = self.step_y/2
    while y < self.height:
      x = self.step_x/2
      while x < self.width:
        r, c = round((y-self.step_y/2)/self.step_y), round((x-self.step_x/2)/self.step_x)
        number = self.board[r][c] or ''
        self.text_ids[r][c] = self.canvas.create_text(x, y, text=str(number), **style.numbers)
        sleep(0.05)
        self.canvas.update()
        x += self.step_x
      y += self.step_y
    self.is_operating = False
    
  def solve(self):
    if not(self.is_operating or helpers.is_empty(self.board)):
      start = perf_counter()
      self.elapsed_time = 0
      
      self.is_operating = True
      def _recursive():
        self.elapsed_time = int(perf_counter() - start)
        self.runtime['text'] = f'{self.elapsed_time//60:02d}:{self.elapsed_time%60:02d}'
        pos = helpers.find_empty(self.board)
        if not pos:
          return True
        else:
          row, col = pos
        
        for num in range(1, 10):
          if helpers.is_valid(self.board, num, pos):
            self.board[row][col] = num
            self.canvas.itemconfigure(self.text_ids[row][col], text=str(num))
            sleep(10 / self.speed.get())
            self.canvas.update()

            if _recursive():
              return True
            
            self.board[row][col] = 0
            self.canvas.itemconfigure(self.text_ids[row][col], text='')
            sleep(10 / self.speed.get())
            self.canvas.update()
        return False
      _recursive()
      self.is_operating = False
    elif helpers.is_empty(self.board):
      msg.showerror("Empty Box", "Please generate a board")
    
  def reset(self):
    if not(self.is_operating or helpers.is_empty(self.board)):
      self.is_operating = True
      self.elapsed_time = 0
      self.runtime['text'] = '00:00'
      self.board = [[0]*9 for _ in range(9)]
      for r in range(9):
        for c in range(9):
          self.canvas.itemconfigure(self.text_ids[r][c], text='')
          sleep(0.02)
          self.canvas.update()
      self.is_operating = False
  
  
  def generate(self):
    if not self.is_operating:
      self.reset()
      self.is_operating = True
      self.board = helpers.generate_board(level=self.level)
      self.write_given_numbers()