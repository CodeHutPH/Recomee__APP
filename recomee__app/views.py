from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from joblib import load
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Create your views here.

def get_started(request):
    if request.method == 'POST':
        return render (request, 'get_user_input.html')
    return render (request, 'get_started.html')


def career_results(request):
    if request.method == 'POST':
        user_course = request.POST.get('course')
        user_skills = request.POST.get('skills')
        user_interest = request.POST.get('interest')
        user_industry = request.POST.get('industry')

        # Combine user input into a single string
        user_input_combined = ' '.join([user_course, user_skills, user_interest, user_industry])

        # Load the model and vectorizer
        vectorizer = load('thesisapp/models/ml_vectorizer.joblib')
        nb_model = load('thesisapp/models/ml_model.joblib')

        # Transform user input into numerical format
        user_input_vec = vectorizer.transform([user_input_combined])

        # Make a prediction and get probability estimates
        prediction_probabilities = nb_model.predict_proba(user_input_vec)[0]

        # Get the indices of the top three predictions
        top_three_indices = prediction_probabilities.argsort()[-4:][::-1]

        # Get the top three predictions and their probabilities
        top_three_predictions = nb_model.classes_[top_three_indices]
        top_three_probabilities = prediction_probabilities[top_three_indices]

        # Assigning results in a variable to be used for HTML
        top_one = {'first_career' : top_three_predictions[0].upper(), 'first_probability': '{:.2f}'.format(top_three_probabilities[0] * 100)}
        top_two = {'second_career' : top_three_predictions[1].upper(), 'second_probability' : '{:.2f}'.format(top_three_probabilities[1] * 100)}
        top_three = {'third_career' : top_three_predictions[2].upper(), 'third_probability' : '{:.2f}'.format(top_three_probabilities[2] * 100)}
        # top_four = {'fourth_career' : top_three_predictions[3].upper(), 'fourth_probability' : '{:.2f}'.format(top_three_probabilities[3] * 100)}

    
        if top_three_probabilities[0] < 0.03:
            return render(request, 'no_results.html')
        
        combined_results = {**top_one, **top_two, **top_three,}
        
        return render(request,'app_result.html', {
        **combined_results,
        'top_three_predictions': top_three_predictions,
        'top_three_probabilities': top_three_probabilities, 
        })
    return render(request, 'get_user_input.html')