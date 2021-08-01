from common import *
from helpfun import get_column, get_row, to_binary, left_shift

def generate_key(key_in):
  
  key_out =[]
  for i in key_in:
    key_out.extend(to_binary(ord(i)))
  
    C = []
    D = []
    r = []
    for i in range(28):
        C.append(key_out[PC1_C[i]])
    for i in range(28):
        D.append(key_out[PC1_D[i]])
    for i in range(0, 16):
        if i in [0, 1, 8, 15]:
            C = left_shift(C, 1)
            D = left_shift(D, 1)
        else:
            C = left_shift(C, 2)
            D = left_shift(D, 2)
        CD = []
        CD.extend(C)
        CD.extend(D)
        dummy = []
        for i in range(48):
            dummy.append(CD[PC2[i]])
        r.append(dummy)
    return r