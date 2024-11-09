from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth = (Column(DateTime),)
    created = Column(DateTime, default=datetime.utcnow)  # This is bad.

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return (
            f"UserModel(id={self.id=}; first_name={self.first_name};"
            f"last_name={self.last_name};"
            f"birth={self.birth}; created={self.created})"
        )


users = [
    UserModel(first_name="Bob", last_name="Preston", birth=datetime(1980, 5, 2)),
    UserModel(first_name="Susan", last_name="Sage", birth=datetime(1979, 6, 12)),
]

session_maker = sessionmaker(bind=create_engine("sqlite://models.db"))


def create_users():
    with session_maker() as session:
        for user in users:
            print(f"{user.full_name=}")
            session.add(user)
        session.commit()


create_users()







>>> user = crud.user.get_by_email(db, email=su.email)
>>> user
<app.models.user.User object at 0x7fa1be372110>
>>> user.__dict__
{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x7fa1b9856380>, 'is_superuser': True, 'id': 2, 'hashed_password': '$2b$12$6LqHxk9bcSK2yVtHDHUmeeHIDMruABcC9RxiLemr/PzqEhCzaX2gW', 'email': 'admin2@admin.com', 'full_name': 'admin2', 'is_active': True}
>>> x = dict(user)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'User' object is not iterable
>>> x = user.__dict__
>>> x.keys()
dict_keys(['_sa_instance_state', 'is_superuser', 'id', 'hashed_password', 'email', 'full_name', 'is_active'])
>>> x.values()
dict_values([<sqlalchemy.orm.state.InstanceState object at 0x7fa1b9856380>, True, 2, '$2b$12$6LqHxk9bcSK2yVtHDHUmeeHIDMruABcC9RxiLemr/PzqEhCzaX2gW', 'admin2@admin.com', 'admin2', True])
>>>
>>>
>>> user
<app.models.user.User object at 0x7fa1be372110>
>>> user.__dict__
{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x7fa1b9856380>, 'is_superuser': True, 'id': 2, 'hashed_password': '$2b$12$6LqHxk9bcSK2yVtHDHUmeeHIDMruABcC9RxiLemr/PzqEhCzaX2gW', 'email': 'admin2@admin.com', 'full_name': 'admin2', 'is_active': True, 'recipes': [<app.models.recipe.Recipe object at 0x7fa1be3a01f0>]}
>>> user['recipes'].__dict__
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'User' object is not subscriptable
>>> user['recipes']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'User' object is not subscriptable
>>> user.recipes
[<app.models.recipe.Recipe object at 0x7fa1be3a01f0>]
>>> user.recipes.__dict__
{'_sa_adapter': <sqlalchemy.orm.collections.CollectionAdapter object at 0x7fa1b97e7760>}
>>> user.recipes.all()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'InstrumentedList' object has no attribute 'all'
>>> print(user.recipes)
[<app.models.recipe.Recipe object at 0x7fa1be3a01f0>]
>>>
>>> print(user.recipes[0])
<app.models.recipe.Recipe object at 0x7fa1be3a01f0>
>>> print(user.recipes[0].id)
11
>>> print(user.recipes[0].label)
Chicken Paprikash
>>> print(user.recipes[0].__dict__)
{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x7fa1b9855f60>, 'source': 'No Recipes', 'id': 11, 'url': 'http://norecipes.com/recipe/chicken-paprikash/', 'label': 'Chicken Paprikash', 'submitter_id': 2}
>>>
