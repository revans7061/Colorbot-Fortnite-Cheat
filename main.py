import keyboard
import mss
import numpy as np

ZONE = 4
DELAY = 0.03
active = False


def toggle():
    global active
    active = not active


def on_target(frame):
    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2
    zone = frame[cy - ZONE:cy + ZONE, cx - ZONE:cx + ZONE]
    r, g, b = zone[:, :, 2], zone[:, :, 1], zone[:, :, 0]
    return int(((r > 200) & (g < 90) & (b < 90)).sum()) > 6


def main():
    keyboard.add_hotkey("f8", toggle)
    with mss.mss() as sct:
        while True:
            if active and on_target(np.array(sct.grab(sct.monitors[1]))):
                keyboard.press_and_release("mouse left")
                keyboard.call_later(lambda: None, DELAY)


if __name__ == "__main__":
    main()
