import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.styles.theme import OVERLAY_THEME, FONTS, COLORS
from src.core.auto_bubble import AutoHealMacro
from src.core.auto_clone import AutoCloneMacro

class MacroSettingsModal(tk.Toplevel):
    def __init__(self, parent, auto_bubble_macro: AutoHealMacro, auto_clone_macro: AutoCloneMacro):
        super().__init__(parent)
        self.auto_bubble_macro = auto_bubble_macro
        self.auto_clone_macro = auto_clone_macro
        
        # Configure window
        self.title("Macro Settings")
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
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True, pady=(0, 20))
        
        # Auto Bubble tab
        bubble_frame = tk.Frame(
            notebook,
            bg=OVERLAY_THEME['frame']['bg'],
            padx=10,
            pady=10
        )
        notebook.add(bubble_frame, text='Auto Bubble')
        
        # Auto Clone tab
        clone_frame = tk.Frame(
            notebook,
            bg=OVERLAY_THEME['frame']['bg'],
            padx=10,
            pady=10
        )
        notebook.add(clone_frame, text='Auto Clone')
        
        # Setup entries for Auto Bubble
        self.bubble_entries = {}
        bubble_settings = [
            ('look_down_amount', 'Look Down Amount', self.auto_bubble_macro.look_down_amount),
            ('up_movement_ratio', 'Up Movement Ratio', self.auto_bubble_macro.up_movement_ratio),
            ('move_down_step', 'Move Down Step Size', self.auto_bubble_macro.move_down_step),
            ('move_up_step', 'Move Up Step Size', self.auto_bubble_macro.move_up_step),
            ('heal_delay', 'Heal Delay', self.auto_bubble_macro.heal_delay)
        ]
        
        for setting_id, label, current_value in bubble_settings:
            frame = tk.Frame(
                bubble_frame,
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
            entry.insert(0, str(current_value))
            
            self.bubble_entries[setting_id] = entry
            
        # Setup entries for Auto Clone
        self.clone_entries = {}
        clone_settings = [
            ('sequence_delay', 'Key Sequence Delay', self.auto_clone_macro.sequence_delay)
        ]
        
        for setting_id, label, current_value in clone_settings:
            frame = tk.Frame(
                clone_frame,
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
            entry.insert(0, str(current_value))
            
            self.clone_entries[setting_id] = entry
        
        # Buttons
        button_frame = tk.Frame(
            main_frame,
            bg=OVERLAY_THEME['frame']['bg']
        )
        button_frame.pack(fill='x')
        
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
        """Save settings back to macros"""
        try:
            # Update Auto Bubble settings
            self.auto_bubble_macro.look_down_amount = int(self.bubble_entries['look_down_amount'].get())
            self.auto_bubble_macro.up_movement_ratio = float(self.bubble_entries['up_movement_ratio'].get())
            self.auto_bubble_macro.move_down_step = int(self.bubble_entries['move_down_step'].get())
            self.auto_bubble_macro.move_up_step = int(self.bubble_entries['move_up_step'].get())
            self.auto_bubble_macro.heal_delay = float(self.bubble_entries['heal_delay'].get())
            
            # Update Auto Clone settings
            self.auto_clone_macro.sequence_delay = float(self.clone_entries['sequence_delay'].get())
            
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror(
                "Invalid Input",
                "Please ensure all values are numbers.\n\n"
                "Auto Bubble:\n"
                "- Look Down Amount: Integer\n"
                "- Up Movement Ratio: Decimal between 0 and 1\n"
                "- Step Sizes: Integer\n"
                "- Heal Delay: Decimal in seconds\n\n"
                "Auto Clone:\n"
                "- Sequence Delay: Decimal in seconds"
            )