# Booth_Metis

# Real estate description analysis

# Summary

In this project I will use natural language processing and clustering techniques to group real estate descriptions based on the similarities in the choice of language of the documents.  The data was scraped from Zillow.com and has the descriptions of the properties as well as numerical data from the properties.  I used an LDA model to group the descriptions and created word clouds to familiarize myself with the language in each of the groups.  I then tied the numerical data of each property to their respective group and was able to find certain language that real estate brokers can use to help sell property faster.

# Method

## Data 

The data was gathered from Zillow's website using a combination of Selenium and BeautifulSoup.  The properties were all active listings at the time of data gathering.  The data includes descriptions as well as numerical data for each of the properties gathered.  

## Model 

I first removed stop words (ex: I, a, and, of, for) and words that added no information to a cluster.  I then used a count vectorizer to turn the descrptions into vectors of counts of the words present in the descriptions.  From here I used an LDA model to group the vectorized descriptions by their cosine distances.  Using cosine distance instead of euclidean or manhattan distances is useful in natural language processing because it focuses on common words and not as much on number of words.  I chose for the LDA model to group the descriptions into 6 topics.  After reviewing the most common words in each of the topics I named them as such: 1 = luxury, 2 = yard, 3 = foreclosure, 4 = builder, 5 = open, 6 = cookie cutter. Once the descriptions had been groupded I added a new column to the data frame that contained the topic each property was assigned.  I was then able to group the numerical data of each of the properties by their topic.  I then used some visualization tools to determine the demographics of each of the topics.

# Results

Some conclusions I was able to draw from the data visualization was that the "cookie cutter" topic group was, on average, the group that spent the most time on Zillow.  Some of the words most common in the "cookie cutter" group are "square foot", "bedrooms", "bathrooms", and "single family".  It is easy to see why a property with a description like this doesn't seem very appealing.  These words don't add any information that the prospective buyer doesn't already know before he clicks on the home to learn more.  Additionally, this type of language seems very low effort and makes the home feel boring.  The purpose of a description is to get the reader so excited about a home that they feel compelled to take the next step in the buying process and visit the home.  When looking at the topic "open", that had the lowest average time on Zillow, we can see words that are much more descriptive in nature.  Some of the most common words in the "open" group are "bonus", "great room", "walk in closet", "island", "wood", "cabinets", "lighting", "schools", "perfect", and "pantry".  None of the words listed relate to anything that a buyer might already know about a house from the basic numerical data that is shown before clicking on the house.  In conclusion, I would suggest that when writing a description for real estate it is worth the extra time and effort it takes to use more descriptive language and to focus on aspects of the property that a prospective buyer wouldn't already know.  The code for this project can be found at the github repo tied to this blog post.
