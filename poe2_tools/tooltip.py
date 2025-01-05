import tkinter as tk
import pyautogui

class TooltipWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.withdraw()  # Hide the main window
        
        # Create tooltip window
        self.tooltip = tk.Toplevel()
        self.tooltip.withdraw()
        self.tooltip.overrideredirect(True)  # Remove window decorations
        
        # Configure tooltip appearance
        self.tooltip.configure(bg='black')
        self.label = tk.Label(
            self.tooltip,
            justify=tk.LEFT,
            bg='black',
            fg='white',
            font=('Consolas', 10),
            padx=10,
            pady=10
        )
        self.label.pack()
        
        # Movement tracking
        self.last_pos = pyautogui.position()
        self.movement_threshold = 50  # pixels
        self.check_interval = 100  # milliseconds
        
        # Start position checking
        self.check_movement()
        
    def show_tooltip(self, text):
        self.label.config(text=text)
        x, y = pyautogui.position()
        self.last_pos = (x, y)
        
        # Position tooltip near cursor
        self.tooltip.geometry(f"+{x+20}+{y+20}")
        self.tooltip.deiconify()
        self.tooltip.lift()
        
    def hide_tooltip(self):
        self.tooltip.withdraw()
        
    def check_movement(self):
        current_pos = pyautogui.position()
        distance = ((current_pos[0] - self.last_pos[0]) ** 2 + 
                   (current_pos[1] - self.last_pos[1]) ** 2) ** 0.5
                   
        if distance > self.movement_threshold:
            self.hide_tooltip()
            
        self.window.after(self.check_interval, self.check_movement)
        
    def run(self):
        self.window.mainloop()

def create_tooltip_window():
    """Create a singleton tooltip window instance."""
    global tooltip_window
    if not hasattr(create_tooltip_window, 'tooltip'):
        create_tooltip_window.tooltip = TooltipWindow()
    return create_tooltip_window.tooltip