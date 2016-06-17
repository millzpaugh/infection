from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.http import HttpResponse
import time
from infection.forms import FullInfectionForm, LimitedInfectionForm
from infection.mockaroo_api import MockarooAPIClient, MockarooResponse, MockarooAPIException
from infection.infect import infect_users, remove_outliers
from infection.models import KhanUser

# Create your views here.

class HomeView(View):
    template = "home.html"

    def get(self, request, *args, **kwargs):

        return render(request,  self.template, {})

class FullInfectionView(View):
    template = "full_infection.html"
    form_class = FullInfectionForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        get = True

        return render(request,  self.template, {'form':form, 'get':get})

    def post(self, request, *args, **kwargs):
        form = FullInfectionForm(request.POST)
        if form.is_valid():
            form_data = form.clean()
            try:
                pool_size = form_data['pool_size']
                m = MockarooAPIClient()
                r = m.retrieve_data_with_custom_schema(pool_size)
            except MockarooAPIException:
                messages.error(request, "The Mockaroo API is not working. :( ")
                return redirect('full_infection')


            mresponse = MockarooResponse(users=r)
            mresponse.create_test_users()
            mresponse.assign_mentees()
            origin_user = KhanUser.objects.order_by('?').first()
            all_users = KhanUser.objects.all()
            relevant_users = remove_outliers(all_users)
            infection_result = infect_users(origin_user, relevant_users)

            return render(request,  self.template, {'infection_result':infection_result,
                                                    'pool_size':pool_size})
        else:
            return render(request,  self.template, {'form':form,
                                                    'get': True})


class LimitedInfection(View):
    template = "limited_infection.html"
    form_class = LimitedInfectionForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        get = True

        return render(request,  self.template, {'form':form, 'get':get})

    def post(self, request, *args, **kwargs):
        users = None
        form = LimitedInfectionForm(request.POST)
        if form.is_valid():
            form_data = form.clean()
            try:
                pool_size = form_data['pool_size']
                infection_size = form_data['infection_size']
                m = MockarooAPIClient()
                r = m.retrieve_data_with_custom_schema(pool_size)
            except MockarooAPIException:
                messages.error(request, "The Mockaroo API is not working. :( ")
                return redirect('full_infection')

            mresponse = MockarooResponse(users=r)
            mresponse.create_test_users()
            mresponse.assign_mentees()
            origin_user = KhanUser.objects.order_by('?').first()
            all_users = KhanUser.objects.all()
            relevant_users = remove_outliers(all_users)
            infection_result = infect_users(origin_user, relevant_users)
            users = infection_result.limit_user_infection(infection_size)

            return render(request,  self.template, {'users':users,
                                                'infection_result':infection_result,
                                                'infection_size':infection_size,
                                                'pool_size':pool_size})
        else:
            return render(request,  self.template, {'form':form,
                                                    'get': True})
