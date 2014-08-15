from win32api import keybd_event, mouse_event
import win32con
import time
import random

Base = {
    '0': 48,
    '1': 49,
    '2': 50,
    '3': 51,
    '4': 52,
    '5': 53,
    '6': 54,
    '7': 55,
    '8': 56,
    '9': 57,
    'a': 65,
    'b': 66,
    'c': 67,
    'd': 68,
    'e': 69,
    'f': 70,
    'g': 71,
    'h': 72,
    'i': 73,
    'j': 74,
    'k': 75,
    'l': 76,
    'm': 77,
    'n': 78,
    'o': 79,
    'p': 80,
    'q': 81,
    'r': 82,
    's': 83,
    't': 84,
    'u': 85,
    'v': 86,
    'w': 87,
    'x': 88,
    'y': 89,
    'z': 90,
    '.': 190,
    '-': 189,
    ',': 188,
    '=': 187,
    '/': 191,
    ';': 186,
    '[': 219,
    ']': 221,
    '\\': 220,
    "'": 222,
    'ALT': 18,
    'TAB': 9,
    'CAPSLOCK': 20,
    'ENTER': 13,
    'BS': 8,
    'CTRL': 17,
    'ESC': 27,
    ' ': 32,
    'END': 35,
    'DOWN': 40,
    'LEFT': 37,
    'UP': 38,
    'RIGHT': 39,
    'SELECT': 41,
    'PRINTSCR': 44,
    'INS': 45,
    'DEL': 46,
    'LWIN': 91,
    'RWIN': 92,
    'LSHIFT': 160,
    'SHIFT': 161,
    'LCTRL': 162,
    'RCTRL': 163,
    'VOLUP': 175,
    'DOLDOWN': 174,
    'NUMLOCK': 144,
    'SCROLL': 145 }

def KeyUp(Key):
    keybd_event(Key, 0, 2, 0)

def KeyDown(Key):
    keybd_event(Key, 0, 1, 0)

def MouseButton(side, state):
    if side == 0: # left
        if state:
            mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
        else:
            mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    else: # right
        if state:
            mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0,0,0)
        else:
            mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0,0,0)


def MouseMoveRel(x,y):
    mouse_event(win32con.MOUSEEVENTF_MOVE, int(x), int(y))
    
if __name__ == "__main__":
  time.sleep(10.0)
  MouseMoveRel(100,100)
  
  