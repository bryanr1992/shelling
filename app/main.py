import sys


def main():
    #RPL loop
    while True:
        sys.stdout.write("$ ")

        command = input()
        
        #if command == exit stop the shell. temp solution using lower case for now until
        #I learn more about shell behavior
        if command.lower() == "exit":
            break
        
        print(f"{command}: command not found")
        pass


if __name__ == "__main__":
    main()
