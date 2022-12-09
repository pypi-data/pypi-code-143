# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_baseClasses.ipynb.

# %% ../nbs/00_baseClasses.ipynb 5
from __future__ import annotations
from fastcore.docments import *
from fastcore.test import *
from fastcore.utils import *
from fastcore.script import *

import pandas as pd
import numpy as np
from numpy.random import uniform
from sklearn.base import BaseEstimator

import copy
from abc import ABC, abstractmethod

# %% auto 0
__all__ = ['BaseLSx', 'BaseWeightsBasedEstimator', 'BaseWeightsBasedEstimator_multivariate']

# %% ../nbs/00_baseClasses.ipynb 7
class BaseLSx:
    """
    Base class for the Level-Set based approaches. This class is not supposed to be used directly.
    Use derived classes instead.
    """
    
    def __init__(self, 
                 estimator, # Model with a `fit` and `predict` method (implementing the scikit-learn estimator interface).
                 binSize: int=None, # Number of training samples considered for creating weights.
                 # Determines behaviour of method `getWeights`. If False, all weights receive the same  
                 # value. If True, the distance of the point forecasts is taking into account.
                 weightsByDistance: bool=False,  
                 ):
        
        if not (hasattr(estimator, 'predict') and callable(estimator.predict)):
            raise ValueError("'estimator' has to have a 'predict'-method!")
            
        if not (isinstance(binSize, (int, np.integer)) or binSize is None):
            raise ValueError("'binSize' has to be an integer!")
            
        self.estimator = copy.deepcopy(estimator)
        self.binSize = binSize
        self.weightsByDistance = weightsByDistance      
        
    #---
    
    def pointPredict(self: BaseLSx, 
                     # Feature matrix for which point predictions are computed based
                     # on the point forecasting model specified via `estimator`.
                     X: np.ndarray 
                     ):
        
        return self.estimator.predict(X)
    
    #---
    
    def refitPointEstimator(self: BaseLSx, 
                            X: np.ndarray, # Input feature matrix
                            y: np.ndarray, # Target values
                            **kwargs):
        
        try:
            self.estimator.set_params(**kwargs)
        except:
            raise NotImplementedError("The 'estimator' object has no 'set_params' method, so the"
                                      "provided parameters via **kwargs can't be set!")
        else:
            setattr(self, 'estimator', self.estimator.fit(X = X, y = y))

