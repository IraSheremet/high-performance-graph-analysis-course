import json


def load_json(filename, test_name):
    with open(filename) as file:
        graph = json.load(file)
        file.close()
    return graph[test_name]
