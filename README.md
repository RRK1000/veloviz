# Velo Viz

## Inspiration
VeloViz is inspired by the intersection of data and urban mobility trends, bringing clarity to how people like to travel across their cities. Insights from VeloViz can guide better infrastructure, policy changes, and sustainability initiatives.

The rise of bike-sharing systems worldwide has transformed urban mobility. The data generated from usage will help optimize stations, improve accessibility, and encourage cycling culture. Cities often rely on raw numbers, but visualizing movement patterns makes data actionable. But by merging real ride data with survey responses, VeloViz captures both quantitative trends and qualitative information like user requirements.

At its core, VeloViz is about making bike data more than just numbers—it’s about telling the story of movement, choice, and city life. 🚲✨

## What it does
VeloViz brings bike sharing data and mode share transport data to life. Bikeshare in Toronto has 9000+ bikes and 800+ stations. Information collected from bikeshare is published by Toronto as open data, from which we gathered some significant insights such as:

* In the past 6 years, there is a significant increase in the casual membership, accounting for the doubling of total annual rides taken.
* We were able to identify the most popular station for starting and ending rides, which was York St/Queens Quay W Station. We observe this trend likely because of the station's prominence in the city. 


## How we built it
Using the [Toronto Open Data website](https://open.toronto.ca/), we used the following datasets:

* [E-Bike Survey Response Results](https://open.toronto.ca/dataset/e-bike-survey-response-results/) - CSV of survey results
* [Bike Share Toronto Ridership Data](https://open.toronto.ca/dataset/bike-share-toronto-ridership-data/) - CSV of Ridership data
* [Bikeshare station information](https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information) - JSON file of station information.

This data was then processed and uploaded to MongoDB using a temporal workflow. Metabase was connected to MongoDB as a data source. This enabled Metabase to gain access to our data for visualization. We finally explored the information and gained some insights by creating some cool visuals. 😃

## What's next for VeloViz
* Better Temporal workflow with advanced processing
* Support for GeoJSON datasets
* Inclusion of AI driven-insights
