

def get_labels_info(on_production):

    error = None

    if on_production:
        # TODO: to implement
        pass
        
    else:
        # load data from file 
        import json
        import os
        filepath = os.path.join(os.getcwd(), "tests/fixtures", "fake_labels_info.json")

        with open(filepath, "r") as f:
            data = json.load(f)

    labels_info = data.get("items", [])
        
    return labels_info, error
