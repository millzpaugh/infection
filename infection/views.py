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
from infection.forms import FullInfectionForm
import json
import requests
from infection.models import KhanUser, Coach, Student
from infection.mockaroo_api import MockarooAPIClient, MockarooResponse, infect_all_users, MockarooAPIException
import itertools
import collections
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
            rounds = infect_all_users()
            infection_rounds = rounds['rounds']
            rounds_for_total_infection = len(rounds['rounds'].keys())
            networked_users = len(rounds['networked_users'])
            students_only = KhanUser.objects.filter(is_coach=False)
            outliers = [s for s in students_only if s.is_coached == False]
            for k,v in infection_rounds.iteritems():
                users = []
                if k > 1:
                    for list in v:
                        for u in list:
                            if u not in users:
                                users.append(u)
                    infection_rounds[k] = users

            return render(request,  self.template, {'rounds':rounds,
                                                    'rounds_for_total_infection':rounds_for_total_infection,
                                                    'networked_users':networked_users,
                                                    'pool_size':pool_size,
                                                    'infection_rounds':infection_rounds,
                                                    'outliers':outliers})


class LimitedInfection(View):
    template = "limited_infection.html"

    def get(self, request, *args, **kwargs):

        return render(request,  self.template, {})
