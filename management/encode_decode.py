from hashids import Hashids
from . import roles

sample_form_user_salt = "user"
sample_form_supervisor_salt = "supervisor"
sample_form_analyst_salt = "analyst"
sample_form_verifier_salt = "verifier"

def generateEncodeIdforSampleForm(original_id,salt):
    hashids = Hashids(salt=salt, min_length=6)
    encoded_id = hashids.encode(original_id)
    return encoded_id

def generateAutoEncodeIdforSampleForm(original_id,user):
    if user.role == roles.USER:
        hashids = Hashids(salt=sample_form_user_salt, min_length=6)
    elif user.role == roles.SUPERVISOR:
        hashids = Hashids(salt=sample_form_supervisor_salt, min_length=6)
    elif user.role == roles.ANALYST:
        hashids = Hashids(salt=sample_form_analyst_salt, min_length=6)
    else:
        return original_id
    encoded_id = hashids.encode(original_id)
    return encoded_id

def generateDecodeIdforSampleForm(encoded_id,user):
    if user.role == roles.USER:
        hashids = Hashids(salt=sample_form_user_salt,min_length=6)

    elif user.role == roles.SUPERVISOR:
        hashids = Hashids(salt=sample_form_supervisor_salt,min_length=6)

    elif user.role == roles.ANALYST:
        hashids = Hashids(salt=sample_form_analyst_salt,min_length=6)
    # elif user.role == roles.SUPERVISOR:
    #     hashids = Hashids(salt="supervisor")
    # elif user.role == roles.ANALYST:
    #     hashids = Hashids(salt="analyst")
    # elif user.role == roles.VERIFIER:
    #     hashids = Hashids(salt="verifier")
    else:
        return encoded_id
    
    decoded_ids = hashids.decode(encoded_id)

    if decoded_ids:
        return decoded_ids[0]  # Extract the first decoded ID
    return None
