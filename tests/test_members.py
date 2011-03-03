import common
import be.apps
app = be.apps.cowapp

data = dict(username='shon0', password='secret', enabled=True, email='who@example.net', address='Pune', city='Pune', country='IND', pincode='411000', organization='pydevers', home_no=None, mobile_no=None, first_name="Shekhar", last_name="Tiwatne", short_description="Programmer", long_description="<i>Programmer</i>", twitter_handle="shon_", facebook_name=None, blog=None, linkedin_contact=None, use_gravtar=None)

def test_add(data):
    username = data['username']
    data['username'] = username + str(int(username[-1]) + 1)
    member_id = app.members.add(**data)

def test_get(member_id):
    member = app.members.get(member_id)

print common.timer(test_add, [data], 1)
print common.timer(test_get, [1])
#print common.timer(test_add, [data], 10000)
#print common.timer(test_get, [1])