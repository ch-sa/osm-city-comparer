import overpy

from geopy.geocoders import Nominatim


# Geocoding request via Nominatim
class NominatimSearch:

    def __init__(self):
        self.geolocator = Nominatim(user_agent="city_compare")

    def get_city_id(self, in_city):
        geo_results = self.geolocator.geocode(in_city, exactly_one=False, limit=3)
        geo = geo_results[0]

        if geo is None:
            print("We could not find your city.")
            return None

        print("%s will be analysed." % geo)
        return geo

    def get_city_options(self, city_initials):
        geo_results = self.geolocator.geocode(city_initials, exactly_one=False, limit=3)
        if geo_results is None:
            return None

        options = []

        for geo in geo_results:
            if geo.raw.get("osm_type") == "relation":
                options.append(str(geo.raw.get("display_name")))

        return options


class Overpass:

    def __init__(self):
        self.api = overpy.Overpass(url="https://lz4.overpass-api.de/api/interpreter")

    # Retrieve city names

    def query(self, city):
        return self.api.query("""
                area(%s)->.searchArea;
                (
                  node["amenity"](area.searchArea);
                  way["amenity"](area.searchArea);
                  relation["amenity"](area.searchArea);
                );
                out body;
                """ % get_query_id(city))


# Make correct city id for query
def get_query_id(city):
    return str(int(city.raw.get("osm_id")) + 3600000000)
