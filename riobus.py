import collections
from coopy.decorators import readonly

class RioBus(object):
    def __init__(self):
        self.lines = {}
        self.streets = {}

    def get_or_create_street(self, name, city_name, direction):
        key = (name, city_name, direction)
        if key in self.streets:
            return self.streets[key]
        else:
            self.streets[key] = dict(name=name,
                                     city_name=city_name,
                                     direction=direction)
            return self.streets[key]

    def add_street(self, street, line_id):
        self.lines[line_id]['streets']\
                           [(street['name'], street['direction'])] = street

    def init_line(self, name):
        self.lines[name] = dict(line_id=name,
                                name=None,
                                city=None,
                                streets=collections.OrderedDict())

    def update_name_and_city(self, line_id, name, city):
        line = self.lines[line_id]
        line['name'] = name
        line['city'] = city

    @readonly
    def search_street(self, nome):
        from collections import defaultdict
        result = defaultdict(list)
        for line_name, line in self.lines.items():
            for street_name, street in line['streets'].items():
                if street_name[0].upper() in street['name'].upper():
                    result[line['name']].append(street)
        return result
