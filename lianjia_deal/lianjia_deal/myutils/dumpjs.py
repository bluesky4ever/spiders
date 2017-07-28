import json
import os

class DumpJs(object):

    scrapy_item = []
    name_prefix = ''
    file_path = ''

    def __init__(self, items, name = '', filepath=''):
        self.scrapy_item = items[:]
        self.name_prefix = name
        self.file_path = filepath

    def dump_to_js(self):
        if self.file_path == '':
            self.file_path = './'

        if self.name_prefix == '':
            self.name_prefix = 'export.json'
        else:
            self.name_prefix = self.name_prefix + '.json'
        
        js_file = os.path.join(self.file_path, self.name_prefix)

        with open(js_file, 'w') as fp:
            for i in self.scrapy_item:
                line = json.dumps(dict(i), ensure_ascii=False) + '\n'
                fp.write(line)
        