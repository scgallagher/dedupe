import os
import sys

class Deduplicate:

    def __init__(self, report_file_path='report.txt', print_to_console=False):

        self.report_file = open(report_file_path, "w")
        self.print_to_console = print_to_console

    # Generates a report that details the total amount of duplicate records NOT
    # including the original record.  For example, if Key-A is in the file 3 times,
    # a count of 2 will be added to the overall duplicate count.
    def generate_report(self, seen, input_file_path, log_keys=False):

        self.report_file.write(input_file_path + '\n')
        if self.print_to_console:
            print(input_file_path)

        dupe_count = 0
        # Number of keys with one or more duplicate
        dupe_key_count = 0

        for key in seen:

            count = seen.get(key)
            dupe_count += count - 1

            if count > 1:
                dupe_key_count += 1
                if log_keys:
                    report_line = '    ' + key + ': ' + str(count) + '\n'
                    self.report_file.write(report_line)

        self.report_file.write('  Keys With Duplicates: ' + str(dupe_key_count) + '\n')
        self.report_file.write('  Duplicate Count:      ' + str(dupe_count) + '\n\n')
        if self.print_to_console:
            print('  Keys With Duplicates: ' + str(dupe_key_count))
            print('  Duplicate Count:      ' + str(dupe_count) + '\n')

    def dedupe_file(self, input_file_path, key_index=None, delimiter='|', log_keys=False, debug=False):

        input_file_path_arr = input_file_path.split('.')
        output_file_path = input_file_path_arr[0] + '_deduped.' + input_file_path_arr[1]

        input_file = open(input_file_path, "r")
        output_file = open(output_file_path, "w")

        seen = {}
        dupe_count = 0

        line = input_file.readline()
        while line:

            line = line.strip()
            if key_index:
                key_index_type = type(key_index)
                if key_index_type is int:
                    key = line.split(delimiter)[key_index]
                elif key_index_type is list:
                    key = ''
                    line_arr = line.split(delimiter)
                    for i in key_index:
                        key += line_arr[i]
                else:
                    print('ERROR: Invalid key index type: ' + str(key_index_type))
            else:
                key = line

            if debug:
                print(key)

            count = seen.get(key)
            if count == None:
                output_file.write(line + '\n')
                seen[key] = 1
            else:
                seen[key] = count + 1
                dupe_count += 1

            line = input_file.readline()

        self.generate_report(seen, input_file_path, log_keys)

        input_file.close()
        output_file.close()

    def dedupe_batch(self, input_dir, log_keys=False):

        input_files = [file for file in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, file))]

        os.chdir(input_dir)

        for file in input_files:

            self.dedupe_file(file, log_keys)

    def check_file(self, input_file_path, key_index=None, delimiter='|'):

        input_file = open(input_file_path, "r")

        seen = {}
        row_count = 1

        line = input_file.readline()
        while line:

            if key_index:
                key_index_type = type(key_index)
                if key_index_type is int:
                    key = line.strip().split(delimiter)[key_index]
                elif key_index_type is list:
                    key = ''
                    line_arr = line.split(delimiter)
                    for i in key_index:
                        key += line_arr[i]
                else:
                    print('ERROR: Invalid key index type: ' + str(key_index_type))
            else:
                key = line.strip()

            key_exists = seen.get(key)
            if key_exists:
                print('Duplicate at row ' + str(row_count))
                sys.exit(2)
            else:
                seen[key] = True

            row_count += 1
            line = input_file.readline()

        print('No duplicates found')
        input_file.close()

    def __del__(self):

        self.report_file.close()
