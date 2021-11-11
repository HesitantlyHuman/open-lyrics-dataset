def noneless_dictionary_update(old, new):
    old.update( (k,v) for k,v in new.items() if v is not None)