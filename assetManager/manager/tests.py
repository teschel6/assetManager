from django.test import TestCase

import datetime
import time
import random
from .models import *

#Inventory Tests
class InventoryModelTests(TestCase):
    
    def test_search_speed_large_inventory(self):
        today = datetime.date.today()
        size = 1000
        #Create test Inventory
        for i in range(size):
            m = Inventory(asset_tag=i)
            m.save()
        start = time.time()
        m = Inventory.objects.get(pk = random.randint(0,size - 1))
        end = time.time()
        print('Database lookup took: ',end - start,'S')
