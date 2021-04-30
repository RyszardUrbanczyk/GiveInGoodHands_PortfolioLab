from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from GiveInGoodHands_app.forms import RegisterForm, LoginForm
from GiveInGoodHands_app.models import Donation, Institution, Category


class LandingPageView(View):

    def get(self, request):
        quantity_bags = Donation.get_quantity_all(self)
        quantity_institutions = Institution.get_institution_count(self)
        objects1 = Institution.objects.filter(type=1)
        objects2 = Institution.objects.filter(type=2)
        objects3 = Institution.objects.filter(type=3)
        return render(request, 'base.html', {'quantity_bags': quantity_bags,
                                             'quantity_institutions': quantity_institutions,
                                             'objects1': objects1, 'objects2': objects2,
                                             'objects3': objects3, })


class AddDonationView(LoginRequiredMixin, View):

    def get(self, request):
        objects = Category.objects.all()
        ctx = {
            'objects':objects,
        }
        return render(request, 'add-donation.html', ctx)


class RegisterView(View):
    """
    New user registration view.
    """

    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['name']
            last_name = form.cleaned_data['surname']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            if User.objects.filter(username=form.cleaned_data['email']).exists():
                m = f'Istnieje taki adres e-mail w bazie!'
                return render(request, 'register.html', {'form': form, 'm': m})
            if form.cleaned_data['password1'] != form.cleaned_data['password2']:
                n = f'Różne hasła!'
                return render(request, 'register.html', {'form': form, 'n': n})
            u = User.objects.create(first_name=first_name, last_name=last_name, username=email)
            u.set_password(password1)
            u.email = email
            u.save()
            return redirect(reverse('login'))
        else:
            return render(request, 'register.html', {'form': form})


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            if not User.objects.filter(username=form.cleaned_data['username']).exists():
                redirect_url = request.GET.get('next', 'register')
                return redirect(redirect_url)
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                login(request, user)
                redirect_url = request.GET.get('next', 'index')
                # próbujemy pobrać ze słownika request.GET wartość która znajduje sie pod kluczem "next" jesli nie ma 'next'
                # to zwracamy "index"
                return redirect(redirect_url)
            else:
                return redirect('login')


class LogOutView(View):

    def get(self, request):
        logout(request)
        return redirect('index')
