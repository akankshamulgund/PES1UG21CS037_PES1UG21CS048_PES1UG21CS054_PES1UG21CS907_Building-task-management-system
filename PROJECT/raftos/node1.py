import threading
import time
import mysql.connector
from config import cfg
import utils

FOLLOWER = 0
CANDIDATE = 1
LEADER = 2


class Node():
    def __init__(self, fellow, my_ip):
        self.addr = my_ip
        self.fellow = fellow
        self.lock = threading.Lock()

        # Initialize MySQL connection
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Akanksha#31",
            database="yourdatabase"
        )
        self.db_cursor = self.db_connection.cursor()

        self.log = []
        self.staged = None
        self.term = 0
        self.status = FOLLOWER
        self.majority = ((len(self.fellow) + 1) // 2) + 1
        self.voteCount = 0
        self.commitIdx = 0
        self.timeout_thread = None
        self.init_timeout()

    def incrementVote(self):
        self.voteCount += 1
        if self.voteCount >= self.majority:
            print(f"{self.addr} becomes the leader of term {self.term}")
            self.status = LEADER
            self.startHeartBeat()

    def startElection(self):
        self.term += 1
        self.voteCount = 0
        self.status = CANDIDATE
        self.init_timeout()
        self.incrementVote()
        self.send_vote_req()

    def send_vote_req(self):
        for voter in self.fellow:
            threading.Thread(target=self.ask_for_vote, args=(voter, self.term)).start()

    def ask_for_vote(self, voter, term):
        message = {
            "term": term,
            "commitIdx": self.commitIdx,
            "staged": self.staged
        }
        route = "vote_req"
        while self.status == CANDIDATE and self.term == term:
            reply = utils.send(voter, route, message)
            if reply:
                choice = reply.json()["choice"]
                if choice and self.status == CANDIDATE:
                    self.incrementVote()
                elif not choice:
                    term = reply.json()["term"]
                    if term > self.term:
                        self.term = term
                        self.status = FOLLOWER
                break

    def decide_vote(self, term, commitIdx, staged):
        if self.term < term and self.commitIdx <= commitIdx and (
                staged or (self.staged == staged)):
            self.reset_timeout()
            self.term = term
            return True, self.term
        else:
            return False, self.term

    def startHeartBeat(self):
        print("Starting HEARTBEAT")
        if self.staged:
            self.handle_put(self.staged)

        for each in self.fellow:
            t = threading.Thread(target=self.send_heartbeat, args=(each,))
            t.start()

    def update_follower_commitIdx(self, follower):
        route = "heartbeat"
        first_message = {"term": self.term, "addr": self.addr}
        second_message = {
            "term": self.term,
            "addr": self.addr,
            "action": "commit",
            "payload": self.log[-1]
        }
        reply = utils.send(follower, route, first_message)
        if reply and reply.json()["commitIdx"] < self.commitIdx:
            reply = utils.send(follower, route, second_message)

    def send_heartbeat(self, follower):
        if self.log:
            self.update_follower_commitIdx(follower)

        route = "heartbeat"
        message = {"term": self.term, "addr": self.addr}
        while self.status == LEADER:
            start = time.time()
            reply = utils.send(follower, route, message)
            if reply:
                self.heartbeat_reply_handler(reply.json()["term"],
                                             reply.json()["commitIdx"])
            delta = time.time() - start
            time.sleep((cfg.HB_TIME - delta) / 1000)

    def heartbeat_reply_handler(self, term, commitIdx):
        if term > self.term:
            self.term = term
            self.status = FOLLOWER
            self.init_timeout()

    def reset_timeout(self):
        self.election_time = time.time() + utils.random_timeout()

    def heartbeat_follower(self, msg):
        term = msg["term"]
        if self.term <= term:
            self.leader = msg["addr"]
            self.reset_timeout()
            if self.status == CANDIDATE:
                self.status = FOLLOWER
            elif self.status == LEADER:
                self.status = FOLLOWER
                self.init_timeout()
            if self.term < term:
                self.term = term

            if "action" in msg:
                action = msg["action"]
                if action == "log":
                    payload = msg["payload"]
                    self.staged = payload
                elif self.commitIdx <= msg["commitIdx"]:
                    if not self.staged:
                        self.staged = msg["payload"]
                    self.commit()

        return self.term, self.commitIdx

    def init_timeout(self):
        self.reset_timeout()
        if self.timeout_thread and self.timeout_thread.isAlive():
            return
        self.timeout_thread = threading.Thread(target=self.timeout_loop)
        self.timeout_thread.start()

    def timeout_loop(self):
        while self.status != LEADER:
            delta = self.election_time - time.time()
            if delta < 0:
                self.startElection()
            else:
                time.sleep(delta)

    def handle_get(self, payload):
        key = payload["key"]
        query = "SELECT value FROM your_table WHERE key = %s"
        self.db_cursor.execute(query, (key,))
        result = self.db_cursor.fetchone()
        if result:
            payload["value"] = result[0]
            return payload
        else:
            return None

    def handle_put(self, payload):
        key = payload["key"]
        value = payload["value"]
        query = "INSERT INTO your_table (key, value) VALUES (%s, %s) ON DUPLICATE KEY UPDATE value = VALUES(value)"
        self.db_cursor.execute(query, (key, value))
        self.db_connection.commit()
        return True

    def commit(self):
        self.commitIdx += 1
        self.log.append(self.staged)
        key = self.staged["key"]
        value = self.staged["value"]
        self.DB[key] = value
        self.staged = None

