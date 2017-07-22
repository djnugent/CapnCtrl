import numpy as np
import win32gui, win32ui, win32con, win32api, pywintypes
import time
from keyboard import VK_CODE

### TODO
# - Add joystick cap and ctrl Support
# - Add mouse click and scroll cap Support
# - Add callback events

### Class outline
# ctrl.joystick(idx, action={})
# ctrl.keyboard(down=[],up=[])
# crtl.mouse(pos)

# cap.screen(name = None, region = None, padding = [0,0,0,0]) -> numpy
# cap.joystick(idx) -> dict
# cap.keyboard() -> array
# cap.mouse() -> array

# cap.async_screen(name = None, region = None, padding = [0,0,0,0], rate = 0)
# cap.async_joystick(idx, rate = 0)
# cap.async_keyboard(rate = 0)
# cap.async_mouse(rate = 0)

# async.start()
# async.stop()
# async.mute()
# async.unmute()

# async_screen.add_listener(callback)
# async_joystick.add_listener(callback, event_type, whitelist = None, blacklist = None)
# async_keyboard.add_listener(callback, event_type, whitelist = None, blacklist = None)
# async_mouse.add_listener(callback, event_type, whitelist = None, blacklist = None)


# Joystick event types: STREAM, ALL, BUTTON_DOWN, BUTTON_UP, BUTTON_PRESS, AXIS
# Keys event types: STREAM, KEY_DOWN, KEY_UP, KEY_PRESS
# Mouse event types: STREAM, ALL


class ctrl:
    # Dictionary of initialized joysticks
    joysticks = {}

    @classmethod
    def create_joystick(cls, idx):
        if idx < 0:
            raise KeyError("Joystick id must be >= 0")
        js = vJoy(idx)
        js.open()
        cls.joysticks[idx] = js

    def close_joystick(cls,idx):
        # Close all joysticks
        if idx  == -1:
            for _idx, js in cls.joysticks.items:
                js.close()
                del cls.joysticks[idx]
        # Close a specific joystick
        elif idx in cls.joysticks:
            cls.joysticks[idx].close()
            del cls.joysticks[idx]
        else:
            raise KeyError("Joystick does not exist")


    @classmethod
    def joystick(cls,idx,actions={}):
        # Check for a virtual joystick
        if not idx in cls.joysticks:
            raise KeyError("Joystick {} has not been created. Please call create_joystick({})".format(idx,idx))

        js = cls.joysticks[idx]
        # TODO do stuff


    @classmethod
    def key_press(cls,*args,hold_time=0.0):
        #https://gist.github.com/chriskiehl/2906125
        # Key down
        for i in args:
            win32api.keybd_event(VK_CODE[i], 0,0,0)
        # wait
        time.sleep(hold_time)
        # Key up
        for i in args:
            win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)

    @classmethod
    def key_down(cls,*args):
        #https://gist.github.com/chriskiehl/2906125
        for i in args:
            win32api.keybd_event(VK_CODE[i], 0,0,0)

    @classmethod
    def key_up(cls,*args):
        #https://gist.github.com/chriskiehl/2906125
        for i in args:
            win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)

    @classmethod
    def mouse(cls,pos,relative=False):
        if relative:
            current_pos = win32api.GetCursorPos()
            x,y = pos[0] + current_pos[0], pos[1] + current_pos[1]
            win32api.SetCursorPos((x,y))
        else:
            win32api.SetCursorPos(pos)

    @classmethod
    def click(cls,pos=None,typ="left",hold_time=0,relative=False):
        # Click at current location
        if pos is None:
            x, y = win32gui.GetCursorPos()
        # Click at location
        else:
            # Relative to current position
            if relative:
                current_pos = win32api.GetCursorPos()
                x,y = pos[0] + current_pos[0], pos[1] + current_pos[1]
            win32api.SetCursorPos((x,y))

        # Type of click
        if typ.lower() == "left":
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
            time.sleep(hold_time)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        elif typ.lower() == "middle":
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN,x,y,0,0)
            time.sleep(hold_time)
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUPTUP,x,y,0,0)
        elif typ.lower() == "right":
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
            time.sleep(hold_time)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
        else:
            raise ValueError("Invalid click type: {} - Supported: LEFT, RIGHT, MIDDLE".format(typ))


    @classmethod
    def click_down(cls,pos=None,typ="left",relative=False):
        # Click at current location
        if pos is None:
            x, y = win32gui.GetCursorPos()
        # Click at location
        else:
            # Relative to current position
            if relative:
                current_pos = win32api.GetCursorPos()
                x,y = pos[0] + current_pos[0], pos[1] + current_pos[1]
            win32api.SetCursorPos((x,y))

        # Type of click
        if typ.lower() == "left":
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        elif typ.lower() == "middle":
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN,x,y,0,0)
        elif typ.lower() == "right":
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
        else:
            raise ValueError("Invalid click type: {} - Supported: LEFT, RIGHT, MIDDLE".format(typ))

    @classmethod
    def click_up(cls,pos=None,typ="left",relative=False):
        # Click at current location
        if pos is None:
            x, y = win32gui.GetCursorPos()
        # Click at location
        else:
            # Relative to current position
            if relative:
                current_pos = win32api.GetCursorPos()
                x,y = pos[0] + current_pos[0], pos[1] + current_pos[1]
            win32api.SetCursorPos((x,y))

        # Type of click
        if typ.lower() == "left":
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        elif typ.lower() == "middle":
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP,x,y,0,0)
        elif typ.lower() == "right":
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
        else:
            raise ValueError("Invalid click type: {} - Supported: LEFT, RIGHT, MIDDLE".format(typ))

    @classmethod
    def scroll_wheel(cls,vertical,horizontal):
        x, y = win32gui.GetCursorPos()
        win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, vertical, horizontal)

