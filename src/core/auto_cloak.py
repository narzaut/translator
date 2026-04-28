import time
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Button, Listener as MouseListener
from pynput.mouse import Controller as MouseController
from pynput import keyboard as pkbd

class SimpleMacro:
    def __init__(self):
        self.running = True
        self.paused = False
        self.hotkey_x = 'x'  # Press 'x' to trigger shift + right click
        self.hotkey_z = 'z'  # Press 'z' to trigger shift + e + shift
        
        # Controllers for keyboard and mouse
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.keyboard_listener = None
        self.mouse_listener = None
        
        # Settings for X sequence (shift + right click)
        self.shift_duration = 0.05
        self.wait_delay = 0.265  # Wait time between shift and right click
        
        # Settings for Z sequence (shift + e + shift)
        self.z_shift1_duration = 0.05      # First shift hold duration
        self.z_delay_shift_to_e = 0.26      # Delay between first shift and E
        self.z_e_duration = 0.05           # E key hold duration  
        self.z_delay_e_to_shift = 0.5      # Delay between E and second shift
        self.z_shift2_duration = 0.05      # Second shift hold duration
        
    def precise_sleep(self, duration):
        """More precise sleep timing"""
        start = time.perf_counter()
        while time.perf_counter() - start < duration:
            pass
    
    def press_shift(self, duration=None):
        """Press and release shift key"""
        if duration is None:
            duration = self.shift_duration
        self.keyboard.press(Key.shift)
        self.precise_sleep(duration)
        self.keyboard.release(Key.shift)
    
    def press_e(self, duration=None):
        """Press and release E key"""
        if duration is None:
            duration = self.z_e_duration
        self.keyboard.press('e')
        self.precise_sleep(duration)
        self.keyboard.release('e')
    
    def right_click(self):
        """Simulate right mouse click using pynput with press/release"""
        print("Performing right click...")
        self.mouse.press(Button.right)
        self.precise_sleep(0.05)
        self.mouse.release(Button.right)
        self.precise_sleep(0.01)
    
    def perform_x_action(self):
        """Perform the X sequence: shift + wait + right click"""
        if self.paused:
            print("Macro is paused - X sequence skipped")
            return
            
        try:
            print("Starting X sequence (shift + right click)...")
            
            # Press shift
            print("Pressing shift...")
            self.press_shift()
            
            # Wait
            print(f"Waiting {self.wait_delay} seconds...")
            self.precise_sleep(self.wait_delay)
            
            # Right click
            self.right_click()
            
            print("X sequence complete!")
            
        except Exception as e:
            print(f"Error during X action: {e}")
    
    def perform_z_action(self):
        """Perform the Z sequence: shift + e + shift"""
        if self.paused:
            print("Macro is paused - Z sequence skipped")
            return
            
        try:
            print("Starting Z sequence (shift + e + shift)...")
            
            # First shift
            print(f"Pressing first shift ({self.z_shift1_duration}s)...")
            self.keyboard.press(Key.shift)
            self.precise_sleep(self.z_shift1_duration)
            self.keyboard.release(Key.shift)
            
            # Delay between shift and E
            print(f"Waiting {self.z_delay_shift_to_e}s before E...")
            self.precise_sleep(self.z_delay_shift_to_e)
            
            # Press E
            print(f"Pressing E ({self.z_e_duration}s)...")
            self.press_e()
            
            # Delay between E and second shift
            print(f"Waiting {self.z_delay_e_to_shift}s before second shift...")
            self.precise_sleep(self.z_delay_e_to_shift)
            
            # Second shift
            print(f"Pressing second shift ({self.z_shift2_duration}s)...")
            self.keyboard.press(Key.shift)
            self.precise_sleep(self.z_shift2_duration)
            self.keyboard.release(Key.shift)
            
            print("Z sequence complete!")
            
        except Exception as e:
            print(f"Error during Z action: {e}")
    
    def toggle_pause(self):
        """Toggle pause state"""
        self.paused = not self.paused
        status = "PAUSED" if self.paused else "ACTIVE"
        print(f"\n*** MACRO {status} ***")
        if self.paused:
            print("X and Z hotkeys disabled. Press Mouse Button 5 to resume.")
        else:
            print("X and Z hotkeys enabled. Press Mouse Button 5 to pause.")
    
    def start_listener(self):
        """Start global hotkey and mouse listeners"""
        def on_key_press(key):
            try:
                if key.char == self.hotkey_x:
                    self.perform_x_action()
                elif key.char == self.hotkey_z:
                    self.perform_z_action()
            except AttributeError:
                # Non-character keys don't have .char
                pass

        def on_mouse_click(x, y, button, pressed):
            # Only respond to button press (not release) and only for mouse button 5
            if pressed and button == Button.x2:  # x2 is mouse button 5 (side button)
                self.toggle_pause()

        # Start keyboard listener
        self.keyboard_listener = pkbd.Listener(on_press=on_key_press)
        self.keyboard_listener.daemon = True
        self.keyboard_listener.start()
        
        # Start mouse listener
        self.mouse_listener = MouseListener(on_click=on_mouse_click)
        self.mouse_listener.daemon = True
        self.mouse_listener.start()

