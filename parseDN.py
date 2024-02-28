import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
from datetime import datetime
import re
from alive_progress import alive_bar

# Read in articles
# Replace with name of input excel file.
# This excel file should have two columns: "Text" and "Rubrik". 
# The text will be analyzed, and the Rubrik is used to key the articles afterwards.
# A sample data file is included with only 3 articles.
df = pd.read_excel('sample_data_dn.xlsx')

# Two different word lists for looking at deaths or AAAAAAA
# Comment out the appropriate word list for the analysis you want to do.
# 1. Word list for looking at mentions of deaths only
words = ['dör?', 'dog', 'dötts?', 'dödats?', 'dödades?', 'döds\w{1,15}', 'döda',
         'mörda\w{0,3}', 'mord\w{0,2}',
         'massak\w{0,8}',
         'massmord\w{0,2}',
         'slakt\w{0,5}'
        ]

# 2. Word list for looking at emotive words and antisemitism and islamophobia.
words = ['mörda\w{0,3}', 'mord\w{0,3}',
         'massak\w{0,8}',
         'massmord\w{0,3}',
         'slakt\w{0,5}',
         'blodig\w{0,4}',
         'brutal\w{0,4}',
         'antisemit\w{0,5}',
         'judehat\w{0,4}',
         'islamofob\w{0,4}',
         'muslimhat\w{0,4}',
         'gisslan\w{0,14}',
         'kidnapp\w{0,14}',
         '\w{0,4}fånga\w{0,7}'
        ]

# Length of raw data
N = len(df)

# Build the regex pattern for the word list.
# re library does not support variable-length lookbehinds, so need to run three patterns, one for each possible sentence start. 
# Then merge the results.
# Looks for words in a sentence. Captures the whole sentence and the matched word.
# Three patterns because re library doesn't allow for variable length lookbehinds.
# The lookbehind enforces that the sentences is preceded by \n, ^, or ". ".
pattern_base = r"([^.\n]*?(" + "|".join(words) + r")(?:[ ,;:][^.\n]+?)?[.?!])"
patterns = ["(?<=^)" + pattern_base,
            "(?<=\n)" + pattern_base, 
            "(?<=[.!?] )" + pattern_base]

# Print the patterns to see.
print(patterns[0])

# Pattern to find the date in the DN articles.
pattern_date = r"Publicerad (\d{4}-\d{2}-\d{2})"

# Init output dataframe
out = pd.DataFrame(columns=['date', 'headline', 'sentence', 'matched word'])

# Loop through articles
with alive_bar(N) as bar:
    for i in range(N):
        bar()

        # get data from frame
        text = df.loc[i, 'Text']
        headline = df.loc[i, 'Rubrik']

        # Extract date
        date_all = re.findall(pattern_date, text)
        date = date_all[0] if len(date_all) > 0 else "[UNKNOWN]"

         # Build up list of all matches in expressions list
        expressions = []
        # Loop through patterns and match
        for pat in patterns:
            expressions = expressions + re.findall(pat, text, re.IGNORECASE)

        # For each match, save it to the output dataframe
        for match in expressions:
            # print("Match:\n\t{}\n\t{}".format(match[0], match[1]))
            out = out.append({
                'date': date,
                'headline': headline,
                'sentence': match[0],
                'matched word': match[1]
            }, ignore_index=True)

# Save data
timestring = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_filename = "./dn/results/script_out_{}.xlsx".format(timestring)

# Write the DataFrame to an Excel file
out.to_excel(output_filename, index=False)
print("Saved results to {}".format(output_filename))