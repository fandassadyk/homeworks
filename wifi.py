import json
import numpy as np
import matplotlib.pyplot as plt


def decoder(values, seq):
    elements = np.convolve(values, seq, mode='full')
    bits = []

    i = 1
    while True:
        if (elements[i] > 43 or elements[i] < -40):
            if elements[i-1] < elements[i] and elements[i+1] < elements[i]:
                bits.append(1)
            elif elements[i-1] > elements[i] and elements[i+1] > elements[i]:
                bits.append(0)
        i += 1
        if i > (len(elements) - 1):
            break

    answer = bits2signal(bits)
    return answer


def bits2signal(bits):
    byte_array = np.packbits(bits)
    byte_str = byte_array.tobytes()
    s = byte_str.decode(encoding='ascii')
    return s


barker_seq = (1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1)
seq = (np.repeat(barker_seq, 5))[::-1]

values = np.loadtxt("Садыков.txt", delimiter='\t')

answer = decoder(values, seq)


dict = {"message": answer}
myFile = open("wifi.json", 'w')
json.dump(dict, myFile)
myFile.close()
