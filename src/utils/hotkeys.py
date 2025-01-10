import keyboard
import threading
import time
import logging
from src.config.constants import HOTKEYS

logger = logging.getLogger(__name__)

class HotkeyManager:
    def __init__(self, app):
        self.app = app
        self.running = False
        self.thread = None
        self._last_trigger_time = {}
        
    def start(self):
        """Start hotkey monitoring using hybrid approach"""
        self.running = True
        self.thread = threading.Thread(target=self._monitor_toggle_hotkeys)
        self.thread.daemon = True
        self.thread.start()
        
        # Register event handler specifically for the macro trigger
        keyboard.on_press_key(HOTKEYS['trigger_auto_bubble'], 
            lambda _: self._handle_macro_trigger())
        
        logger.info("Hotkey monitoring started")
    
    def stop(self):
        """Stop hotkey monitoring"""
        self.running = False
        if self.thread:
            self.thread.join()
        keyboard.unhook_all()
        logger.info("Hotkey monitoring stopped")
    
    def _handle_macro_trigger(self):
        """Handle macro trigger events"""
        try:
            current_time = time.time()
            key = HOTKEYS['trigger_auto_bubble']
            
            # Queue the command immediately
            self.app.command_queue.put('trigger_auto_bubble')
            logger.debug(f"Macro trigger at {current_time}")
            
        except Exception as e:
            logger.error(f"Error handling macro trigger: {e}")
    
    def _monitor_toggle_hotkeys(self):
        """Monitor toggle-type hotkeys using polling"""
        while self.running:
            try:
                # Check toggle-type hotkeys
                if keyboard.is_pressed(HOTKEYS['toggle_overlay']):
                    self.app.command_queue.put('toggle_overlay')
                    time.sleep(0.3)
                elif keyboard.is_pressed(HOTKEYS['clear_fields']):
                    self.app.command_queue.put('clear_fields')
                    time.sleep(0.3)
                elif keyboard.is_pressed(HOTKEYS['select_area']):
                    self.app.command_queue.put('select_area')
                    time.sleep(0.3)
                elif keyboard.is_pressed(HOTKEYS['copy_translation']):
                    self.app.command_queue.put('copy_translation')
                    time.sleep(0.3)
                elif keyboard.is_pressed(HOTKEYS['toggle_auto_bubble']):
                    self.app.command_queue.put('toggle_auto_bubble')
                    time.sleep(0.3)
                
            except Exception as e:
                logger.error(f"Error in hotkey monitoring: {e}")
            
            time.sleep(0.1)  # Small sleep to prevent high CPU usage