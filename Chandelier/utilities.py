from __future__ import print_function
from datetime import datetime
import os
import sys

def errprint(*args, **kwargs):
    print(datetime.now(), *args, file=sys.stderr, **kwargs)

def stdprint(*args, **kwargs):
    print(datetime.now(), *args, file=sys.stdout, **kwargs)
