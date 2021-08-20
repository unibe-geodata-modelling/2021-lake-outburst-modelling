# Hydraulic Model of the Glacial Lake Outburst Flood at Lake Oeschinen, Switzerland

## Background
This code was written by Sibylle Wilhelm and Michèle Grindat in the course of the seminar paper for the “Geodata Analysis and Modelling” seminar during spring semester 2021. <br />
The "Spize Stei" rock formation above Lake Oeschinen is moving, there is a possibility that the falling down rocks will hit Lake Oeschinen and steadly fill up the lake and create a natural dam in front of it. As there is a potential that the dam would break, two lake outburst scenarios (one for a small flood and one for a big flood)were modelled in BASEMENT. Further details about the modelling itself can be found in the pdf document. 

## Puropose
The two resulting flood layers were further processed in Python to determine the number of affected buildings as well their respective building type. Furthermore the maximum flow depths at each building was devided into five categories for the visualisation of the affected buildings in QGIS. 

## How To Use It

### Software and Packages
The skript was written in Python 3.9. in the PyCharm 2021.1 Community Edition. <br />
In order to run the skript, the packages "Numpy" and "Geopandas" are needed.

### Input Data
In order to run the skript, the the following input data is needed:
* flood layer
  * format: polygon shapefile 
  * attributes: maximum flow depth
* building layer
  * format: polygon shapefile 
  * attributes: object id, building type <br />
The code can be tested with the flood and building layers that we used in our seminar paper. The layers can be found in the folder "input_data".

### Running the Skript
1. The workspace has to be defined. The flood- and building layer have to be saved at this directory and the output will be safed there as well.
2. The flood layer and the building layer are imported as a geodataframe, in order to correctly process the underlying spatial information. 
3. The data can be checked to in order to ensure that the geodataframe was produced correctly.
4. The coordinate reference system (crs) is checked. Both layers have to be in the same crs for the "overlay" command to work. If this is not the case, one layer has to be reprojected. In this code, the building layer has to be reprojected to the CH1903+ crs. This part of the code has to be adjusted if other input layers than the provided ones are used. 
5. The flood and building layers get overlayed, meaning that the spatial intersections of the two layers are selected, resulting in the _fbo_ (flood building overlay) geodataframe (gdf). It contains all the buildings that overlay with the flood layer. The attribute information of the flood layer is attached to the buildings. 
6. Because the flood layer consists of many small triangles, some buildings are located on several triangles, some of them have different maximum flow depths assigned. As the goal is to identify the maximum flow depth that will hit a building. Therefore the _fbo_ is sorted descending according to their object ID (meaning that entries with the same object-ID follow eachother, with the highest maximum flow depth on the top of each object-ID "staple"). Then the _fbo_ gets dissolved based on the object-ID. This leads to a geodataframe only containing one entry per building, with its highest maximum flow depth.
7. The BASEMENT model calculates the flow depth for each triangle in the provided boundary. This leads to many triangles with a maximum flow depth of 0, as the boundary is set to be a bit bigger than the acutal flooded area. In this step all the buildings with a maximum flow depth of 0 are removed, as they represent the non-flooded buildings, which are not of interest for our research question.
8. To check if there are no more dupilicates, the `duplicated().any()` function is used. 
9. The number of affected buildings is calculated by counting the length of the object-ID column.
10. To count the number of affected buildings per building type, the geodataframe was grouped by the column OBJEKTART and then the number of entries per OBJEKTART was counted. 
11. In the last step, the flood categories were created. The purpose of the categories is to create five groups of different flow depths, that can be later used to visualize the maximum affected flow depth of each building with a GIS. Conditions were created and merged with the name of the category (e.g. all entries with a maximum flow depth > 0.5 get assigned to the category "<0.5"). This information was then stored in a new column. 
12. Now the resulting geodataframe can be saved as a shapefile for further processing with a GIS.

## Result
The flow depth categories created in the skript were used visualize the flow depth for each of the affected buildings. As an example to show the differences in affected buildings and flow depth between the two scenarios two detailed maps of Kanderstege were created. The figures below show the maximum flow depth that affects each building in Kandersteg. Left is the result of the small flood scenario, right for the big flood scenario. For further results regarding the flood extension that didn‘t include processing in Python, see the pdf documentation.  <br />
![kandersteg_small_flood](https://user-images.githubusercontent.com/71430008/130251231-d51ec383-52d3-481e-bcd4-164999dbf7b3.jpg)
![kandersteg_big_flood](https://user-images.githubusercontent.com/71430008/130250771-e7fc5558-da7d-479a-858c-a810b048aec5.jpg)


## Improvements
* Creation of flow depth categories <br />
The code, conditions and categories were used to create the flow depth categories. This is very cumbersome and leads to an unnessecary amount of code lines. In lack of a better solution this method was used. For a leaner code this section could be replaced. 
* Process automatisation <br />
As there were only two flood layers to process, there was no need to automate the process. If the code was used to process several files, the code could be modified so that one only has to determine the input files and output location, and the layer processing and saving would work automatically for the selectet input files. 
## Contact
Michèle Grindat: michele.grindat@students.unibe.ch <br />
Sibylle Wilhelm: sibylle.wilhelm@students.unibe.ch
