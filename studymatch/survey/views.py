from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import csv

def survey(request):
    if request.method == 'POST':
        # Retrieving survey responses from form submission
        responses = []
        for i in range(1, 9):
            response = int(request.POST[f'q{i}'])
            responses.append(response)

        # Saving the survey responses to CSV
        with open('matches.csv', mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(responses)

        # Completing survey
        return HttpResponseRedirect(reverse('survey_thanks'))

    else:
        # Rendering the survey form
        return render(request, 'survey.html')
