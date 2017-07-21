import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api


# TODO how to initialize virtual joystick

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
    ### Static Class variables go here
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
    def keyboard(cls,down=[],up=[]):



        pass

    @classmethod
    def mouse(cls,pos):
        pass


class cap:

    # Static Class variables go here

    @classmethod
    def screen(cls, name = None, region = None, padding = [0,0,0,0]):
        return cls.__grab_screen(region)

    @classmethod
    def joystick(idx):
        return {}

    @classmethod
    def keyboard(cls):
        return []

    @classmethod
    def mouse():
        return []

    # Done by Frannecklp
    @classmethod
    def __grab_screen(cls,region=None):

        hwin = win32gui.GetDesktopWindow()

        if region:
                left,top,x2,y2 = region
                width = x2 - left + 1
                height = y2 - top + 1
        else:
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

        hwindc = win32gui.GetWindowDC(hwin)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (height,width,4)

        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(hwin, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())

        return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
