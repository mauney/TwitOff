# to run in flask shell: exec(open("./add_users.py").read())
from twitoff.models import DB, User, Tweet

DB.drop_all()
DB.create_all()

u1 = User(name='Mort')
t1 = Tweet(text='What time is it?')
t2 = Tweet(text='Are these my shoes?')
t3 = Tweet(text='Not my chair, not my problem.')

u1.tweets += [t1, t2, t3]

u2 = User(name='Jack')
t4 = Tweet(text='Rocket 88')
t5 = Tweet(text='Deep Deep Sleep')
t6 = Tweet(text="Somethin' Else")

u2.tweets += [t4, t5, t6]

adds = [u1, u2, t1, t2, t3, t4, t5, t6]
for add in adds:
    DB.session.add(add)
DB.session.commit()
