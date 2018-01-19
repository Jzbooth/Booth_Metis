# Jared Booth

## Benson Project

### Overview

My first project at Metis challenged my partner and I to optimize the allocation of street teams in order to maximize attendance and donations at an upcoming gala hosted by the WTWY.  To accomplish this task we were specifically asked to use MTA subway data and we decided to supplement this data with data from the U.S census and the locations of tech companies in NYC.

### Method

**Understand the project**
- First, we looked at what type of people the WTWY was most interested in attracting to the gala.  We understood that it is a fundraising event so the desired population should have disposable income.  Because of this we used U.S. census data to find the areas of New York City with the highest average/median incomes.  We then thought that just having money wasn't going to be enough and we should further narrow our search.  From this we decided to only consider posting our street teams in areas where tech companies are prevelant. Combining these considerations with the mta data we were able to find a few subway stations that we could recommend.

**Gather and clean the data**
- Gathering the data was simple.  We found the MTA and census data on their respective websites and we found a map of the locations of startups in New York City online. After bringing the MTA data into our Jupyter Notebook we moved it into a data frame.  Once in the data frame we could drop columns that were irrelevant to our search and isolated the variables DATE, TIME, SCP, STATION, ENTRIES, EXITS.  When in this format we could look at entries per day for each of the stations and find the ones with the highest traffic.

- Once the census data was imported into our notebook we could pull out the relevant data using a key provided by the census website.  The key was required because the data was in the form of a 176 character string of numbers.  From this data we decided that Borough, Sub-Borough, and Overall Income were the most important peices of data to extract.  After bringing this into a dataframe we found the mean and median incomes for the sub-boroughs of manhattan.  

- The locations of startups in NYC was found online.  This map showed that the vast majority of startups are located in lower to mid Manhattan.  Because of this we decided that we should focus our street teams in Manhattan exclusively.

### Recomendation

After completing our analysis all of our data pointed towards lower and middle Manhattan as the prime locations for our street teams.  

- There were a number of very high volume subway terminals that we could utilize to get the most exposure.

- The census data showed that these sub-boroughs had the highest average and median incomes in Manhattan.

- The map of startups showed that the vast majority of startup companies were located in lower and middle Manhattan.

### Conclusion

In conclusion, we would reccomend that the people of WTWY place their street teams in the high volume subway terminals located in lower to middle Manhattan.


