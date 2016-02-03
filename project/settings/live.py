from .base import *
import os

import dj_database_url

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES =  {'default':'postgres://wqbahqraoftxuf:_NkBP1KD9_df7Q-t0Qq2XRpAAc@ec2-54-225-199-245.compute-1.amazonaws.com:5432/d1q238v1m1l86l'}