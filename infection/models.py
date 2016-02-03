from __future__ import unicode_literals

from django.db import models
import itertools

from django.contrib.auth.models import User



# Create your models here.

class KhanUserManager(models.Manager):
    def reset_infection_status_to_zero(self):
        users = self.all()
        for u in users:
            u.is_infected = False
            u.save()

class KhanUser(models.Model):
    objects = KhanUserManager()
    mockaroo_id = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    is_coach = models.BooleanField(default=False)
    is_infected = models.BooleanField(default=False)

    def __unicode__(self):
        return self.mockaroo_id

    @property
    def is_coached(self):
        coaches = Coach.objects.all()
        student = Student.objects.get(user=self)
        coached_by = []
        for c in coaches:
            if student in c.students.all():
                coached_by.append(c.user)
        if len(coached_by) > 0:
            return True
        else:
            return False

    def coached_by(self):
        coaches = Coach.objects.all()
        student = Student.objects.get(user=self)
        coached_by = []
        for c in coaches:
            if student in c.students.all():
                coached_by.append(c.user)
        return coached_by


class Student(models.Model):
    user = models.ForeignKey(KhanUser, null=True)
    def __unicode__(self):
        return self.user.mockaroo_id

class Coach(models.Model):
    user = models.ForeignKey(KhanUser, null=True)

    students = models.ManyToManyField(Student)

    def __unicode__(self):
        return self.user.mockaroo_id





















