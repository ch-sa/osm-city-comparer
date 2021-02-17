import os

from PyQt5.QtCore import QUrl
from yattag import Doc, indent
from comparecities.osm import Overpass, NominatimSearch


class Comparer:

    def __init__(self, gui):
        self.gui = gui
        self.overpass = Overpass()
        self.citybook = NominatimSearch()

        self.city1_id = None
        self.city2_id = None
        self.counts = None

        self.set_connections()

    def set_connections(self):
        self.gui.compare_button.clicked.connect(self.run_it)
        self.gui.city1_input.editTextChanged.connect(self.on_city1_changed)
        self.gui.city2_input.editTextChanged.connect(self.on_city2_changed)

    def on_city1_changed(self, text):

        if len(text) > 4:
            options = self.citybook.get_city_options(text)
            if options is not None:
                self.gui.city1_input.addItems(options)

    def on_city2_changed(self, text):

        if len(text) > 4:
            options = self.citybook.get_city_options(text)
            if options is not None:
                self.gui.city2_input.addItems(options)

    def run_it(self):
        self.set_cities()
        self.search()
        self.create_website()

        # Publish website
        print("Publishing website")
        self.gui.browser.page().profile().clearHttpCache()
        site_url = QUrl("file:///" + os.path.join(os.getcwd(), "resources", "index.html"))
        self.gui.browser.load(site_url)

    # Check city options using Nominatin and set Ids
    def set_cities(self):
        self.city1_id = self.citybook.get_city_id(self.gui.city1_input.currentText())
        self.city2_id = self.citybook.get_city_id(self.gui.city2_input.currentText())

    # Execute overpass query
    def search(self):
        result_one = self.overpass.query(self.city1_id)
        result_two = self.overpass.query(self.city2_id)

        print("Amenities in first city: %d nodes & %d ways." % (len(result_one.nodes), len(result_one.ways)))
        print("Amenities in second city: %d nodes & %d ways." % (len(result_two.nodes), len(result_two.ways)))

        # Counting amenity types
        count1 = count_amenities(result_one.nodes + result_one.ways)
        count2 = count_amenities(result_two.nodes + result_two.ways)

        # Merging two count dictionaries
        self.counts = merge_dicts(count1, count2)

    def create_website(self):
        doc, tag, text = Doc().tagtext()

        with tag('html'):
            with tag('head'):
                doc.asis('<link rel="stylesheet" href="style.css">')
            with tag('body'):
                with tag('h1', id='main'):
                    text('Comparing Cities with OpenStreetMaps Data')

                with tag('table', klass='all-pr'):
                    with tag('tr'):
                        for h in ["AMENITIES", parse_city_name(self.city1_id.raw.get("display_name")),
                                  parse_city_name(self.city2_id.raw.get("display_name")), "Ratio*"]:
                            with tag('th'):
                                text(h)
                    for key, value in sorted(self.counts.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
                        with tag('tr'):
                            with tag('td'):
                                text(key)
                            with tag('td'):
                                text(value[0])
                            with tag('td'):
                                text(value[1])
                            diff = get_diff(value)
                            ratio = get_ratio(value)
                            if diff > 0:
                                diff_style = 'positive'
                            elif diff == 0:
                                diff_style = 'neutral'
                            else:
                                diff_style = 'negative'
                            with tag('td', klass=diff_style):
                                # text(format(diff, '+.01f') + " %")
                                text(ratio)

                with tag('div', klass='footer'):
                    text('* relative from the first city.')
                    with tag('a', href='https://www.openstreetmap.org/'):
                        text('Data from OpenStreetMaps')

        f = open(os.path.join(os.getcwd(), "resources", "index.html"), "w+")
        f.write(indent(doc.getvalue(), indent_text=True))
        f.close()

        return True  # if succeeded


# HELPER FUNCTIONS

# Count number of specific amenities
def count_amenities(all_nodes):
    roi_counts = {}

    for n in all_nodes:
        a = n.tags.get("amenity")
        if a not in roi_counts:
            roi_counts.update({a: 1})
        else:
            roi_counts[a] += 1

    return roi_counts


# Merge two dictionaries by adding the values to a tupel
def merge_dicts(dict1, dict2):
    merged = {}
    for k in dict1:
        if k in dict2:
            merged.update({k: [dict1[k], dict2[k]]})
        else:
            merged.update({k: [dict1[k], 0]})
    for k in dict2:
        if k not in merged:
            merged.update({k: [0, dict2[k]]})

    return merged


def get_diff(value):
    if value[1] == 0:
        diff = -100
    elif value[0] == 0:
        diff = 100
    else:
        diff = (float(value[1] - value[0]) / value[1]) * 100
    return diff


def get_ratio(value):
    left = value[0]
    right = value[1]

    min_val = max(min(left, right), 1)

    left_ratio = round(left / min_val, 1)
    left_ratio = 1 if left_ratio == 1 else left_ratio
    right_ratio = round(right / min_val, 1)
    right_ratio = 1 if right_ratio == 1 else right_ratio
    return "%s : %s" % (left_ratio, right_ratio)


# Parse the city name from geo request
def parse_city_name(city_string, mode="normal"):
    splitted = str(city_string).split(', ')
    if mode == "long":
        if len(splitted) == 2:
            name = splitted[0] + " in " + splitted[1]
        else:
            name = splitted[0] + " in " + splitted[1] + " (" + splitted[2] + ")"
    elif mode == "normal":
        if len(splitted) == 2:
            name = splitted[0] + " (" + splitted[1] + ")"
        else:
            name = splitted[0] + " (" + splitted[2] + ")"
    elif mode == "short":
        name = splitted[0]
    else:
        print("Unknown mode.")
    return name
