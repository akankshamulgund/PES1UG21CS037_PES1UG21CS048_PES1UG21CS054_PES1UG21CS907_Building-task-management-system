import mysql.connector

# Establish connection to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Akanksha#31",
    database="task_manager_db"
)

# Create cursor object
cursor = db_connection.cursor()

# CRUD Operations

def create_task(task_data):
    sql = "INSERT INTO tasks (task_name, task_description, due_date) VALUES (%s, %s, %s)"
    cursor.execute(sql, task_data)
    db_connection.commit()
    return cursor.lastrowid

def read_task(task_id):
    sql = "SELECT * FROM tasks WHERE task_id = %s"
    cursor.execute(sql, (task_id,))
    return cursor.fetchone()

def update_task(task_id, new_task_data):
    sql = "UPDATE tasks SET task_name = %s, task_description = %s, due_date = %s WHERE task_id = %s"
    cursor.execute(sql, (*new_task_data, task_id))
    db_connection.commit()

def delete_task(task_id):
    sql = "DELETE FROM tasks WHERE task_id = %s"
    cursor.execute(sql, (task_id,))
    db_connection.commit()

# CLI Frontend
def main():
    while True:
        print("\n1. Create Task")
        print("2. Read Task")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ")

        if choice == '1':
            task_name = input("Enter task name: ")
            task_description = input("Enter task description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            task_id = create_task((task_name, task_description, due_date))
            print("Task created with ID:", task_id)
        elif choice == '2':
            task_id = input("Enter task ID: ")
            task = read_task(task_id)
            if task:
                print("Task details:", task)
            else:
                print("Task not found.")
        elif choice == '3':
            task_id = input("Enter task ID: ")
            new_task_name = input("Enter new task name: ")
            new_task_description = input("Enter new task description: ")
            new_due_date = input("Enter new due date (YYYY-MM-DD): ")
            update_task(task_id, (new_task_name, new_task_description, new_due_date))
            print("Task updated successfully.")
        elif choice == '4':
            task_id = input("Enter task ID: ")
            delete_task(task_id)
            print("Task deleted successfully.")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

    # Close cursor and database connection when done
    cursor.close()
    db_connection.close()

if __name__ == "__main__":
    main()