class cap:

    @classmethod
    # Inspired by Frannecklp
    def screen(cls, window = None, region = None, padding = [0,0,0,0]):
        # Can capture a window or a region, not both
        if window is not None and region is not None:
            raise ValueError("Please specify 'window' or 'region', not both")

        # Screen region defined by window name
        if window is not None:
            try:
                winhdl = win32gui.FindWindow(None,window)
                region = win32gui.GetWindowRect(winhdl)
                win32gui.SetForegroundWindow(winhdl)
                time.sleep(0.004)
            except pywintypes.error:
                raise ValueError("Window does not exist. Run tools.active_windows() to see available windows") from None

        # Region is defined by user or window
        if region:
                left,top,x2,y2 = region
                width = x2 - left + 1
                height = y2 - top + 1
        # Capture the entire screens
        else:
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

        # Pad the image
        left += padding[0] # left padding
        width += - padding[1] - padding[0] # right padding
        top += padding[2] # top padding
        height += - padding[3] - padding[2] # bottom padding

        # Capture desktop
        hwin = win32gui.GetDesktopWindow()
        hwindc = win32gui.GetWindowDC(hwin)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

        # Convert to numpy array
        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (height,width,4)

        # Remove alpha channel
        img = img[:,:,:3]

        # Clean up
        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(hwin, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())

        return img

    @classmethod
    def joystick(idx):
        # pysdl2
        raise NotImplementedError("Joystick capture is not implemented")

    @classmethod
    def keyboard(cls):
        keys = []
        for key, code in VK_CODE.items():
            if win32api.GetAsyncKeyState(code):
                keys.append(key)
        return keys

    @classmethod
    def mouse(cls):
        return win32gui.GetCursorPos()

    @classmethod
    def mouse_click(cls):
        raise NotImplementedError("Mouse click capture is not implemented")
        '''
        import pyHook, pythoncom
        def onclick(event):
            print(event.Position)
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
        '''
    @classmethod
    def scroll_wheel(cls):
        raise NotImplementedError("Scroll wheel capture is not implemented")



class tools:
    @staticmethod
    def active_windows():
        titles = []
        def callback(handle, data):
            titles.append(win32gui.GetWindowText(handle))
        win32gui.EnumWindows(callback, None)
        return titles
