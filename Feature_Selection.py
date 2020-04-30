# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 16:41:54 2020

@author: Sara
"""

def Read_Data():
    
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
    from sklearn.impute import SimpleImputer, KNNImputer
    import seaborn as sns
    
    #------------ READ DATA -----------------
    Data_all_train = pd.read_csv("train.csv")
    Data_all_test = pd.read_csv("test.csv")
    
    df_Data_test = Data_all_test.iloc[:, 1:]
    df_Data_train = Data_all_train.iloc[:,1:-1]
    y = Data_all_train.iloc[:, -1].values
    
    train_location = df_Data_train.shape[0]
    
    #--- join test and tran set for presprocessing --------
    df_Data = pd.concat([df_Data_train, df_Data_test], axis=0)
    df_Data = df_Data.reset_index()
    

    # Data_all_train['Combo'] = Data_all_train['Exterior1st'] + Data_all_train['Exterior2nd']
    # sns.barplot(x = 'Combo', y ='SalePrice', data = Data_all_train) 

  
    #-------------- MAPPING THE ORDINAL FEATURES AND NAN VALUES WITH MEANING -----------------------------
    
    #---- NOMINAL CATHEGORICAL features -------------
    maping_function = { np.nan: 'Not_Having'}
    df_Data['Alley'] = df_Data['Alley'].replace(maping_function)
    df_Data['GarageType'] = df_Data['GarageType'].replace(maping_function)
    df_Data['Fence'] = df_Data['Fence'].replace(maping_function)
    df_Data['MiscFeature'] = df_Data['MiscFeature'].replace(maping_function)
    
    
    #------- ORDINAL features ---------------
    
    maping_function = {'Ex': 5, 'Gd': 4, 'TA': 3, 'Fa': 2, 'Po': 1, np.nan: 0}     
        
    df_Data['ExterCond'] = df_Data['ExterCond'].replace(maping_function)
    df_Data['ExterQual'] = df_Data['ExterQual'].replace(maping_function)
    
    df_Data['BsmtQual'] = df_Data['BsmtQual'].replace(maping_function)
    df_Data['BsmtCond'] = df_Data['BsmtCond'].replace(maping_function)
    
    df_Data['GarageQual'] = df_Data['GarageQual'].replace(maping_function)
    df_Data['GarageCond'] = df_Data['GarageCond'].replace(maping_function)
    
    df_Data['HeatingQC'] = df_Data['HeatingQC'].replace(maping_function)
    df_Data['KitchenQual'] = df_Data['KitchenQual'].replace(maping_function)
    
    df_Data['PoolQC'] = df_Data['PoolQC'].replace(maping_function)
    
    df_Data['FireplaceQu'] = df_Data['FireplaceQu'].replace(maping_function)
    
    
    maping_function = {'Gd': 4, 'Av': 3, 'Mn': 2, 'No': 1, np.nan: 0}
    df_Data['BsmtExposure'] = df_Data['BsmtExposure'].replace(maping_function)
    
    
    maping_function = {'Fin': 3, 'RFn': 2, 'Unf': 1, np.nan: 0}
    df_Data['GarageFinish'] = df_Data['GarageFinish'].replace(maping_function)
    
    
    
    
 #--------- INGENEER FEATURES --------------------------
   
    #--- (Quality+Condition)^2 is a new variable that is linear-ish with Price -------
    New_ax = np.square(df_Data[['OverallQual', 'OverallCond']].sum(axis=1))    
    New_ax = np.array(New_ax)
    New_ax[New_ax<40.0] = 40.0   
    df_Data = df_Data.drop(['OverallQual', 'OverallCond'], axis=1)
    df_Data = df_Data.assign(Overall_QualCond = New_ax)
    
    New_ax = np.square(df_Data[['ExterCond', 'ExterQual']].sum(axis=1))   
    New_ax = np.array(New_ax)
    New_ax[New_ax > 64.0] = 64.0    
    df_Data = df_Data.drop(['ExterCond', 'ExterQual'], axis=1)
    df_Data = df_Data.assign(Exter_QualCond = New_ax)
    
    New_ax = np.square(df_Data[['BsmtQual', 'BsmtCond']].sum(axis=1))   
    New_ax = np.array(New_ax)
    New_ax[New_ax > 64.0] = 64.0  
    df_Data = df_Data.drop(['BsmtQual', 'BsmtCond'], axis=1)
    df_Data = df_Data.assign(Bsmt_QualCond = New_ax) #Zero indicates there was no Basment
    
    New_ax = np.square(df_Data[['GarageQual', 'GarageCond']].sum(axis=1))   
    New_ax = np.array(New_ax) 
    df_Data = df_Data.drop(['GarageQual', 'GarageCond'], axis=1)
    df_Data = df_Data.assign(Garage_QualCond = New_ax) #Zero indicates there was no Basment
       
    
    #------------ Garage_QualCond * GarageArea ------------------------
    df_Data['Garage_Size_Quality'] = df_Data['Garage_QualCond'] + df_Data['GarageArea']
 
     #------------Rating of two basement finished areas -------------------
    df_Data['BsmtFinType'] = df_Data['BsmtFinType1'] + df_Data['BsmtFinType2']   
 
    #------------Area two basement finished areas -------------------
    df_Data['BsmtFinSF'] = df_Data['BsmtFinSF1'] + df_Data['BsmtFinSF2']      
    
    #------------Total living Area minus low quality area -------------------
    df_Data['GrLivArea_Quality'] = df_Data['GrLivArea'] + df_Data['LowQualFinSF'] 
 
     #----- Total Num of Bathrooms --------
    df_Data['TotalBath'] = df_Data["FullBath"]  + 0.5 * df_Data["HalfBath"]
    df_Data['TotalBath_Bsmt'] =  df_Data["BsmtFullBath"] + 0.5 * df_Data["BsmtHalfBath"]
    df_Data = df_Data.drop(["FullBath", "HalfBath", "BsmtFullBath", "BsmtHalfBath"], axis=1)
       
    #------- House area + Basment area ----------------
    df_Data['TotalSF'] = df_Data["GrLivArea"] + df_Data["TotalBsmtSF"]
    
    # ---------- Total Porch Area ---------------------------
    df_Data['TotalPorchSF'] = df_Data["OpenPorchSF"] + df_Data["EnclosedPorch"] + df_Data["3SsnPorch"] + df_Data["ScreenPorch"]
    
     #------------- Proximity to various conditions plus if more than one is present --------------
    df_Data['Condition_together'] = df_Data['Condition1'] + df_Data['Condition2']
  
    
    #------------- Exterior covering on house plus if more than one is present --------------
    df_Data['Exterior'] = df_Data['Exterior1st'] + df_Data['Exterior2nd']
    
    #------------------Style of dwelling + Type of dwelling --------------
    df_Data['House_Style_Type'] = df_Data['BldgType'] + df_Data['HouseStyle']
    
    # ------------- Type of roof + Roof material ---------------------
    df_Data['Roof_Style_Matl'] = df_Data['RoofStyle'] + df_Data['RoofMatl']
    
    #---------- Fireplace Quality and Number ---------------
    df_Data['Fireplaces_Num_Qual'] = df_Data['Fireplaces'] + df_Data['FireplaceQu']
    
    #------------Sale condition and type -------------------
    df_Data['Sale_Cond_type'] = df_Data['SaleType'] + df_Data['SaleCondition']
 
#--------------- NOMINAL FEATURES --------------------------------------------
    nominal_feat = ['MSSubClass', 'MSZoning', 'Street', 'Alley', 'LotShape', 'LandContour',
                    'Utilities', 'LotConfig', 'LandSlope', 'Neighborhood', 
                    'Exterior', 'MasVnrType', 'Foundation', 
                    'BsmtFinType', 'Heating', 'CentralAir', 'Electrical',
                    'Functional', 'GarageType', 'PavedDrive', 'Fence', 'MiscFeature',
                    'MoSold', 'YrSold', 
                    'House_Style_Type', 'Condition_together', 'Roof_Style_Matl', 
                    'GarageCars', 'PoolQC', 'Sale_Cond_type',
                    'TotalBath', 'TotalBath_Bsmt']     

    
    
    #TEST FOR NOT RANDOM NANs
    # Nan_Test_data = pd.concat([df_Data[nominal_feat].isna().astype(int), df_Data['BothFloorsSF'], Data_all_train['SalePrice']], axis=1)   
    # Missing_features = df_Data[nominal_feat].isna().any()[lambda x: x] 
    # sns.barplot(x = Missing_features.index[10], y ='SalePrice', data = Nan_Test_data) 

    #List of not randomly missing variables (found by barplot nan vs. not nan values)
    MNAR_Nominal = ['MasVnrType']
    maping_str = {np.nan: 'Not_Having'}    
    df_Data['MasVnrType'] = df_Data['MasVnrType'].replace(maping_str)

    Nominal = df_Data[nominal_feat]
     
    imputer_frequency = SimpleImputer(missing_values = np.nan, strategy='most_frequent')
    Nominal = imputer_frequency.fit_transform(Nominal.values)
        
    
    le = OneHotEncoder()  
    ohe = OneHotEncoder(drop= 'first')
    Nominal = ohe.fit_transform(Nominal).toarray()


    
#--------------- ORDINAL FEATURES -------------------------------------------- 

    ordinal_feat = ['Overall_QualCond', 'Exter_QualCond', 'Bsmt_QualCond', 'HeatingQC',
                    'BsmtExposure',
                    'BedroomAbvGr', 'KitchenQual', 'TotRmsAbvGrd', 
                    'GarageFinish', 'Garage_QualCond', 
                    'Fireplaces_Num_Qual']
    
    Ordinal = df_Data[ordinal_feat]
    
    #TEST FOR NOT RANDOM NANs
    # Nan_Test_data = pd.concat([df_Data[ordinal_feat].isna().astype(int), Data_all_train['SalePrice']], axis=1)   
    # Missing_features = df_Data[ordinal_feat].isna().any()[lambda x: x] 
    # sns.barplot(x = Missing_features.index[0], y ='SalePrice', data = Nan_Test_data) 
    
    # Ordinal_data = pd.concat([(df_Data[ordinal_feat]), np.log(Data_all_train['SalePrice'])], axis=1)        
    # sns.barplot(x = 'PoolQC', y ='SalePrice', data = Ordinal_data) 
    
#--------------- CONTINOUS FEATURES --------------------------------------------
    
    continous_feat = ['LotFrontage', 'LotArea', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea',
                      'BsmtFinSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF',
                      'GrLivArea_Quality', 'GrLivArea', 'GarageYrBlt', 
                      'WoodDeckSF', 'TotalSF', 'TotalPorchSF',
                      'Garage_Size_Quality']
                      
    Continous = df_Data[continous_feat]
    
    #TEST FOR NOT RANDOM NANs
    # Nan_Test_data = pd.concat([df_Data[continous_feat].isna().astype(int), Data_all_train['SalePrice']], axis=1)   
    # Missing_features = df_Data[continous_feat].isna().any()[lambda x: x] 
    # sns.barplot(x = Missing_features.index[0], y ='SalePrice', data = Nan_Test_data) 
    
    MNAR_Continous = ['MasVnrArea', 'GarageYrBlt']     
    
    # Continous_data = pd.concat([(df_Data[continous_feat]), np.log(Data_all_train['SalePrice'])], axis=1)        
    # sns.scatterplot(x = 'BsmtFinSF2', y ='SalePrice', data = Continous_data) 
           
    #Impute Random NaNs with KNN
    Ordinal_and_Continous = pd.concat([Ordinal, Continous], axis = 1)
    imputer_knn = KNNImputer(n_neighbors = 10) 
    Ordinal_and_Continous = imputer_knn.fit_transform(Ordinal_and_Continous) 
    
    Ordinal = Ordinal_and_Continous[:,0:len(ordinal_feat)-1]
    Continous = Ordinal_and_Continous[:,len(ordinal_feat):]
    
    
    
    y = np.log(y)
    Continous = np.log(Continous + 1)
    
    # skew = pd.DataFrame(Continous).skew(numeric_only=True).abs()
    # cols = skew[skew > 1].index
    # print(cols)
    
    # from scipy.special import boxcox1p
    # from scipy.stats import boxcox_normmax
    
    # for col in cols:
    #     pd.DataFrame(Continous)[col] = boxcox1p(pd.DataFrame(Continous)[col], boxcox_normmax(pd.DataFrame(Continous)[col] + 1))
        
    
    sc = StandardScaler()
    Continous = sc.fit_transform(Continous)
      
    
# --------------- Combine Categorical and not Categorical ---------------------
    Clean_Set = pd.concat([pd.DataFrame(Nominal), pd.DataFrame(Ordinal), pd.DataFrame(Continous)], axis=1)
    X = Clean_Set[0:train_location].values
    X_test = Clean_Set[train_location:].values

    
    return X, y, X_test
    
    