# TODO: which sign combination needs to be used, to mark sections (e.g. section "import packages")? ( -> more appealing/structured code)
#### import packages ####
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import fiona
import pyproj
import rtree
import shapely
import geopandas as gpd

#### set workspace #### TODO: Adjust to "neutral" workspace in final code!


# Workspace
myworkspace = "/Users/michelegrindat/Desktop/oeschinensee/Data"

#### Read flood layer and building layer as a geodataframe ####

# flood_gdf=gpd.read_file(myworkspace+"/"+"SmallFlood_1250_7200_20800_11h.shp")
flood_gdf=gpd.read_file(myworkspace+"/"+"BigFlood_4450_7200_19775_20h.shp")
buildings_gdf=gpd.read_file(myworkspace+"/"+"TLM_GEBAEUDE_FOOTPRINT_Kander.shp")

## Check data
# show attribute table
flood_gdf.head() #TODO: Those lines could be deleted for final code?
buildings_gdf.head()
# check columns
flood_gdf.columns
buildings_gdf.columns
#show the geopandas dataframe
flood_gdf
buildings_gdf
# check projection of layer with .crs
flood_gdf.crs
buildings_gdf.crs
# if layers do not use the same projection, reproject, e.g to EPSG 2056
buildings_gdf = buildings_gdf.to_crs("EPSG:2056") # NOTE: Had to reproject buildings layer, wasn‘t in EPSG 2056!
# buildings_gdf.crs
buildings_gdf.plot()


#### Overlay flood layer and building layer ####

flood_building_overlay = gpd.overlay(buildings_gdf, flood_gdf, how="intersection")

flood_building_overlay_dissolved_raw = flood_building_overlay.dissolve(by= "OBJECTID", as_index=False)

# flood_building_overlay_dissolved.to_file(myworkspace+"/"+"flood_building_overlay_dissolved.shp")

# flood_building_overlay_test_2 = flood_building_overlay_raw.merge(on="OBJECTID")

# flood_building_overlay_test_2 = flood_building_overlay_raw.groupby.aggregate()




## data clean up
# remove all the values with a flow depth of 0
flood_building_overlay_raw_without_0=flood_building_overlay_dissolved_raw[flood_building_overlay_dissolved_raw.max_depth != 0]
# only assign the highest flow depth on a building, if building is affected by several flow depths
flood_building_overlay_dissolved = flood_building_overlay_raw_without_0.sort_values("max_depth", ascending=False).drop_duplicates("OBJECTID").sort_index()
## checking the data
# check if there are still some duplicates, based on the Object ID
if flood_building_overlay_dissolved["OBJECTID"].duplicated().any() == True:  # TODO: could also be removed, just had some fun :)
    print("There are still some duplicates!")
else:
    print("There are no more duplicates.")
# visually check correctness of overlay
flood_building_overlay.plot()


#### Number of affected buildings ####

# count total no. of buildings affected
total_buildings = len(flood_building_overlay_dissolved["OBJECTID"])
print("In total {} buildings are going to be affected by the flood.".format(total_buildings))
# count no. of buildings per building type
buildings_per_buildingtype=flood_building_overlay_dissolved[["geometry","OBJEKTART"]].groupby(by="OBJEKTART").count()
flood_building_overlay_dissolved[["geometry","OBJEKTART"]].groupby(by="OBJEKTART").count()


# print("Offene Gebäude: {}, ")
#TODO:Wenn noch Zeit/Lust: print Funktion welche anzeigt wie viele Objekte pro Kategorie
# count no. of buildings per flood category
# 1. preprocessing: create flood categories
# 1.1. create a list of conditions
conditions = [
    (flood_building_overlay_dissolved["max_depth"] <= 0.5),
    (flood_building_overlay_dissolved["max_depth"] > 0.5) & (flood_building_overlay_dissolved["max_depth"] <= 1),
    (flood_building_overlay_dissolved["max_depth"] > 1) & (flood_building_overlay_dissolved["max_depth"] <= 2),
    (flood_building_overlay_dissolved["max_depth"] > 2) & (flood_building_overlay_dissolved["max_depth"] <= 3),
    (flood_building_overlay_dissolved["max_depth"] > 3)
    ]
# 1.2. create a list of the values to assign for each condition
categories = ["0.5", "1", "2", "3", ">3"]
# 1.3. create a new column and use np.select to assign values to it using the list as arguments
flood_building_overlay_dissolved["flow_depth_category"] = np.select(conditions, categories)
# 1.4. display updated DataFrame
flood_building_overlay_dissolved.head()
# 2. assign a variable to each of the categories
var05 = len(flood_building_overlay_dissolved[flood_building_overlay_dissolved["flow_depth_category"] == "0.5"])
var1 = len(flood_building_overlay_dissolved[flood_building_overlay_dissolved["flow_depth_category"] == "1"])
var2 = len(flood_building_overlay_dissolved[flood_building_overlay_dissolved["flow_depth_category"] == "2"])
var3 = len(flood_building_overlay_dissolved[flood_building_overlay_dissolved["flow_depth_category"] == "3"])
var3plus = len(flood_building_overlay_dissolved[flood_building_overlay_dissolved["flow_depth_category"] == ">3"])

print(" {} buildings will be affected by a flow depth of up to 0.5m, {} with up to 1m, {} with up to 2m,{} with up to 3m and and {} with over 3m.".format(var05, var1, var2, var3, var3plus))
# TODO: The line could be improved so that the 0.5m etc. do not need to be changed by hand, e.g. by "input" at the beginning of preprocessing

##### write the output file ####
# flood_building_overlay_dissolved.to_file(myworkspace+"/"+"flood_building_overlay_dissolved_small_flood.shp")
# flood_building_overlay_dissolved.to_file(myworkspace+"/"+"flood_building_overlay_dissolved_big_flood.shp")
