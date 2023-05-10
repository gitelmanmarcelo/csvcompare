import csv
import json
import unittest
import sys


def is_valid_row(file, row, cols):
    if len(row) != cols or not row[0].isdigit():
        raise Exception("Invalid csv record on file " + str(file))
    else:
        return True


def is_valid_and_sorted_row(file, row, idd, cols):
    if len(row) != cols or not row[0].isdigit():
        raise Exception("Invalid csv record on file " + str(file))
    if int(row[0]) <= idd:
        raise Exception("File ID is not in ascending order on file " + str(file))
    return True


def csv_compare(file1, file2):

    try:
        with open(file1, 'r') as file1, open(file2, 'r') as file2:
            csv_reader1 = csv.reader(file1)
            csv_reader2 = csv.reader(file2)

            header1 = next(csv_reader1)
            header2 = next(csv_reader2)

            if header1 != header2:
                raise Exception("Different columns in files")

            if header1[0] != 'ID':
                raise Exception("Missing ID column in file1")

            if header2[0] != 'ID':
                raise Exception("Missing ID column in file2")

            file_cols = len(header2)

            not_changed = 0
            id1 = None
            added = []
            changed = []
            deleted = []
            eof2 = False

            row2 = next(csv_reader2)
            if is_valid_row(2, row2, file_cols):
                id2 = int(row2[0])

            for row1 in csv_reader1:
                is_valid_row(1, row1, file_cols)

                if id1 is None:
                    id1 = int(row1[0])
                elif int(row1[0]) <= id1:
                    raise Exception("File ID is not in ascending order on file 1")
                else:
                    id1 = int(row1[0])

                if id1 < id2:
                    added.append(id1)

                elif id1 == id2:
                    if row1[1:] != row2[1:]:
                        changed.append(id1)
                    else:
                        not_changed = id1
                    try:
                        row2 = next(csv_reader2)

                        if is_valid_and_sorted_row(2, row2, id2, file_cols):
                            id2 = int(row2[0])
                    except StopIteration:
                        eof2 = True

                else:   # id1 > id2
                    if eof2:
                        added.append(id1)
                    else:
                        deleted.append(id2)
                        while id1 > id2:
                            try:
                                row2 = next(csv_reader2)

                                if is_valid_and_sorted_row(2, row2, id2, file_cols):
                                    id2 = int(row2[0])
                                if id2 < id1:
                                    deleted.append(id2)
                            except StopIteration:
                                eof2 = True
                                break
                        if id1 != id2:
                            added.append(id1)
                        else:   # id1 == id2
                            if row1[1:] != row2[1:]:
                                changed.append(id1)
                            try:
                                row2 = next(csv_reader2)
                                if is_valid_and_sorted_row(2, row2, id2, file_cols):
                                    id2 = int(row2[0])
                            except StopIteration:
                                eof2 = True
            if id2 > id1:
                if not_changed != id1 and changed != [] and changed[-1] != id1 and added != [] and added[-1] != id1:
                    added.append(id1)
                deleted.append(id2)

            for row2 in csv_reader2:
                if is_valid_and_sorted_row(2, row2, id2, file_cols):
                    id2 = int(row2[0])

                deleted.append(id2)

            return(json.dumps({
                                "added": added,
                                "deleted": deleted,
                                "changed": changed
                                                    }))
    except IOError:
        return "Error: Failed to open the CSV file."
    except csv.Error as e:
        return "csv Error:" + str(e)
    except Exception as e:
        return "Error:" + str(e)


