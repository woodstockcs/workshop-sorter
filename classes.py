class Student:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.preferences = []
        if not self.get_id().isalpha():
            print(f" !! need to fix input for {self.get_id()}")

    def get_id(self):
        id = (self.last_name[0:4] + self.first_name[0:2]).lower()
        return id

    def set_preferences(self, preferences):
        self.preferences = preferences

    def get_all_preferences(self):
        return self.preferences

    def get_preferences_by_num(self, num):
        if len(self.get_all_preferences()) > 0:
            tops = [i for i, x in enumerate(
                self.get_all_preferences()) if x == str(num)]
            return tops
        else:
            return []


class Workshop:
    def __init__(self, id, name, capacity_a, capacity_b):
        self.name = name
        self.id = id
        self.capacity_a = capacity_a
        self.capacity_b = capacity_b
        self.enrollments_a = []
        self.enrollments_b = []

    def get_id(self):
        return self.id

    def is_session_available(self, session):
        # print(f"checking workshop {self.get_id()}", end=": ")
        if session == 1:
            # print(f"{len(self.enrollments_a)} of {self.capacity_a} filled")
            return self.capacity_a > len(self.enrollments_a)
        if session == 2:
            # print(f"{len(self.enrollments_b)} of {self.capacity_b} filled")
            return self.capacity_b > len(self.enrollments_b)

    def get_space(self, session):
        if session == 1:
            return self.capacity_a - len(self.enrollments_a)
        elif session == 2:
            return self.capacity_b - len(self.enrollments_b)

    def get_session_count(self, session):
        if session == 1:
            return len(self.enrollments_a)
        elif session == 2:
            return len(self.enrollments_b)

    def enroll(self, id, session):
        if session == 1:
            self.enrollments_a.append(id)
        if session == 2:
            self.enrollments_b.append(id)


class Request:
    def __init__(self, timestamp, email, preferences):
        self.timestamp = timestamp
        self.email = email
        self.preferences = preferences

    def get_id(self):
        return self.email[2:8]

    def get_preferences(self):
        return self.preferences
