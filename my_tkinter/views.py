import tkinter as tk


class BaseView:
    def __init__(self):
        self.window = tk.Tk()

    def open(self):
        self.window.mainloop()

    def close(self):
        self.window.destroy()


class NormalView(BaseView):
    def __init__(self, button_event):
        super().__init__()
        self.button_event = button_event
        self.url_label = tk.Label(self.window, text="網址：")
        self.url_entry = tk.Entry(self.window, width=50)
        self.start_button = tk.Button(self.window, text="執行", width=10, command=self.start_click)
        self.url_label.grid(row=0, column=0)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, )
        self.start_button.grid(row=1, column=1, pady=5)

    def start_click(self):
        if self.button_event:
            self.button_event(self.url_entry.get())

    def set_url(self, text):
        self.url_entry.insert(0, text)
    