def main():
    macro = SimpleMacro()
    macro.start_listener()

    print("\nDual Macro System")
    print(f"Hotkeys:")
    print(f"  '{macro.hotkey_x}' - Shift + Right Click")
    print(f"  '{macro.hotkey_z}' - Shift + E + Shift")
    print(f"  'Mouse Button 5' - Pause/Resume macros")
    print("Note: Using pynput for all inputs (no root required)")
    print(f"\nMacro status: {'PAUSED' if macro.paused else 'ACTIVE'}")

    while True:
        print("\nCommands:")
        print(" [1] Pause/Resume Macro")
        print(" [2] Test X sequence (shift + right click)")
        print(" [3] Test Z sequence (shift + e + shift)")
        print(" [4] Adjust X sequence timings")
        print(" [5] Adjust Z sequence timings")
        print(" [6] Show current settings")
        print(" [7] Exit")
        
        choice = input("\nSelect option: ").strip()

        if choice == '1':
            macro.toggle_pause()
        elif choice == '2':
            print("Testing X sequence...")
            macro.perform_x_action()
        elif choice == '3':
            print("Testing Z sequence...")
            macro.perform_z_action()
        elif choice == '4':
            print("\nX Sequence Timing Settings:")
            print(f" [1] Shift duration: {macro.shift_duration}")
            print(f" [2] Wait before right click: {macro.wait_delay}")
            
            sub_choice = input("Which to modify (1-2)? ").strip()
            if sub_choice == '1':
                try:
                    new_val = float(input(f"Enter new shift duration (current: {macro.shift_duration}): "))
                    macro.shift_duration = new_val
                    print(f"Shift duration set to {macro.shift_duration}")
                except ValueError:
                    print("Invalid value.")
            elif sub_choice == '2':
                try:
                    new_val = float(input(f"Enter new wait delay (current: {macro.wait_delay}): "))
                    macro.wait_delay = new_val
                    print(f"Wait delay set to {macro.wait_delay}")
                except ValueError:
                    print("Invalid value.")
                    
        elif choice == '5':
            print("\nZ Sequence Timing Settings:")
            print(f" [1] First shift duration: {macro.z_shift1_duration}")
            print(f" [2] Delay shift->E: {macro.z_delay_shift_to_e}")
            print(f" [3] E key duration: {macro.z_e_duration}")
            print(f" [4] Delay E->shift: {macro.z_delay_e_to_shift}")
            print(f" [5] Second shift duration: {macro.z_shift2_duration}")
            
            sub_choice = input("Which to modify (1-5)? ").strip()
            if sub_choice == '1':
                try:
                    new_val = float(input(f"Enter new first shift duration (current: {macro.z_shift1_duration}): "))
                    macro.z_shift1_duration = new_val
                    print(f"First shift duration set to {macro.z_shift1_duration}")
                except ValueError:
                    print("Invalid value.")
            elif sub_choice == '2':
                try:
                    new_val = float(input(f"Enter new shift->E delay (current: {macro.z_delay_shift_to_e}): "))
                    macro.z_delay_shift_to_e = new_val
                    print(f"Shift->E delay set to {macro.z_delay_shift_to_e}")
                except ValueError:
                    print("Invalid value.")
            elif sub_choice == '3':
                try:
                    new_val = float(input(f"Enter new E duration (current: {macro.z_e_duration}): "))
                    macro.z_e_duration = new_val
                    print(f"E duration set to {macro.z_e_duration}")
                except ValueError:
                    print("Invalid value.")
            elif sub_choice == '4':
                try:
                    new_val = float(input(f"Enter new E->shift delay (current: {macro.z_delay_e_to_shift}): "))
                    macro.z_delay_e_to_shift = new_val
                    print(f"E->shift delay set to {macro.z_delay_e_to_shift}")
                except ValueError:
                    print("Invalid value.")
            elif sub_choice == '5':
                try:
                    new_val = float(input(f"Enter new second shift duration (current: {macro.z_shift2_duration}): "))
                    macro.z_shift2_duration = new_val
                    print(f"Second shift duration set to {macro.z_shift2_duration}")
                except ValueError:
                    print("Invalid value.")
                    
        elif choice == '6':
            print("\nCurrent Settings:")
            print("X Sequence (shift + right click):")
            print(f"  Shift duration: {macro.shift_duration}")
            print(f"  Wait before right click: {macro.wait_delay}")
            print("\nZ Sequence (shift + e + shift):")
            print(f"  First shift duration: {macro.z_shift1_duration}")
            print(f"  Delay shift->E: {macro.z_delay_shift_to_e}")
            print(f"  E key duration: {macro.z_e_duration}")
            print(f"  Delay E->shift: {macro.z_delay_e_to_shift}")
            print(f"  Second shift duration: {macro.z_shift2_duration}")
            
        elif choice == '7':
            print("Exiting...")
            # Stop listeners
            if macro.keyboard_listener:
                macro.keyboard_listener.stop()
            if macro.mouse_listener:
                macro.mouse_listener.stop()
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()