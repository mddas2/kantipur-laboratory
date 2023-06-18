from hashids import Hashids

def generateEncodeIdforSampleForm(original_id,salt):
    hashids = Hashids(salt=salt, min_length=6)
    encoded_id = hashids.encode(original_id)
    return encoded_id
