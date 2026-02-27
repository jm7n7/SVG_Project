# **First Step: Problem Breakdown**
The very first step in my process, before any code is written, is to understand the assignment. After reviewing the provided `Junior Data Scientist Project.pdf`, here is a cleaned outline of my reasoning and understanding. (I originally write out on paper, then translate to markdown)

---

## Dataset Overview
This dataset contains records about potential customers, referred to as **Leads**. Each lead can progress through three key statuses:

- **Contact:** Customer answers a salesperson's call (removed from pool of active leads).
- **Quote:** After a successful contact, if the customer is eligible for the service, they are given a quote.
- **Application:** If the customer accepts the quote, they proceed to submit a formal application.

The path for a typical lead is:

1. **Lead** is in the pool.
2. **Contact** is made → Status updates.
3. If qualified, lead receives a **Quote** → Status updates.
4. If interested, lead submits an **Application** → Status updates.

---

## Prediction Model
- Each lead is assigned a **prediction score** estimating their likelihood to become a sale (i.e., to submit an application).
- Salespersons view and call leads sorted by this score (highest first).

**Key Problem:**  
How can we improve the prediction score (and/or model) to maximize sales (applications submitted)?

---

## Key Questions
1. **Post-Contact Management:**  
   What happens to customers who have been contacted but either aren't eligible or aren't interested?  
   - Are they only removed from the calling pool but still recorded in the dataset?
   - Do they ever re-enter the pool after some time?
2. **Lead Status Distribution:**  
   - What percentage of the dataset have each status (contacted, quoted, application)?
   - Does the dataset only include leads who have been contacted? (Assumption: Yes, but to confirm.)
3. **Prediction Score Characteristics:**  
   - What is its range and distribution? Is it a 0-10 / 0-100 value that tries to give a percentage likelihood or probability?
   - Is it binary (e.g., likely/unlikely with threshold), or continuous?
4. **Score Dynamics:**  
   - Does the prediction score update after each contact attempt, or is it fixed per lead?
   - Is the model using only static features? (Assuming the prediction score model is trained on external features from this dataset)
5. **Model Validation and Business Objectives:**  
   - What does success look like? Getting to an application status is the goal. However, because we are trying to validate the ability of the prediction score model, we 
really only want to see application status on those leads who have a high prediction score. Application status leads with low prediction scores, although good for the company, are not good 
for the accuracy of the model.
   - Does the model skew pessimistic or optimistic?
   - There are potential model training biases that could be considered, but for the scope of this assignment, I think that might be diving a bit too far. Looking into bias would be a way to 
possibly improve the model, but I wont focus on that too much here.
   - Quantify the business need. The goal is to maximize sales. That means making the salespersons more efficient. Less time calling with zero contact, or with leads that are not applicable / 
do not want the service. Making an assumption before looking at the data, there are probably a higher proportion of non-sales compared against submitted applications. Currently, the model is 
set up as a positive reinforcement; salespersons look to the highest prediction score, thinking they are the most likely to submit an application. Low scores are assumed to be instant no's. 
(I would like to look at the accuracy of the 'assumed dominant class' and see how often low scores submit applications)

---

## Metrics
- **Basic Efficiency Ratio:**
  - `applications submitted / number of calls`
    - A higher number indicates greater efficiency.

- **Adjusted Efficiency Metric (using prediction scores):**
  - If prediction scores are not binary:
    - `applications submitted / [(1 - avg(prediction score of accepted applications)) × number of calls]`
    - Rationale:  
      - High average prediction scores for successful applications indicate that the model is prioritizing the right leads.
      - Lower average scores (i.e., when applications come from low-scoring leads) penalize the metric, highlighting model improvement needs.
      - Possible issue with this metric is that there might not be enough volumne of submitted application records. Might not be a true representation.

---

# **Second Step: Data Dictionary Generation**
Upon receiving the dataset with no dictionary, my next move is to create the Data Dictionary myself to better understand what the data is even consisting of. Using some basic python code to explore the specifics of the dataset. Extracting all features with their types, basic stats, and unique values. This allows me to see a bit better about what each individual feature is. Then, I can look at each individual one and either deduce or assume a description. This data dictionary is created as a markdown document 'data_dictionary.md'.

