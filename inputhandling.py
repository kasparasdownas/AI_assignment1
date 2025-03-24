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
    Supports WASD and arrow keys.
    """
    move = get_key()
    if move == 'w' or move == '\x1b[A':  # up
        return 'UP'
    elif move == 's' or move == '\x1b[B':  # down
        return 'DOWN'
    elif move == 'a' or move == '\x1b[D':  # left
        return 'LEFT'
    elif move == 'd' or move == '\x1b[C':  # right
        return 'RIGHT'
    elif move == 'c':  # restart
        return 'RESTART'
    elif move == 'q':  # quit
        return 'QUIT'
    elif move == 'p':  # toggle AI
        return 'TOGGLE_AI'
    return None