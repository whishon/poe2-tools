import keyboard as kb
from commands import (
    send_item_parse_command,
    send_hideout_command,
    send_xp_command,
    send_leech_command,
    exit_script
)
from tooltip import create_tooltip_window

def main():
    print("POE Tools is running...")
    print("Press Ctrl+H to send hideout command")
    print("Press Ctrl+R to send reset xp command")
    print("Press Ctrl+L to send leech command")
    print("Press Ctrl+C to send item parse command")
    print("Press Ctrl+ESC to exit")

    # Initialize tooltip window
    tooltip_window = create_tooltip_window()

    # Register all hotkeys
    kb.add_hotkey('ctrl+h', send_hideout_command)
    kb.add_hotkey('ctrl+r', send_xp_command)
    kb.add_hotkey('ctrl+l', send_leech_command)
    kb.add_hotkey('ctrl+c', send_item_parse_command)
    kb.add_hotkey('ctrl+esc', exit_script)

    # Run the tooltip window's main loop
    tooltip_window.run()

if __name__ == '__main__':
    main()