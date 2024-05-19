import os

def valid_name(name):
    for c in name:
        if 48<=ord(c)<=57 or 65<=ord(c)<=90 or 97<=ord(c)<=122:
            continue
        else:
            return False
    return True


path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "src"))
print("Make sure you do not change the file structure.")
lang = input("Please enter which language you use {cpp/java/py}:")
if lang not in ["cpp","java","py","python"]:
    raise Exception("Unsupport language.")

if lang == "cpp":
    path = os.path.join(path, "checkers-cpp")
elif lang == "java":
    path = os.path.join(path, "checkers-java")
else:
    if lang == 'python':
        lang = "py"
    path = os.path.join(path, "checkers-python")

if not os.path.exists(path):
    raise IOError("Src folder does not exist. Make sure you do not change the file structure.")


name = input("please input your team name: ")
if not valid_name(name):
    raise Exception("Your team name can only contain alphanumeric characters")

os.system("zip -r "+name+"_"+lang+".zip"+" "+path)

print("The {teamname}_{language}.zip is under the tools/. Please submit it into Canvas.")