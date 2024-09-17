import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from users.forms import UserRegistrationForm
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from users.models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.core.signing import Signer, BadSignature
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

token_generator = PasswordResetTokenGenerator()


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        if remember_me:
            request.session.set_expiry(1209600)  # 2 weeks in seconds
        else:
            request.session.set_expiry(0)

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful! Welcome ' + user.username + '!')
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

            # Create a unique token for activation
            uid = urlsafe_base64_encode(force_bytes(user.email))
            token = token_generator.make_token(user)

            # Send activation email
            activation_link = request.build_absolute_uri(reverse('activate', args=[uid,token]) )

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

def activate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid or has expired.')
        return redirect('login')


def send_test_email(request):
    messages.success(request, 'Registration successful! Please check your email to activate your account.')
    return render(request, 'login_page.html')