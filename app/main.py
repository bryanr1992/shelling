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
    #TODO:
    #Better splitting logic Not sure on how to go about it yet
    #Verify if our writing directory is a valid directory or at least formatted correctly
    if ">" in exec or "1>" in exec:
        source = []
        if "1>" in exec:
            dest = ''.join(args).split("1>")
        else:
            dest = ''.join(args).split(">")
        for arg in exec:
            if arg == ">" or arg == "1>":
                break
            source.append(arg)
        with open(dest[1], "w", econdign="utf-8") as file:
            subprocess.run(source, stdout=file)
        return
    if cmd == "echo":
        print(" ".join(args))

    elif cmd == "type":
        if not args:
            print(f"{args}: not found")
            return
        #if arguments were given check if its a built in
        if args[0] in BUILT_INS:
            print(f"{args[0]} is a shell builtin")
        #if is not a built in check if it exist in PATH and return the full PATH
        #else pring that the command given was not found
        elif p:= is_executable(dirs,args[0]):
            print(f"{args[0]} is {p}")
            return
        else:
            print(f"{args[0]}: not found") #prints when args is not empty and the built in command does not exist

    elif cmd == "pwd":
        print(f"{Path.cwd()}")

    elif cmd == "cd":
        if not args:
            print(f"{cmd}: no arguments given to command")
            return
        p = Path.cwd()
        p = p / args[0]

        #Check if the arg on CD is ~ and go to the home dir if it is
        if args[0] == "~":
            os.chdir(Path.home())
            return
        elif p.is_dir():
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

def parser(string):
    i = 0
    single_quotes = False
    double_quotes = False
    scape = False
    args = []
    current_arg = []

    while i < len(string):
        char = string[i]

        if scape and not single_quotes:
            current_arg.append(char)
            i += 1
            scape = False
            continue

        if char == '\\' and not single_quotes:
            scape = not scape
            i+= 1
            continue

        if char == "'" and not double_quotes:
            single_quotes = not single_quotes
            i += 1
            continue

        if char == '"' and not single_quotes:
            double_quotes = not double_quotes
            i += 1
            continue

        if char.isspace() and not single_quotes and not double_quotes:
            if current_arg:
                args.append(''.join(current_arg))
                current_arg = []
            i += 1
            continue

        #add char
        current_arg.append(char)
        i += 1

    #if remaining arg append it
    if current_arg:
        args.append(''.join(current_arg))
    return args

def main():
    #REPL loop
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input().strip()

        if not command:
            continue
        #naive parsing (not sure, but probably)
        command = parser(command)

        cmd = command[0]

        args = command[1:] if len(command) > 1 else ""


        if cmd == "exit":
            break
        else:
            handle_command(cmd,args,command)


if __name__ == "__main__":
    main()
