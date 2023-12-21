from time import sleep
from memory_controller import MemoryController


class Context:
    def __init__(self) -> None:
        self.memory_controller = MemoryController()
        self.action_sequence = [
            ("allocate", "Process A", 3),
            ("allocate", "Process B", 4),
            ("allocate", "Process C", 2),
            ("free", "Process B"),
            ("compact",),
            ("allocate", "Process D", 2),
            ("free", "Process A"),
            ("compact",),
            ("allocate", "Process E", 3),
            ("free", "Process C"),
            ("compact",),
            ("free", "Process D"),
            ("compact",),
            ("free", "Process E"),
            ("compact",),
        ]
        self.static_hard_sequence = []
        pass

    def run_dynamic_allocating(self):
        c = self.memory_controller
        for action in self.action_sequence:
            if action[0] == "allocate":
                c.allocate(action[1], action[2])
            elif action[0] == "free":
                c.free(action[1])
            elif action[0] == "compact":
                c.do_compact()
            sleep(1)
        self.suicide()

    def run_static_allocating(self):
        c = self.memory_controller
        # first, culculate the static sequence
        self.calculate_static_sequence()
        for action in self.static_hard_sequence:
            if action[0] == "hard_allocate":
                c.hard_allocate(action[1], action[2], action[3])
            elif action[0] == "free":
                c.free(action[1])
            elif action[0] == "compact":
                c.do_compact()
            sleep(1)
        self.suicide()

    def suicide(self):
        from tkinter import messagebox
        import sys
        from gui import MemoryTable
        messagebox.showinfo('提示', '全部进程结束，点击确定退出')
        men = MemoryTable()
        men.root.destroy()
        sys.exit()

    def calculate_static_sequence(self):
        current_index = 0
        self.static_hard_sequence.clear()
        for action in self.action_sequence:
            if action[0] == "allocate":
                self.static_hard_sequence.append(
                    ("hard_allocate", action[1], current_index, action[2]))
                current_index += action[2]
            elif action[0] == "free":
                self.static_hard_sequence.append(("free", action[1]))
            elif action[0] == "compact":
                self.static_hard_sequence.append(("compact",))
        pass
