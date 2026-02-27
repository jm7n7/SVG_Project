# Data Dictionary for provided_data.csv
The code to generate this information is in 'data_dictionary.py'

## Feature Information
### Unnamed: 0
- **Dtype:** int
- **Description:** most likely an artifact of 'row-names'. It simply spans 0 - len(data) in numerical order.
- **min:** 0
- **max:** 141929
- **med:** 70964.5
- **mean:** 70964.5
- **Notes/Comments:** Can either be dropped or renamed and converted to index.

### MATCHER_EVENT_ID
- **Dtype:** int
- **Description:** Possibly a unique ID for the given contact event.
- **min:** 62380981
- **max:** 64226019
- **med:** 63303519.5
- **mean:** 63303500.1786
- **Notes/Comments:** what happens if there are multiple call sessions with the same lead?

### LEADS_PII_ID
- **Dtype:** int
- **Description:** Possibly a unique ID for the lead / customer.
- **min:** 55937392
- **max:** 59600537
- **med:** 57768964.5
- **mean:** 57768863.3103
- **Notes/Comments:**

### AGENT_ID
- **Dtype:** int
- **Description:** Possibly a unique ID for the salesperson.
- **min:** 600000
- **max:** 737520
- **med:** 661884.0
- **mean:** 663009.7925
- **Notes/Comments:**

### DIAL_COUNT
- **Dtype:** int
- **Description:** Not too sure. Possibly the amount of contact attempts it took to make successful contact with the lead.
- **min:** 1
- **max:** 19
- **med:** 3.0
- **mean:** 3.6448
- **Notes/Comments:** Does this number include the actuall contacting call? i.e. if I called 9 times, but on the 10th they finally answered, is this value 9 or 10?

### AGE
- **Dtype:** int
- **Description:** The age of the lead.
- **min:** 18
- **max:** 125
- **med:** 70.0
- **mean:** 71.3657
- **Notes/Comments:**

### STATE
- **Dtype:** object
- **Description:** The state in which the lead resides.
- **Unique:** ['MI', 'MD', 'WI', 'IN', 'DE', 'GA', 'SC', 'IL', 'SD', 'NH', 'TX', 'VA', 'KY', 'NJ', 'PA', 'TN', 'IA', 'OH', 'OK', 'KS', 'MS', 'NC', 'MO', 'LA', 'AR', 'AL', 'WV', 'AZ', 'UT', 'MT', 'ID', 'ND', 'CO', 'WY', 'OR', 'NV']
- **Notes/Comments:**

### GENDER
- **Dtype:** object
- **Description:** The gender of the lead.
- **Unique:** [nan, 'F', 'M']
- **Notes/Comments:** There are some nan values. Could be from abstain or true missing at random? Will need to decide on how to treat feature. Could provide some insight, or might be insignificant. Possible to create a third "unknown" category to still allow its use.

### LEAD_COST
- **Dtype:** float
- **Description:** Possibly the amount of money ($) it cost the company to know about this lead/customer?
- **min:** 0.0
- **max:** 150.0
- **med:** 29.91
- **mean:** 33.9706
- **Notes/Comments:** Not 100% certain on this feature and my description of it.

### PHONE_TYPE
- **Dtype:** object
- **Description:** Assuming the type of phone used by the lead (landline, mobile, cell, house,...)
- **Unique:** ['P2', 'I9', 'A7', 'B5', nan]
- **Notes/Comments:** Possible google search later to see if these are standard categories? There are some nan values. Will need to investigate to see how many are missing. Intuition thinks this feature most likely wont correlate to anything beneficial, but leave room to be surprised.

### SECONDS_AVAILABLE
- **Dtype:** int
- **Description:** DO NOT KNOW (Still need to figure out)
- **min:** -52
- **max:** 4929
- **med:** 0.0
- **mean:** 4.8579
- **Notes/Comments:** Based on the context clues of the stats, I do not have much of a clue. A negative min with a very large max, but a median around 0 tells me this feature is probably very unimodal around 0, with a couple outliers.

### TREATMENT_GROUP
- **Dtype:** object
- **Description:** Some sort of categorical. Not sure what it signifies.
- **Unique:** ['full_dials_lifo', 'full_talk_to_spend_v1', nan]
- **Notes/Comments:** not really sure which each group signifies, but there are some nans. Will need to see how many. What does a nan mean? Is it possible to create a new treatment group, similar to the method of gender? Will that muddy class seperation?

### LEAD_CREATION_DATE
- **Dtype:** object
- **Description:** The date and time in which the lead was created.
- **Unique:** (sample) ['2025-11-03 08:01:02', '2025-11-03 08:01:19', '2025-11-03 08:01:42', ...]
- **Earliest:** 
- **Latest:** 
- **Notes/Comments:** Most likely the moment they entered the lead pool and had their prediction score generated. Not sure what time zone this is standardized in (assuming central).

### SOURCE_TYPE
- **Dtype:** object
- **Description:** Possibly the method in which SVG learned of this lead.
- **Unique:** ['Form', 'Delivery']
- **Notes/Comments:** Either a self submitted from, or an 3rd party delivered aquisition?

