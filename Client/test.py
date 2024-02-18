from kyber1024 import Kyber
import sys

print(sys.getsizeof(Kyber().keygen()[1]))