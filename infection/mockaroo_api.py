import requests
import json
import sys
from requests.exceptions import RequestException
from infection.models import KhanUser, Coach, Student
import itertools

class MockarooAPIException(Exception):
    pass

class MockarooResponse():
    def __init__(self, users):
        self.users = users

    def create_test_users(self):
        if Student.objects.all():
            Student.objects.all().delete()
        if Coach.objects.all():
            Coach.objects.all().delete()
        if KhanUser.objects.all():
            KhanUser.objects.all().delete()

        for u in self.users:
            user = KhanUser(mockaroo_id=u['id'],
                        first_name=u['first_name'],
                        last_name=u['last_name'])
            user.save()

            student = Student(user=user)
            student.save()

            mentees = u['mentees']

            if mentees:
                user.is_coach = True
                user.save()
                coach = Coach(user=user)
                coach.save()

    def assign_mentees(self):
        for mock_user in self.users:
            uid = str(mock_user['id'])
            kuser = KhanUser.objects.filter(mockaroo_id=uid)[0]
            if kuser.is_coach:
                coach = Coach.objects.get(user=kuser)
                coach_student = Student.objects.get(user=kuser)
                mentee_ids = [m['id'] for m in mock_user['mentees']]

                mentees = []

                if mentee_ids:
                    for ident in mentee_ids:
                        student_id = str(ident)
                        student_user = KhanUser.objects.filter(mockaroo_id=student_id)[0]
                        student = Student.objects.get(user=student_user)
                        #checks that for self-coaching relationship
                        if student_user.is_coach:
                            student_coach = Coach.objects.filter(user=student_user)[0]
                            if not student_id == coach.user.mockaroo_id:
                                mentees.append(student)
                        # eliminates possiblity to have coach - student, student-coach relationship
                            elif student_coach.students.all() and not coach_student in student_coach.students.all():
                                mentees.append(student)
                    print "MENTEES FINAL"
                    print mentees
                    coach.students = mentees
                    coach.save()




class MockarooAPIClient():
    def __init__(self):
        self.url = 'http://www.mockaroo.com/api/generate.json?'
        self.key = '3b34e3e0'

    def retrieve_data(self):

        url = self.url
        params = {'key': self.key, 'schema': 'Khan'}
        response = requests.get(url=url, data=params)
        try:
           response.raise_for_status()
        except RequestException as ex:
            raise MockarooAPIException("Error from Mockaroo API: {}".format(ex.message)), None, sys.exc_info()[2]
        return response.json()

    def retrieve_data_with_custom_schema(self, data_count):
        schema = [{
                    "name": 'id',
                    "type": 'Row Number',
                    "percentBlank": 0
                }, {
                    "name": 'first_name',
                    "type": 'First Name',
                    "percentBlank": 0

                },{
                    "name": 'last_name',
                    "type": 'Last Name',
                    "percentBlank": 0

                },{
                    "name": 'mentees',
                    "type": 'JSON Array',
                    "percentBlank": 0,
                    "minItems": 0,
                    "maxItems": 10
                }, {
                    "name": 'mentees.id',
                    "type": 'Number',
                    "percentBlank": 0,
                    "decimals":0,
                    "min": 1,
                    "max": data_count
                }]


        data = json.dumps(schema)
        headers = { 'Accept': 'application/json'}
        params = {'key': self.key, 'count': data_count}
        response = requests.post(url=self.url, headers=headers, params=params,data=data)
        try:
           response.raise_for_status()
        except RequestException as ex:
            raise MockarooAPIException("Error from Mockaroo API: {}".format(ex.message)), None, sys.exc_info()[2]
        return response.json()

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

def infect():
    KhanUser.objects.reset_infection_status_to_zero()

    user = KhanUser.objects.order_by('?').first()
    rounds_of_infections = {1:[user]}

    all_users = KhanUser.objects.all()
    relevant_users = remove_outliers(all_users)
    print 'STATEMENT TRUE?!?!'
    print all([u.is_infected for u in relevant_users])
    infection_spreading = True

    while infection_spreading:
        if rounds_of_infections.keys()[-1] == 1:
            first_network = infect_network(user)
            rounds_of_infections[2] = [first_network]

        networks = []
        current_infection_round = rounds_of_infections.keys()[-1]

        user_networks_to_infect = rounds_of_infections[current_infection_round]
        print user_networks_to_infect

        network_size = len(user_networks_to_infect)
        print network_size

        for i in range(0,network_size):
            print network_size
            for u in user_networks_to_infect[i]:
                network = infect_network(u)
                networks.append(network)
        next_infection_round = rounds_of_infections.keys()[-1] + 1
        rounds_of_infections[next_infection_round] = networks

        all_users = KhanUser.objects.all()
        relevant_users = remove_outliers(all_users)
        print 'STATEMENT TRUE?!?!'
        print all([u.is_infected for u in relevant_users])

        if all([u.is_infected for u in relevant_users]):
            break
        else:
            continue

    return {'rounds':rounds_of_infections, 'networked_users': relevant_users}


