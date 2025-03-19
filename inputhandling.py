import sys
import termios
import tty

def get_key():
    """
    Captures arrow key escape sequences on Unix-like systems.
    This function returns a string representing the key pressed.
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(3)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def get_move():
    """
    Returns a move from the user.
    Supports WASD and arrow key sequences.
    """
    move = input("Enter move (WASD or arrow keys, Q to quit): ").upper()
    return move