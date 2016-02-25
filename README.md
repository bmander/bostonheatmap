## Make a craigslist housinng price heatmap for Boston

<img src="screenshot.png?raw=true" width="350"/>

https://www.youtube.com/watch?v=F8nqxJ7YFic

### 1 - Get Data

Save all the CSVs from [Jeff's site](http://www.jefftk.com/apartment_prices/data-listing) and put them in a sub-folder named 'data'.

### 2 - Join data files and remove duplicates

    python joinfiles.py

### 3 - Remove outliers

    python deoutlier.py

### 4 - Generate

    python makeheatmap.py
