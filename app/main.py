import sys


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
        elif command[0] == "echo":
            print(" ".join(command[1:]))
        else:
            print(f"{command[0]}: command not found")
        pass


if __name__ == "__main__":
    main()
