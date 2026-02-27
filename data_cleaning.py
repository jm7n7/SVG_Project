# Load libraries / packages
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SEP = "-" * 100

# -----------------------------------------------------------------------------
# Load data
# -----------------------------------------------------------------------------
data = pd.read_csv("provided_data.csv")
data = data.drop(columns=['Unnamed: 0'])  # drop the original ghost index column

# -----------------------------------------------------------------------------
# Fix the nan values in gender
# -----------------------------------------------------------------------------
data['GENDER'] = data['GENDER'].fillna('U')  # hot encode the nans
print(SEP)
print("GENDER value_counts (after fillna):")
print(SEP)
print(data['GENDER'].value_counts(dropna=False))
'''
U    63194
M    46530
F    32206

The majority of records are unknown gender. Of the 78,736 known gender records, males take up ~59%.
'''

# -----------------------------------------------------------------------------
# Fix the nan values in phone type
# -----------------------------------------------------------------------------
data['PHONE_TYPE'] = data['PHONE_TYPE'].fillna('Unknown')  # hot encode the nans
print("\n" + SEP)
print("PHONE_TYPE value_counts (after fillna):")
print(SEP)
print(data['PHONE_TYPE'].value_counts(dropna=False))
'''
A7        28618
I9        28551
Unkown    28527
P2        28172
B5        28062

The records for phone type are evenly distributed.
'''

# -----------------------------------------------------------------------------
# Fix the nan values in treatment group
# -----------------------------------------------------------------------------
print("\n" + SEP)
print("TREATMENT_GROUP value_counts (before fillna):")
print(SEP)
print(data['TREATMENT_GROUP'].value_counts(dropna=False))

nan_tg = data['TREATMENT_GROUP'].isna()  # grab index for all nans

print("\n" + SEP)
print("Stats (nan TREATMENT_GROUP rows): DIAL_COUNT, AGE, PHONE_SCORE, BLOCK_SCORE, CONTACT, QUOTE, APPLICATION")
print(SEP)
print(data.loc[nan_tg, ['DIAL_COUNT', 'AGE', 'PHONE_SCORE', 'BLOCK_SCORE', 'CONTACT', 'QUOTE', 'APPLICATION']].describe())

print("\n" + SEP)
print("Stats (non-nan TREATMENT_GROUP rows): same columns")
print(SEP)
print(data.loc[~nan_tg, ['DIAL_COUNT', 'AGE', 'PHONE_SCORE', 'BLOCK_SCORE', 'CONTACT', 'QUOTE', 'APPLICATION']].describe())
'''
The records belonging to nan TREATMENT_GROUP are actually pretty significant. The PHONE_SCORE of the nan group is higher than that of the rest of the population.
BLOCK_SCORE is relatively even. There is a significant amount of records in the nan group that have CONTACT and QUOTE status indicators.
CONCLUSION: we cannot simply drop these nan values from the data, they appear to be important.
How to handle them?
- We can either create a new unknown class, or try to classify them into one of the two classes we have for TREATMENT_GROUP
- Given the scope of this assingment, we are going to classify them as unknown. In the real world, if I had a better understanding of what each class meant, I would try and classify them correctly.
'''

data['TREATMENT_GROUP'] = data['TREATMENT_GROUP'].fillna('Unknown')  # hot encode the nans
print("\n" + SEP)
print("TREATMENT_GROUP value_counts (after fillna):")
print(SEP)
print(data['TREATMENT_GROUP'].value_counts(dropna=False))

# -----------------------------------------------------------------------------
# Fix the nan values in lead cost
# -----------------------------------------------------------------------------
print("\n" + SEP)
print("LEAD_COST missing count and basic stats:")
print(SEP)
print("Missing count:", data['LEAD_COST'].isna().sum())
print("min:", data['LEAD_COST'].min())
print("max:", data['LEAD_COST'].max())
print("med:", data['LEAD_COST'].median())
print("mean:", data['LEAD_COST'].mean().round(4))

