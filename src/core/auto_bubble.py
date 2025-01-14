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
        self.double_heal_hotkey = 'z'
        
        # Store current settings as properties
        self._settings = {
            'look_down_amount': 1500,
            'up_movement_ratio': 0.97,
            'move_down_step': 25,
            'move_up_step': 10,
            'heal_delay': 0.05
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
        
    @property
    def heal_delay(self):
        return self._settings['heal_delay']
    
    @heal_delay.setter
    def heal_delay(self, value):
        self._settings['heal_delay'] = value
    
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
    
    def heal_sequence(self, double_heal=False):
        """Perform the healing key sequence"""
        self.press_key(0x45)
        self.precise_sleep(self.heal_delay)
        self.press_shift()
        
        if double_heal:
            self.precise_sleep(self.heal_delay * 2)
            self.press_key(0x45)
            self.precise_sleep(self.heal_delay)
            self.press_shift()
    
    def perform_heal_action(self, double_heal=False):
        """Perform the complete heal action sequence"""
        if self.paused:
            return
            
        try:
            self.move_down()
            self.heal_sequence(double_heal)
            self.precise_sleep(self.heal_delay)
            self.move_up()
            
        except Exception as e:
            print(f"Error during heal action: {e}")