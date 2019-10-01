"""energy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.urls import reverse_lazy
from survey.views import user_login, signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('survey/', include(('survey.urls'), namespace='survey')),
    path('signup/', signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', user_login, name="login"),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('survey:home')), name='logout'),
]
