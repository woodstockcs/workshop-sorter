import csv
import math
import random
import sys
from classes import *


def main():
    '''
    assigns one day's worth of students to workshops
    '''
    print(" [inf] loading data...")

    students = get_students("students-day2.csv")
    print(f" [inf] loaded {len(students)} students")

    dupe_ids = get_dupe_students(students)
    if len(dupe_ids) > 0:
        print(f" [err] !! {len(dupe_ids)} duplicates found: ", end="")
        for id in dupe_ids:
            print(id, end=" ")
        print()

    workshops = get_workshops("workshops.csv")
    print(f" [inf] loaded {len(workshops)} workshops")

    requests = get_requests("responses.csv")
    print(f" [inf] loaded {len(requests)} requests")

    students = add_requests_to_student(requests, students)
    # print_top_preferences(students)

    workshops = create_enrollments(students, workshops)

    print_teacher_views(students, workshops)
    print_student_views(students, workshops)


def print_teacher_views(students, workshops):
    for workshop in workshops:
        print(workshop.get_id())
        print(workshop.enrollments_a)
        print(workshop.enrollments_b)


def print_student_views(students, workshops):
    for student in students:
        id = student.get_id()
        enrolled = get_enrollments_for_student(id, workshops)
        print(id, enrolled)
        if enrolled[0] == enrolled[1]:
            print("[err] !! duplicate")
            print(student.get_all_preferences())
            # break


def get_enrollments_for_student(id, workshops):
    output = [-1, -1]
    for workshop in workshops:
        if id in workshop.enrollments_a:
            output[0] = workshop.get_id()
        if id in workshop.enrollments_b:
            output[1] = workshop.get_id()
    return output


def print_top_preferences(students):
    for s in students:
        print(s.get_top_preferences(5))


def print_enrollments(workshops):
    for workshop in workshops:
        print(workshop.get_id())
        print(workshop.enrollments_a)
        print(workshop.enrollments_b)


def create_enrollments(students, workshops):
    students_with_requests = [
        s for s in students if len(s.get_all_preferences()) > 0]
    # print(f"enrolling {len(students_with_requests)} students with requests")
    for student in students_with_requests:
        # print_enrollments(workshops)
        # print(f"{student.get_id()} requests {student.get_all_preferences()}")
        # session 1
        selections = [-1, -1]
        while selections[0] == -1:
            num = 5
            while num > 0:
                tops = student.get_preferences_by_num(num)
                # print(f"{student.get_id()} is enrolled in {selections} and requests {tops} with rank {num}")
                if len(tops) < 1:
                    num -= 1
                    continue
                available = 0
                for top in tops:
                    if workshops[top].is_session_available(1):
                        available += 1
                if available == 0:
                    num -= 1
                    continue
                else:
                    candidate = workshops[random.choice(tops)]
                    if candidate.is_session_available(1):
                        candidate.enroll(student.get_id(), 1)
                        selections[0] = candidate.get_id()
                        break
            # nothing's available. just get in one.
            # print("nothing available!")
            if selections[0] == -1:
                for i in range(len(workshops)):
                    if workshops[i].is_session_available(1):
                        workshops[i].enroll(student.get_id(), 1)
                        selections[0] = i
                        break
        # print(f"{student.get_id()} gets workshops {selections}")
        # session 2
        while selections[1] == -1:
            num = 5
            while num > 0:
                tops = student.get_preferences_by_num(num)
                # print(f"{student.get_id()} is enrolled in {selections} and requests {tops} with rank {num}")
                if len(tops) < 1:
                    num -= 1
                    continue
                else:
                    try:
                        tops.remove(selections[0])
                        # print(f"removed an item. now its {tops}")
                        if len(tops) < 1:
                            num -= 1
                            continue
                    except Exception:
                        pass
                available = 0
                for top in tops:
                    if workshops[top].is_session_available(2):
                        available += 1
                if available == 0:
                    num -= 1
                    continue
                else:
                    candidate = workshops[random.choice(tops)]
                    if candidate.is_session_available(2):
                        candidate.enroll(student.get_id(), 2)
                        selections[1] = candidate.get_id()
                        break
            # nothing's available. just get in one.
            # print("nothing available!")
            if selections[1] == -1:
                for i in range(len(workshops)):
                    if workshops[i].is_session_available(2):
                        workshops[i].enroll(student.get_id(), 2)
                        selections[1] = i
                        break
        # print(f"{student.get_id()} gets workshops {selections}")

    students_without_requests = [
        s for s in students if len(s.get_all_preferences()) == 0]
    for student in students_without_requests:
        # print(f"enrolling {student.get_id()}")
        # print_enrollments(workshops)
        # session 1
        selections = [-1, -1]
        while selections[0] == -1:
            lowest = get_most_space(workshops, 1, -1)
            candidate = workshops[lowest]
            #candidate = workshops[random.choice(lowest)]
            candidate.enroll(student.get_id(), 1)
            selections[0] = candidate.get_id()
        # session 2
        while selections[1] == -1:
            lowest = get_most_space(workshops, 2, selections[0])
            candidate = workshops[lowest]
            #candidate = workshops[random.choice(lowest)]
            candidate.enroll(student.get_id(), 2)
            selections[1] = candidate.get_id()
        # print(f"{student.get_id()} gets {selections}")
        if selections[0] == selections[1]:
            print('DUPE')
            sys.exit(0)

    return workshops


