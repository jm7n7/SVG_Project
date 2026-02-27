## SVG Analytics - Junior Data Scientist Project
Joseph Marinello

### Executive Summary

Thank you for the opportunity to work on this assessment. Per the project instructions, I strictly adhered to the recommended 4-hour time limit. Because I believe strong predictive models must be built on a deep understanding of the underlying data, I focused my time on problem breakdown, data cleaning, and exploratory data analysis (EDA).

I found a natural stopping point after completing my initial exploratory phase. Rather than rushing to implement a poorly optimized model at the last minute, I have outlined my findings, a formal solution design based the EDA I was able to complete, and a roadmap for the subsequent steps I would take given more time.

### Project Workflow & File Directory

I have broken down my workflow into sequential scripts and markdown files to showcase my process:

- `process_and_reasoning.md`: A detailed log of my initial problem breakdown, assumptions, and running notes throughout the 4-hour sprint.

- `data_dictionary.py` & `data_dictionary.md`: Since no schema was provided, I built a script to extract feature types and basic stats to define the dataset.

- `data_cleaning.py`: My logic and code for handling missing values (e.g., standardizing GENDER, PHONE_TYPE, and safely imputing 0.00 for specific LEAD_COST sub-categories based on SOURCE_TYPE).

- `data_exploration_outliers.py`: A Tukey's Fence analysis to verify the robustness of the numerical features.

- `data_exploration_relationships.py`: Bivariate analysis plotting PHONE_SCORE against BLOCK_SCORE segmented by lead status (CONTACT, QUOTE, APPLICATION).

### Proposed Solution Design

The Insight: Based on my bivariate EDA, CONTACT events are relatively broad and densely populated across higher BLOCK_SCOREs. However, when we filter for QUOTE and APPLICATION, a much more distinct density patch emerges. The current scores (PHONE_SCORE, BLOCK_SCORE, etc.) seem well-suited for predicting initial contact, but we need to optimize for actual sales.

The Solution: I propose building a supervised classification model (such as a Random Forest or Support Vector Machine) optimized to predict the probability of a lead reaching the QUOTE or APPLICATION stage, rather than just the CONTACT stage.

Feature Engineering: We can utilize the existing PHONE_SCORE and BLOCK_SCORE, but we should supplement them by extracting temporal features from INITIATION_TIMESTAMP (e.g., Time of Day, Day of Week) and utilizing categorical features like STATE and LEAD_SOURCE.

Implementation: The model would output a continuous probability score (0-100) representing the likelihood of a sale. Salespersons would sort their active lead pool by this new, sales-calibrated prediction score.

Measuring Success: To compare this new model to the production model, we should track an Adjusted Efficiency Metric alongside baseline conversion rates.

- **Baseline**: Total Applications Submitted / Total Calls Made

- **Adjusted Efficiency**: Applications Submitted / [(1 - avg(prediction score of accepted applications)) × number of calls]

Rationale: This penalizes the model if high-value applications are coming from low-scoring leads (meaning the model missed them) and rewards the model when successful applications match high prediction scores. We would validate this via an A/B test routing a percentage of leads through the new model vs. the baseline system.

### Future Work (Next Steps)

Given more time or resources, my immediate next steps would be:

- Temporal Feature Engineering: Strip INITIATION_TIMESTAMP into discrete Day and Time features to perform trend analysis on when successful contacts occur.

- Demographic/Source Analysis: Investigate trends and calculate conversion ratios grouped by GENDER, AGE, STATE, and LEAD_SOURCE.

- Outlier Treatment: Investigate the 21 extreme records in DIAL_COUNT flagged during my expanded Tukey's Fence check.

- Model Training & Tuning: Split the cleaned data, handle class imbalances (given applications are only ~1.25% of the data) using techniques like SMOTE or class weighting, and train/validate the proposed classification model.

### AI Disclosure

In accordance with SVG Analytics' guidelines, I utilized AI responsibly during this assessment. I used an AI assistant as a pair-programmer to act as a sounding board for my logical deductions regarding missing value imputation, to review my matplotlib code for efficiency, and to help structure and format this final markdown documentation. All critical thinking, logic, and code architecture are my own.