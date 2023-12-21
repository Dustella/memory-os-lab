import tkinter as tk

from memory_controller import SingletonMeta


class MemoryTable(metaclass=SingletonMeta):
    def __init__(self):
        root = tk.Tk()
        self.root = root
        self.root.title("Memory Page Visualization")
        self.root.geometry("1300x200")

        # Create a canvas to draw the memory pages
        self.canvas = tk.Canvas(root, width=800, height=100)

        # Create a list to store references to the page rectangles
        self.page_rectangles = []

        # Create memory pages
        self.num_pages = 16  # Total number of memory pages
        self.create_memory_pages()

        self.canvas.grid(row=0, column=0, padx=10, pady=10)

    def create_memory_pages(self):
        # Calculate the width of each memory page rectangle
        page_width = 800 // self.num_pages

        # Create memory page rectangles and store references
        for i in range(self.num_pages):
            x1 = i * page_width
            x2 = (i + 1) * page_width
            y1 = 0
            y2 = 0 + 40
            rectangle = self.canvas.create_rectangle(
                x1, y1, x2, y2, fill="white", outline="black")
            self.page_rectangles.append(rectangle)

    def update_page_status(self):
        # Update the fill color of the specified page rectangle
        # color = "green" if is_allocated else "white"
        # self.canvas.itemconfig(self.page_rectangles[page_index], fill=color)
        from memory_controller import MemoryController
        mem = MemoryController()
        res = mem.get_colored_list()
        for index, item in enumerate(res):
            self.canvas.itemconfig(
                self.page_rectangles[index], fill=item)
        self.root.after(100, self.update_page_status)

    def get_widgets(self):
        return self.canvas

    def start(self):
        self.update_page_status()
        self.root.mainloop()
