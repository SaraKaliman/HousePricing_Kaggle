# HousePricing_Kaggle

Predicting house prices is a common Machine Learning problem and many different approaches are recommended from Linear Regression, Gradient Boosting, Random Forest to Deep Learning models. But which one will give the best results? Often it is unclear which role plays complex feature engineering.

To answer all these questions, I have done a detailed analysis on the Ames House Prices which is modernized and expanded version of the often-cited Boston Housing dataset. 
Data set is downloaded from Kaggle: https://www.kaggle.com/c/house-prices-advanced-regression-techniques

I have adjusted the model parameters depending on the model result on the validation set (30% of the training set). 
The final score is calculated as root mean logarithmic error on the Test results.
The test results are made public in this Kaggle Notebook:  https://www.kaggle.com/moradnejad/perfect-score-for-evaluation-purposes


As the final model I use a weight combination of Ridge Linear Regression, Gradient Boost Regression and Support Vector Regression.

With very simple feature engineering this approach scores 0.1247 on test set (HousePrices_Comparing_Models_SIMPLE_FEATURE_SELECTION.ipynb)
NOTE: I have found that log transform of the continuous features and prices improved results much more than for example PowerTransform. 

Upon complex feature engineering the score was 0.11596. (HousePrices_Comparing_Models.ipynb)

Furthermore, a Deep Learning Model approach is tested. (HousePrices_Comparing_Models_plus_DL_Model.ipynb)


SHORT CONCLUSION:

The best results were obtained with weight combination of Ridge Linear Regression, Gradient Boost Regression and Support Vector Regression which were all quick to optimize. Complex feature engineering improved significantly the results.
Deep Learning models took long time to optimize and train and the final result was no better than the standard ML models (for this data set). Still, for DL approach I would recommend relatively deep network with several layers and regularization (I have used both Dropout and kernel L2 regularization) and using 'sigmoid' activation function on the output layer together with binary_crossentropy loss function (MinMaxScaler on the Prices before).


Hope you will find these Notebooks useful!
