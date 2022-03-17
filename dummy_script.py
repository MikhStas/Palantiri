import time
import signal
import sys
from functools import partial


def stage3(signal, frame, message):
    print('stage 3')
    print(message)
    sys.exit(0)
    
    

print('stage1')
sigint_handler = partial(stage3, message='Bye!')
signal.signal(signal.SIGINT, sigint_handler)

while True:
    print('stage2')
    time.sleep(1)

