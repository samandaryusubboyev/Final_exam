
from django.shortcuts import redirect, render
from .models import UserModel


from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.urls.base import reverse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth import get_user_model

from .forms import UserCreationForm

User = get_user_model()


class UserLogin(LoginView):
    template_name = 'app_users/login.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'is_login': True,
    }
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            next_page_url = request.POST.get('next')
            user = authenticate(request=request, username=request.POST.get('email'), password=request.POST.get('password'))
            if user:
                login(request, user)
                if next_page_url:
                    return redirect(next_page_url)
                else:
                    return redirect('categories')
        return super().dispatch(request, *args, **kwargs)
class UserRegistration(CreateView):
    model = User
    template_name = 'app_users/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


def user_logout(request):
    logout(request)
    return redirect('login')


def acoount_view(request):

    user = UserModel.objects.all()

    context = {
        'users': user,
    }

    return render(request, 'app_main/account.html', context=context)


