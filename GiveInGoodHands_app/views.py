from django.shortcuts import render

# Create your views here.
from django.views import View

from GiveInGoodHands_app.models import Donation, Institution


class LandingPageView(View):

    def get(self, request):
        quantity_bags = Donation.get_quantity_all(self)
        quantity_institutions = Institution.get_institution_count(self)
        return render(request, 'base.html', {'quantity_bags': quantity_bags,
                                             'quantity_institutions': quantity_institutions})


class AddDonationView(View):

    def get(self, request):
        return render(request, 'add-donation.html')


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    """
    New user registration view.
    """

    def get(self, request):
        # form = RegisterForm()
        return render(request, 'register.html')
        # return render(request, 'form.html', {'form': form})

    # def post(self, request):
    #     form = RegisterForm(request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password1']
    #         # if User.objects.filter(username=username).exists():
    #         #     m = f'Isnieje taki użytkownik.'
    #         #     return render(request, 'form.html', {'form': form, 'm':m})
    #         u = User.objects.create(username=username)
    #         u.set_password(password)
    #         u.save()
    #         return redirect('login')
    #     else:
    #         return render(request, 'form.html', {'form': form})
