## SVG Analytics - Junior Data Scientist Project
Joseph Marinello

### Executive Summary

Thank you for the opportunity to work on this assessment. Per the project instructions, I adhered to the recommended 4-hour time limit. Because I believe strong predictive models must be built on a deep understanding of the underlying data, I focused my time on problem breakdown, data cleaning, and exploratory data analysis (EDA).

I stopped after completing my initial exploratory analysis, choosing not to rush into additional graphs or quick model fitting to respect the time limit. Instead, I documented my findings, outlined next steps, and proposed a solution design based on the completed EDA.

### Project Workflow & File Directory

I have broken down my workflow into sequential scripts and markdown files to showcase my process:

- `process_and_reasoning.md`: A detailed log of my initial problem breakdown, assumptions, and running notes throughout the 4-hour sprint.

- `data_dictionary.py` & `data_dictionary.md`: Since no schema was provided, I built a script to extract feature types and basic stats to define the dataset.

- `data_cleaning.py`: My logic and code for handling missing values (e.g., standardizing GENDER, PHONE_TYPE, and safely imputing 0.00 for specific LEAD_COST sub-categories based on SOURCE_TYPE).

- `data_exploration_outliers.py`: A Tukey's Fence analysis to verify the robustness of the numerical features.

- `data_exploration_relationships.py`: Bivariate analysis plotting PHONE_SCORE against BLOCK_SCORE segmented by lead status (CONTACT, QUOTE, APPLICATION).

### Future Work (Next Steps)

Given more time, my immediate next steps would be:

- Temporal Feature Engineering: Split INITIATION_TIMESTAMP into discrete Day and Time features to perform trend analysis
    - When do successful contacts occur? Is there a trend?
    - Is there an overall trend in time of calls? (workday hours?)
    - Is there a trend in contact times only?
    - I would create visual plots for all of these questions to try and investigate if splitting this one feature into two could glean more information.

- Demographic/Source Analysis: Investigate trends and calculate conversion ratios grouped by GENDER, AGE, STATE, and LEAD_SOURCE.
    - Simple distribution plots to visualize demographics.
    - Where in the demographic range are we successful with CONTACT, QUOTE, and APPLICATION?
        - Subset the data to our successful records and create bar charts for each feature.
    - Find the ratios of status success for each feature.
        - Within each feature, do any classes stand out? Possible class separation for a decision tree or SVM model?

- Outlier Treatment: Investigate the 21 extreme records in DIAL_COUNT flagged during my expanded Tukey's Fence check. Are they real data points or typos?

- Model Training & Tuning:
    - Split the cleaned data. Since there is a very large imbalance in non-status to status records, we have to handle this carefully. We cannot simply do a random 70/30 split of the data. We have to make sure our train set and test set have close to equal proportionality of non-success to success. We need to do a Stratified Sampling approach to keep the original, real-world, proportion of the data the same. If there are no success records in the test set, we cannot accurately validate the results of our model.
        - We can also use SMOTE or class weighting to help with the imbalance.
    - This process is iterative. I would apply the model I thought best fits the data based on my exploration and analysis. Then I would train, test, and validate.
        - Based on the results, I would see if anything could possibly be tweaked to perform better, and go through a process of implementing one variable change at a time and record the outcome.
        - Once I feel satisfied with one model type, I would attempt a second approach, a different model. See how it compares.
        - I would perform this iteration through all the models I felt apply to the data and the goal.
- Documentation and Presentation:
    - The last step is to make sure all of my process and results are documented. I would take everything and then create a presentation or paper to explain all of my findings.

### Proposed Solution Design

The Insight: Based on my bivariate EDA, CONTACT events are relatively broad and densely populated across higher BLOCK_SCOREs. However, when we filter for QUOTE and APPLICATION, a much more distinct density patch emerges. The current scores (PHONE_SCORE, BLOCK_SCORE, etc.) seem well-suited for predicting initial contact, but we need to optimize for actual sales.

The Solution:  
I think an ensemble model would be an interesting approach to try. We have four score variables that get generated at the time of lead creation [email, address, phone, block]. Using this dataset, we can build a model to create a single score metric.  
Two Concerns:
- We cannot include any future features as predictors. We cannot create a prediction based on an event that has not happened yet. So, we cannot use INITIATION_TIMESTAMP, or any features engineered from this, as a predictor of our single score metric.
    - If these two engineered features revealed a strong pattern for success versus non-success, this would be a separate bit of information to provide to the salesperson (i.e., we see a lot of success happening on Mon-Wed between 10am - 12pm, so focus your high scorers in that window).
- Compounding bias. If the four score variables are themselves predicted values, they will come with some amount of error and bias. By building a new prediction model using those predicted values as independent predictors, we are compounding any error and bias. This is not ideal, and something to keep in mind when evaluating results.  

I propose building a supervised classification model (such as a Decision Tree / Random Forest or Support Vector Machine) optimized to predict the probability of a lead reaching the QUOTE or APPLICATION stage, rather than just the CONTACT stage.
- We have a large number of records that reach a CONTACT status. But converting to a QUOTE or APPLICATION stage is drastically less common.
    - If we can identify what makes those leads who commit further different from those who stop at CONTACT, we can make the SALESPERSON more efficient.
        - Making a call that lasts 10 seconds does not waste a ton of time; but compare that to a call that takes 10 minutes and does not become a QUOTE.
        - If we can increase the amount of CONTACT -> QUOTE conversions, that would increase efficiency. Make more contact calls matter.
- This now creates three classes for our records [No success, contact, conversion]
    - I would build out a multi-class classification model that gives the probability that a lead would result in any of our three classes.

Implementation: While the model outputs three probabilities (summing to 1.0), raw probabilities are not directly actionable for sales agents. Simply sorting by \(P(\text{Conversion})\) also ignores the operational cost of the other outcomes (e.g., spending 10 minutes on a "Contact" that doesn’t convert is worse than a quick "No Success" call).

To address this, I propose converting these probabilities into a single Expected Value (EV) Score. By assigning a business value or cost to each outcome (e.g., a heavy penalty for time-wasting "Contacts", a small penalty for "No Success", and a strong reward for "Conversions"), we get:

Expected Value = \((P_{\text{NoSuccess}} \times \text{Cost}_{\text{NoSuccess}}) + (P_{\text{Contact}} \times \text{Cost}_{\text{Contact}}) + (P_{\text{Conversion}} \times \text{Reward}_{\text{Conversion}})\)

Sales agents would then sort their leads by this score, ensuring high-conversion leads are prioritized while penalizing time-wasting calls. This approach better aligns the model’s output to actual business objectives.

Measuring Success: To evaluate this model versus the current system, track an Adjusted Efficiency Metric along with baseline conversion rates:

- **Baseline**: Total Applications Submitted / Total Calls Made
- **Adjusted Efficiency**: Applications Submitted / \((1 - \text{avg}(\text{prediction score of accepted applications})) \times \text{number of calls}\)

This measure penalizes the model if successful applications come from low-scoring leads (misses) and rewards it when high scores match successful outcomes. Validation would be via A/B testing with leads split between the new model and the baseline.

This metric can also be adapted to include both QUOTE and APPLICATION stages for a more direct comparison with the baseline.

### AI Disclosure

In accordance with SVG Analytics' guidelines, I utilized AI responsibly during this assessment. I used an AI assistant (Google's Gemini) as a coding assistant. It helps with making Python code more efficient, especially with plotting. It also helps with reformatting long string text into markdown. All critical thinking, logic, and code architecture are my own.