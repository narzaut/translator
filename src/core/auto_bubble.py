import keyboard
import time
import sys
import win32api
import ctypes
from win32con import KEYEVENTF_KEYUP

MOUSEEVENTF_MOVE = 0x0001

class AutoHealMacro:
    def __init__(self):
        self.running = True
        self.paused = False  # Add pause state
        self.hotkey = 'x'
        self.pause_hotkey = 'p'  # Add pause hotkey
        self.look_down_amount = 4000
        self.up_movement_ratio = 0.265
        
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
        STEP_SIZE = 100
        total_steps = (self.look_down_amount + STEP_SIZE - 1) // STEP_SIZE
        movement_per_step = self.look_down_amount / total_steps
        
        for _ in range(total_steps):
            self.move_mouse_relative(int(movement_per_step))
    
    def move_up(self):
        """Upward movement with overshoot and correction"""
        up_amount = int(self.look_down_amount * self.up_movement_ratio)
        STEP_SIZE = 10
        total_steps = (up_amount + STEP_SIZE - 1) // STEP_SIZE
        movement_per_step = up_amount / total_steps

        # Move up with overshoot
        for _ in range(total_steps):
            self.move_mouse_relative(int(-movement_per_step * 1))
    
    def toggle_pause(self):
        """Toggle the pause state"""
        self.paused = not self.paused
        print(f"Macro {'paused' if self.paused else 'resumed'}")
    
    def perform_heal_action(self):
        if self.paused:  # Skip if paused
            return
            
        try:
            # Clean look down
            self.move_down()
            
            # Quick keypress sequence
            win32api.keybd_event(0x45, 0, 0, 0)  # Press E
            self.precise_sleep(0.05)
            win32api.keybd_event(0x45, 0, KEYEVENTF_KEYUP, 0)  # Release E
            
            ctypes.windll.user32.keybd_event(0x10, 0x2A, 0, 0)  # Press Left Shift
            self.precise_sleep(0.05)
            ctypes.windll.user32.keybd_event(0x10, 0x2A, KEYEVENTF_KEYUP, 0)  # Release Left Shift
            
            self.precise_sleep(0.05)
            
            # Look up with overshoot and correction
            self.move_up()
            
        except Exception as e:
            print(f"Error during heal action: {e}")
    
    def start(self):
        """Start the macro"""
        print(f"\nAuto Heal Macro started!")
        print(f"Press '{self.hotkey}' to heal")
        print(f"Press '{self.pause_hotkey}' to pause/unpause")
        print("Press 'F1' to exit.")
        
        keyboard.on_press_key(self.hotkey, lambda _: self.perform_heal_action())
        keyboard.on_press_key(self.pause_hotkey, self.toggle_pause)  # Add pause hotkey
        keyboard.wait('F1')
        self.running = False
        print("Macro stopped.")