import csv
from assets.util.colleges_and_codes import college_n_codes

rounds = ['assets/data/csv/cmdk-24-r1.csv', 'assets/data/csv/cmdk-24-r2.csv', 'assets/data/csv/cmdk-24-r3.csv',
          'assets/data/csv/cmdk-24-mock.csv', 'assets/data/csv/cmdk-25-mock.csv']


def retrieve_college_data(counselling_round):
    colleges = []

    with open(rounds[counselling_round], newline='') as file:
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

    return colleges


def main():
    while True:
        print("-=-=-=-=-=-=-+[ COMED-K 2024 Cut-Offs ]+-=-=-=-=-=-=-")
        print("1. Search through college code")
        print("2. Search through rank")
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        choice = int(input(">> Enter your choice: "))
        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

        if choice == 1:
            college_code = input(">> Enter college code: ")
            counselling_round = int(input(">> Enter Round (1/2/3/4/5): ")) - 1

            colleges_list = retrieve_college_data(counselling_round)

            college = None
            for thing in colleges_list:
                if thing[0] == college_code:
                    college = thing

            if college:
                course_name = college[2]
                cutoff_rank = college[3]

                # Display
                print()
                header = "-=-=-=-=-=-=-+[ " + college[1] + " ]+-=-=-=-=-=-=-"
                print(header)

                for i in range(len(course_name)):
                    if course_name[i] and cutoff_rank[i]:
                        if course_name[i][0:2] in ['AI', 'AD', 'CB', 'CD', 'CS', 'CY', 'IC', 'IS', 'CI']:
                            print("[>]", course_name[i], " ➜ ", cutoff_rank[i])

                print("-=" * (len(header) // 2))
                print()
            else:
                print("[!] College not found!")

        elif choice == 2:

            start = int(input(">> Enter lower limit of rank (inclusive): "))
            end = int(input(">> Enter upper limit of rank (inclusive): "))

            counselling_round = int(input(">> Enter Round (1/2/3/4/5): ")) - 1

            colleges_list = retrieve_college_data(counselling_round)

            # Display
            for college in colleges_list:
                if len(college[2]) == len(college[3]):
                    valid_courses = []

                    course_name = college[2]
                    cutoff_rank = college[3]

                    for i in range(len(course_name)):
                        if course_name[i] and cutoff_rank[i]:
                            if start <= int(cutoff_rank[i]) <= end:
                                valid_courses.append((course_name[i], cutoff_rank[i]))

                    if valid_courses:
                        header = "-=-=-=-=-=-=-+[ " + college[1] + " ]+-=-=-=-=-=-=-"
                        print(header)

                        for course in valid_courses:
                            print("[>]", course[0], " ➜ ", course[1])

                        print("-=" * (len(header) // 2))
                        print()

        redo = input(">> Recheck? (Y/N): ")
        print()
        if redo.upper() != 'Y': break


if __name__ == "__main__":
    main()
