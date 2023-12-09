#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install folium


# In[2]:


import pandas as pd
import folium

file_path = r'C:\Users\SL Admin\Downloads\HMdata.csv'
data = pd.read_csv(file_path, delimiter=';')

latitude = data['Latitude'].tolist()
longitude = data['Longitude'].tolist()

# Create a list of latitude and longitude pairs
coordinates = list(zip(latitude, longitude))

from folium.plugins import AntPath
mapObj = folium.Map(location=[61.499861888587475, 23.759549595415592], zoom_start=12)

# create antpath and add to map
AntPath(coordinates, delay=800, dash_array=[30, 15], color="red", weight=3).add_to(mapObj)

# save the map object as an HTML file
mapObj.save('output.html')

# Display the map
mapObj


# In[3]:


import pandas as pd
import folium

# Read the CSV file containing the marathon route data
file_path = r'C:\Users\SL Admin\Downloads\HMdata.csv'  
data = pd.read_csv(file_path, delimiter=';')

# Create a map centered around the first coordinate pair
mapObj = folium.Map(location=[data['Latitude'].iloc[0], data['Longitude'].iloc[0]], zoom_start=12)

# Plot the route using polyline
route_points = list(zip(data['Latitude'], data['Longitude']))
folium.PolyLine(locations=route_points, color='blue', weight=3).add_to(mapObj)

# Save the map as an HTML file
mapObj.save('marathon_route_map.html')

# Display the map
mapObj


# In[4]:


import pandas as pd
import folium
import numpy as np

# Read the CSV file containing the marathon route data
file_path = r'C:\Users\SL Admin\Downloads\HMdata.csv'
data = pd.read_csv(file_path, delimiter=';')

# Function to calculate distance between coordinates using Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance

# Calculate distances between consecutive points and accumulate to segment the route
data['Distance_KM'] = np.insert(np.cumsum(haversine(data['Latitude'].values[:-1],
                                                     data['Longitude'].values[:-1],
                                                     data['Latitude'].values[1:],
                                                     data['Longitude'].values[1:])), 0, 0)

# Create a color palette for different kilometers
colors = ['#FF5733', '#FFC300', '#C70039', '#900C3F', '#581845']  # Example colors, adjust as needed for 22 kilometers

# Create a map centered around the first coordinate pair
mapObj = folium.Map(location=[data['Latitude'].iloc[0], data['Longitude'].iloc[0]], zoom_start=12)

# Plot the route segmenting by kilometers and add labels for every kilometer
for i in range(1, 23):  # Loop for 22 kilometers
    route_points = list(zip(data[data['Distance_KM'].between((i - 1), i)].loc[:, 'Latitude'].tolist(),
                            data[data['Distance_KM'].between((i - 1), i)].loc[:, 'Longitude'].tolist()))
    if len(route_points) > 1:
        folium.PolyLine(locations=route_points, color=colors[(i - 1) % len(colors)], weight=3).add_to(mapObj)
        folium.Marker(location=route_points[-1], popup=f'Kilometer {i}', icon=folium.Icon()).add_to(mapObj)

# Extract all coordinates
coordinates = []
for i in range(1, 23):
    route_points = list(zip(data[data['Distance_KM'].between((i - 1), i)].loc[:, 'Latitude'].tolist(),
                            data[data['Distance_KM'].between((i - 1), i)].loc[:, 'Longitude'].tolist()))
    if len(route_points) > 1:
        coordinates.extend(route_points)

# Create AntPath with animation
ant_path = folium.plugins.AntPath(locations=coordinates, dash_array=[10, 20], delay=800, color='blue')
ant_path.add_to(mapObj)

# Save the map as an HTML file
mapObj.save('half_marathon_route_with_antpath.html')

# Display the map
mapObj


# In[ ]:




