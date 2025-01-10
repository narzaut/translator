import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.styles.theme import OVERLAY_THEME, FONTS, COLORS
from src.core.auto_bubble import AutoHealMacro

class MacroSettingsModal(tk.Toplevel):
    def __init__(self, parent, macro: AutoHealMacro):
        super().__init__(parent)
        self.macro = macro
        
        # Configure window
        self.title("Auto Bubble Settings")
        self.configure(bg=OVERLAY_THEME['window']['bg'])
        self.attributes("-topmost", True)
        
        # Center the modal relative to parent
        self.geometry("+%d+%d" % (
            parent.winfo_x() + 50,
            parent.winfo_y() + 50
        ))
        
        self.setup_ui()
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
    def setup_ui(self):
        """Setup settings UI components"""
        main_frame = tk.Frame(
            self,
            bg=OVERLAY_THEME['frame']['bg'],
            padx=20,
            pady=20
        )
        main_frame.pack(fill='both', expand=True)
        
        # Title
        tk.Label(
            main_frame,
            text="Auto Bubble Configuration",
            font=FONTS['header'],
            bg=OVERLAY_THEME['frame']['bg'],
            fg=COLORS['text']
        ).pack(pady=(0, 20))
        
        # Settings container
        settings_frame = tk.Frame(
            main_frame,
            bg=OVERLAY_THEME['frame']['bg']
        )
        settings_frame.pack(fill='x')
        
        # Create entries for each setting
        self.entries = {}
        
        # Use current values from macro
        settings = [
            ('look_down_amount', 'Look Down Amount', self.macro.look_down_amount),
            ('up_movement_ratio', 'Up Movement Ratio', self.macro.up_movement_ratio),
            ('move_down_step', 'Move Down Step Size', self.macro.move_down_step),
            ('move_up_step', 'Move Up Step Size', self.macro.move_up_step)
        ]
        
        for i, (setting_id, label, current_value) in enumerate(settings):
            frame = tk.Frame(
                settings_frame,
                bg=OVERLAY_THEME['frame']['bg']
            )
            frame.pack(fill='x', pady=(0, 10))
            
            tk.Label(
                frame,
                text=f"{label}:",
                bg=OVERLAY_THEME['frame']['bg'],
                fg=COLORS['text'],
                font=FONTS['small']
            ).pack(side='left')
            
            entry = tk.Entry(
                frame,
                **OVERLAY_THEME['entry'],
                width=10
            )
            entry.pack(side='right')
            entry.insert(0, str(current_value))  # Use current value from macro
            
            self.entries[setting_id] = entry
        
        # Buttons
        button_frame = tk.Frame(
            main_frame,
            bg=OVERLAY_THEME['frame']['bg']
        )
        button_frame.pack(fill='x', pady=(20, 0))
        
        tk.Button(
            button_frame,
            text="Save",
            command=self.save_settings,
            **OVERLAY_THEME['button']
        ).pack(side='right', padx=(5, 0))
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy,
            **OVERLAY_THEME['button_danger']
        ).pack(side='right')
        
    def save_settings(self):
        """Save settings back to macro"""
        try:
            # Update macro settings
            self.macro.look_down_amount = int(self.entries['look_down_amount'].get())
            self.macro.up_movement_ratio = float(self.entries['up_movement_ratio'].get())
            self.macro.move_down_step = int(self.entries['move_down_step'].get())
            self.macro.move_up_step = int(self.entries['move_up_step'].get())
            
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror(
                "Invalid Input",
                "Please ensure all values are numbers.\n\n"
                "Look Down Amount: Integer\n"
                "Up Movement Ratio: Decimal between 0 and 1\n"
                "Step Sizes: Integer"
            )