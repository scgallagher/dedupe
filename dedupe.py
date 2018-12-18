import sys
import os
from lib.deduplicate import Deduplicate

def parse_options(options_arr):

    options = {}

    if options_arr[1][0] != '-':
        options['batch_mode'] = False
        options['input_file_path'] = options_arr[1]
    else:
        i = 1
        while i < len(options_arr):
            if options_arr[i] == '-d':
                options['batch_mode'] = True
                options['input_dir'] = options_arr[i + 1]
            else:
                print('Error: Unknown option,', options_arr[i])
            i += 2

    return options

if (len(sys.argv) < 2):
    print('\nUsage: dedupe.py <input file>')
    sys.exit(1)

options = parse_options(sys.argv)
batch_mode = options.get('batch_mode')
dd = Deduplicate()

if batch_mode:
    input_dir = options.get('input_dir')
    dd.dedupe_batch(input_dir)
else:
    input_file_path = options.get('input_file_path')
    dd.dedupe_file(input_file_path, key_index=[0, 1, 2], log_keys=True)
