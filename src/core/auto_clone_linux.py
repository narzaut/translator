import time
import uinput
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Button, Listener as MouseListener
from pynput.mouse import Controller as MouseController
from pynput import keyboard as pkbd
import threading

class AutoCloneMacro:
    def __init__(self):
        self.running = True
        self.paused = False
        # Hotkeys
        self.hotkey = 'x'  # Default hotkey for clone sequence (E > Click > Shift)
        self.alt_hotkey = 'z'  # Alternative sequence (E > Click > F)
        
        # uinput device for raw relative mouse movement (requires root) - only for movement
        self.device = uinput.Device([uinput.REL_X, uinput.REL_Y])
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.listener = None
        
        # Store current settings as properties
        self._settings = {
            'sequence_delay': 0.05,  # Delay between key presses
            'key_press_duration': 0.05,  # How long to hold keys
            'mouse_click_duration': 0.05,  # How long to hold mouse button
            'alt_sequence_delay': 0.2,  # Longer delay for alt sequence (between click and F)
        }
    
    @property
    def sequence_delay(self):
        return self._settings['sequence_delay']
    
    @sequence_delay.setter
    def sequence_delay(self, value):
        self._settings['sequence_delay'] = value
        
    @property
    def key_press_duration(self):
        return self._settings['key_press_duration']
    
    @key_press_duration.setter
    def key_press_duration(self, value):
        self._settings['key_press_duration'] = value
        
    @property
    def mouse_click_duration(self):
        return self._settings['mouse_click_duration']
    
    @mouse_click_duration.setter
    def mouse_click_duration(self, value):
        self._settings['mouse_click_duration'] = value
        
    @property
    def alt_sequence_delay(self):
        return self._settings['alt_sequence_delay']
    
    @alt_sequence_delay.setter
    def alt_sequence_delay(self, value):
        self._settings['alt_sequence_delay'] = value
    
    def precise_sleep(self, duration):
        """More precise sleep using performance counter"""
        start = time.perf_counter()
        while time.perf_counter() - start < duration:
            pass
    
    def press_key(self, key_code, duration=None):
        """Helper method to press and release a key"""
        if duration is None:
            duration = self.key_press_duration
            
        # Accepts integer key codes (e.g., 0x45 for 'E') or single-character strings
        key_char = chr(key_code).lower() if isinstance(key_code, int) else (key_code.lower() if isinstance(key_code, str) else key_code)
        self.keyboard.press(key_char)
        self.precise_sleep(duration)
        self.keyboard.release(key_char)
    
    def press_shift(self, duration=None):
        """Helper method to press and release shift"""
        if duration is None:
            duration = self.key_press_duration
            
        self.keyboard.press(Key.shift)
        self.precise_sleep(duration)
        self.keyboard.release(Key.shift)
    
    def click_left_mouse(self, duration=None):
        """Helper method to click and release left mouse button via pynput"""
        if duration is None:
            duration = self.mouse_click_duration
            
        self.mouse.press(Button.left)
        self.precise_sleep(duration)
        self.mouse.release(Button.left)
    
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
            self.press_key('e')  # Use character for consistency
            self.precise_sleep(self.sequence_delay)
            
            # Left mouse click
            self.click_left_mouse()
            self.precise_sleep(self.sequence_delay)
            
            # Press shift
            self.press_shift()
            
        except Exception as e:
            print(f"Error during key sequence: {e}")

    def perform_alt_sequence(self):
        """Perform the alternative key/mouse sequence: E > Left Click > F"""
        if self.paused:
            return
            
        try:
            # Press E
            self.press_key('e')  # Use character for consistency
            self.precise_sleep(self.sequence_delay)
            
            # Left mouse click
            self.click_left_mouse()
            # Use longer delay before F key
            self.precise_sleep(self.alt_sequence_delay)
            
            # Press F instead of shift
            self.press_key('f')  # Use character 'f'
            print("Alt sequence: E -> Click -> F completed")  # Debug output
            
        except Exception as e:
            print(f"Error during alternative key sequence: {e}")

    def start_listener(self):
        """Start global hotkey listener on a separate thread"""
        def on_press(key):
            try:
                if key.char == self.hotkey:
                    self.perform_sequence()
                elif key.char == self.alt_hotkey:
                    self.perform_alt_sequence()
            except AttributeError:
                # Non-character keys (e.g., shift) don't have .char
                pass

        # Run listener in daemon thread so it doesn't block program exit
        self.listener = pkbd.Listener(on_press=on_press)
        self.listener.daemon = True
        self.listener.start()

