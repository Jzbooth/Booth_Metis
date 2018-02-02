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

The data was, for the most part, very easy to work with.  The only cleaning that I had to do was on the names of the players.  I needed to get all of the names to be the same format so that I could easily merge the player data frames with the dataframes containing the salary information.

## Method

### Exploratory Analysis

The first step of my linear regression was to check the correlation coefficients to determine which variables might be significant in determining the salary of players.

### Transforming Salary

I found very early on that performing a log transformation on salary would result in a much better fit for my regression.  It is important to note that when performing this transformation the coefficients of the independent variables can be interpreted as a percent change in the salary.  For example, if one of my coefficients is .25 then, given all else constant, for every 1 unit increase in this variable the salary will increase, on average, by 25%.

###  Transforming independent variables

The next step was to examine the independent variables and test if a transformation of them would result in a lower mean squared error in the model.  It was found that a few of the variables were worth transforming and so they were added to the data set.

### Regularization

Regularization is a way of manipulating the cost function to punish the complexity of the model and can be a good way to prevent over fitting.  I used a ridge regression to regularize my model.  When splitting the data set to train the model on part and test on another the model that resulted in the ridge regression resulted in the highest adjusted R^2.  

## Conclusion

In conclusion, the final models for batters and pitchers had an adjusted testing R^2 of .61 nad .63 respectively.  This means that 61% and 63% of the variance can be explained by the model.  The variables found to be most useful in predicting the salaries of batters are: Age, Sacrifice Hits, Hits into Double Play (GDP), Hits, Runs, Total Bases, Walks, RBIs, Plate appearances and At Bats. Yhe variables found to be most useful in predicting the salaries of pitchers are: Age, HR per 9, Walks per 9, Games Started, Strikeouts/Wins, Loses, HR, Complete Games, Runs and Shutouts. 

## Additional information

Additional information including a powerpoint and the jupyter note book can be found in the github repo with the same name as this blog.











