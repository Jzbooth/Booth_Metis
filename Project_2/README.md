# Booth_Metis

# Project Luther

## Overview

The purpose of this project was to use a linear regression model in order to determine which statistics are most relevant when predicting a player's salary.  This was done by first scraping data from different webisites.  Then performing some exploratory analysis while cleaning the data. After the data was in a useable format a regression was done, at which point I could narrow down the number of features to optimize the model.  The next step was transforming variables and determining their usefulness within the model.  The final step was regularization and drawing conclusions from the model.

## Data 

### Gathering

#### Beautiful soup

I used the python package beautiful soup to scrape the batters data from sportrac.com.  I was able to identify the table and rows that I wanted to scrape by examining the raw html and using thier locations to itterate through the tabel.

#### Selenium
 
When attempting to scrape the data for pitchers from the same website I saw the limits of beautiful soup.  The website required some interaction to get to the pitching data and when scraping that url with beautiful soup it would still give me the batters data.  To overcome this problem I used the python package Selenium.  Selenium is great because it allows you to interact with the website.  Selenium allowed me to scrape the rest of the data.

### Cleaning
