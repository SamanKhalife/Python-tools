import json
import logging

logging.basicConfig(filename='policy_audit.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def review_access_policies(current_policies):
    default_policies = {
        'admin': 'full_access',
        'user': 'limited_access',
        'guest': 'read_only',
        'superuser': 'full_access',
        'developer': 'modify_code',
        'auditor': 'view_logs'
    }
    updates = []

    for role, access in default_policies.items():
        if role not in current_policies or current_policies[role] != access:
            updates.append((role, access))
    return updates

def load_policies_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            policies = json.load(file)
            logging.info(f"Loaded policies from {file_path}.")
            return policies
    except FileNotFoundError:
        logging.warning(f"Policy file {file_path} not found. Loading default policies.")
        return {}

def save_updates_to_file(updates, file_path):
    with open(file_path, 'w') as file:
        json.dump(updates, file, indent=4)
    logging.info(f"Policy updates saved to {file_path}.")
    print(f"Updates saved to {file_path}.")

def interactive_policy_input():
    policies = {}
    print("Enter policy information (type 'done' when finished):")

    while True:
        role = input("Enter role: ")
        if role == 'done':
            break
        access = input(f"Enter access level for {role}: ")
        policies[role] = access

    return policies

def main():
    policy_file = 'current_policies.json'
    update_file = 'policy_updates.json'

    input_method = input("Load policies from file or enter interactively? (file/interactive): ")

    if input_method == 'file':
        current_policies = load_policies_from_file(policy_file)
    else:
        current_policies = interactive_policy_input()

    updates = review_access_policies(current_policies)

    if updates:
        print("Recommended policy updates:")
        for role, access in updates:
            print(f"{role}: {access}")

        save_updates_to_file(updates, update_file)
    else:
        print("All policies are up to date.")

if __name__ == "__main__":
    main()
