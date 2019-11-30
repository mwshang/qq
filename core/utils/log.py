
from core.utils.config import ENABLED_LOG;

def log(msg):
    if ENABLED_LOG:
        print(msg)