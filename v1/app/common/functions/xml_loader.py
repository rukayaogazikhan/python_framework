import xml.etree.ElementTree as etree
import os


class XML:
    def __init__(self, xml_file):
        self.xml_file = xml_file

    def get_xml_data(self):
        xml_data = None
        if os.path.isfile(self.xml_file):
            xml_data = etree.parse(self.xml_file)

        return xml_data

    def xml_find_tag_values(self, tag, value, value_2):
        xml_data = self.get_xml_data()
        sub_xml_data = xml_data.findall(tag)

        list_of_results = []
        for child in sub_xml_data:

            list_of_results.append({value: child.attrib.get(value).strip()
                        , value_2: child.attrib.get(value_2).strip()})

        return list_of_results


if __name__ == '__main__':
    pass