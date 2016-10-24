#!/usr/bin/env python

from __future__ import print_function
import hashlib
import subprocess
import sys
import os
import time


def get_output(program, stdin):
    p = subprocess.Popen([os.getenv('BF_RUN', './jit-x64'), program] +
                         sys.argv[1:], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    start = time.time()
    output = p.communicate(input=stdin)[0]
    return output, time.time() - start


expected_output_hashes = [
    [('progs/awib.b', open('progs/awib.b', 'rb').read()), '3b4f9a78ec3ee32e05969e108916a4affa0c2bba'],
    ['progs/mandelbrot.b', 'b77a017f811831f0b74e0d69c08b78e620dbda2b'],
    ['progs/hanoi.b', '32cdfe329039ce63531dcd4b340df269d4fd8f7f'],
]

for filename, expected_hash in expected_output_hashes:
    stdin = ''
    if isinstance(filename, tuple):
        filename, stdin = filename
    output, elapsed = get_output(filename, stdin)
    actual_hash = hashlib.sha1(output).hexdigest()

    print(filename.ljust(24), end='')
    if actual_hash == expected_hash:
        print('GOOD\t%.1fms' % (elapsed * 1000))
    else:
        print('bad output: expected %s got %s' % (
            expected_hash, actual_hash))
        print(output.decode('ascii', 'replace'))
