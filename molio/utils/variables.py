import os

try:
    TERM_SIZE = os.get_terminal_size().columns
except:
    TERM_SIZE = 80