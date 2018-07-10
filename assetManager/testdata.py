#A script to auto populate data for testing
#and that clears the manager app Database

#WARNING: For development purposes only

import os, sys

proj_path = "/"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "assetManager.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from manager.models import *
from random import randint
import datetime

TEST_AMOUNT = 3000 #number in sample to be added

#confirmation prompt
print("WARNING: This script will remove the current Inventory database.")
question = "Are you sure you want to proceed (Yes/No)? "
yes = set(['yes','y', 'ye'])
choice = input(question).lower()
if choice in yes:

    #CLEAR DATABASE
    print("Deleting database")
    Inventory.objects.all().delete()
    Deployed.objects.all().delete()
    History.objects.all().delete()
    Group.objects.all().delete()
    print("Database cleared")

    #ADD SAMPLE
    print("Adding sample data...")

    models = ['Dell Optiplex 720','Dell Optiplex 7010','Dell Latitude E5530',
                'Dell Latitude E6540', 'Dell Optiplex 320','Dell Optiplex 9010',
                'Macbook Pro 2012', 'Macbook Pro 2016','iMac 21.5 2009','iMac 21.5 2012'
                'Dell Venue','Mac mini','Dell Latitude E5570']

    username = ['podium','Tom','Dick','Harry','John','Bob','Gary','Dylan','Sam','Sue','Sally','Susan','Hannah']

    location = ['B101','S034','S105','S132','G343','G13','G101','F011','F207','RH3410','RH2333','RH39','C13','D34','W767','library']

    os = ['Windows XP','Windows 7','Windows 10','macOS 10.12','macOS 10.11','Windows 98','Ubuntu 18.04','RedHat','SUSE','Android','IOS']

    groups = ['Podiums','Faculty & Staff','Lab Computer']

    for g in groups:
        new_group = Group(group=g)
        new_group.save()

    progress = 0 #progress bar status
    for i in range(TEST_AMOUNT):
        #progress bar        
        if i % (TEST_AMOUNT / 10) == 0:
            progress += 10
            sys.stdout.write(".." + str(progress))
            sys.stdout.flush()

        a = Inventory(asset_tag=i)
        a.computer_name = str(randint(10000, 90000))
        a.model = models[randint(0,len(models)-1)]
        a.os = os[randint(0,len(os)-1)]
        a.serial = str(randint(10000,90000))
        a.purchase_date = datetime.date(randint(1998,2018),randint(1,12),randint(1,27))
        a.warrenty_expiration = datetime.date(randint(1998,2018),randint(1,12),randint(1,27))
        a.last_updated = datetime.date.today()
        a.save()
        deploy = randint(0,1)
        if deploy == 1:
            d = Deployed(asset_tag = a)
            d.username = username[randint(0,len(username)-1)]
            d.location = location[randint(0,len(location)-1)]
            grp = groups[randint(0,len(groups)-1)]
            d.group = Group.objects.get(group = grp)
            d.date_issued = datetime.date.today()
            d.save()
    print("\nSuccessfully added ",TEST_AMOUNT," assets")



