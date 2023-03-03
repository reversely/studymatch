# Import required libraries
import numpy as np
from scipy.spatial.distance import cosine
import csv

# Read survey responses from CSV file
with open('matches.csv', newline='') as csvfile:
    survey_responses = np.array(list(csv.reader(csvfile, delimiter=','))).astype(int)

# Define a function to calculate the cosine similarity between two respondents
def similarity(respondent_1, respondent_2):
    return 1 - cosine(respondent_1, respondent_2)

# Define a function to sort the matched respondents by compatibility
def sort_matches(matches, respondent):
    similarities = [similarity(respondent, survey_responses[match]) for match in matches]
    sorted_matches = [match for _, match in sorted(zip(similarities, matches), reverse=True)]
    return sorted_matches

# Match respondents based on their similarity of answers
matched_respondents = {}
for i, respondent in enumerate(survey_responses):
    # Find respondents with matching responses to first three questions
    matching_indices = [j for j, r in enumerate(survey_responses) if (r[0]==respondent[0] and r[1]==respondent[1] and r[2]==respondent[2]) and j != i]
    # Sort matching respondents by compatibility with the current respondent
    sorted_matches = sort_matches(matching_indices, respondent)
    # If there are less than 3 matches, find additional matches from non-matching respondents
    if len(sorted_matches) < 3:
        non_matching_indices = [j for j, r in enumerate(survey_responses) if j not in matching_indices and j != i]
        non_matching_sorted = sort_matches(non_matching_indices, respondent)
        # Add indication in the print statement that the additional matches are from non-matching respondents
        if len(non_matching_sorted) >= 3 - len(matching_indices):
            print(f"Respondent {i+1} also matches with Respondent(s) {', '.join([str(non_matching_sorted[j]+1) for j in range(3 - len(matching_indices))])} from non-matching respondents.")
        sorted_matches += non_matching_sorted[:3-len(sorted_matches)]
    # Print the matched respondents
    matched_respondents[i] = sorted_matches[:3]
    if respondent[2] == 2:
        # If the respondent's answer to Q3 is 2, check if their matches have the same answer for Q4
        for match in matched_respondents[i]:
            if survey_responses[match][3] == respondent[3]:
                print(f"Respondent {i+1} matches with Respondent {match+1}")
            else:
                print(f"Respondent {i+1} matches with Respondent {match+1}, but their answer to Q4 is different")
