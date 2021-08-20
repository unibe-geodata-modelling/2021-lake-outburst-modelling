#### Import packages ####
import numpy as np
import geopandas as gpd

#### Set workspace ####
myworkspace = "insert the path to your workspace here"

#### Read flood layer and building layer as a geodataframe ####
# remove or add hashtag depending on which flood scenario you want to calculate
buildings_gdf = gpd.read_file(myworkspace+"/"+"TLM_GEBAEUDE_FOOTPRINT_Kander.shp")
# flood_gdf=gpd.read_file(myworkspace+"/"+"SmallFlood_1250_7200_20800_11h.shp")
flood_gdf = gpd.read_file(myworkspace+"/"+"BigFlood_4450_7200_19775_20h.shp")

## Check data
# show attribute table
print(flood_gdf.head())
print(buildings_gdf.head())
# Check columns
print(flood_gdf.columns)
print(buildings_gdf.columns)
# Show the geopandas dataframe
print(flood_gdf)
print(buildings_gdf)
# Check projection of layer with .crs
print(flood_gdf.crs)
print(buildings_gdf.crs)
# If layers do not use the same projection, reproject one of them, e.g. here to EPSG 2056
buildings_gdf = buildings_gdf.to_crs("EPSG:2056")
# Check if projected crs is correct
print(buildings_gdf.crs)

#### Overlay of flood layer and building layer ####
fbo = gpd.overlay(buildings_gdf, flood_gdf, how="intersection")
# Dissolve building pieces of same building (represented by OBJECTID) with different flow depths,
# assign highest flow depth to building
fbo_dis_raw = fbo.sort_values("max_depth", ascending=False).dissolve(by="OBJECTID", as_index=False)
# Remove all records with a flow depth of 0
fbo_dis = fbo_dis_raw[fbo_dis_raw.max_depth != 0]
# check if there are still some duplicates, based on the Object ID
if fbo_dis["OBJECTID"].duplicated().any():
else:
    print("There are no more duplicates.")

#### Count Number of affected buildings ####
# Count total no. of buildings affected
total_buildings = len(fbo_dis["OBJECTID"])
print("In total {} buildings are going to be affected by the flood.".format(total_buildings))
# Count no. of buildings per building type
buildings_per_buildingtype = fbo_dis[["geometry", "OBJEKTART"]].groupby(by="OBJEKTART").count()
fbo_dis[["geometry", "OBJEKTART"]].groupby(by="OBJEKTART").count()
# Create flood categories, count no. of buildings per flood category
# 1. Preprocessing: create flood categories
# 1.1. Create a list of conditions
conditions = [
    (fbo_dis["max_depth"] <= 0.5),
    (fbo_dis["max_depth"] > 0.5) & (fbo_dis["max_depth"] <= 1),
    (fbo_dis["max_depth"] > 1) & (fbo_dis["max_depth"] <= 2),
    (fbo_dis["max_depth"] > 2) & (fbo_dis["max_depth"] <= 3),
    (fbo_dis["max_depth"] > 3)
    ]
# 1.2. Create a list of the values to assign for each condition
categories = ["0.5", "1", "2", "3", ">3"]
# 1.3. Create a new column and use np.select to assign values to it using the list as arguments
fbo_dis["flow_depth_category"] = np.select(conditions, categories)
# 1.4. Display updated DataFrame
fbo_dis.head()
# 2. Assign a variable to each of the categories
var05 = len(fbo_dis[fbo_dis["flow_depth_category"] == "0.5"])
var1 = len(fbo_dis[fbo_dis["flow_depth_category"] == "1"])
var2 = len(fbo_dis[fbo_dis["flow_depth_category"] == "2"])
var3 = len(fbo_dis[fbo_dis["flow_depth_category"] == "3"])
var3plus = len(fbo_dis[fbo_dis["flow_depth_category"] == ">3"])

print(" {} buildings will be affected by a flow depth of up to 0.5m, {} with up to 1m, {} with up to 2m,{} with up to 3m and and {} with over 3m.".format(var05, var1, var2, var3, var3plus))
# TODO: The line could be improved so that the 0.5m etc. do not need to be changed by hand, e.g. by "input" at the beginning of preprocessing

##### write the output file ####
# remove or add hashtag depending on which flood scenario you want to calculate
fbo_dis.to_file(myworkspace+"/" + "flood_building_overlay_dissolved_small_flood_test_dissolve.shp")
# flood_building_overlay_dissolved.to_file(myworkspace+"/"+"flood_building_overlay_dissolved_big_flood.shp")
