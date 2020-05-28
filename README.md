# HousePricing_Kaggle

These are demonstration Notebooks showing 2 different approaches to building a prediction model for Ames House Prices which is modernized and expanded version of the often-cited Boston Housing dataset. 
Data set is downloaded from Kaggle: https://www.kaggle.com/c/house-prices-advanced-regression-techniques

I have adjusted the model parameters depending on the model result on the validation set (30% of the training set). 

The final score is calculated as root mean logarithmic error on the Test results.
The test results are made public in this Kaggle Notebook:  https://www.kaggle.com/moradnejad/perfect-score-for-evaluation-purposes

As the final model I use a weight combination of Ridge Linear Regression, Gradient Boost Regression and Support Vector Regression.

With very simple feature engineering this approach scores 0.1247 on test set.
Upon complex feature engineering the score was 0.11596.

Furthermore, a Deep Learning Model approach is tested. 