# ----------------------------- CLI ENTRYPOINT ----------------------------- #

def main():
    macro = AutoCloneMacro()
    macro.start_listener()

    print("\nAutoCloneMacro CLI (Linux version)")
    print(f"Hotkeys: '{macro.hotkey}' for clone sequence (E > Left Click > Shift)")
    print(f"         '{macro.alt_hotkey}' for alt sequence (E > Left Click > F)")
    print("Note: Uses pynput for mouse clicks, uinput only for potential mouse movement")

    while True:
        print("\nCommands:")
        print(" [1] Pause/Resume Macro")
        print(" [2] Show Current Settings")
        print(" [3] Modify Settings")
        print(" [4] Change Hotkey")
        print(" [5] Test Sequence")
        print(" [6] Exit")
        choice = input("Select option: ").strip()

        if choice == '1':
            macro.toggle_pause()
        elif choice == '2':
            print("\nCurrent Settings:")
            print(f"  Primary Hotkey (E>Click>Shift): {macro.hotkey}")
            print(f"  Alt Hotkey (E>Click>F): {macro.alt_hotkey}")
            for k, v in macro._settings.items():
                print(f"  {k}: {v}")
        elif choice == '3':
            print("\nWhich setting would you like to modify?")
            keys = list(macro._settings.keys())
            for idx, key in enumerate(keys, 1):
                print(f" [{idx}] {key} (current: {macro._settings[key]})")
            idx_choice = input("Enter number or leave blank to cancel: ").strip()
            if idx_choice.isdigit() and 1 <= int(idx_choice) <= len(keys):
                sel_key = keys[int(idx_choice) - 1]
                new_val = input(f"Enter new value for {sel_key}: ").strip()
                try:
                    # Convert to appropriate type (float for timing values)
                    macro._settings[sel_key] = float(new_val)
                    print(f"Updated {sel_key} to {macro._settings[sel_key]}")
                except ValueError:
                    print("Invalid value. No changes made.")
            else:
                print("Cancelled.")
        elif choice == '4':
            print("Which hotkey would you like to change?")
            print(f" [1] Primary hotkey (current: {macro.hotkey}) - E>Click>Shift")
            print(f" [2] Alt hotkey (current: {macro.alt_hotkey}) - E>Click>F")
            hotkey_choice = input("Enter number or leave blank to cancel: ").strip()
            
            if hotkey_choice == '1':
                new_hotkey = input(f"Enter new primary hotkey (current: {macro.hotkey}): ").strip()
                if new_hotkey and len(new_hotkey) == 1:
                    macro.hotkey = new_hotkey.lower()
                    print(f"Primary hotkey changed to '{macro.hotkey}'")
                    # Restart listener with new hotkey
                    if macro.listener:
                        macro.listener.stop()
                    macro.start_listener()
                else:
                    print("Invalid hotkey. Must be a single character.")
            elif hotkey_choice == '2':
                new_hotkey = input(f"Enter new alt hotkey (current: {macro.alt_hotkey}): ").strip()
                if new_hotkey and len(new_hotkey) == 1:
                    macro.alt_hotkey = new_hotkey.lower()
                    print(f"Alt hotkey changed to '{macro.alt_hotkey}'")
                    # Restart listener with new hotkey
                    if macro.listener:
                        macro.listener.stop()
                    macro.start_listener()
                else:
                    print("Invalid hotkey. Must be a single character.")
            else:
                print("Cancelled.")
        elif choice == '5':
            print("Which sequence would you like to test?")
            print(" [1] Primary sequence (E > Click > Shift)")
            print(" [2] Alt sequence (E > Click > F)")
            test_choice = input("Enter number: ").strip()
            
            if test_choice == '1':
                print("Testing primary sequence...")
                macro.perform_sequence()
                print("Primary sequence completed.")
            elif test_choice == '2':
                print("Testing alt sequence...")
                macro.perform_alt_sequence()
                print("Alt sequence completed.")
            else:
                print("Invalid choice.")
        elif choice == '6':
            print("Exiting...")
            if macro.listener:
                macro.listener.stop()
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == '__main__':
    main()
