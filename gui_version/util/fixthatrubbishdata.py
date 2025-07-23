from util.colleges_and_codes import college_n_codes
import json
import csv

colleges = []

with open("CSV-FILE-PATH", newline='') as file:
    reader = list(csv.reader(file))
    for code in college_n_codes:
        course_name = []
        cutoff_rank = []

        for line in reader:
            if line[0] == "College Code":
                course_name += line[3:]
            if line[0] == code and line[2] == 'GM':
                cutoff_rank += line[3:]

        college = (code, college_n_codes[code], course_name, cutoff_rank)
        colleges.append(college)

with open("NEW-FILE-PATH", 'w') as file:
    final_obj = []
    for college in colleges:

        valid_courses = []
        valid_ranks = []

        for i in range(len(college[2])):
            if len(college[2]) == len(college[3]):
                if college[2][i] and college[3][i]: # both course name and rank is there
                    valid_courses.append(college[2][i])
                    valid_ranks.append(college[3][i])

        obj = {
            "code": college[0],
            "name": college[1],
            "courses": dict(zip((course for course in valid_courses), (rank for rank in valid_ranks)))
        }
        final_obj.append(obj)
    json.dump(final_obj, file, indent=4)
