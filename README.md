# Work_Samples
A repository containing examples of Martin Palkovic's code

<b>DBSCAN_Analysis.ipynb</b> - Using machine learning to explore residential development pressure on groundwater in La Plata County, Colorado

<b>USGS_Pubs_Scraper.ipynb</b> - A web scraper for iteratively extracting data from the USGS publications warehouse

<b>DenverSnowfall_MultipleRegression.ipynb</b> - Code for my Towards Data Science Article -> <a>https://towardsdatascience.com/estimating-future-snowfall-in-denver-colorado-using-machine-learning-in-python-ada88a531001</a>

<b>Main_USGS_Wildfires_v2.ipynb</b> - Interactive Python map of a USGS wildfire dataset
  
<b>Main_Kaggle_Wildfires.ipynb</b> - Interactive Python map of a Kaggle wildfire dataset
  -From my Towards Data Science Article -> <a>https://towardsdatascience.com/creating-an-interactive-map-of-wildfire-data-using-folium-in-python-7d6373b6334a</a>

<b>La Plata County Python Workflow_v2.py</b> - a lengthy Python program I wrote that calculated the aquifer that ~10,000 groundwater monitoring wells were completed in, using available geologic data for the area. Note that this was my first Python project for work, and looking back, I could definitely improve on the efficiency of some parts of the workflow by bringing the data out of ArcGIS and into Pandas. Start around line 750 to see the logic I used to calculate each aquifer.


<b>Data you'll need:</b>

Data for DBSCAN_Analysis.ipynb: 
DWR_LAS.txt (located in this repository)

Data for Main_USGS_Wildfires_v2.ipynb (read in the .shp file in your GeoPandas dataframe):
https://www.sciencebase.gov/catalog/item/5ee13de982ce3bd58d7be7e7

Data for Main_Kaggle_Wildfires.ipynb:
https://www.kaggle.com/rtatman/188-million-us-wildfires
