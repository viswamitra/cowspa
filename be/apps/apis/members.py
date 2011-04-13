import colander

import bases.constants as constants
import be.repository.stores as stores

import commonlib
import commonlib.messaging.email as emaillib
import commonlib.messaging as messaging

memberstore = stores.memberstore
profilestore = stores.profilestore
registered_store = stores.registered_store

create_activation_key = commonlib.helpers.random_key_gen

class RegisterSchema(colander.MappingSchema):
    first_name = colander.SchemaNode(colander.String(), validator=colander.All(colander.Length(1, 50)))
    last_name = colander.SchemaNode(colander.String(), missing=None, validator=colander.All(colander.Length(None, max=50)))
    email = colander.SchemaNode(colander.String(), title="Email Address", validator=colander.Email())

def register(first_name, last_name, email, ipaddr, sendmail=False):
    activation_key = create_activation_key()
    registered = registered_store.add(activation_key, first_name, last_name, email, ipaddr)
    activation_url = "http://127.0.0.1/members/activate/" + activation_key
    data = dict (first_name = first_name, activation_url = activation_url)
    mail_data = messaging.activation.create_message(data)
    if sendmail:
        env.mailer.send(**mail_data)
    return activation_key

register.exec_mode = constants.exec_modes.BG

def get_activation_info(activation_key):
    member = registered_store.fetch_one_by(activation_key=activation_key)
    if not member:
        raise erros.APIExecutionError("Invalid/Expired Activation key")
    return registered_store.obj2dict(member)

def activate(activation_key, **member_data):
    activation_info = get_activation_info(activation_key)
    member_data.update(activation_info)
    member_data.pop('activation_key')
    member_data.pop('ipaddr')
    member_id = add(**member_data)
    return member_id

#class AddValidator(SchemaValidator):
#    username = v.StringValidator(required=True)
#    password = v.StringValidator(required=True)
#    enabled = v.EmailAddressValidator(required=True)

def add(username, password, enabled, email, address=None, city=None, country=None, pincode=None, organization=None, home_no=None, mobile_no=None, fax_no=None, skype_name=None, sip_id=None, website=None, first_name=None, last_name=None, short_description=None, long_description=None, twitter_handle=None, facebook_name=None, blog=None, linkedin_contact=None, use_gravtar=None):
    member = memberstore.add(username, password, enabled, email, address, city, country, pincode, organization, home_no, mobile_no, fax_no, skype_name, sip_id, website, first_name, last_name, short_description, long_description, twitter_handle, facebook_name, blog, linkedin_contact, use_gravtar)
    return member.id

def get(member_id):
    return memberstore.fetch_by_id(member_id)

def get_details(member_id):
    member = memberstore.fetch_by_id(member_id)
    details = {}
    for attr in ('user', 'contact', 'profile'):
        details[attr] = memberstore.obj2dict(getattr(member, attr))
    return details

def get_my_details():
    member_id = env.context.user_id
    return get_details(member_id)

def get_my_profile():
    member_id = env.context.user_id
    return get_profile(member_id)

def edit_my_profile(mod_data):
    member_id = env.context.user_id
    return edit_profile(member_id, mod_data)

def get_profile(member_id):
    member = memberstore.fetch_by_id(member_id)
    return memberstore.obj2dict(member.profile)

def edit_profile(member_id, mod_data):
    profilestore.edit(member_id, mod_data)
    return True
