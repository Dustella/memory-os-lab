import threading
from time import sleep
from context import Context


if __name__ == "__main__":
    print("请选择模式：")
    print("1. 动态重定位")
    print("2. 静态重定位")
    mode = input()
    context = Context()
    sleep(1)
    if mode == "1":
        threading.Thread(target=context.run_dynamic_allocating).start()
    elif mode == "2":
        threading.Thread(target=context.run_static_allocating).start()
    else:
        print("输入错误")
        raise Exception("输入错误")

    from gui import MemoryTable
    gui = MemoryTable()
    gui.start()
