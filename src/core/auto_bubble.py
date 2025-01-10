import time
import win32api
import ctypes
from win32con import KEYEVENTF_KEYUP

MOUSEEVENTF_MOVE = 0x0001

class AutoHealMacro:
    def __init__(self):
        self.running = True
        self.paused = False
        self.hotkey = 'x'
        
        # Store current settings as properties
        self._settings = {
            'look_down_amount': 1800,
            'up_movement_ratio': 0.7,
            'move_down_step': 50,
            'move_up_step': 10
        }
        
    @property
    def look_down_amount(self):
        return self._settings['look_down_amount']
    
    @look_down_amount.setter
    def look_down_amount(self, value):
        self._settings['look_down_amount'] = value
        
    @property
    def up_movement_ratio(self):
        return self._settings['up_movement_ratio']
    
    @up_movement_ratio.setter
    def up_movement_ratio(self, value):
        self._settings['up_movement_ratio'] = value
        
    @property
    def move_down_step(self):
        return self._settings['move_down_step']
    
    @move_down_step.setter
    def move_down_step(self, value):
        self._settings['move_down_step'] = value
        
    @property
    def move_up_step(self):
        return self._settings['move_up_step']
    
    @move_up_step.setter
    def move_up_step(self, value):
        self._settings['move_up_step'] = value
    
    def precise_sleep(self, duration):
        """More precise sleep using Windows timer"""
        start = time.perf_counter()
        while time.perf_counter() - start < duration:
            pass
    
    def move_mouse_relative(self, dy):
        """Simulate relative mouse movement"""
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, 0, dy, 0, 0)
        self.precise_sleep(0.0009)
    
    def move_down(self):
        """Clean, straightforward downward movement"""
        total_steps = (self.look_down_amount + self.move_down_step - 1) // self.move_down_step
        movement_per_step = self.look_down_amount / total_steps
        
        for _ in range(total_steps):
            self.move_mouse_relative(int(movement_per_step))
    
    def move_up(self):
        """Upward movement with overshoot and correction"""
        up_amount = int(self.look_down_amount * self.up_movement_ratio)
        total_steps = (up_amount + self.move_up_step - 1) // self.move_up_step
        movement_per_step = up_amount / total_steps

        # Move up with overshoot
        for _ in range(total_steps):
            self.move_mouse_relative(int(-movement_per_step * 1))
    
    def toggle_pause(self):
        """Toggle the pause state"""
        self.paused = not self.paused
        print(f"Macro {'paused' if self.paused else 'resumed'}")
    
    def perform_heal_action(self):
        if self.paused:
            return
            
        try:
            self.move_down()
            
            win32api.keybd_event(0x45, 0, 0, 0)  # Press E
            self.precise_sleep(0.05)
            win32api.keybd_event(0x45, 0, KEYEVENTF_KEYUP, 0)  # Release E
            
            ctypes.windll.user32.keybd_event(0x10, 0x2A, 0, 0)  # Press Left Shift
            self.precise_sleep(0.05)
            ctypes.windll.user32.keybd_event(0x10, 0x2A, KEYEVENTF_KEYUP, 0)  # Release Left Shift
            
            self.precise_sleep(0.05)
            
            self.move_up()
            
        except Exception as e:
            print(f"Error during heal action: {e}")