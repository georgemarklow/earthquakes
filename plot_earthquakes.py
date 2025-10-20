import requests
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

def get_data():
    """Retrieve the data we will be working with."""
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


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    year = date.fromtimestamp(timestamp / 1000).year
    return year


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.

    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    magnitudes_per_year = dict()
    for earthquake in earthquakes:
        year = get_year(earthquake)
        magnitude = get_magnitude(earthquake)
        if year in magnitudes_per_year:
            magnitudes_per_year[year].append(magnitude)
        else:
            magnitudes_per_year[year] = [magnitude]

    return magnitudes_per_year

"""Plot average earthquake magnitudes per year"""
def plot_average_magnitude_per_year(earthquakes):
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    years = []
    average_magnitudes_per_year = []
    for year, magnitudes in magnitudes_per_year.items():
        years.append(year)
        average_magnitudes_per_year.append(np.average(magnitudes))

    x_values = np.array(years)
    y_values = np.array(average_magnitudes_per_year)
    plt.bar(x_values, y_values)
    plt.xlabel("Year")
    plt.show()

"""Plot number of earthquakes per year"""
def plot_number_per_year(earthquakes):
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    years = []
    number_of_earthquakes = []
    for year, magnitudes in magnitudes_per_year.items():
        years.append(year)
        number_of_earthquakes.append(len(magnitudes))

    x_values = np.array(years)
    y_values = np.array(number_of_earthquakes)
    plt.bar(x_values, y_values)
    plt.xlabel("Year")
    plt.ylabel("Number of earthquakes")
    plt.show()


# Get the data we will work with
quakes = get_data()['features']
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)