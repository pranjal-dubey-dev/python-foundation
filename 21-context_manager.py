"""
Context Managers
----------------
Whenever you need setup before an operation and cleanup
afterward, a context manager can help.
"""

import os
from contextlib import contextmanager


# 1. Manual File Handling

# f = open("sample.txt", "w")
# f.write("Lorem ipsum dolor sit amet")
# f.close()


# 2. Built-in Context Manager

# with open("sample.txt", "w") as f:
#     f.write("Lorem ipsum dolor sit amet")


# 3. Class-Based Context Manager

class OpenFile:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, traceback):
        self.file.close()


# with OpenFile("sample.txt", "w") as f:
#     f.write("Testing")

# print(f.closed)


# 4. Generator-Based Context Manager

@contextmanager
def open_file(filename, mode):
    f = open(filename, mode)

    try:
        yield f
    finally:
        f.close()


with open_file("sample.txt", "w") as f:
    f.write("Vae Victus")

print(f.closed)


# 5. Manual Directory Handling

# cwd = os.getcwd()
# os.chdir("Sample-Dir-One")
# print(os.listdir())
# os.chdir(cwd)


# 6. Generator-Based Directory Context Manager

@contextmanager
def change_dir(destination):
    cwd = os.getcwd()

    try:
        os.chdir(destination)
        yield
    finally:
        os.chdir(cwd)


# with change_dir("Sample-Dir-One"):
#     print(os.listdir())

# with change_dir("Sample-Dir-Two"):
#     print(os.listdir())


# 7. Class-Based Directory Context Manager

class DirectoryLister:
    def __init__(self, destination):
        self.destination = destination

    def __enter__(self):
        self.cwd = os.getcwd()
        os.chdir(self.destination)

    def __exit__(self, exc_type, exc_val, traceback):
        os.chdir(self.cwd)


with DirectoryLister('for_testing'):
    print(os.listdir())
