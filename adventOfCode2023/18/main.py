def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    test_path = "./test.txt"
    data_path = "./data.txt"
    data = read([test_path, data_path][0])
    return 0

if __name__ == "__main__":
    main()
