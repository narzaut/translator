import time
import win32api
import ctypes
from win32con import KEYEVENTF_KEYUP

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

class AutoCloneMacro:
    def __init__(self):
        self.running = True
        self.paused = False
        self.hotkey = 'x'  # You can change this to your preferred hotkey
        self._settings = {
            'sequence_delay': 0.00001  # Delay between key presses
        }
    
    @property
    def sequence_delay(self):
        return self._settings['sequence_delay']
    
    @sequence_delay.setter
    def sequence_delay(self, value):
        self._settings['sequence_delay'] = value
    
    def precise_sleep(self, duration):
        """More precise sleep using Windows timer"""
        start = time.perf_counter()
        while time.perf_counter() - start < duration:
            pass
    
    def press_key(self, key_code, duration=0.05):
        """Helper method to press and release a key"""
        win32api.keybd_event(key_code, 0, 0, 0)
        self.precise_sleep(duration)
        win32api.keybd_event(key_code, 0, KEYEVENTF_KEYUP, 0)
    
    def press_shift(self, duration=0.05):
        """Helper method to press and release shift"""
        ctypes.windll.user32.keybd_event(0x10, 0x2A, 0, 0)
        self.precise_sleep(duration)
        ctypes.windll.user32.keybd_event(0x10, 0x2A, KEYEVENTF_KEYUP, 0)
    
    def click_left_mouse(self, duration=0.05):
        """Helper method to click and release left mouse button"""
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        self.precise_sleep(duration)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
    def toggle_pause(self):
        """Toggle the pause state"""
        self.paused = not self.paused
        print(f"Macro {'paused' if self.paused else 'resumed'}")
    
    def perform_sequence(self):
        """Perform the key/mouse sequence: E > Left Click > Left Shift"""
        if self.paused:
            return
            
        try:
            # Press E
            self.press_key(0x45)
            self.precise_sleep(self.sequence_delay)
            
            # Left mouse click
            self.click_left_mouse()
            self.precise_sleep(self.sequence_delay)
            
            # Press shift
            self.press_shift()
            
        except Exception as e:
            print(f"Error during key sequence: {e}")