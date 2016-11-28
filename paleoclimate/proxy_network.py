"""
Reproduces figure 1 of Mann et al. (2008), except color coding
is by data type instead of by year.

"""

import folium

from datasets import mann2008a


data = mann2008a(infilled=True)
# latitude, longitude and proxy data type code for each site
lat = data.variables['lat'].data
lon = data.variables['lon'].data
data_type = data.variables['data_type'].data.astype(int)

data_type_names = {
    2000: 'Lutenbacher',
    3000: 'Tree ring',
    3001: 'Sediment',
    4000: 'Sediment',
    4001: 'sediment',
    5000: 'Document',
    5001: 'Document',
    6000: 'Speleothem',
    6001: 'Speleothem',
    7000: 'Coral',
    7001: 'Coral',
    7500: 'MXD',
    8000: 'Ice cores',
    8001: 'Ice cores',
    9000: 'Tree ring',
    }

# brown palette
colors = ['#f5deb3', '#d2b48c', '#bc8f8f', '#f4a460',
          '#daa520', '#d2691e', '8b4513', '#800000']


data_map = folium.Map(location=[0, 0], tiles='Mapbox Bright', zoom_start=2)

for ix in range(lat.size):
    folium.RegularPolygonMarker(
        [lat[ix], lon[ix]],
        popup="ix: {0}; data: {1}".format(ix, data_type_names[data_type[ix]]),
        fill_color=colors[int(data_type[ix]/1000 - 2)],
        number_of_sides=int(data_type[ix] / 1000),
        radius=4
        ).add_to(data_map)

data_map.save('map_of_data_types.html')

