import unittest
import queue
import keyboard
import threading
import time
from unittest.mock import MagicMock, patch
from src.utils.hotkeys import HotkeyManager
from src.core.auto_bubble import AutoHealMacro

class TestHotkeyChain(unittest.TestCase):
    def setUp(self):
        # Create a mock app with a command queue
        self.command_queue = queue.Queue()
        self.mock_app = MagicMock()
        self.mock_app.command_queue = self.command_queue
        
        # Create actual instances of the key components
        self.macro = AutoHealMacro()
        self.hotkey_manager = HotkeyManager(self.mock_app)
        
        # Create a file for output testing
        self.test_file = 'keypress_test.txt'
        
    def tearDown(self):
        self.hotkey_manager.stop()
        try:
            import os
            os.remove(self.test_file)
        except:
            pass

    def test_hotkey_to_macro_chain(self):
        """Test the entire chain from hotkey press to macro execution"""
        
        # Start the hotkey manager
        self.hotkey_manager.start()
        
        # Create a way to track actual keypresses
        actual_keypresses = []
        
        def key_logger(event):
            if event.event_type == 'down':
                actual_keypresses.append(event.name)
                with open(self.test_file, 'a') as f:
                    f.write(event.name)
        
        # Register our key logger
        keyboard.hook(key_logger)
        
        try:
            # Simulate pressing 'x' (or whatever HOTKEYS['trigger_macro'] is set to)
            keyboard.press_and_release('x')
            
            # Give some time for the event to propagate
            time.sleep(0.2)
            
            # Check if the command was put in the queue
            try:
                command = self.command_queue.get_nowait()
                self.assertEqual(command, 'trigger_macro')
            except queue.Empty:
                self.fail("No command was queued after hotkey press")
            
            # Verify the keypress output
            with open(self.test_file, 'r') as f:
                content = f.read()
                self.assertIn('x', content)
                # If working correctly, should see 'xe'
                self.assertIn('e', content)
            
            # Also verify the actual sequence of keypresses
            self.assertIn('x', actual_keypresses)
            self.assertIn('e', actual_keypresses)
            
        finally:
            keyboard.unhook(key_logger)

    def test_timing_consistency(self):
        """Test timing consistency between hotkey press and macro execution"""
        timing_results = []
        
        for _ in range(10):  # Run 10 tests
            start_time = time.time()
            
            # Simulate pressing the hotkey
            keyboard.press_and_release('x')
            
            # Wait for command to appear in queue
            try:
                self.command_queue.get(timeout=1)
                end_time = time.time()
                timing_results.append(end_time - start_time)
            except queue.Empty:
                timing_results.append(None)
            
            time.sleep(0.5)  # Wait between tests
        
        # Analyze timing results
        failed_triggers = timing_results.count(None)
        successful_triggers = len(timing_results) - failed_triggers
        
        print(f"\nTiming Analysis:")
        print(f"Successful triggers: {successful_triggers}/10")
        print(f"Failed triggers: {failed_triggers}/10")
        if successful_triggers > 0:
            avg_time = sum(t for t in timing_results if t is not None) / successful_triggers
            print(f"Average response time: {avg_time*1000:.2f}ms")
            
        # Test should fail if we have any failed triggers
        self.assertEqual(failed_triggers, 0, "Some hotkey triggers failed to register")

if __name__ == '__main__':
    unittest.main()