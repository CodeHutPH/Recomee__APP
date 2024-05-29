from django.shortcuts import render, redirect
from joblib import load
from .models import InputResults
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm




def get_started(request):
    return render(request, 'get_started.html')

def user_registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('get_started')  # Redirect to 'get_started' after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'dashboard.html')  # Redirect to 'get_user_input' after successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else: 
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return render(request, 'get_started.html')

@login_required
def career_results(request):
    if request.method == 'POST':
        user_course = request.POST.get('course')
        user_skills = request.POST.get('skills')
        user_interest = request.POST.get('interest')
        user_industry = request.POST.get('industry')

        # Combine user input into a single string
        user_input_combined = ' '.join([user_skills, user_interest, user_industry])

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

        combined_results = {**top_one, **top_two, **top_three,}

        first_probability = int(top_three_probabilities[0] * 100)
        second_probability = int(top_three_probabilities[1] * 100)
        third_probability = int(top_three_probabilities[2] * 100)

        # Get the logged-in user
        user_instance = request.user

        # Save history entry associated with the logged-in user
        InputResults.objects.create(
            user=user_instance,
            user_course=user_course,
            user_industry=user_industry,
            user_skills=user_skills,
            user_interest=user_interest,
            career_one=top_three_predictions[0],
            career_two=top_three_predictions[1],
            career_three=top_three_predictions[2],
            career_one_prob=int(top_three_probabilities[0] * 100),
            career_two_prob=int(top_three_probabilities[1] * 100),
            career_three_prob=int(top_three_probabilities[2] * 100)
        )

        context = {
            'first_probability': int(top_three_probabilities[0] * 100),
            'second_probability': int(top_three_probabilities[1] * 100),
            'third_probability': int(top_three_probabilities[2] * 100),
        }

        return render(request,'app_result.html', {
            **combined_results,
            **context,
            'top_three_predictions': top_three_predictions,
            'top_three_probabilities': top_three_probabilities, 
        })
    return render(request, 'get_user_input.html')

@login_required
def display_data(request):
    user_results = InputResults.objects.filter(user=request.user)
    return render(request, 'history_page.html', {'user_results': user_results})