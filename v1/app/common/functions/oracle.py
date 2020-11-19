#!/usr/bin/env python3.6
import cx_Oracle as oracle
import os
import v1.app.common.functions.files as file_processor


class OracleQuery:
    def __init__(self, tns, username, password):
        self.connection = None
        self.cursor = None
        self.tns = tns
        self.username = username
        self.password = password

    @staticmethod
    def find_query(query_name):
        query_files = file_processor.Files(os.path.join(os.path.dirname(__file__), '../../resources/sql_queries'))
        path_to_query = query_files.search_folders(name=query_name)[0]
        query = query_files.read_file_to_string(path_to_query)
        return query

    @staticmethod
    def parametise_query(parameters):
        bind_variables = {}
        bind_values = {}

        for key, value in parameters.items():
            if isinstance(value, list):
                bind_variable = ', '.join([':' + key + str(i) for i in range(len(value))])
                bind_values.update({key + str(i): j for i, j in enumerate(value)})
                bind_variables[key] = bind_variable
            else:
                bind_variables[key] = value
                bind_values[key] = f':{key}'

        return bind_variables, bind_values

    def run_query(self, query_name, parameters):
        query = self.find_query(query_name)
        bind_variables, bind_values = self.parametise_query(parameters)
        query = query.format(**bind_variables)

        connection = oracle.connect(self.username, self.password, self.tns)
        cursor = connection.cursor()

        if parameters:
            cursor.execute(query, bind_values)
        else:
            cursor.execute(query)

        fields = [item[0] for item in cursor.description]
        result = []
        for item in cursor:
            result.append(dict(zip(fields, item)))

        cursor.close()
        connection.close()

        return self.find_query(query_name)


if __name__ == '__main__':
    pass


