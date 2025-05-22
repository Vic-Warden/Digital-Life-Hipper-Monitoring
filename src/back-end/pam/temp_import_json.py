import json

# checks the PAM_devices.json and returns the desired mac addres if asked for
def get_address_by_label(label_id, filename="PAM_devices.json"):
    label_id = "label_" + str(label_id)
    try:
        with open(filename, "r") as f:
            labels = json.load(f)
        return labels.get(label_id, "Label ID not found.")
    except FileNotFoundError:
        return "File not found."
    except json.JSONDecodeError:
        return "Error decoding JSON."

# Example usage:
id = 90243
print(f"Address for {id}: {get_address_by_label(id)}")
