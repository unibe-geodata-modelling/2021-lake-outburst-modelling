# Hydraulic Model of the Glacial Lake Outburst Flood at Lake Oeschinen, Switzerland

## Purpose
This code was written by Sibylle Wilhelm and Michèle Grindat in the course of the seminar paper for the “Geodata Analysis and Modelling” seminar during spring semester 2021. <br />
The two lake outburst scenarios of Lake Oeschinen were modelled in BASEMENT. The resulting flood layers were further processed in Python to determine the number of affected buildings and their respective building type. Furthermore the maximum flow depths were seperated into 5 categories for visualisation in QGIS. 

## Software details
The skript is written in Python 3.9. 


## How To Use It
### Input Data
In order to run the skript, the the following input data is needed:
* flood layer
  * format: shapefile, polygon
  * attributes: maximum flow depth
* building layer
  * format: shapefile, polygon
  * attributes: object id, building type

## Result


## Contact
Michèle Grindat: michele.grindat@students.unibe.ch <br />
Sibylle Wilhelm: sibylle.wilhelm@students.unibe.ch
