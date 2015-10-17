
def tag_contains_whitelist(data):
    for d in data:
        if d == 'whitelist':
            return True
