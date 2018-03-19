# Predicting credit card defaults

# Summary

In my third project at Metis I took on a classification problem where the target was whether or not a credit card holder will default on their balance.  The data was gathered from the UCI machine learning website and focused on credit card holders from Taiwan. I tested a variety of models and chose the best one to analyze further.  I added a profit function that I then maximized.  

# Method

## Data

After getting and cleaning the data I split the data into train and test sets so the mdoels can be tested on data that they have never seen.  There was a fairly large imbalance in the classes withing the test and train sets with non-defaults having nearly three times as much representation.  To address this problem I used bootstrapping to up-sample the minority class so that they were even.  

## Model selection

After the data was ready, I compared different classicfication methods by their roc curves on the test sets.  Having determined that Logistic regression and Random forest methods worked the best I contunued with only those methods.  I then used a grid search method to optimize both the parameters of each of the models.

## Cost function

When examining the results of the models it was clear that there were a significant amount of misclassification present in both models.  After doing some research on the costs associated with a false positive and false negative, which are classifiying a borrower as going to default when they would have payed their balance and classifying a borrower as going to pay when they really won't, I decided to implement a cost function.  I first made a few assumptions to make things simpler; first, I assumed that a false positive will only return the price that a collections company is willing to pay for the debt when, if the borrower had been correctly classified the lender would have returned the entire balance. Second, I assumed that a false negative will result in the borrower not being able to pay his debt. This means that the lender will return none of the balance owed when they would have returned the price that a collections agency is willing to pay had the borrower been classified correctly.  Third, after some research I found that on average, a collections agency is willing to pay about 5% of the balance owed after the borrower has defaulted.  Therefore, the overall cost associated with a false poitive is much greater than that of a flase negative at the current rate a collections agency is willing to pay.


# Results

The conclusions reached from this model are that at the current accuracy level of the model and the current rate that debt collectors are willing to pay result in a maximized profit function when nearly everyone is chosen to not default. As a result the lendor then choses to never sell the borrowers debt.  We can see that this number changes as the rate that a debt collector is willing to pay increases. Additionally, we can infer that if the accuracy of the model were to increase we would be more willing to classify more borrowers in the default class.  A visualization of the effect a change in the rate a collections agency is willing to pay can be found at the github repo tied to this blog.
