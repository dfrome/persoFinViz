# %%
# loads path to your input files : base_processed, base_raw, base_models...
from init_ import *

# %%
# Optional : list the available files to chose one for the next cell
import os

csv_files = [file for file in os.listdir(base_raw) if file.endswith('.csv')]
print("\nAvailable files in the raw folder:\n")
for file in csv_files:
    print("* "+file)


# %%
# enter the file name (no extension) you want to work with
my_data_file = 'example_fin_data_v03'  # default example
# my_data_file = 'your_file'

map_definition='50m' # '110m', '50m', '10m' : resolution of the map, as downloaded from https://www.naturalearthdata.com/downloads/50m-cultural-vectors/

print(f"\nNow processing: {my_data_file} as defined in the variable my_data_file of file {os.path.basename(__file__)}\n")
print(f"and searching for map definition in: {map_definition} conform to the variable map_definition\n")


# %%
# Remove the .csv extension if present
if my_data_file.endswith('.csv'):
    my_data_file = my_data_file[:-4]  # Strip the last 4 characters (.csv)



# %%
import pandas as pd
# Read the CSV file into a new DataFrame
df = pd.read_csv(base_raw + my_data_file + '.csv')

# in case needed
# print(df)

# %%
import numpy as np

# Replace NaN values in 'geography' and 'type' with 'not specified'
df['geography'] = df['geography'].fillna('not specified')
df['type'] = df['type'].fillna('not specified')

# Get the unique types
types = df['type'].unique()

# Group by 'geography' and calculate the sum of 'amount' for each 'type'
grouped = df.groupby(['geography', 'type'])['amount'].sum().unstack(fill_value=0)

# Convert the grouped data into a NumPy array of tuples
result_array = np.array([tuple(row) for row in grouped.values])

# Display the result
# print(result_array)

# %%
# for developper info only
"""
# Display the grouped DataFrame
print(grouped)

# Display the row index (geography values)
print("Row index (geography):", grouped.index.tolist())

# Display the column names (type values)
print("Column names (types):", grouped.columns.tolist())
"""

# %%
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Replace NaN values in 'geography' with 'not specified'
df['geography'] = df['geography'].fillna('not specified')

transformations = {
    "US": "United States of America",
    "USA": "United States of America",
    "Congo": "Democratic Republic of the Congo",
    "Bahamas": "The Bahamas",
    "UAE": "United Arab Emirates",
    "NL": "Netherlands",
    "CH": "Switzerland"
}
df['geography'] = df['geography'].map(transformations).where(df['geography'].map(transformations).notna(), df['geography'])



# Group by 'geography' and calculate the sum of 'amount'
grouped_geography = df.groupby('geography')['amount'].sum().reset_index()

# Calculate percentages
total_amount = grouped_geography['amount'].sum()  # Total amount for normalization
grouped_geography['percentage'] = (grouped_geography['amount'] / total_amount) * 100


# Load the world map shapefile using GeoPandas
# Path to the dataset shapefile
shapefile_path = base_data+"/for_geopandas/ne_"+map_definition+"_admin_0_countries.shp"
# Load the world map shapefile
world = gpd.read_file(shapefile_path)


# Merge the world map with the grouped data
# Ensure the 'geography' column matches the 'name' column in the world map
world = world.merge(grouped_geography, how='left', left_on='ADMIN', right_on='geography')

# Plot the world map
fig, ax = plt.subplots(figsize=(14,16))
world.plot(
    column='percentage',  # Use the 'amount' column for coloring
    cmap='OrRd',  # Color map (e.g., 'OrRd' for orange-red)
    legend=True,  # Add a legend
    ax=ax,
    missing_kwds={"color": "lightgrey", "label": "No Data"},  # Handle missing data
    legend_kwds={
    "shrink": 0.8,                   # Shrink the legend size to fit
    "label": "% of Amounts",       # Add a label to the legend
    "format": "%.1f%%",              # Format the legend values as percentages
    "orientation": "horizontal",     # Display the legend horizontally
    "pad": 0.02,                     # Adjust padding
}

)

# Set axis limits to focus on Europe
ax.set_xlim(-170, 176)  # Longitude range
ax.set_ylim(-58, 82)   # Latitude range

# Set aspect ratio
ax.set_aspect('equal')  # Ensure the map is not distorted
# Tighten layout to maximize map space
plt.tight_layout()


plt.title('Amount per Geography', fontsize=16)

# Turn off the grid and axis
ax.axis("off")


# Save as an image file
save_path = base_images + my_data_file + '_map_world.png'
plt.savefig(save_path, dpi=300, bbox_inches='tight')

# %%
import matplotlib.pyplot as plt

# Plot the world map
fig, ax = plt.subplots(figsize=(10, 12))
world.plot(
    column='percentage',  # Use the 'percentage' column for coloring
    cmap='OrRd',  # Color map (e.g., 'OrRd' for orange-red)
    legend=True,  # Add a legend
    ax=ax,
    missing_kwds={"color": "lightgrey", "label": "No Data"},  # Handle missing data
    legend_kwds={
        "shrink": 0.8,                   # Shrink the legend size to fit
        "label": "% of Amounts",         # Add a label to the legend
        "format": "%.1f%%",              # Format the legend values as percentages
        "orientation": "horizontal",     # Display the legend horizontally
        "pad": 0.02,                     # Adjust padding
    }
)

# Set axis limits to focus on Europe
ax.set_xlim(-20, 40)  # Longitude range
ax.set_ylim(30, 71)   # Latitude range

# Set aspect ratio
ax.set_aspect('equal')  # Ensure the map is not distorted

# Tighten layout to maximize map space
plt.tight_layout()

plt.title('Amount per Geography (Europe)', fontsize=16)

# Turn off the grid and axis
ax.axis("off")

# Save as an image file
save_path = base_images + my_data_file + '_map_europe.png'
plt.savefig(save_path, dpi=300, bbox_inches='tight')

print(f"Look for created images in: {base_images}")


# %%
#print(world['ADMIN'].unique()) # in case needed to map countries names


