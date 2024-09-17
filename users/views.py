from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from users.forms import UserRegistrationForm

from django.utils import timezone
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from users.models import CustomUser


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login_page.html', {'error': 'Invalid email or password', 'email': email})
    return render(request, 'login_page.html')


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set user to inactive initially
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Send activation email
            activation_link = request.build_absolute_uri(reverse('activate', args=[user.email]) )

            subject = 'Activate Your Account'
            html_message = render_to_string('activation_email.html', {'activation_link': activation_link})
            plain_message = strip_tags(html_message)
            from_email = 'noreply.nnuh.research@najah.edu'
            send_mail(subject, plain_message, from_email, [user.email], html_message=html_message)

            messages.success(request, 'Registration successful! Please check your email to activate your account.')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register_page.html', {'form': form})

@login_required
def home_view(request):
    return render(request, "home_page.html")

def activate(request, email):
    user = get_object_or_404(CustomUser, email=email)  # Use email to get the user
    user.is_active = True  # Activate the user account
    user.save()
    messages.success(request, 'Your account has been activated. You can now log in.')
    return redirect(request, 'login')


def send_test_email(request):
    messages.success(request, 'Registration successful! Please check your email to activate your account.')
    return render(request, 'login_page.html')