## TLDR of the Data Dictionary
### Thoughts
- There are a couple of fields that, even through data context, I am still not 100% sure on what they represent. In a real world scenario for which I am an employee working at SVG, I would try to look up any internal documents to identify what the feature represents, or I would simply ask a coworker or manager to see if they were familiar.
- The biggest discovery is that the 'predictive_score' outlined in the project document is not one singular feature, but rather four individual scores [email, address, phone, block]. This definetly changes any sort of singular approach I had in mind for model performance validation, comparrison, and improvement suggestion. Assuming the salesperson is only going to perform calls, we can isolate the phone and block scores and disregard the email and address scores.

### Fields with NAN values:
- **Gender**             (63194)
- **Phone Type**         (28527)
- **Treatment Group**    (327)
- **Lead Cost**          (43885)
I will have to address these in my data cleaning/exploration step.

### Planned explorations:
- Based on the current data, what are the ratios that exist?
    - How many CONTACT / QUOTE / APPLICATION
    - Of all APPLICATION, what were the PHONE and BLOCK scores?
- Are there any trends in Gender, Age, State, Phone Type, Lead Source?
- Investigate day and time of contacts in relation to success metrics.
- Generate the efficiency validation statistics.

### Planned Feature Engineering:
- We can break our two date features apart.
    - Lead Creation Date (Most likely not important)
    - Initiation Timestamp
        - Current both Y-M-D and H-M-S are combined. We can strip this into day and time features.
        - This allows for trend analysis for specific time of year, as well as time of day.
- Gender can have a new "unkown" class hot encoded into all 'nan' value records
- Treatment Group might get a new "unkown" class hot encoded for its 'nan' value records. (only 327 missing records is very low for the ~142,000 total records) If the class separation is strong, we could just drop the 327 records with a missing value. Will need to investigate.

# **Third Step: Data Cleaning**
Time to look into all of the features with missing values. All of my data cleaning was conducted in the 'data_cleaning.py' file. The result of this code was a cleaned csv file (as to not overwrite the original).

GENDER, PHONE_TYPE, and TREATMENT_GROUP were all handled similarly. They were simply given a new class of "Unknown" to be filled into their nan values.
- GENDER: The majority was missing, but it is possible in exploration that Male/Female dynamics could be pattern seeking.
- PHONE_TYPE: All classes, including the nan values, had almost equal representation. It is possible that these nan values actually represent a real class that just so happened to be missed in this dataset. By setting them to "Unkown", we essentially fix this and allow for all those nans to be grouped together (Really big assumption that could haunt us later).
- TREATMENT_GROUP: The amount of missing records here was incredibly low compared to the entire dataset. However, the features that seem to have strong importance had significant values that I feel should not be disregarded. It might be possible to go through each record and try to identify which of the two classes each missing value record belongs to, but given its even distribution, I figured correctly classifying them might not matter too much. We simply need to give it a class value as to retain it in our data.

LEAD_COST was a bit of a similar story, but require much more of a process. There was a much larger portion of the dataset that was missing. To investigate, I first looked at the distribution of the values for what was not missing. This distribution revealed some unnatural tendencies, bringing me to conclude that a simple global average hot encoding would not be a good idea. This led me to look at two other features [LEAD_SOURCE, SOURCE_TYPE]. I checked the proportion of the SOURCE_TYPE class and found very few 'Form' class had a value for LEAD_COST. On top of this, every value was 0.00. I then checked the opposite, whatthe SOURCE_TYPE value was for all of our missing LEAD_COST records. Every single one was a 'Form' class value. This led me to believe that it might be possible to simply replace all nan LEAD_COST values with a value of 0.00. Before I fully submitted to that idea, I decided to check the count values for our different LEAD_SOURCE classes. I identified which sources had missing LEAD_COST values and the total count of missing records. Then, I checked to see if those sources had any non-missing values in the data set. Every single source that had at least one missing LEAD_COST value had 0 non-missing records. This confirmed for me that we can go ahead and fill in all missing LEAD_COST values as 0.00.

