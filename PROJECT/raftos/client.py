import requests

# Define the base URL of the backend API
BASE_URL = 'http://localhost:5000/'  # Update the URL if your backend is running on a different host or port

# Function to create a task
def create_task(task_data):
    url = BASE_URL + 'create_task'
    response = requests.post(url, json=task_data)
    return response.json()

# Function to read a task by ID
def read_task(task_id):
    url = BASE_URL + f'read_task/{task_id}'
    response = requests.get(url)
    return response.json()

# Function to update a task by ID
def update_task(task_id, new_task_data):
    url = BASE_URL + f'update_task/{task_id}'
    response = requests.put(url, json=new_task_data)
    return response.json()

# Function to delete a task by ID
def delete_task(task_id):
    url = BASE_URL + f'delete_task/{task_id}'
    response = requests.delete(url)
    return response.json()

# Example usage
if __name__ == "__main__":
    # Create a new task
    task_data = {
        'task_name': 'Task 1',
        'task_description': 'Description of Task 1',
        'due_date': '2024-04-11'
    }
    print("Creating task...")
    task_id = create_task(task_data)
    print("Task created with ID:", task_id)

    # Read the task
    print("Reading task...")
    task = read_task(task_id)
    print("Task details:", task)

    # Update the task
    print("Updating task...")
    new_task_data = {
        'task_name': 'Updated Task 1',
        'task_description': 'Updated description of Task 1',
        'due_date': '2024-04-15'
    }
    update_result = update_task(task_id, new_task_data)
    print("Update result:", update_result)

    # Delete the task
    print("Deleting task...")
    delete_result = delete_task(task_id)
    print("Delete result:", delete_result)

