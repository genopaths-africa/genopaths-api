from flask_seeder import Seeder, Faker, generator
from genopaths.modules.users.models import User, UserSchema

class UserSeeder(Seeder):

    def run(self):
        # Create a new Faker and tell it how to create User objects
        faker = Faker(
            cls=User,
            init={
                "username": generator.Email(),
                "first_name": generator.Name(),
                "last_name": generator.Name(),
                "other_names": generator.Name(),
                "password": generator.String("abc[5-9]{4}\c[xyz]"),
                "phone_number": '0778000000',
                "job_title": "Mr",
                "is_account_non_expired": False,
                "is_account_non_locked": True,
                "is_enabled": True,
                "role": 'admin',
                "photo": 'photo.jpg',
                "token": generator.String("abc[5-9]{8}\c[xyz]")
            }
        )


        # Create 5 new users
        for user in faker.create(5):
            print("Adding user: %s" % user)
            self.db.session.add(user)
