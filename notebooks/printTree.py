import os

def print_tree(path, indent=""):
    ignored_folders = {"__pycache__", ".obsidian"}  # Danh sách các thư mục cần bỏ qua
    try:
        entries = os.listdir(path)
    except PermissionError:
        print(indent + "[Permission Denied]")
        return
    
    # Lọc ra danh sách thư mục và tệp
    folders = [entry for entry in entries if os.path.isdir(os.path.join(path, entry)) and entry not in ignored_folders]
    files = [entry for entry in entries if os.path.isfile(os.path.join(path, entry))]

    # Duyệt qua các thư mục trước
    for folder in folders:
        full_path = os.path.join(path, folder)
        print(indent + "|-- " + folder + "/")
        print_tree(full_path, indent + "    ")

    # Sau đó duyệt qua các tệp
    for file in files:
        print(indent + "|-- " + file)

root_path = r"E:\ChatBot_RAG"  # Thay bằng đường dẫn thư mục của bạn
print(f"{root_path}:")
print_tree(root_path)