class TestCsvCompare(unittest.TestCase):

    def test_01(self):
        self.assertEqual(csv_compare('.\\file1.csv', '.\\test\\file2.csv'),
                         'Error: Failed to open the CSV file.')
        self.assertEqual(csv_compare('.\\test\\file1.csv', '.\\file2.csv',),
                         'Error: Failed to open the CSV file.')
        self.assertEqual(csv_compare('.\\test\\file1.csv', '.\\test\\file2.csv',),
                         'Error: Failed to open the CSV file.')
        self.assertEqual(csv_compare('.\\ffile1.csv', '.\\ffile2.csv'),
                         'Error: Failed to open the CSV file.')
        self.assertEqual(csv_compare('.\\ffile1.csv', '.\\file2.csv',),
                         'Error: Failed to open the CSV file.')
        self.assertEqual(csv_compare('.\\file1.csv', '.\\ffile2.csv',),
                         'Error: Failed to open the CSV file.')
        self.assertEqual(csv_compare('.\\invalid1.csv', '.\\file2.csv',),
                         'Error:Different columns in files')
        self.assertEqual(csv_compare('.\\file1.csv', '.\\invalid2.csv',),
                         'Error:Different columns in files')
        self.assertEqual(csv_compare('.\\nonumber1.csv', '.\\file2.csv',),
                         'Error:Invalid csv record on file 1')
        self.assertEqual(csv_compare('.\\file1.csv', '.\\nonumber2.csv',),
                         'Error:Invalid csv record on file 2')
        self.assertEqual(csv_compare('.\\nonumber1.csv', '.\\nonumber2.csv',),
                         'Error:Invalid csv record on file 2')
        self.assertEqual(csv_compare('.\\unsorted1.csv', '.\\file2.csv',),
                         'Error:File ID is not in ascending order on file 1')
        self.assertEqual(csv_compare('.\\file1.csv', '.\\unsorted2.csv',),
                         'Error:File ID is not in ascending order on file 2')
        self.assertEqual(csv_compare('.\\unsorted1.csv', '.\\unsorted2.csv',),
                         'Error:File ID is not in ascending order on file 2')
        self.assertEqual(csv_compare('.\\badstruct1.csv', '.\\file2.csv',),
                         'Error:Invalid csv record on file 1')
        self.assertEqual(csv_compare('.\\file1.csv', '.\\badstruct2.csv',),
                         'Error:Invalid csv record on file 2')
        self.assertEqual(csv_compare('.\\badstruct1.csv', '.\\badstruct2.csv',),
                         'Error:Invalid csv record on file 2')
        self.assertEqual(csv_compare('.\\corrupt1.csv', '.\\file2.csv',),
                         'Error:Invalid csv record on file 1')
        self.assertEqual(csv_compare('.\\file1.csv', '.\\corrupt2.csv',),
                         'Error:Invalid csv record on file 2')
        self.assertEqual(csv_compare('.\\corrupt1.csv', '.\\corrupt2.csv',),
                         'Error:Invalid csv record on file 2')
        self.assertEqual(csv_compare('.\\1-9.csv', '.\\10-20.csv',),
                         '{"added": [1, 2, 3, 4, 5, 6, 7, 8, 9], '
                         '"deleted": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],'
                         ' "changed": []}')
        self.assertEqual(csv_compare('.\\10-20.csv', '.\\1-9.csv',),
                         '{"added": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], '
                         '"deleted": [1, 2, 3, 4, 5, 6, 7, 8, 9],'
                         ' "changed": []}')
        self.assertEqual(csv_compare('.\\10-20-30-35.csv', '.\\1-9-21-25.csv',),
                         '{"added": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 31, 32, 33, 34, 35],'
                         ' "deleted": [1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25], "changed": []}')
        self.assertEqual(csv_compare('.\\1-9-21-25.csv', '.\\10-20-30-35.csv',),
                         '{"added": [1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 22, 23, 24, 25], '
                         '"deleted": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 31, 32, 33, 34, 35],'
                         ' "changed": []}')
        self.assertEqual(csv_compare('.\\1-9.csv', '.\\8-15.csv',),
                         '{"added": [1, 2, 3, 4, 5, 6, 7], "deleted": [10, 11, 12, 13, 14, 15], "changed": []}')
        self.assertEqual(csv_compare('.\\8-15.csv', '.\\1-9.csv',),
                         '{"added": [10, 11, 12, 13, 14, 15], "deleted": [1, 2, 3, 4, 5, 6, 7], "changed": []}')
        self.assertEqual(csv_compare('.\\8-15-9diff.csv', '.\\1-9.csv',),
                         '{"added": [10, 11, 12, 13, 14, 15], "deleted": [1, 2, 3, 4, 5, 6, 7], "changed": [9]}')
        self.assertEqual(csv_compare('.\\1-9.csv', '.\\8-15-9diff.csv',),
                         '{"added": [1, 2, 3, 4, 5, 6, 7], "deleted": [10, 11, 12, 13, 14, 15], "changed": [9]}')
        self.assertEqual(csv_compare('.\\1-9.csv', '.\\1-9-21-25.csv',),
                         '{"added": [], "deleted": [21, 22, 23, 24, 25], "changed": []}')
        self.assertEqual(csv_compare('.\\1-9-21-25.csv', '.\\1-9.csv',),
                         '{"added": [21, 22, 23, 24, 25], "deleted": [], "changed": []}')
        self.assertEqual(csv_compare('.\\combinations.csv', '.\\combinations2.csv'),
                         '{"added": [1, 8, 19, 31, 37, 45], '
                         '"deleted": [4, 11, 16, 17, 18, 23, 24, 36, 50], "changed": [5, 10, 22, 28, 35, 40]}')
        self.assertEqual(csv_compare('.\\file1.csv', '.\\file2.csv'),
                         '{"added": [1], "deleted": [3], "changed": [2]}')
        self.assertEqual(csv_compare('.\\smaller1.csv', '.\\smaller2.csv'),
                         '{"added": [300, 400, 500, 600],'
                         ' "deleted": [20, 21, 22, 23, 24, 101, 102, 201, 202, 301, 401], "changed": [200]}')
        self.assertEqual(csv_compare('.\\morecols1.csv', '.\\morecols2.csv'),
                         '{"added": [4], "deleted": [3], "changed": [2]}')
        self.assertEqual(csv_compare('.\\morecolsbad1.csv', '.\\morecols2.csv'),
                         'Error:Invalid csv record on file 1')


if len(sys.argv) >= 3:
    path1 = sys.argv[1]
    path2 = sys.argv[2]
else:
    path1 = input("Enter the path of the first CSV file: ")
    path2 = input("Enter the path of the second CSV file: ")
print(csv_compare(path1, path2))
# unittest.main()
