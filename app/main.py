import sys
import os
import subprocess
from pathlib import Path

path_var = os.environ.get('PATH','')
dirs = [Path(p) for p in path_var.split(os.pathsep)]

BUILT_INS = {"exit": True,
             "echo": True,
              "type": True,
               "pwd": True,
                "cd": True }

def is_executable(path,c):
    """
        Loops through dirs in PATH and adds the "cmd" to the path
        if this path resolves to an executable we return the full
        path else return an empty string
    """
    for p in path:
        p = p/c
        if p.is_file():
            if os.access(p, os.X_OK):
                return p
    return ""


def handle_command(cmd, args, exec):
    if cmd == "echo":
        print(" ".join(args))

    elif cmd == "type":
        #if arguments were given check if its a built in
        if args and args[0] in BUILT_INS:
            print(f"{args[0]} is a shell builtin")
        #if is not a built in check if it exist in PATH and return the full PATH
        #else pring that the command given was not found
        elif args:
            if p:= is_executable(dirs,args[0]):
                print(f"{args[0]} is {p}")
                return

            print(f"{args[0]}: not found") #prints when args is not empty and the built in command does not exist
                        
        else:
            print(f"{args}: not found")#prints when args is empty

    elif cmd == "pwd":
        print(f"{Path.cwd()}")

    elif cmd == "cd":
        p = Path.cwd()
        p = p / args[0]

        if p.is_dir():
            os.chdir(p)
            return
        print(f"cd: {p}: No such file or directory")
        return
    else: 
        #No built in command found check PATH
        #If it exist in path execute, otherwise print command not found
        if is_executable(dirs,cmd):
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
