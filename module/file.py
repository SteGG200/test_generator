def get_file_content(path):
    f = open(path, "r", encoding="utf-8")
    s = f.read()
    f.close()
    return s