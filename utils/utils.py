def try_dictionary_access(dictionary, keys):
    '''Tries to access a value in a nested dictionary, returns None if it fails'''
    try:
        for key in keys:
            dictionary = dictionary[key]
        return dictionary
    except (TypeError, KeyError) as error:
        return None

def noneless_dictionary_update(old, new):
    return old.update( (k,v) for k,v in new.items() if v is not None)