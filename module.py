from datetime import datetime
from handler import create_exam_document, get_exam_content, convert_to_QTI
from module import txt2csv, txt2qti, getLatestPath, getDatabasePath, text_to_data2, get_file_content
import pandas as pd
import csv
import random
import os

def addToCsv(file_path):
    file = open(file_path, "r", encoding="utf-8")
    file_content = file.read()
    file.close()
    current_data = txt2csv.text_to_data(file_content)
    cnt = 1
    for ques in current_data:
        print(str(cnt) + ". Question: " + ques['question'])
        print("A. " + ques['a'])
        print("B. " + ques['b'])
        print("C. " + ques['c'])
        print("D. " + ques['d'])
        print("Correct Anwser: " + ques['anwser'])
        cnt += 1
    check = input("Save this question [y/n]?")
    if(check == 'y'):
        df = pd.DataFrame.from_dict(current_data)
        print(df)
        df.to_csv(getDatabasePath(), mode='a', index=False,
                  header=False, encoding="utf-8")

def rowToString(row, question_num):
    res = ""
    header = {"type": 0, "question": 1, "a": 2,
              "b": 3, "c": 4, "d": 5, "anwser": 6}
    res += str(question_num) + ". "
    res += row[1] + "\n"
    queslist_string = ["a)", "b)", "c)", "d)"]
    answer_index = header[row[6]]
    for i in range(2, 6):
        if(answer_index == i):
            res += "*"
        res += queslist_string[i - 2] + " "
        res += row[i] + "\n"
    return res
def groupToString(questions, pick):
    res = ""
    cnt = 0
    if(pick == len(questions)):
        for question in questions:
            cnt += 1
            res += rowToString(question, cnt)
            res += "\n"
    else:
        res += "GROUP\n"
        res += "pick: " + str(pick) + "\n"
        for question in questions:
            cnt += 1
            res += rowToString(question, cnt)
            res += "\n"
        res += "END_GROUP\n"
    return res
def deleteDuplicate():
    path = f"./dist/{datetime.now().strftime('%Y%m%d_%H%M%S')}_database_exported"
    exam_path = path + "/exam.txt"
    question_bank_path = path + "/bank.txt"
    if not os.path.exists(path):
        os.makedirs(path)
    allrows = []
    type_dict = {}
    with open(getDatabasePath(), "r", encoding="utf-8") as file:
        filedata = csv.reader(file)
        for row in filedata:
            allrows.append(row)
    for row in allrows:
        type_dict[row[0]] = []
    for row in allrows:
        type_dict[row[0]].append(row)
    data = []
    check = {}
    count = 0
    for questions in type_dict.values():
        for i in range(len(questions)):
            if questions[i][1] not in check:
                check[questions[i][1]] = 1
                data.append({})
                for j in range(7):
                    data[-1][j] = questions[i][j]
            else:
                count += 1
    df = pd.DataFrame.from_dict(data)
    print(df)
    df.to_csv(getDatabasePath(), mode='w', index=False,
                header=False, encoding="utf-8")
    print("Question removed: " + str(count))
            
def exportDatabase():
    path = f"./dist/{datetime.now().strftime('%Y%m%d_%H%M%S')}_database_exported"
    exam_path = path + "/exam.txt"
    question_bank_path = path + "/bank.txt"
    if not os.path.exists(path):
        os.makedirs(path)
    allrows = []
    type_dict = {}
    with open(getDatabasePath(), "r", encoding="utf-8") as file:
        filedata = csv.reader(file)
        for row in filedata:
            allrows.append(row)
    for row in allrows:
        type_dict[row[0]] = []
    for row in allrows:
        type_dict[row[0]].append(row)
    exam_data = ""
    bank_data = ""
    question_count = 0
    for type in type_dict.keys():
        number = int(input("Choose number of " + type + " questions (current have " + str(len(type_dict[type])) + " questions): "))
        number = min(number, len(type_dict[type]))
        if(number == 0): continue
        bank_data += groupToString(type_dict[type], number)
        bank_data += "\n"
        list_questions = random.sample(type_dict[type], number)
        for question in list_questions:
            question_count += 1
            exam_data += rowToString(question, question_count) + "\n"
    # print(text_to_data2(exam_data))
    suffled_data = (text_to_data2(exam_data))
    random.shuffle(suffled_data)
    exam_data = ""
    for i in range(len(suffled_data)):
        current_row = []
        for value in suffled_data[i].values():
            current_row.append(value)
        exam_data += rowToString(current_row, i + 1)
        exam_data += "\n"

    file = open(exam_path, "w+", encoding="utf-8")
    file.write(exam_data)
    file.close()
    file = open(question_bank_path, "w+", encoding="utf-8")
    file.write(bank_data)
    file.close()
    print("Đang tạo tài liệu...")
    create_exam_document(path, exam_data)
    
    print("Đang tạo tài liệu QTI...")
    convert_to_QTI(path, bank_data, "bank.txt")
    convert_to_QTI(path, exam_data, "exam.txt")

def module():
    feature = "1.Add to database\n2.Text to qti\n3.Export database\n4.Delete duplicate question in database\n"
    mode = "1.Latest path\n2.Custom path\n"
    feature_choosed = int(input(feature + "Choose mode: "))
    if(feature_choosed == 1):
        mode_choosed = int(input(mode + "Choose mode: "))
        if(mode_choosed == 1):
            addToCsv(getLatestPath() + "/content.txt")
        else:
            path = input("Enter name of containing folder: ")
            addToCsv("./dist/" + path + "/content.txt")
    elif(feature_choosed == 2):
        mode_choosed = int(input(mode + "Choose mode: "))
        if(mode_choosed == 1):
            exam_content = get_file_content(getLatestPath() + "/content.txt")
            convert_to_QTI(getLatestPath(), exam_content)
        else:
            path = input("Enter name of containing folder: ")
            filename = input("Enter name of file: ")
            exam_content = get_file_content("./dist/" + path + "/" + filename)
            convert_to_QTI("./dist/" + path, exam_content, filename)
    elif(feature_choosed == 3):
        exportDatabase()
    elif(feature_choosed == 4):
        deleteDuplicate()


if __name__ == "__main__":
    module()
