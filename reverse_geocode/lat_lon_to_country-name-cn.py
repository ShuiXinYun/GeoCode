# -*- coding: utf-8 -*-
import time
import random
import collections, csv, logging, os, sys
if sys.platform == 'win32':
    csv.field_size_limit(2**31-1)
else:
    csv.field_size_limit(sys.maxsize)
from scipy.spatial import cKDTree as KDTree


def singleton(cls):
    """Singleton pattern to avoid loading class multiple times
    """
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class GeocodeData:
    def __init__(self, geocode_filename='geocode.csv', country_filename='countries_cn.csv'):
        # coordinates:[(lat1, lon1), ...], locations:['country_code':CN, 'city':Beijing}, ...]
        coordinates, self.locations = self.extract(rel_path(geocode_filename))
        self.tree = KDTree(coordinates)
        # countries:{'CN':China, ...}
        self.countries = {}
        self.load_countries(rel_path(country_filename))

    def load_countries(self, country_filename):
        """Load a map of country code to name
        """
        for code, name in csv.reader(open(country_filename, 'r', encoding='utf-8')):
            self.countries[code] = name

    def query(self, coordinates):
        """Find closest match to this list of coordinates
        """
        try:
            distances, indices = self.tree.query(coordinates, k=1)
        except ValueError as e:
            logging.info('Unable to parse coordinates: {}'.format(coordinates))
            raise e
        else:
            results = [self.locations[index] for index in indices]
            for result in results:
                result['country'] = self.countries.get(result['country_code'], '')
            return results

    def extract(self, local_filename):
        """Extract geocode data from zip
        """
        try:
            rows = csv.reader(open(local_filename, 'r', encoding='utf-8'))
            # load a list of known coordinates and corresponding locations
            coordinates, locations = [], []
            for latitude, longitude, country_code, city in rows:
                coordinates.append((latitude, longitude))
                locations.append(dict(country_code=country_code, city=city))
            return coordinates, locations
        except BaseException as e:
            raise e


def rel_path(filename):
    """Return the path of this filename relative to the current script
    """
    return os.path.join(os.getcwd(), os.path.dirname(__file__), filename)


def get(coordinate):
    """Search for closest known location to this coordinate
    """
    gd = GeocodeData()
    return gd.query([coordinate])[0]


def search(coordinates):
    """Search for closest known locations to these coordinates
    """
    gd = GeocodeData()
    return gd.query(coordinates)


if __name__ == '__main__':
    # test some coordinate lookups
    city1 = -37.81, 144.96
    city2 = 31.76, 35.21
    city3 = 37.783843, 126.384504
    print(get(city1)['country'])
    print(get(city2)['country'])
    print(get(city3)['country'])


