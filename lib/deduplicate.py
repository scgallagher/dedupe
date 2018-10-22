import os
import sys

class Deduplicate:

    def __init__(self, report_file_path='report.txt'):

        self.report_file = open(report_file_path, "w")

    # Generates a report that details the total amount of duplicate records NOT
    # including the original record.  For example, if Key-A is in the file 3 times,
    # a count of 2 will be added to the overall duplicate count.
    def generate_report(self, seen, input_file_path, log_keys=False):

        self.report_file.write(input_file_path + '\n')

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

    def dedupe_file(self, input_file_path, log_keys=False):

        output_file_path = input_file_path + ".deduped"

        input_file = open(input_file_path, "r")
        output_file = open(output_file_path, "w")

        seen = {}
        dupe_count = 0

        line = input_file.readline()
        while line:

            line = line.strip()
            count = seen.get(line)
            if count == None:
                output_file.write(line + "\n")
                seen[line] = 1
            else:
                seen[line] = count + 1
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

    def __del__(self):

        self.report_file.close()