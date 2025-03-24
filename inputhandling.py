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
    move = get_key()
    if move == 'w' or move == '\x1b[A':  
        return 'UP'
    elif move == 's' or move == '\x1b[B':  
        return 'DOWN'
    elif move == 'a' or move == '\x1b[D':  
        return 'LEFT'
    elif move == 'd' or move == '\x1b[C':  
        return 'RIGHT'
    elif move == 'c':  
        return 'RESTART'
    elif move == 'q':  
        return 'QUIT'
    elif move == 'p':  
        return 'TOGGLE_AI'
    return None