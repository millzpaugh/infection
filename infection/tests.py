from django.test import TestCase
from mockaroo_api import MockarooResponse
from infection.models import KhanUser, Student, Coach
from infect import remove_outliers, InfectionResult, infect_users
# Create your tests here.

TEST_DATA = [{u'first_name': u'Adam', u'last_name': u'Chavez', u'id': 1, u'mentees': [{u'id': 11}]}, {u'first_name': u'Rose', u'last_name': u'White', u'id': 2, u'mentees': [{u'id': 6}, {u'id': 10}, {u'id': 2}, {u'id': 5}, {u'id': 12}, {u'id': 2}, {u'id': 2}]}, {u'first_name': u'Cheryl', u'last_name': u'Freeman', u'id': 3, u'mentees': [{u'id': 8}, {u'id': 4}, {u'id': 1}, {u'id': 11}, {u'id': 10}, {u'id': 3}]}, {u'first_name': u'Betty', u'last_name': u'Stewart', u'id': 4, u'mentees': []}, {u'first_name': u'Dorothy', u'last_name': u'Ray', u'id': 5, u'mentees': [{u'id': 8}, {u'id': 6}, {u'id': 2}, {u'id': 7}]}, {u'first_name': u'Stephen', u'last_name': u'Robinson', u'id': 6, u'mentees': [{u'id': 6}, {u'id': 11}, {u'id': 10}]}, {u'first_name': u'Kelly', u'last_name': u'Gilbert', u'id': 7, u'mentees': [{u'id': 12}, {u'id': 9}, {u'id': 7}, {u'id': 10}, {u'id': 4}]}, {u'first_name': u'Patrick', u'last_name': u'Daniels', u'id': 8, u'mentees': [{u'id': 5}, {u'id': 4}]}, {u'first_name': u'Jimmy', u'last_name': u'Stewart', u'id': 9, u'mentees': [{u'id': 11}, {u'id': 9}]}, {u'first_name': u'Clarence', u'last_name': u'Bailey', u'id': 10, u'mentees': []}, {u'first_name': u'Sandra', u'last_name': u'Carpenter', u'id': 11, u'mentees': [{u'id': 6}, {u'id': 1}, {u'id': 12}, {u'id': 10}, {u'id': 6}, {u'id': 9}, {u'id': 12}, {u'id': 2}]}, {u'first_name': u'Angela', u'last_name': u'Schmidt', u'id': 12, u'mentees': [{u'id': 5}, {u'id': 7}, {u'id': 8}, {u'id': 9}, {u'id': 10}, {u'id': 3}]}]

class InfectionTest(TestCase):
    def setUp(self):
        data = MockarooResponse(users=TEST_DATA)
        data.create_test_users()
        data.assign_mentees()
        all_users = KhanUser.objects.all()
        relevant_users = remove_outliers(all_users)
        original_user = KhanUser.objects.get(id=12)
        self.infection_result = InfectionResult(original_user_infected=original_user, users=all_users, networked_users=relevant_users)


    def test_users_who_are_outliers(self):
        outliers = self.infection_result.users_who_are_outliers
        outlier_users = [u.id for u in outliers]
        outlier_ids = [4,10]

        all_users = KhanUser.objects.all()
        relevant_users = remove_outliers(all_users)
        r_users = [u.id for u in relevant_users]
        user_ids = [1,2,3,5,6,7,8,9,11,12]

        self.assertEqual(r_users, user_ids)
        self.assertEqual(outlier_users, outlier_ids)

    def infect_user(self):
        pass

    def test_infect_network(self):
        result = infect_users()
        networked_users = len(result.networked_users)
        network = self.infection_result.retrieve_most_recently_infected_network
        user1 = KhanUser.objects.get(id=1)
        user2 = KhanUser.objects.get(id=6)
        last_round = [user1,user2]
        self.assertEqual(networked_users, 10)
        self.assertEqual(network, last_round)

