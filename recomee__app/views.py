from django.shortcuts import render
from joblib import load
# from .models import InputResults


def get_started(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        return render(request, 'get_user_input.html')
    return render(request, 'get_started.html')


def career_results(request):
    if request.method == 'POST':
        user_course = request.POST.get('course')
        user_skills = request.POST.get('skills')
        user_interest = request.POST.get('interest')
        user_industry = request.POST.get('industry')

        # Combine user input into a single string
        user_input_combined = ' '.join([user_course, user_skills, user_interest, user_industry])

        # Load the model and vectorizer
        vectorizer = load('recomee__app/models/ml_vectorizer.joblib')
        nb_model = load('recomee__app/models/ml_model.joblib')

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
        # username = request.session.get('username')
        prediction_result = InputResults(
            user_course=user_course,
            user_industry=user_industry,
            user_skills=user_skills,
            user_interest =user_interest,
            career_one=top_three_predictions[0],
            career_two=top_three_predictions[1],
            career_three=top_three_predictions[2],
            career_one_prob=top_three_probabilities[0],
            career_two_prob=top_three_probabilities[1],
            career_three_prob=top_three_probabilities[2])
            
        prediction_result.save()
    
        if top_three_probabilities[0] < 0.03:
            return render(request, 'no_results.html')
        
        combined_results = {**top_one, **top_two, **top_three,}
        
        return render(request,'app_result.html', {
        **combined_results,
        'top_three_predictions': top_three_predictions,
        'top_three_probabilities': top_three_probabilities, 
        })
    return render(request, 'get_user_input.html')


def test(request):
    return render(request, "index.html")


def display_data(request):

    prediction_result = InputResults.objects.all()
    return render(request, 'history_page.html', {'prediction_result': prediction_result})