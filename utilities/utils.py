def try_dictionary_access(dictionary, keys):
    '''Tries to access a value in a nested dictionary, returns None if it fails'''
    try:
        for key in keys:
            dictionary = dictionary[key]
        return dictionary
    except (TypeError, KeyError) as error:
        return None