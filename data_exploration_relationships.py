# Load libraries / packages
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

SEP = "-" * 100

# -----------------------------------------------------------------------------
# Load data
# -----------------------------------------------------------------------------
data = pd.read_csv("data_cleaned.csv")
print(len(data))
print(SEP)

# -----------------------------------------------------------------------------
# Identify how many CONTACT / QUOTE / APPLICATION
# -----------------------------------------------------------------------------
no_status_count = ((data[['CONTACT', 'QUOTE', 'APPLICATION']].sum(axis=1) == 0)).sum()
no_status_ratio = ((no_status_count/len(data)) * 100).round(2)
print(f"Records with no CONTACT/QUOTE/APPLICATION (i.e., zero in all three): {no_status_count} | {no_status_ratio}%")
print(SEP)

contact_amount = data['CONTACT'].sum()
con_ratio = ((contact_amount/len(data))*100).round(2)

quote_amount = data['QUOTE'].sum()
quote_ratio = ((quote_amount/len(data))*100).round(2)

application_amount = data['APPLICATION'].sum()
app_ratio = ((application_amount/len(data))*100).round(2)

print(f'CONTACT: {contact_amount} | {con_ratio}%\nQUOTE: {quote_amount} | {quote_ratio}%\nAPPLICATION: {application_amount} | {app_ratio}%')
print(SEP)

'''
Based on the quick analysis, a very small percentage of the dataset have indicators for our three status types.
- Contact:     11,360 | 8%
- Quote:       3109   | 2.19%
- Application  1771   | 1.25%
This shows a dominancy bias towards the negative. The vast majority of calls result in no contact, with even fewer making it to the Quote stage, and further fewer to the application stage.
'''

# -----------------------------------------------------------------------------
# Plot the PHONE & BLOCK scores for all records that were a status
# -----------------------------------------------------------------------------
# Filter records where APPLICATION == 1
applications = data[data['APPLICATION'] == 1]
# Create scatter plot of PHONE_SCORE vs BLOCK_SCORE
plt.figure(figsize=(8, 6))
plt.scatter(applications['PHONE_SCORE'], applications['BLOCK_SCORE'], alpha=0.5)
arc = Arc((95, 0), 55 * 2, 40, angle=0, theta1=90, theta2=180, color='red', alpha=0.4, linewidth=3)
plt.gca().add_patch(arc)
plt.xlabel('PHONE_SCORE')
plt.ylabel('BLOCK_SCORE')
plt.title('PHONE_SCORE vs BLOCK_SCORE for APPLICATION=1')
plt.grid(True)
plt.tight_layout()
plt.savefig('Plots_folder/phone_vs_block_apps.png')
plt.show()

'''
This plot reveals quite a lot of chaos. For all 1771 records that were an application, we see PHONE_SCORES ranging from 0 - 95.
We also see BLOCK_SCORES ranging from 0 - 36. There is more density on the right hand side (higher Phone score).
However, we see a uniform conal dispersion from the bottom right with no clear pattern.
The density of this cone appears to range from a Phone Score of 40 to a Block Score of 20.
'''

# Filter records where QUOTE == 1
quote = data[data['QUOTE'] == 1]
# Create scatter plot of PHONE_SCORE vs BLOCK_SCORE
plt.figure(figsize=(8, 6))
plt.scatter(quote['PHONE_SCORE'], quote['BLOCK_SCORE'], alpha=0.5)
arc = Arc((95, 0), 55 * 2, 40, angle=0, theta1=90, theta2=180, color='red', alpha=0.4, linewidth=3)
plt.gca().add_patch(arc)
plt.xlabel('PHONE_SCORE')
plt.ylabel('BLOCK_SCORE')
plt.title('PHONE_SCORE vs BLOCK_SCORE for QUOTE=1')
plt.grid(True)
plt.tight_layout()
plt.savefig('Plots_folder/phone_vs_block_quote.png')
plt.show()

# Filter records where CONTACT == 1
contact = data[data['CONTACT'] == 1]
# Create scatter plot of PHONE_SCORE vs BLOCK_SCORE
plt.figure(figsize=(8, 6))
plt.scatter(contact['PHONE_SCORE'], contact['BLOCK_SCORE'], alpha=0.5)
arc = Arc((95, 0), 55 * 2, 40, angle=0, theta1=90, theta2=180, color='red', alpha=0.4, linewidth=3)
plt.gca().add_patch(arc)
plt.xlabel('PHONE_SCORE')
plt.ylabel('BLOCK_SCORE')
plt.title('PHONE_SCORE vs BLOCK_SCORE for CONTACT=1')
plt.grid(True)
plt.tight_layout()
plt.savefig('Plots_folder/phone_vs_block_contact.png')
plt.show()

'''
By plotting the same features, but expanding to the QUOTE and CONTACT status, we can see the density of leads who did not convert to applications.
QUOTE did not reveal too much of a pattern difference. Everything was in the same conal tendency as Applications.
The CONTACT plot however had a much larger density patch at a higher BLOCK_SCORE. The Center seemed to be around a Phone score value of 70 and a Block score of 30.
This suggests that there is a level at which people will answer, but some plane that can be used to divide those that continue on to a QUOTE and eventually an APPLICATION.
'''

# Filter records where none of CONTACT, QUOTE, or APPLICATION is 1
no_success = data[(data['CONTACT'] != 1) & (data['QUOTE'] != 1) & (data['APPLICATION'] != 1)]
# Create scatter plot of PHONE_SCORE vs BLOCK_SCORE for these records
plt.figure(figsize=(8, 6))
plt.scatter(no_success['PHONE_SCORE'], no_success['BLOCK_SCORE'], alpha=0.5)
arc = Arc((95, 0), 55 * 2, 40, angle=0, theta1=90, theta2=180, color='red', alpha=0.4, linewidth=3)
plt.gca().add_patch(arc)
plt.xlabel('PHONE_SCORE')
plt.ylabel('BLOCK_SCORE')
plt.title('PHONE_SCORE vs BLOCK_SCORE for records with no CONTACT/QUOTE/APPLICATION')
plt.grid(True)
plt.tight_layout()
plt.savefig('Plots_folder/phone_vs_block_nosuccess.png')
plt.show()

'''
This plot does not reveal much. It is essentially a giant block that spans the entire spectrum. From low to high Phone Score, as well as low to high block score.
What this does tell us is that no status leads happen all across the board.
This also shows us that no contacts still happen with the high phone/low block combo.
There are tons of records that exist in the zone in which we would consider to be high potential for success.
Even within the red cone of APPLICATION success, there are tons of no status records.
We would have to investigate some other features to try and see if anything can explain this.
'''

