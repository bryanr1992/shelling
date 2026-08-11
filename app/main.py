import sys
import os
import subprocess
from pathlib import Path

path_var = os.environ.get('PATH','')
dirs = [Path(p) for p in path_var.split(os.pathsep)]

BUILT_INS = {"exit": True,
             "echo": True,
              "type": True }

def is_executable(path):

    if path.is_file():
        if os.access(path, os.X_OK):
            return True
    return False


def handle_command(command):
    if command[0] == "echo":
        print(" ".join(command[1:]))
    elif command[0] == "type":
        if command[1] in BUILT_INS:
            print(f"{command[1]} is a shell builtin")
        else:
            #Check if a file with the command name exist,
                #check for execute permision
                    #print <command> full path if execute pernussion
                    #return
            for dir in dirs:
                dir = dir / command[1]
                if is_executable(dir):
                    print(f"{command[1]} is {dir}")
                    return
                        
            print(f"{command[1]}: not found")
    else:
        for dir in dirs:
            dir = dir / command[0]
            if is_executable(dir):
                try:
                    subprocess.run(command)
                except subprocess.CalledProcessError as e:
                    print(f"Command failed with exit code {e.returncode}")
                    print(f"Error message: {e.stderr}")
        print(f"{command[0]}: command not found")#tmp command not found

def main():
    #REPL loop
    while True:
        sys.stdout.write("$ ")

        command = input()
        
        #if command == exit stop the shell. temp solution using lower case for now until
        #I learn more about shell behavior

        #naive parsing (not sure, but probably)

        command = command.split(" ")

        if command[0] == "exit":
            break
        elif command[0] == "":
            continue
        else:
            handle_command(command)
        pass


if __name__ == "__main__":
    main()