# plot to identify the distribution
plt.figure(figsize=(8, 5))
data['LEAD_COST'].hist(bins=50, edgecolor='k')
plt.title('Distribution of LEAD_COST')
plt.xlabel('LEAD_COST')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('Plots_folder/LEAD_COST_exploration.png')
plt.show()

'''
This feature is not very normal. It has a very large right skew, with a bi-modal nature well left of center.
The mean is fairly larger than the median, which hinted at non-normalcy in its distribution.
Given the large span, I would be weary as to just replacing all nans with the global average.
It might be possible to see if there are any localized clusterings of LEAD_COST, based on a different feature, from which we could populate an average. (Grouped Imputation)

We can look at two other features:
- SOURCE_TYPE
- LEAD_SOURCE
'''

# First look at SOURCE_TYPE
print("\n" + SEP)
print("SOURCE_TYPE value_counts (all rows):")
print(SEP)
print(data['SOURCE_TYPE'].value_counts(dropna=False))

nan_leadcost = data['LEAD_COST'].isna()
# Use .loc and explicit column name for clarity instead of .iloc
print("\n" + SEP)
print("SOURCE_TYPE where LEAD_COST is NaN:")
print(SEP)
print(data.loc[nan_leadcost, 'SOURCE_TYPE'].value_counts(dropna=False))
print("\nSOURCE_TYPE where LEAD_COST is not NaN:")
print(data.loc[~nan_leadcost, 'SOURCE_TYPE'].value_counts(dropna=False))

'''
All of the nan LEAD_COST values have a SOURCE_TYPE = 'Form'.
Within the subset of data that does not have a nan value for LEAD_COST, only 1985 out of ~98,000 have a 'Form' value for SOURCE_TYPE.
Lets check to see what the LEAD_COST values are for those 1985.
'''

# find the math stats of LEAD_COST for the 1985 records where SOURCE_TYPE = Form
form_lead_costs = data.loc[(data['SOURCE_TYPE'] == 'Form') & (data['LEAD_COST'].notna()), 'LEAD_COST']
print("\n" + SEP)
print("LEAD_COST for SOURCE_TYPE='Form' (non-missing):")
print(SEP)
print("min:", form_lead_costs.min(), "| max:", form_lead_costs.max(), "| mean:", form_lead_costs.mean().round(4))
'''
Based on this query, all 1985 LEAD_COST values where SOURCE_TYPE = Form, had a value of 0.00. We could assume from this that any form submission types are truley a value of 0, and that this feature had a data recording issue.
We could take it a step further and isolate the LEAD_SOURCE.
'''

# 1. Check counts of missing per LEAD_SOURCE and TREATMENT_GROUP
print("\n" + SEP)
print("Missing LEAD_COST counts by LEAD_SOURCE:")
print(SEP)
sources_with_nan = data.loc[data['LEAD_COST'].isna(), 'LEAD_SOURCE'].unique()
print(data[data['LEAD_COST'].isna()]['LEAD_SOURCE'].value_counts())

# Check for any records within these LEAD_SOURCE values that have a non-missing LEAD_COST
print("\n" + SEP)
print("Are there any non-nan LEAD_COST in LEAD_SOURCE groups:")
print(SEP)
for ls in sources_with_nan:
    non_missing_count = data[(data['LEAD_SOURCE'] == ls) & (~data['LEAD_COST'].isna())].shape[0]
    total_count = data[data['LEAD_SOURCE'] == ls].shape[0]
    print(f"  {ls}: non-missing {non_missing_count}/{total_count}")

'''
Every source that is shown to have a LEAD_COST with a nan value, does not have a single record that is a proper value.
'''

# Simply replace all nan values in LEAD_COST with 0.00
data['LEAD_COST'].fillna(0.00, inplace=True)
print("\n" + SEP)
print("LEAD_COST missing count after fillna(0.00):", data['LEAD_COST'].isna().sum())
print(SEP)

# Save the cleaned DataFrame to a new CSV file
cleaned_csv_path = "data_cleaned.csv"
data.to_csv(cleaned_csv_path, index=False)
print(f"Cleaned data saved to: {cleaned_csv_path}")