from module import getLatestPath
def text_to_data2(exam_content):
    data = []
    if len(exam_content) == 0:
        raise ValueError("Nội dung đề thi không hợp lệ")
    # difficulty = int(input("Difficulty (1-3): "))
    typelist = ["HTML_CSS", "DaoDuc", "Luat", "AI", "SQLCode", "SQLTheory", "Network"]
    print("--------------------")
    print("Choose question type: ")
    for i in range(1, len(typelist) + 1):
        print(str(i) + ". " + typelist[i-1])
    # print(typelist)
    type = 1
    lines = exam_content.split('\n')
    for line in lines:
        line = line.strip()
        if line == '':
            continue
        if line.startswith(('a)', 'b)', 'c)', 'd)')):
            array_answer = line.split(')', 1)
            # print(array_answer)
            if len(array_answer)!= 2:
                raise ValueError('Invalid array answer format')
            order_answer, content_answer = array_answer
            data[-1][order_answer] = content_answer.strip()
        elif line.startswith('*'):
            array_answer = line[1:].split(')', 1)
            if len(array_answer)!= 2:
                raise ValueError('Invalid array answer format')
            order_answer, content_answer = array_answer
            # print(array_answer)
            # order_answer = order_answer[1]
            data[-1][order_answer] = content_answer.strip()
            data[-1]['anwser'] = order_answer
        else:
            data.append({})
            data[-1]['type'] = typelist[type - 1]
            data[-1]['question'] = ""
            data[-1]['a'] = ""
            data[-1]['b'] = ""
            data[-1]['c'] = ""
            data[-1]['d'] = ""
            data[-1]['anwser'] = ""

            index_separator = line.find('.')
            if index_separator == -1:
                raise ValueError('Invalid question format')
            array_answer = line.split('.', 1)
            if len(array_answer)!= 2:
                raise ValueError('Invalid question format')
            number_question, content_question = array_answer
            if not number_question.isnumeric():
                raise ValueError('Invalid question format')
            data[-1]['question'] = content_question.strip()
    return data
def text_to_data(exam_content):
    data = []
    if len(exam_content) == 0:
        raise ValueError("Nội dung đề thi không hợp lệ")
    # difficulty = int(input("Difficulty (1-3): "))
    typelist = ["HTML_CSS", "DaoDuc", "Luat", "AI", "SQLCode", "SQLTheory", "Network"]
    print("--------------------")
    print("Choose question type: ")
    for i in range(1, len(typelist) + 1):
        print(str(i) + ". " + typelist[i-1])
    # print(typelist)
    type = int(input("Question type (number): "))
    lines = exam_content.split('\n')
    for line in lines:
        line = line.strip()
        if line == '':
            continue
        if line.startswith(('a)', 'b)', 'c)', 'd)')):
            array_answer = line.split(')', 1)
            # print(array_answer)
            if len(array_answer)!= 2:
                raise ValueError('Invalid array answer format')
            order_answer, content_answer = array_answer
            data[-1][order_answer] = content_answer.strip()
        elif line.startswith('*'):
            array_answer = line[1:].split(')', 1)
            if len(array_answer)!= 2:
                raise ValueError('Invalid array answer format')
            order_answer, content_answer = array_answer
            # print(array_answer)
            # order_answer = order_answer[1]
            data[-1][order_answer] = content_answer.strip()
            data[-1]['anwser'] = order_answer
        else:
            data.append({})
            data[-1]['type'] = typelist[type - 1]
            data[-1]['question'] = ""
            data[-1]['a'] = ""
            data[-1]['b'] = ""
            data[-1]['c'] = ""
            data[-1]['d'] = ""
            data[-1]['anwser'] = ""

            index_separator = line.find('.')
            if index_separator == -1:
                raise ValueError('Invalid question format')
            array_answer = line.split('.', 1)
            if len(array_answer)!= 2:
                raise ValueError('Invalid question format')
            number_question, content_question = array_answer
            if not number_question.isnumeric():
                raise ValueError('Invalid question format')
            data[-1]['question'] = content_question.strip()
    return data

# def latest():
# 	path = getLatestPath() + "/content.txt"
# 	txt_file = open(path, 'r', encoding="utf-8")
# 	file_content = txt_file.read()
# 	txt_file.close()
# 	data = text_to_data(file_content)
# 	for x in data:
# 		print(x)
# 	print(len(data))