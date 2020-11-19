import json
import os


class JSONReader:
    def __init__(self, json_file):
        self.json_file = json_file

    def get_json_data(self):
        json_data = None
        if os.path.isfile(self.json_file):
            with open(self.json_file) as file_data:
                json_data = json.load(file_data)
        else:
            pass
        return json_data


class JSONObject(JSONReader):
    def __init__(self, json_file, node):
        #logger.debug('Start JSON.__init__()')
        super().__init__(json_file)
        #logger.debug('End JSON.__init__()')
        self.node = node
        self.node_data = self.get_json_data().get(self.node)
        self.set_obj_values()

    def set_obj_values(self):
        keys = self.get_obj_keys()
        for key in keys:
            setattr(self, key, [d[key] for d in self.node_data])

    def get_obj_keys(self):
        all_keys = list(set().union(*(d.keys() for d in self.node_data)))
        return all_keys

    def get_value_from_key(self, key):
        pass

    #looks up keys and returns matching dictionaries
    def obj_lookup(self, **lookups):
        available_kwargs = self.get_obj_keys()

        lookup = {key: lookups[key]
                  for key in lookups
                  if key in available_kwargs}

        result_set = self.node_data

        for key, value in lookup.items():

            for m in result_set:

                if m.get('match') is None:
                    m['match'] = True

                if isinstance(m[key], list):
                    l = [m for i in m[key] if i in value]
                    if l:
                        m['match'] = True
                    else:
                        m['match'] = False

                else:
                    if m[key] in value and m['match'] is not False:
                        m['match'] = True

                    if m[key] not in value and m['match'] is not False:
                        m['match'] = False

            result_set = [r for r in result_set if r.get('match')]

            for n in result_set:
                n.pop('match', None)

        return result_set


if __name__ == '__main__':
    pass