import requests
import json
import sys
from requests.exceptions import RequestException
from infection.models import KhanUser, Coach, Student
import itertools

class InfectionResult():
    def __init__(self, users, original_user_infected, networked_users):
        self.rounds = []
        self.original_user_infected = original_user_infected
        self.users = users
        self.networked_users = networked_users

    @property
    def number_of_outliers(self):
        return len(self.users) - len(self.networked_users)

    @property
    def users_who_are_outliers(self):
        students_only = KhanUser.objects.filter(is_coach=False)
        outliers = [s for s in students_only if s.is_coached == False]
        return outliers

    @property
    def number_of_rounds(self):
        return len(self.rounds)

    @property
    def retrieve_most_recently_infected_network(self):
        network_to_infection = len(self.rounds) - 1
        return self.rounds[network_to_infection].users_infected

    @property
    def entire_network_infected(self):
        return all([u.is_infected for u in self.networked_users])

class InfectionRound():
    def __init__(self):
        self.users_infected = None

    def clean_network(self):
        for network in self.users_infected:
            users = []
            if network == []:
                for list in v:
                    for u in list:
                        if u not in users:
                            users.append(u)
                infection_rounds[k] = users

class UsersToInfect():
    def __init__(self, user):
        self.user = user
        self.is_infected = False

def infect_network(user):
    user.is_infected = True
    user.save()
    infected = []

    if user.is_coach:
        coach = Coach.objects.get(user=user)
        for s in coach.students.all():
            infected.append(s.user)
    if user.is_coached:
        for c in user.coached_by():
            infected.append(c)

    newly_infected = []
    for u in infected:
        if u.is_infected == False:
            u.is_infected = True
            u.save()
            newly_infected.append(u)

    return newly_infected

def remove_outliers(all_users):
    relevant_users = []
    for u in all_users:
        if u.is_coached == True or u.is_coach == True:
            relevant_users.append(u)
    return relevant_users

def infect_all_users():
    KhanUser.objects.reset_infection_status_to_zero()

    user = KhanUser.objects.order_by('?').first()
    all_users = KhanUser.objects.all()
    relevant_users = remove_outliers(all_users)

    infection_result = InfectionResult(original_user_infected=user, users=all_users, relevant_users=relevant_users)

    round = InfectionRound(users_infected=[user])
    infection_result.rounds.append(round)

    infection_spreading = True

    while infection_spreading:
        if infection_result.number_of_rounds == 1:
            first_network = infect_network(user)
            round = InfectionRound(users_infected=first_network)
            infection_result.rounds.append(round)

        round = InfectionRound(users_infected=[])

        user_networks_to_infect = infection_result.retrieve_most_recently_infected_network

        network_size = len(user_networks_to_infect)

        for i in range(0,network_size):
            for u in user_networks_to_infect[i]:
                network = infect_network(u)
                round.users_infected.append(network)

        if infection_result.entire_network_infected:
            break
        else:
            continue

    return infection_result



