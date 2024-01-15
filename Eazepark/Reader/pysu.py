import pyautogui as p
import time
p.hotkey('ctrl','tab')
time.sleep(2)
for i in range(77):
    for j in range(4):
        p.press('delete')
    p.press('down')