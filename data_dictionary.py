# Load libraries / packages
import pandas as pd



# load csv as DF
data = pd.read_csv("provided_data.csv")

# Display all the basic statistics of the DataFrame
print("DataFrame Info:")
print(data.info())
print("\nFirst 5 Rows:")
print(data.head())
print("\nSummary Statistics (Numerical):")
print(data.describe())
print("\nSummary Statistics (Categorical):")
print(data.describe(include=['O']))
print("\nNull Value Counts:")
print(data.isnull().sum())



# Divide the features into two lists based on quantifiable / categorical nature
numerical_features = data.select_dtypes(include=['int','float']).columns.tolist()
categorical_features = data.select_dtypes(include=['object']).columns.tolist()


# Loop through each categorical feature to print out their unique values
for item in categorical_features:
    print(f"Unique values for {item}:")
    print(data[item].unique())
    print(f"Number of NaN values: {data[item].isna().sum()}") # grab count of nan's
    print()  # Add a blank line for readability

# Loop through each quantifiable feature to print out their stat values
for item in numerical_features:
    print(f"Unique values for {item}:")
    print(f'min: {data[item].min()}')
    print(f'max: {data[item].max()}')
    print(f'med: {data[item].median()}')
    print(f'mean: {data[item].mean().round(4)}')
    print(f"Number of NaN values: {data[item].isna().sum()}") # grab count of nan's
    print()  # Add a blank line for readability