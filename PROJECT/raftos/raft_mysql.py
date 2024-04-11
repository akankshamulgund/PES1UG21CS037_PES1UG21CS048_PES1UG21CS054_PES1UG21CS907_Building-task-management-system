import mysql.connector
import raftos
import asyncio
import argparse

PORTS = [8000, 8001, 8002]

parser = argparse.ArgumentParser()
parser.add_argument('--node')
args = parser.parse_args()

NODE_ID = int(args.node)

PORT = PORTS[NODE_ID-1]
NODE_LOGFILE = f'node{NODE_ID}_CUSTOMLOG.log'
# Since this is run for each 'node', we're telling this node
# what ports the other nodes are running on.
other_nodes_ports = [p for p in [8000, 8001, 8002] if p != PORT]

# Configure Raft
raftos.configure({
    'log_path': './',
    'serializer': raftos.serializers.JSONSerializer
})
loop = asyncio.get_event_loop()

# Establish connection to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Akanksha#31",
    database="task_manager_db"
)

# Create cursor object for MySQL operations
cursor = db_connection.cursor()

# Each port is simulating a real life
# node/machine connected over a network.
this_node_address = f'127.0.0.1:{PORT}'

loop.create_task(
    raftos.register(
        this_node_address,

        # Telling Raft which ones are 
        # part of this node's cluster
        cluster=[
            f'127.0.0.1:{other_nodes_ports[0]}',
            f'127.0.0.1:{other_nodes_ports[1]}'
        ]
    )
)

with open(NODE_LOGFILE, 'w') as log_file:
    pass

async def run(loop):
    VARIABLE = raftos.Replicated(name='VARIABLE')

    # Non leaders get stuck in this loop!
    old_leader = None
    while raftos.get_leader() != this_node_address:

        await asyncio.sleep(5)

        with open(NODE_LOGFILE, 'a') as log_file:
            current_leader = raftos.get_leader()
            if current_leader != old_leader:
                log_file.write(f'Leader is now: {current_leader}\n')
            old_leader = current_leader

    # A node that reaches here has to be the leader.
    await asyncio.sleep(5)

    with open(NODE_LOGFILE, 'a') as log_file:
        # Simulate CLIENT telling the CLUSTER to set the value of VARIABLE
        try:
            # Perform database operation to read or write data
            cursor.execute("SELECT task_name, task_description, due_date FROM tasks")
            tasks = cursor.fetchall()
            # Convert tasks to a format suitable for replication
            tasks_data = [(task[0], task[1], task[2]) for task in tasks]

            # Update the Raft variable with the data from the database
            await VARIABLE.set(tasks_data)
        except mysql.connector.Error as err:
            print("MySQL Error:", err)

        log_file.write('Done synchronizing data with Raft variable.\n')

loop.run_until_complete(run(loop))
loop.run_forever()

