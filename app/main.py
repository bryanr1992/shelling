import sys
import os

path = os.environ.get('PATH','')
dirs = path.split(os.pathsep)

BUILT_INS = {"exit": True,
             "echo": True,
              "type": True }

def handle_command(command):
    if command[0] == "echo":
        print(" ".join(command[1:]))
    elif command[0] == "type":
        if command[1] in BUILT_INS:
            print(f"{command[1]} is a shell builtin")
        else:
            for dir in dirs:
                #Check if a file with the command name exist,
                    #check for execute permision
                    #print <command> full path if execute pernussion
                    #return
                file = os.path.join(dir, command[1])
                if os.path.exists(file):
                    if os.access(file, os.X_OK):
                        print(f"{command[1]} is {file}")
                        return
                        
            print(f"{command[1]}: not found")
    else:
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