def get_most_space(workshops, session, exclude):
    most_space = 0
    id = -1
    ok = False
    for w in workshops:
        if w.get_id() != exclude:
            space = w.get_space(session)
            # print(f"{w.get_id()} has {space} spaces left in session {session}.")
            if space > 0:
                ok = True
            if space > most_space:
                most_space = space
                id = w.get_id()
    if not ok:
        print(f" [err] !! NO MORE SPACE in any workshops for session {session}.")
        sys.exit(0)
    return id


def get_students(filename):
    output = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            if not row:
                continue
            item = Student(row[1], row[0])
            output.append(item)
    return output


def get_dupe_students(students):
    output = []
    for s1 in students:
        count = 0
        for s2 in students:
            if s1.get_id() == s2.get_id():
                count += 1
        if count > 1 and s1.get_id() not in output:
            output.append(s1.get_id())
    return output


def get_requests(filename):
    output = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            if not row:
                continue
            preferences = row[2:15]
            item = Request(row[0], row[1], preferences)
            output.append(item)
    return output


def get_workshops(filename):
    output = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        id = 0
        for row in reader:
            if not row:
                continue
            cap_a = 50
            cap_b = 50
            if int(row[1]) != -1:
                cap_a = int(row[1])
            if int(row[2]) != -1:
                cap_b = int(row[2])
            item = Workshop(id, row[0], cap_a, cap_b)
            output.append(item)
            id += 1
    return output


def add_requests_to_student(requests, students):
    count = 0
    unmatched_requests = []
    for request in requests:
        id = request.get_id()
        student_matches = [s for s in students if s.get_id() == id]
        if len(student_matches) == 0:
            unmatched_requests.append(request)
            # print(f" can't find student for {id}'s request")
        else:
            for idx, item in enumerate(students):
                if item.get_id() == id:
                    students[idx].set_preferences(request.get_preferences())
                    count += 1
                    break
    print(f" [inf] {count} requests matched to students")
    print(f" [wrn] ! {len(unmatched_requests)} requests couldn't find a student: ", end="")
    for u in unmatched_requests:
        print(u.get_id(), end=" ")
    print()
    return students


if __name__ == "__main__":
    main()


#
# requests = []
# with open("responses.csv", "r") as file:
#     reader = csv.reader(file)
#     for row in reader:
#         requests.append(row)
#
# workshops = requests.pop(0)
# print(len(workshops) - 1, "workshops found")
# print(len(requests), "requests found")
# print(math.ceil(len(requests) / (len(workshops) - 1)), "average enrollments")
#
# workshops_max = [6] * len(workshops)
# enrollments = [[] for _ in range(len(workshops))]
#
# workshop_count_fives = [0] * len(workshops)
# for request in requests:
#     for i in range(len(request)):
#         if request[i] == "5":
#             workshop_count_fives[i] += 1
# # print(workshop_count_fives)
#
# request_count_fives = [0] * len(requests)
# for i in range(len(requests)):
#     request_count_fives[i] += requests[i].count("5")
# # print(request_count_fives)
#
# print(enrollments)
# for request in requests:
#     fives = [i for i, x in enumerate(request) if x == '5']
#     if len(fives) > 2:
#         fives = random.sample(fives, 2)
#     for five in fives:
#         enrollments[five].append(request[0])
#
# sum = 0
# for e in enrollments:
#     sum += len(e)
#     print(len(e))
# print(sum)
