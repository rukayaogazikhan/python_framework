#!/usr/bin/env python3.6
import glob
import os
import pandas
import csv
import re
import os

# TO DO
# rewrite find by name - remove folder from FILES init


class Files:
    def __init__(self, folder):
        self.folder = folder

    def delete_files(self, exclusion_files=None):
        for filename in glob.glob(f"{self.folder}*"):
            if os.path.isfile(filename):
                try:
                    if os.path.basename(filename) != exclusion_files:
                        os.remove(filename)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (os.path.basename(filename), e))

    def read_csv_columns(self, file_name):
        csv_file = os.path.join(self.folder, file_name)
        csv_data = []
        if os.path.isfile(csv_file):
            with open(csv_file) as f:
                reader = csv.reader(f)
                a = list(zip(*reader))
                for i in a:
                    column = list(i)
                    column.pop(0)
                    csv_data.append({i[0]: column})
        else:
            print("not a file")
        return csv_data

    def read_excel_columns(self, file_name, column_names=[]):
        excel_file = os.path.join(self.folder, file_name)
        if os.path.isfile(excel_file):
            df = pandas.read_excel(excel_file)
            df = df[column_names]

            excel_data = []
            for i in column_names:
                excel_column_data = df.dropna(subset=[i])
                if len(excel_column_data) == 1:
                    excel_data.append({i: excel_column_data[i].iloc[0]})
                else:
                    excel_data.append({i: excel_column_data[i].values.tolist()})

            return excel_data

    @staticmethod
    def read_file_to_string(file):
        with open(file, 'r') as file:
            data = file.read().replace('\n', ' ')

        return data

    def search_folders(self, name= None, regex=None, starts_with=None, ends_with=None):
        file_paths = self.list_files()
        return_file_paths = []
        for file_path in file_paths:
            if name:
                if os.path.basename(file_path) == name:
                    return_file_paths.append(file_path)
            if starts_with:
                if os.path.basename(file_path).startswith(starts_with):
                    return_file_paths.append(file_path)
            if ends_with:
                if os.path.basename(file_path).endswith(ends_with):
                    return_file_paths.append(file_path)
            if regex:
                if re.match(regex, file_path) is not None:
                    return_file_paths.append(file_path)

        return_file_paths = list(set(return_file_paths))

        return return_file_paths

    def list_files(self):
        r = []
        for root, dirs, files in os.walk(self.folder):
            for name in files:
                r.append(os.path.join(root, name))
        return r


if __name__ == '__main__':
    file_instance = Files(os.path.join(os.path.dirname(__file__), '../../resources/sql_queries'))
    b = file_instance.list_files()
    print(b)