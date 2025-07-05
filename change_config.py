import json


def rewrite_xml(data_path, file_path):
    ''' 
    Function to create a new XML file with a root element and a child element.
    '''

    with open(data_path, 'r') as file:
        data = json.load(file)

    start_xml = '<?xml version="1.0" encoding="UTF-8"?>\n  <configuration>\n'
    end_xml = '  </configuration>\n</xml>\n'

    with open(file_path, 'w') as file:
        file.write(start_xml)
        file.write(f'    <account>{data["accountConnectionString"]}</account>\n')
        file.write(f'    <app>{data["appConnectionString"]}</app>\n')
        file.write(f'    <pattern>{data["appPattern"]}</pattern>\n')
        file.write(end_xml)


file_path = 'abc.config'
rewrite_xml("myconfig.json", file_path)