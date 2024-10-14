import tkinter as tk
from tkinter import font
import config


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # config
        self.title(config.title)
        self.geometry(config.resolution)
        self.iconbitmap(config.icon)
        self.minsize(*config.min_resolution)
        self.first = ''
        self.second = ''
        self.operation = ''
        self.isfirstoperation = 0

        self.result_font = font.Font(
            family=config.result_font,
            size=config.result_font_size,
        )
        self.button_font = font.Font(
            family=config.button_font,
            size=config.button_font_size,
        )

        # All buttons and their places
        self.button_list = ['C', '<-', '', '/',
                            '7', '8', '9', '*',
                            '4', '5', '6', '-',
                            '1', '2', '3', '+',
                            '+/-', '0', '.', '=']

        # Frames
        self.result_frame = tk.Frame(self, background=config.bg_color)
        self.result_frame.place(relx=0, rely=0, relheight=0.25, relwidth=1)

        self.button_frame = tk.Frame(self, background=config.bg_color)
        self.button_frame.place(relx=0, rely=0.25, relheight=1, relwidth=1)

        # Buttons
        x, y = -0.25, 0
        for i in self.button_list:
            if x == 0.75:
                x = 0
                y += 0.15
            else:
                x += 0.25

            if i != '':
                button = tk.Button(
                    self.button_frame,
                    text=i,
                    font=self.button_font,
                    background=config.bg_color,
                    foreground=config.fg_color,
                    activebackground=config.bg_color,
                    activeforeground=config.fg_color,
                    command=lambda i=i: self.update_expression(i),
                )
                button.place(
                    relx=x,
                    rely=y,
                    relheight=0.15,
                    relwidth=0.25
                )
            else:
                continue

        # Label
        self.label = tk.Label(
            self.result_frame,
            text='',
            font=self.result_font,
            background=config.bg_color,
            foreground=config.fg_color
        )
        self.label.place(rely=0.3)

    # Function
    def update_expression(self, symbol: str) -> None:
        if symbol.isdigit() or symbol == '.':
            if not self.isfirstoperation:
                self.first += symbol
                self.label.config(text=self.first)
            else:
                self.second += symbol
                self.label.config(text=self.second)
        elif symbol == '=':
            self.equal()
        elif symbol == 'C':
            self.clear()
        elif symbol == '<-':
            self.backspace()
        elif symbol == '+/-':
            if len(self.second) != 0:
                if float(self.second) > 0:
                    self.second = f'-{self.second}'
                    self.label.config(text=self.second)
                else:
                    self.second = self.second[1:]
                    self.label.config(text=self.second)
            else:
                if float(self.first) > 0:
                    self.first = f'-{self.first}'
                    self.label.config(text=self.first)
                else:
                    self.first = self.first[1:]
                    self.label.config(text=self.first)
        else:
            if len(self.operation) == 0:
                self.operation = symbol
                self.label.config(text=self.operation)
                self.isfirstoperation = 1
            elif len(self.operation) != 0 and len(self.second) != 0:
                self.equal()
                self.operation = symbol
                self.label.config(text=self.operation)
            elif len(self.operation) != 0:
                self.operation = symbol
                self.label.config(text=self.operation)

    # can be better
    def equal(self) -> None:
        try:
            self.first = float(self.first)
            self.second = float(self.second)
        except ValueError:
            self.error_handler()
            return

        if self.operation == '+':
            self.first = self.first + self.second
        elif self.operation == '-':
            self.first = self.first - self.second
        elif self.operation == '*':
            self.first = self.first * self.second
        elif self.operation == '/':
            try:
                self.first = self.first / self.second
            except ZeroDivisionError:
                self.error_handler()
                return

        if self.first.is_integer():
            self.first = str(int(self.first))
        else:
            self.first = str(self.first)

        self.label.config(text=self.first)
        self.second = ''

    def clear(self) -> None:
        self.first = ''
        self.second = ''
        self.operation = ''
        self.isfirstoperation = 0
        self.label.config(text='')

    def backspace(self) -> None:
        if len(self.first) != 0 and len(self.second) == 0:
            self.first = self.first[:-1]
            self.label.config(text=self.first)
        elif len(self.first) != 0 and len(self.second) != 0:
            self.second = self.second[:-1]
            self.label.config(text=self.second)

    def error_handler(self) -> None:
        self.clear()
        self.label.config(text='Error')

    # def check_missclick(self):
    #     if len(self.first) == 0:
    #         return
    #     elif len(self.operation) == 0 and


if __name__ == '__main__':
    root = App()
    root.mainloop()
