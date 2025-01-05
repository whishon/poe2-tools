import keyboard as kb
import time
import pyperclip
from tooltip import create_tooltip_window
from item_parser import parse_item_stats, format_item_summary


def send_item_parse_command():
    """Parse item data from clipboard and display in tooltip."""
    try:
        time.sleep(0.2)  # Short delay for clipboard to update
        clipboard_text = pyperclip.paste()
        if not clipboard_text:
            return
            
        stats = parse_item_stats(clipboard_text)
        summary = format_item_summary(stats)
        
        # Get or create tooltip window
        tooltip = create_tooltip_window()
        tooltip.show_tooltip(summary)
        
    except ValueError as e:
        print(f"Error parsing item: {e}")

def send_hideout_command():
    # Send the keystrokes
    kb.press_and_release('enter')
    time.sleep(0.1)  # Short delay
    kb.write('/hideout')
    time.sleep(0.1)  # Short delay
    kb.press_and_release('enter')

def send_xp_command():
    # Send the keystrokes
    kb.press_and_release('enter')
    time.sleep(0.1)  # Short delay
    kb.write('/reset_xp')
    time.sleep(0.1)  # Short delay
    kb.press_and_release('enter')

def send_leech_command():
    # Send the keystrokes
    kb.press_and_release('enter')
    time.sleep(0.1)  # Short delay
    kb.write(r'%stay close during breaches. do not loot splinters, currency or uniques. do not loot during breaches. do not die.'.upper())
    time.sleep(0.1)  # Short delay
    kb.press_and_release('enter')

def exit_script():
    print("Script terminated.")
    import sys
    sys.exit()