### bfi.py, the Brainfuck Interpreter
### Riley Pinkerton, 7/27/2014

import argparse
import sys

def run(code):
    '''Runs a string of Brainfuck code'''
    # Initialize the data array. Only allocate cells we use for speed and
    # compactness
    data = [0]
    # Initialize the instruction array. Filter the array ahead of time for speed
    inst = list(code)
    inst = [it for it in inst if it in list("<>.,+-[]")]
    # Pointers for the current position in the instruction and data arrays
    dp = 0
    ip = 0
    # A value to keep track of the length of the data array, so that we don't
    # need to take it's length all the time
    dlen = 1
    # A stack for remembering the locations of nested while loops
    loops = []

    # Main loop, run until instructions are exhausted
    while ip != len(inst):
        if inst[ip] == "+":
            data[dp] += 1
        elif inst[ip] == "-":
            data[dp] -= 1
        elif inst[ip] == ">":
            if dp == 29999:
                print "Data overflow!"
                exit(1)
            if dp == dlen - 1:
                data.append(0)
                dp += 1
                dlen += 1
            else:
                dp += 1
        elif inst[ip] == "<":
            if dp == 0:
                print "Data underflow!"
                exit(1)
            dp -= 1
        elif inst[ip] == "[":
            if data[dp] == 0:
                # Move until the proper closing ]
                count = 1
                while count != 0:
                    ip += 1
                    if inst[ip] == "[":
                        count += 1
                    elif inst[ip] == "]":
                        count -= 1
            else:
                loops.append(ip)
        elif inst[ip] == "]":
            ip = loops.pop() - 1
        elif inst[ip] == ",":
            data[dp] = ord(raw_input())
        elif inst[ip] == ".":
            sys.stdout.write(chr(data[dp]))

        # Move to the next instruction
        ip += 1
        

if __name__ == '__main__':

    # Read arguments
    parser = argparse.ArgumentParser(description="A Brainfuck Interpreter")
    parser.add_argument("-c", help="Read input from command line", action="store_true")
    parser.add_argument("input", help="Brainfuck Code")

    args = parser.parse_args()

    cmdline = args.c
    data_in = args.input

    if cmdline:
        run(data_in)
    else:
        file = open(data_in, "r")
        code = ""
        for line in file:
            ''.join([code, line])
        run(code)
