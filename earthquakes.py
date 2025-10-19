# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json

def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    return json.loads(response.text)


def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return data['metadata']['count']


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return earthquake['geometry']['coordinates']


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    earthquake_with_highest_magnitude = max(
        data['features'],
        key=lambda f: f['properties']['mag']
    )

    magnitude = earthquake_with_highest_magnitude['properties']['mag']
    coordinates = get_location(earthquake_with_highest_magnitude)
    return (magnitude, f'longitude={coordinates[0]}, latitude={coordinates[1]}')


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")

# Output
# Loaded 120
# The strongest earthquake was at longitude=-2.15, latitude=52.52 with magnitude 4.8