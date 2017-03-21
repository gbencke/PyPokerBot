import pyautogui


def execute(args):
    if len(args) < 2:
        print("For this task you need at least 3 arguments: <Image Source> <Pos> <size> <FileName to save>")
        return
    x = int(args[0])
    y = int(args[1])
    pyautogui.moveTo(x, y)
    pyautogui.click(x, y)



