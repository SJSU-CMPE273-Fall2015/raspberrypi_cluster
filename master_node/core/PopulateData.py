__author__ = 'saurabh'
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "master_node.master_node.settings"

from master_node.core.models import User

u = User(username="saurabhjinturkar", password="parbhani", email="saurabhjinturkar@gmail.com", name="Saurabh",
         lname="Jinturkar", is_admin=False)
u.save()

u1 = User(username="admin", password="root", email="admin@mysite.com", name="Admin", lname="", is_admin=True)
u1.save()

u2 = User(username="sushain.nada", password="nada@123", email="sushain.nadagoundla@sjsu.edu", name="Sushain",
          lname="Nadagoundla", is_admin=True)
u2.save()

u3 = User(username="sayalee", password="sayalee123", email="sayalee.agashe@sjsu.edu", name="Sayalee", lname="Agashe",
          is_admin=False)
u3.save()

u4 = User(username="adityasharmacs", password="csrocks", email="aditya.sharma1@sjsu.edu", name="Aditya", lname="Sharma",
          is_admin=False)
u4.save()
