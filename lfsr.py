#!/usr/bin/env python3

import sys
import os
import time

def main():
    while True:
        action = int(input("Choose action: \n [1]: set lfsr size/state \n [2]: get n stream bits \n [3]: exit \n"))
        if action == 1:
            lfsr = get_lfsr()
            indexes = get_indexes(len(lfsr))
            print("LFSR set to: ", lfsr, " with taps at indices ", indexes)
        elif action == 2:
            if not 'lfsr' in locals():
                print("LFSR not set, please set it first")
            else:
                generate_n_bits(lfsr, indexes)
        elif action == 3:
            print("Exiting...")
            return

def step_lfsr(lfsr, indexes):
    pop_bit = lfsr[-1]

    #invert indexes
    for idx in indexes:
        idx = len(lfsr) - 1 - idx

    #xor all indices to get new bit
    for idx, bit in enumerate(lfsr):
        if idx in indexes:
            if idx == indexes[0]:
                new_bit = bit
            else:
                new_bit ^= bit
    
    lfsr = [new_bit] + lfsr[:-1]
    return lfsr, pop_bit

def get_lfsr():
    size = int(input("Enter size of LFSR: "))
    clear_last_line()
    lfsr = [0 for _ in range(size)]
    for i in range(size):
        bit = input("Enter bit {}: ".format(i))
        clear_last_line()
        if bit not in ("0","1"):
            raise ValueError("Bit must be 0 or 1")
        lfsr[i] = int(bit)
    return lfsr

def get_indexes(size):
    numindexes = int(input("Enter number of tap bits needed: "))
    clear_last_line()
    if numindexes >= size:
        raise ValueError("Number of tap bits must be less than size of LFSR")
    indexes = []
    for i in range(int(numindexes)):
        index = int(input("Enter tap bit index {}: ".format(i)))
        clear_last_line()
        if index >= size or index < 0:
            raise ValueError("Index must be between 0 and size-1")
        indexes.append(index)
    return indexes

def generate_n_bits(lfsr, indexes):
    output_mode = int(input("Choose output mode: \n [1]: Text file \n [2]: Console \n [3]: Both \n"))
    clear_last_line()

    if output_mode == 1 or output_mode == 3:
        filename = input("Enter a name for the output file: ").strip()
        clear_last_line
        
        if not filename:
            filename = "output"
        
        if not filename.endswith(".txt"):
            filename += ".txt"

    n = int(input("Enter number of bits to generate: "))
    print("initial state: ",lfsr, indexes)

    if output_mode == 1 or output_mode == 3:
        with open(filename, 'w') as f:
            for i in range(n):
                lfsr, pop_bit = step_lfsr(lfsr, indexes)
                if output_mode == 3:
                    print(lfsr, " -> ", pop_bit)
                f.write(str(pop_bit))
        print("Output written to ", filename)

    elif output_mode == 2:
        for i in range(n):
            lfsr, pop_bit = step_lfsr(lfsr, indexes)
            print(lfsr, " -> ", pop_bit)

def clear_last_line():
    sys.stdout.write('\x1b[1A')  # Move cursor up
    sys.stdout.write('\x1b[2K')  # Clear the line
    sys.stdout.flush()

if __name__ == "__main__":
    main()
