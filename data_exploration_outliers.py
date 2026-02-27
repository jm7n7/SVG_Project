# Load libraries / packages
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SEP = "-" * 100

# -----------------------------------------------------------------------------
# Load data
# -----------------------------------------------------------------------------
data = pd.read_csv("data_cleaned.csv")
print(data.head())


# -----------------------------------------------------------------------------
# Identify numeric features
# -----------------------------------------------------------------------------
num_features = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
print(SEP)


# -----------------------------------------------------------------------------
# Outlier Detection (Tukeys Fence)
# -----------------------------------------------------------------------------
def tukeys_fence(series, k=1.5, Q1=0.25, Q3=0.75):
    """
    Identifies outliers in a numeric pandas Series using Tukey's Fence.
    Returns a boolean Series where True indicates an outlier.
    
    Parameters:
        series : pd.Series
            Input numeric series.
        k : float
            The multiplier for IQR (default 1.5 for standard Tukey's Fence).
    Returns:
        pd.Series of bool
    """
    q1 = series.quantile(Q1)
    q3 = series.quantile(Q3)
    iqr = q3 - q1
    lower_fence = q1 - k * iqr
    upper_fence = q3 + k * iqr
    is_outlier = (series < lower_fence) | (series > upper_fence)
    return is_outlier

outlier_summary = {}
print('normal fences')
for col in num_features:
    outlier_mask = tukeys_fence(data[col])
    num_outliers = outlier_mask.sum()
    outlier_summary[col] = num_outliers
    print(f"{col}: {num_outliers} outliers ({round(100*num_outliers/len(data), 2)}%)")
print(SEP)
print('extended fences')
for col in num_features:
    outlier_mask = tukeys_fence(data[col],Q1=0.1,Q3=0.9)
    num_outliers = outlier_mask.sum()
    outlier_summary[col] = num_outliers
    print(f"{col}: {num_outliers} outliers ({round(100*num_outliers/len(data), 2)}%)")

'''
Based on the normal fences, nothing sticks out as a scary outlier.
When we tighten the fences to 0.1 and 0.9, we sand down the features to find records that are more potentially outliers.
That being said, my intuition is telling me that these features are more or less robust.
'''
