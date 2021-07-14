from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView
from GiveInGoodHands_app.forms import AddDonationForm
from GiveInGoodHands_app.forms import RegisterForm, LoginForm
from GiveInGoodHands_app.models import Donation, Institution, Category


class LandingPageView(View):

    def get(self, request):
        quantity_bags = Donation.get_quantity_count(self)
        quantity_institutions = Institution.get_institution_count(self)
        objects1 = Institution.objects.filter(type=1)
        objects2 = Institution.objects.filter(type=2)
        objects3 = Institution.objects.filter(type=3)
        return render(request, 'base.html', {'quantity_bags': quantity_bags,
                                             'quantity_institutions': quantity_institutions,
                                             'objects1': objects1, 'objects2': objects2,
                                             'objects3': objects3,} )


class AddDonationView(LoginRequiredMixin, View):

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        user = request.user
        ctx = {
            'categories': categories,
            'institutions': institutions,
        }
        return render(request, 'add-donation.html', ctx)

    # def only_logged_in(request):
    #     return render(request, 'add-donation.html')


    def post(self, request):
        quantity = request.POST['bags']
        institutions_id = request.POST['organization']
        address = request.POST['address']
        city = request.POST['city']
        zip_code = request.POST['postcode']
        phone_number = request.POST['phone']
        pick_up_date = request.POST['data']
        pick_up_time = request.POST['time']
        pick_up_comment = request.POST['more_info']
        user_id = request.user.id
        donation = Donation.objects.create(quantity=quantity, institution_id=institutions_id, address=address,
                                           city=city, zip_code=zip_code, phone_number=phone_number,
                                           pick_up_date=pick_up_date, pick_up_time=pick_up_time,
                                           pick_up_comment=pick_up_comment, user_id=user_id)
        categories_id = request.POST.getlist('categories')
        categories = Category.objects.filter(id__in=categories_id)
        # donation.categories.set(categories)
        for cat in categories:
            donation.categories.add(cat)

        return redirect('/form-confirmation')

class FormConfirmation(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


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
                # próbujemy pobrać ze słownika request.GET wartość która znajduje sie pod kluczem "next"
                # jesli nie ma 'next' to zwracamy "index"
                return redirect(redirect_url)
            else:
                return redirect('login')


class LogOutView(View):

    def get(self, request):
        logout(request)
        return redirect('index')


class MyFormView(View):

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {
            'categories': categories,
            'institutions': institutions,
        }
        return render(request, 'my-form.html', ctx)

    def post(self, request):
        quantity = request.POST['bags']
        institutions_id = request.POST['organization']
        address = request.POST['address']
        city = request.POST['city']
        zip_code = request.POST['postcode']
        phone_number = request.POST['phone']
        pick_up_date = request.POST['data']
        pick_up_time = request.POST['time']
        pick_up_comment = request.POST['more_info']
        user_id = request.user.id
        donation = Donation.objects.create(quantity=quantity, institution_id=institutions_id, address=address,
                                           city=city, zip_code=zip_code, phone_number=phone_number,
                                           pick_up_date=pick_up_date, pick_up_time=pick_up_time,
                                           pick_up_comment=pick_up_comment, user_id=user_id)
        categories_id = request.POST.getlist('categories')
        categories = Category.objects.filter(id__in=categories_id)
        # donation.categories.set(categories)
        for cat in categories:
            donation.categories.add(cat)

        return redirect("/")


def get_institutions_by_category(request):
    type_ids = request.GET.getlist('type_ids')
    if type_ids is not None:
        institutions = Institution.objects.filter(institution__in=type_ids).distinct()
    else:
        institutions = Institution.objects.all()
    return render(request, "my-form.html", {'institutions': institutions})
