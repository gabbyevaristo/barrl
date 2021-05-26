BOARD = 1
OUT = 1
IN = 1
HIGH = 1
LOW = 1

def setmode(*args, **kwargs):
    print("moch gpio setmode")

def setup(*args, **kwargs):
    print("moch gpio setup")
    
def output(*args, **kwargs):
    print("moch gpio output")
    
def cleanup():
    print("moch gpio clean up")
    
def setwarnings(*args, **kwargs):
    print("set warnings")