# %% ../nbs/00_baseClasses.ipynb 12
class BaseWeightsBasedEstimator(BaseEstimator):
    """ 
    Base class that implements the 'prediction'-method for approaches based 
    on a reweighting of the empirical distribution. This class is not supposed
    to be used directly.
    """
    
    def getWeights(self, 
                   X: np.ndarray, # Feature matrix for which conditional density estimates are computed.
                   # Specifies structure of the returned density estimates. One of: 
                   # 'all', 'onlyPositiveWeights', 'summarized', 'cumDistribution', 'cumDistributionSummarized'
                   outputType: str='onlyPositiveWeights', 
                   # Optional. List with length X.shape[0]. Values are multiplied to the estimated 
                   # density of each sample for scaling purposes.
                   scalingList: list=None,
                   ) -> list: # List whose elements are the conditional density estimates for the samples specified by `X`.
        """
        Computes estimated conditional density for each sample specified by `X`. The concrete structure of each element 
        of the returned list depends on the specified value of `outputType`:
        
        - **all**: An array with the same length as the number of training samples. Each entry represents the probability 
          of each training sample.
        - **onlyPositiveWeights**: A tuple. The first element of the tuple represents the probabilities and the second 
          one the indices of the corresponding training sample. Only probalities greater than zero are returned. 
          Note: This is the most memory and computationally efficient output type.
        - **summarized**: A tuple. The first element of the tuple represents the probabilities and the second one the 
          corresponding value of `yTrain`. The probabilities corresponding to identical values of `yTrain` are aggregated.
        - **cumDistribution**: A tuple. The first element of the tuple represents the probabilities and the second 
          one the corresponding value of `yTrain`.
        - **cumDistributionSummarized**: A tuple. The first element of the tuple represents the probabilities and 
          the second one the corresponding value of `yTrain`. The probabilities corresponding to identical values of `yTrain` are aggregated.
        """
        pass
     
    #---
    
    def predict(self : BaseWeightsBasedEstimator, 
                X: np.ndarray, # Feature matrix for which conditional quantiles are computed.
                probs: list, # Probabilities for which quantiles are computed.
                outputAsDf: bool=True, # Determines output. Either a dataframe with probs as columns or a dict with probs as keys.
                # Optional. List with length X.shape[0]. Values are multiplied to the predictions
                # of each sample to rescale values.
                scalingList: list=None, 
                ): 
        """ Predict p-quantiles based on a reweighting of the empirical distribution function."""
        
        # Checks
        if isinstance(probs, int) or isinstance(probs, float):
            if probs >= 0 and probs <= 1:
                probs = [probs]
            else:
                raise ValueError("The values specified via 'probs' must lie between 0 and 1!")           
                 
        if any([prob > 1 or prob < 0 for prob in probs]):
            raise ValueError("The values specified via 'probs' must lie between 0 and 1!")
            
        try:
            probs = np.array(probs)
        except:
            raise ValueError("Can't convert `probs` to 1-dimensional array.")
        
        #---
                             
        distributionDataList = self.getWeights(X = X,
                                               outputType = 'cumulativeDistribution',
                                               scalingList = scalingList)        
        
        quantilesList = list()
        
        for probsDistribution, valuesDistribution in distributionDataList:
            
            # A tolerance term of 10^-8 is substracted from prob to account for rounding errors due to numerical precision.
            quantileIndices = np.searchsorted(a = probsDistribution, v = probs - 10**-8, side = 'left')
            quantilesList.append(valuesDistribution[quantileIndices])
    
        quantilesDf = pd.DataFrame(quantilesList)
        quantilesDf.columns = probs

        if outputAsDf:
            return quantilesDf

        else:
            return quantilesDf.to_dict(orient = 'series')
    
    #---
    
    def sampleScenarios(self,
                        X: np.ndarray, # Feature matrix for which samples are computed.
                        n: int,
                        # Optional. List with length X.shape[0]. Values are multiplied to the estimated 
                        # density of each sample for scaling purposes.
                        scalingList: list=None,
                        ) -> np.ndarray: # array-like of shape (n_samples_in, n_scenarios)
        
        distributionData = self.getWeights(X = X,
                                           outputType = 'cumulativeDistribution',
                                           scalingList = scalingList)
        
        sampleList = list()
        for probs, values in distributionData:
            randomProbs = uniform(size = n)
            randomProbs = randomProbs.reshape(n, 1)
            sample = values[np.argmax(probs >= randomProbs, axis = 1)]

            sampleList.append(sample)
        
        sampleMatrix = np.concatenate([sampleList], axis = 0)
        
        return sampleMatrix
    

# %% ../nbs/00_baseClasses.ipynb 16
class BaseWeightsBasedEstimator_multivariate(BaseEstimator):
    """ 
    Base class that implements the 'prediction'-method for approaches based 
    on a reweighting of the empirical distribution. This class is not supposed
    to be used directly.
    """
    
    def getWeights(self, 
                   X: np.ndarray, # Feature matrix for which conditional density estimates are computed.
                   # Specifies structure of the returned density estimates. One of: 
                   # 'all', 'onlyPositiveWeights', 'summarized'
                   outputType: str='onlyPositiveWeights', 
                   # Optional. List with length X.shape[0]. Values are multiplied to the estimated 
                   # density of each sample for scaling purposes.
                   scalingList: list=None,
                   ) -> list: # List whose elements are the conditional density estimates for the samples specified by `X`.
        """
        Computes estimated conditional density for each sample specified by `X`. The concrete structure of each element 
        of the returned list depends on the specified value of `outputType`:
        
        - **all**: An array with the same length as the number of training samples. Each entry represents the probability 
          of each training sample.
        - **onlyPositiveWeights**: A tuple. The first element of the tuple represents the probabilities and the second 
          one the indices of the corresponding training sample. Only probalities greater than zero are returned. 
          Note: This is the most memory and computationally efficient output type.
        - **summarized**: A tuple. The first element of the tuple represents the probabilities and the second one the 
          corresponding value of `yTrain`. The probabilities corresponding to identical values of `yTrain` are aggregated.
        """
        pass
        
