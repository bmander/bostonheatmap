## Make a craigslist housinng price heatmap for Boston

### 1 - Get Data

Save all the CSVs from [Jeff's site](http://www.jefftk.com/apartment_prices/data-listing) and put them in a sub-folder named 'data'.

### 2 - Join data files and remove duplicates

    python joinfiles.py

### 3 - Remove outliers

    python deoutlier.py

### 4 - Generate

    python makeheatmap.py
