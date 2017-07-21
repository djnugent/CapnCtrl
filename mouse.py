import win32api, pyHook, pythoncom

width = win32api.GetSystemMetrics(0)
height = win32api.GetSystemMetrics(1)
midWidth = (width + 1) / 2
midHeight = (height + 1) / 2

def moveCursor(x, y):
    print('Moving mouse')
    win32api.SetCursorPos((x, y))

def onclick(event):
    print(event.Position)
    moveCursor(int(midWidth), int(midHeight))
    return True

try:
    hm = pyHook.HookManager()
    hm.SubscribeMouseAllButtonsUp(onclick)
    hm.HookMouse()
    pythoncom.PumpMessages()
except KeyboardInterrupt:
    hm.UnhookMouse()
    print('\nDone.')
    exit()
