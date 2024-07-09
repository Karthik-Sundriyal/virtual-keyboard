import tkinter as tk
from tkinter import ttk
import pyautogui
from pynput import mouse
import win32gui
import win32con

class OnScreenKeyboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("On-Screen Keyboard")
        self.geometry("600x300")
        self.overrideredirect(True)  # Remove window decorations
        self.attributes('-topmost', True)  # Always on top
        self.bind('<Escape>', self.quit)
        
        self.key_frame = ttk.Frame(self)
        self.key_frame.pack(pady=10)
        
        self.create_keyboard()

        # Create listener to detect mouse clicks
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()

    def create_keyboard(self):
        # Define the layout of the keys
        keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        ]
        
        # Create the keys
        for row, key_row in enumerate(keys):
            for col, key in enumerate(key_row):
                ttk.Button(self.key_frame, text=key, width=5,
                           command=lambda key=key: self.press_key(key)).grid(row=row, column=col, padx=5, pady=5)
    
    def press_key(self, key):
        # Function to simulate key press in the active window
        pyautogui.typewrite(key)
    
    def on_click(self, x, y, button, pressed):
        # Callback function for mouse click listener
        if pressed:
            # Simulate key press only if clicked inside the keyboard window
            hwnd = self.winfo_id()
            rect = win32gui.GetWindowRect(hwnd)
            if rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]:
                key = self.get_key_from_coordinates(x, y)
                if key:
                    self.press_key(key)
    
    def get_key_from_coordinates(self, x, y):
        # Determine which key was clicked based on mouse coordinates
        for child in self.key_frame.winfo_children():
            if child.winfo_containing(x, y) == child:
                return child.cget("text")
        return None
    
    def quit(self, event=None):
        # Stop mouse listener and destroy the window
        self.mouse_listener.stop()
        self.destroy()

def main():
    # Initialize the on-screen keyboard application
    keyboard_app = OnScreenKeyboard()
    keyboard_app.mainloop()

if __name__ == "__main__":
    main()
