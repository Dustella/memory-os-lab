from threading import Lock


possible_color_list = [
    "red",
    "green",
    "yellow",
    "blue",
    "purple",
    "cyan",
]


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """
    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class MemoryController(metaclass=SingletonMeta):

    def __init__(self) -> None:
        self.memory_mapping = {}  # 进程名 -> (起始地址, 大小)
        self.color_mapping = {}  # 进程染色 -> 进程名
        self.color_index = 0
        size = 16
        res = [None for _ in range(size)]

        self.memory = res
        pass

    def allocate(self, process_name, size):
        # do real allocation
        addr = self.find_free_address(size)
        if addr is None:
            raise Exception("Memory is full")
        self.memory_mapping[process_name] = (addr, size)
        if process_name not in self.color_mapping:
            self.color_mapping[process_name
                               ] = possible_color_list[self.color_index % 5]
        self.color_index += 1
        for i in range(size):
            self.memory[addr+i] = process_name
        pass

    def hard_allocate(self, process_name, addr, size):
        # do real allocation
        if not self.is_free(addr, size):
            raise Exception("Memory is full")
        if process_name not in self.color_mapping:
            self.color_mapping[process_name
                               ] = possible_color_list[self.color_index % 5]
        self.memory_mapping[process_name] = (addr, size)

        for i in range(size):
            self.memory[addr+i] = process_name

    def free(self, process_name):
        addr, size = self.memory_mapping[process_name]
        self.memory_mapping.pop(process_name)
        self.memory[addr:addr+size] = [None for _ in range(size)]

    def find_free_address(self, size):
        for i in range(len(self.memory)):
            if self.memory[i] is None:
                if self.is_free(i, size):
                    return i
        return None

    def is_free(self, addr, size):
        for i in range(size):
            if self.memory[addr+i] is not None:
                return False
        return True

    def do_compact(self):
        # get all memory mapping, sort by address
        # then erase all memory
        # allocate them again
        sorted_mapping = sorted(
            self.memory_mapping.items(), key=lambda x: x[1][0])
        cp = self.memory_mapping.copy()
        for process_name, process_mapping in cp.items():
            self.free(process_name)
        for process_name, process_mapping in sorted_mapping:
            self.allocate(process_name, process_mapping[1])

    def get_colored_list(self):
        res = []
        # 返回染色进程列表
        for status in self.memory:
            if status is not None and status not in res:
                res.append(self.color_mapping[status])
            elif status is None:
                res.append("white")
        return res
