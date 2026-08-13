import sys
import os
import subprocess
from pathlib import Path

path_var = os.environ.get('PATH','')
dirs = [Path(p) for p in path_var.split(os.pathsep)]

BUILT_INS = {"exit": True,
             "echo": True,
              "type": True,
               "pwd": True }

def is_executable(path):
    """Determines if we have a file instead of a dir
       and if the file has execute permision
    """
    if path.is_file():
        if os.access(path, os.X_OK):
            return True
    return False


def handle_command(cmd, args, exec):
    if cmd == "echo":
        print(" ".join(args))
    elif cmd == "type":
        if args and args[0] in BUILT_INS:
            print(f"{args[0]} is a shell builtin")
        elif args:
            #Check if a file with the command name exist,
                #check for execute permision
                    #print <command> full path if execute pernussion
                    #return
            for dir in dirs:
                dir = dir / args[0]
                if is_executable(dir):
                    print(f"{args[0]} is {dir}")
                    return
            print(f"{args[0]}: not found") #prints when args is not empty and the built in command does not exist
                        
        else:
            print(f"{args}: not found")#prints when args is empty

    elif cmd == "pwd":
        print(f"{Path.cwd()}")
    else:
        for dir in dirs:
            dir = dir / cmd
            if is_executable(dir):
                try:
                    subprocess.run(exec)
                    return
                except subprocess.CalledProcessError as e:
                    print(f"Command failed with exit code {e.returncode}")
                    print(f"Error message: {e.stderr}")
        print(f"{cmd}: command not found")#tmp command not found

def main():
    #REPL loop
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input().strip()

        if not command:
            continue
        #naive parsing (not sure, but probably)

        command = command.split(" ")

        cmd = command[0]

        args = command[1:] if len(command) > 1 else ""


        if cmd == "exit":
            break
        else:
            handle_command(cmd,args,command)
        pass


if __name__ == "__main__":
    main()
