import string
from random import SystemRandom

print(''.join(SystemRandom().choices(string.ascii_letters + string.punctuation, k=64)))
