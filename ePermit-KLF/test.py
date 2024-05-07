#!/usr/bin/python3

from models.base_model import BaseModel
from models.user import User
from models.business import Business
from models.category import Category
import models


# c = Category(category_name="Tech", business_id="1234", description="Technology", fee=12000)
# c.save()

b = Business(name="Google", description="Search Engine", user_id="8c1c6a6c-39c5-4e68-95b7-a3812ae11255", category_id="d1f49a3f-6edb-4824-9968-6cca02c3e585", longitude=37.4220, latitude=-122.0841, KRA_pin="1234", address="1600 Amphitheatre Parkway, Mountain View, CA")
b.save()

u = User(email="diana@gmail.com", password="password")
models.storage.reload()
u.save()
users = models.storage.all(User)
print(users[0].id)