### LEAD_SOURCE
- **Dtype:** object
- **Description:** Categorical identifier for the entity that provided a lead.
- **Unique:** ['source_23', 'source_02', 'source_20', 'source_03', 'source_06', 'source_07', 'source_16', 'source_00', 'source_09', 'source_27', 'source_13', 'source_22', 'source_01', 'source_05', 'source_18', 'source_14', 'source_41', 'source_12', 'source_39', 'source_10', 'source_29', 'source_19', 'source_36', 'source_11', 'source_24', 'source_08', 'source_40', 'source_31', 'source_15', 'source_25', 'source_42', 'source_26', 'source_21', 'source_32', 'source_33', 'source_35', 'source_44', 'source_17', 'source_28', 'source_45', 'source_37', 'source_04', 'source_30', 'source_38', 'source_34', 'source_43']
- **Notes/Comments:** Lots and lots of sources that can provide lead data. Perhaps there are some sources that have a better track records than others?

### INITIATION_METHOD
- **Dtype:** object
- **Description:** Assuming the method used to initiate contact to a lead (outbound call).
- **Unique:** ['OUTBOUND']
- **Notes/Comments:** Since this feature is just one value, it can most likely be ignored entirely.

### INITIATION_TIMESTAMP
- **Dtype:** object
- **Description:** The date and time at which initial contact has been made with a lead.
- **Unique:** (sample) ['2025-11-03 08:01:07', '2025-11-03 08:01:25', '2025-11-03 08:01:55', ...]
- **Earliest:** 
- **Latest:** 
- **Notes/Comments:** Assuming this value does not get overwritten by any possible follow up calls for quote / application submission if the customer was not able to do everything in one session.

### AGENT_INTERACTION_DURATION
- **Dtype:** int
- **Description:** How long (possibly in minutes) the salesperson spends time talking with the lead.
- **min:** 0
- **max:** 11203
- **med:** 10.0
- **mean:** 65.3368
- **Notes/Comments:** If multiple calls, does this aggregate a sum of time? Assuming scale is in minutes, the max value is suspect (186 hours). Assuming seconds, max value is (186 minutes). The average is heavily skewed but median would sit at either 10 minutes or 10 seconds. 10 seconds seems unreasonably fast, unless its an almost instant hangup.

### DISCONNECT_REASON
- **Dtype:** object
- **Description:** Category for how the call ended.
- **Unique:** ['AGENT_DISCONNECT', 'OTHER', 'CUSTOMER_DISCONNECT', 'THIRD_PARTY_DISCONNECT', 'TELECOM_NUMBER_INVALID', 'TELECOM_ORIGINATOR_CANCEL', 'TELECOM_PROBLEM', 'TELECOM_POTENTIAL_BLOCKING', 'TELECOM_UNANSWERED', 'TELECOM_BUSY', 'TELECOM_TIMEOUT']
- **Notes/Comments:** Quite a few classes, but most are very similar to each other. Possible room to do some class grouping to reduce dimensionality.

### AGENT_AFTER_CONTACT_WORK_DURATION
- **Dtype:** int
- **Description:** How long in some unit of time the salesperson proceeded to work on the specific leads case.
- **min:** 0
- **max:** 241772
- **med:** 3.0
- **mean:** 66.5061
- **Notes/Comments:** Another unclear unit of time.

### ELIGIBLE_FOR_REPURCHASE
- **Dtype:** int
- **Description:** Binary indicator variable to identify if the lead is able to perform a 'repurchase'.
- **min:** 0
- **max:** 1
- **med:** 0.0
- **mean:** 0.3996
- **Notes/Comments:** I am not really sure what a 'repurchase' is or means. Are these customers who, if they would submit an application, be allowed/required to repurchase for the next year?

### EMAIL_SCORE
- **Dtype:** int
- **Description:** Some sort of continuous score metric in relation to email.
- **min:** 0
- **max:** 100
- **med:** 38.0
- **mean:** 44.5072
- **Notes/Comments:** Most likely a measure of probability to receive successful contact through email medium.

### ADDRESS_SCORE
- **Dtype:** float
- **Description:** Some sort of continuous score metric in relation to address.
- **min:** 31.0
- **max:** 100.0
- **med:** 74.9
- **mean:** 74.8785
- **Notes/Comments:** Most likely a measure of probability to receive successful contact through physical mail medium.

### PHONE_SCORE
- **Dtype:** int
- **Description:** Some sort of continuous score metric in relation to phone.
- **min:** 0
- **max:** 95
- **med:** 43.0
- **mean:** 43.5823
- **Notes/Comments:** Most likely a measure of probability to receive successful contact through phone call medium.

### BLOCK_SCORE
- **Dtype:** float
- **Description:** Some sort of continuous score metric in relation to block.
- **min:** 0.0
- **max:** 73.1
- **med:** 29.69
- **mean:** 29.5068
- **Notes/Comments:** Most likely a measure of probability that the lead blocks the salespersons number?

### CONTACT
- **Dtype:** int
- **Description:** Binary indicator to show CONTACT Status.
- **min:** 0
- **max:** 1
- **med:** 0.0
- **mean:** 0.08
- **Notes/Comments:**

### QUOTE
- **Dtype:** int
- **Description:** Binary indicator to show QUOTE Status.
- **min:** 0
- **max:** 1
- **med:** 0.0
- **mean:** 0.0219
- **Notes/Comments:**

### APPLICATION
- **Dtype:** int
- **Description:** Binary indicator to show APPLICATION Status.
- **min:** 0
- **max:** 1
- **med:** 0.0
- **mean:** 0.0125
- **Notes/Comments:**  This marks a sale success. Based on the quick stats, there are almost none...
