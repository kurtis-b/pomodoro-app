from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
# WORK_SEC = 1500  # = 25 minutes
# SHORT_BREAK_SEC = 300  # = 5 minutes
# LONG_BREAK_SEC = 1200  # = 20 minutes
WORK_SEC = 3120  # = 52 minutes
SHORT_BREAK_SEC = 1020  # = 17 minutes
LONG_BREAK_SEC = 2496  # = 41.6 minutes
COUNT_INTERVAL = 1000  # = 1 second


class PomodoroApp(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        # Pomodoro technique has 9 reps:
        #   0,2,4,6 are 5 minutes of break
        #   1,3,5,7 are 25 minutes of work
        #   8 is a 20-minute break
        self.pomodoro_rep = 0

        # Create the widgets
        self.header_label = Label(text="Timer", foreground=GREEN, background=YELLOW, font=(FONT_NAME, 54, "bold"))
        self.canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
        self.tomato_img = PhotoImage(file="tomato.png")
        self.canvas.create_image(100, 112, image=self.tomato_img)
        self.timer_text = self.canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 36, "bold"))
        self.timer_start = Button(text="Start", command=self.on_start_clicked, font=(FONT_NAME, 9, "bold"))
        self.timer_reset = Button(text="Reset", command=self.on_reset_clicked, font=(FONT_NAME, 9, "bold"))
        self.check_label = Label(foreground=GREEN, background=YELLOW, font=(FONT_NAME, 18, "bold"))

        # Store the identifier for
        self.timer = self.after(0)

        # Set up the grids
        self.setup()

    def setup(self):
        self.grid()
        self.config(padx=50, pady=25, bg=YELLOW)
        self.header_label.grid(row=0, column=1, sticky='news')
        self.canvas.grid(row=1, column=1, sticky='news')
        self.timer_start.grid(row=2, column=0, sticky='news')
        self.timer_reset.grid(row=2, column=2, sticky='news')
        self.check_label.grid(row=3, column=1, sticky='news')

        # Have the grids scale based on the window size
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

    # ---------------------------- TIMER RESET ------------------------------- #
    def on_reset_clicked(self):
        self.after_cancel(self.timer)
        self.header_label.config(text="Timer", foreground=GREEN)
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.check_label.config(text='')
        self.pomodoro_rep = 0

    # ---------------------------- TIMER MECHANISM ------------------------------- #
    def on_start_clicked(self):
        self.pomodoro_rep += 1
        if self.pomodoro_rep == 8:
            self.header_label.config(text="Taking a Break", foreground=RED)
            self.pomodoro_rep = 0
            self.count_down(LONG_BREAK_SEC)
        elif self.pomodoro_rep % 2 == 0:
            self.header_label.config(text="Taking a Break", foreground=PINK)
            self.count_down(SHORT_BREAK_SEC)
        else:
            self.header_label.config(text="Working", foreground=GREEN)
            self.count_down(WORK_SEC)

    # ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
    def count_down(self, count):
        count_min = math.floor(count / 60)
        count_sec = count % 60
        if count_min < 10:
            count_min = f"0{count_min}"
        if count_sec < 10:
            count_sec = f"0{count_sec}"

        self.canvas.itemconfig(self.timer_text, text=f"{count_min}:{count_sec}")
        if count > 0:
            self.timer = self.after(COUNT_INTERVAL, self.count_down, count - 1)
        else:
            self.on_start_clicked()
            check_marks = ["✔" for _ in range(math.floor(self.pomodoro_rep / 2))]
            self.check_label.config(text=''.join(check_marks))
