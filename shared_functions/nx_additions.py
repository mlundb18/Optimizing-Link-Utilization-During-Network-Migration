
def on_path(edge, path):
    """How many times edge is on path"""
    counter = 0
    for path_edge in path:
        if edge == path_edge:
            counter = counter + 1
    return counter

def has_edge(edge, path):
    for path_edge in path:
        if edge == path_edge:
            return True
    return False