# Parking-Violations-Open-Layers-
This map displays parking violations recorded from the year 2018 to the present in an interactive map application using OpenLayers. Some functionality is described below:
- A side bar with two tabs
  - An about tab saying what the website does
  - A map tab that shows information about the data clicked on
      - For the heatmap it shows the violation code and description for that one point
      - For clusters map it shows all the violation codes and descriptions present in the cluster clicked on
      - The violation code descriptions were retrieved from an API on OpenData
- Total Records that says how many records are in the specified data range
- Start and End year drop downs that filter the data when apply is clicked
- Switch mode that shows the two different ways to view the map, as a heatmap and as a clustered map


Notes:
- The year dropdowns reset when the page reloads after applying the selected filter
- The total records shows the actual amount of records but as it states in the about tab, only 200,000 records show at a time. I set it to this amount(you can see where this is done in views.py) as it is the amount of data that could load in a reasonable amount of time(around 15-20 seconds)
- I set the min year to 2018 as based on the data I was using anything before 2018 is not as accurate
