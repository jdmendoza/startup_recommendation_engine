# Startup Recommendation Engine

Description: Used K-Means clustering + NLP techniques on 20014-2014 CrunchBase data to recommend SF startups for job-seekers and investors. Rather than using a rigid approach like CrunchBase’s search engine (filtering with rules), my engine uses an exploratory approach.

## Files
---
- **Startup_Recommender.ipynb** - This jupyter notebook holds the code for the clustering of the data.
- **data/funding_dict.pickle** - A pickled dictionary where the key is company name and value is total funding for company. Created from CrunchBase data.
- **data/investor_rating_dict.pickle** - A pickled dictionary where the key is company name and investor rating as value. Created from CrunchBase data, it was feature engineered.
- **data/max_rounds_dict.pickle** - A pickled dictionary where the key is company name and value is maximum rounds companies. Created from CrunchBase data.
- **data/startups_sf_2014_to-14_data.csv** - SF subset of CrunchBase data from 2004 to 2014.
- **scripts/push_startups_to_mongo.py** - If MongoDB is desired, run the .py script to automatically load data. Also, uncomment query section in python notebook.
- **app/.** - This folder holds files to run the dashboard locally. See below for a web deployed version.

## Notes
---
See article [here](https://www.linkedin.com/pulse/discovering-startups-clustering-j-danny-mendoza/) for more information on the project.


## Dashboard

Try out the demo here: https://startup-rec.herokuapp.com/