# **Forth Step: Data Exploration**
## Identifying Outliers
I started by isolating all of the numerical features. Then, I analyzed each feature based on tukeys fences. The first pass used normal quartile ranges of 0.25 and 0.75 with a 1.5 IQR coeff. The second pass expanded the quartile ranges to 0.1 and 0.9, keeping the IQR untouched. The thought process here is that if there is a grouping of records that exist beyond these boundaries, even if it is a small sample, it is most likely true data and not a recording error. If there are only a handful of records for a feature that pass these bounds, they are more likely to be mistakes in the data. For this kind of real world data, having a true, representable outlier is not necessarily a bad thing. It is simply mistaken data that I would like to remove/correct. Based on my analysis, I only see possible concern with the DIAL_COUNT feature. there were 21 records that existed outside the second pass fences. Given the full scope of a real project*, I would investigate this further; but as I am running short on my 4 hour alotment, I would like to continue on and assume everything is all okay from an outlier perspective.

## Relationships and Ratios
### Evaluating Success:
_see plots:_ ```'phone_vs_block_apps.png', 'phone_vs_block_quote.png', 'phone_vs_block_contact.png', 'phone_vs_block_nosuccess.png'```  

I began to explore the minority of records in the data that had any sort of status [CONTACT, QUOTE, APPLICATION]. Of the 141,930 total records, only 11,360 made it to the CONTACT status. Of those, 3,109 made it to the QUOTE status. Of those, 1,771 actually submitted an APPLICATION. When plotting just the records with an application, we can see the distribution of PHONE_SCORE to BLOCK_SCORE. We want to see the majority of records exist in the bottom right, High phone with low block. This is pretty close to the reality, albeit the trend of the data is uniformly chaotic, well dispersed in the area.

When I expand to looking at all QUOTE records, the same pattern emerges. The majority of the data is consistent / near identical to the application records.

When I expand to all CONTACT records, we see a very different distribution. There are much more records that exist higher up in BLOCK_SCORE. This suggests that it is easier to get first contact, but moving the lead into a QUOTE status is more of a defined separation. We might be able to define a support vector between the CONTACT customers and the QUOTE/APPLICATION customers.

When I looked at the 130,570 records that did not have any status indicator, there was essentially just a giant block. Every Phone and block score was well represented. There was no pattern discernable.


#------------------ I N T E R U P T I O N ------------------
It is at this time that I have approached my 4 hour time limit. I had spent roughly an hour and a half doing my initial processing and breakdown of the task, as well as create the Data Dictionary. In my process, I really emphasize having a full understanding before I begin to investigate, explore, and come up with a hypothesis.

I had then spent another hour and a half on cleaning up my documentation, performing the data cleaning, and doing the quick outlier checks. I find that it is better to clean and re-organize any code or markdown documents as you build. I know this can be quite time consuming, but it is very easy to lose control and get messy with note taking and documenting your thought process when working on projects, especially when its a new dataset that you are not quite familiar with.

Over the last hour I have been working exploring the relationships. Unfortunately, I was only able to get through the initial exploration of the status indicators and how to measure the current effectiveness of the prediction score model. I was able to plot these features, and get the basic stat line, but I was not able to measure its current effectiveness. I also was not able to fully implement the other explorations that I planned on accomplishing from the planned sections of step 2;

- Are there any trends in Gender, Age, State, Phone Type, Lead Source?
- Investigate day and time of contacts in relation to success metrics.
- Generate the efficiency validation statistics.
- We can break our two date features apart.
    - Lead Creation Date (Most likely not important)
    - Initiation Timestamp
        - Current both Y-M-D and H-M-S are combined. We can strip this into day and time features.
        - This allows for trend analysis for specific time of year, as well as time of day.
- Gender can have a new "unkown" class hot encoded into all 'nan' value records
- Treatment Group might get a new "unkown" class hot encoded for its 'nan' value records. (only 327 missing records is very low for the ~142,000 total records) If the class separation is strong, we could just drop the 327 records with a missing value. Will need to investigate.

These were going to be my next exploration steps.