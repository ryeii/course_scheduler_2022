import itertools as itt
import math
import pandas as pd
from pyrsistent import b


perm6 = list(itt.permutations(range(6)))
comb53 = list(itt.combinations(range(5), 3))
PE5 = [0, 0, 0, 0, 1, 0, 0]
PE6 = [0, 0, 0, 0, 0, 1, 0]

df = pd.read_excel("new.xlsx", sheet_name="Students")

drop_list = {}
success_list = {}
success_electives_list = {}
fail_list = {}

for ind, row in df.iterrows():
    lst = [df["1、你的名字是"][ind]]
    for i in df.columns[9:17]:
        if not math.isnan(row[i]):
            lst.append([int(t) for t in list(str(int(row[i])))])
        else:
            lst.append([0])
    
    dropped = False
    for i in range(3):
        if lst[i+1] == [0]:
            drop_list[lst[0]] = i+1
            dropped = True
            break
    if dropped:
        continue
    
    electives = lst[4: 9]
    solved = False
    for comb in comb53:
        matrix = [[0 for i in range(7)] for j in range(6)]
        for i in range(3):
            for j in lst[i+1]:
                matrix[i][j-1] = 1
        chosen_electives = [electives[i] for i in comb]
        if [0] in chosen_electives:
            continue
        for i in range(3):
            for j in chosen_electives[i]:
                matrix[i+3][j-1] = 1

        for i in perm6:
            scatch = []
            for j in i:
                scatch.append(matrix[j])
            if i[0] == 2 or i[3] == 2:
                scatch = scatch[:5] + [PE6] + scatch[5:]
            else:
                scatch = scatch[:4] + [PE5] + scatch[4:]
            if sum([scatch[i][i] for i in range(7)]) == 7:
                temp = list(i)
                temp = list(map(lambda x: "Chi EN" if x == 0 else x, temp))
                temp = list(map(lambda x: "EN" if x == 1 else x, temp))
                temp = list(map(lambda x: "Math" if x == 2 else x, temp))
                temp = list(map(lambda x: "Electives 1" if x == 3 else x, temp))
                temp = list(map(lambda x: "Electives 2" if x == 4 else x, temp))
                temp = list(map(lambda x: "Electives 3" if x == 5 else x, temp))
                if temp[0] == "Math" or temp[3] == "Math":
                    temp = temp[:5] + ["PE"] + temp[5:]
                else:
                    temp = temp[:4] + ["PE"] + temp[4:]
                success_list[lst[0]] = temp
                temp = list(comb)
                temp = list(map(lambda x: "Choice 1" if x == 0 else x, temp))
                temp = list(map(lambda x: "Choice 2" if x == 1 else x, temp))
                temp = list(map(lambda x: "Choice 3" if x == 2 else x, temp))
                temp = list(map(lambda x: "Choice 4" if x == 3 else x, temp))
                temp = list(map(lambda x: "Choice 5" if x == 4 else x, temp))
                success_electives_list[lst[0]] = temp
                solved = True
                break
        if solved:
            break
    
    if not solved:
        fail_list[lst[0]] = lst[1:]


with open("log_suboptimal.txt", 'w') as f:
    f.write("---------- schedule log ----------\n")
    f.write("** In this log, the schedule might be suboptimal, e.g. 3 electives are chosen from 5 options. **\n")
    f.write("- statistics --------------------------------------------- \n")
    f.write("-> Total number of students: {}\n".format(len(df)))
    f.write("-> Number of students skipped: {}\n".format(len(drop_list)))
    f.write("-> Number of students successfully schduled: {}\n".format(len(success_list)))
    f.write("-> Number of students failed to schedule: {}\n".format(len(fail_list)))
    f.write("---------------------------------------------------------- \n")
    f.write("\n")
    f.write("skip list:\n")
    for i in drop_list:
        if str(drop_list[i]) == "1":
            f.write(i + ": English 1 empty\n")
        elif str(drop_list[i]) == "2":
            f.write(i + ": English 2 empty\n")
        elif str(drop_list[i]) == "3":
            f.write(i + ": Math empty\n")
    f.write("\n")
    f.write("success list:\n")
    for i in success_list:
        f.write(i + ": " + str(success_list[i]) + ", with electives " + str(success_electives_list[i]) + "\n")
    f.write("\n")
    f.write("fail list:\n")
    for i in fail_list:
        f.write(i + ": " + str(fail_list[i]) + "\n")
    f.write("\n")
    f.write("---------- end log ----------\n")
