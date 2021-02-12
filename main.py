import sys
import boto
import getopt

def main(argv):
    #Local Variables
    inputMode = ''
    inputSource =''
    inputDestination = ''

    #Attempt to assign input.
    try:
        inputMode = argv[0]
        inputSource = argv[1]
        inputDestination = argv[2]
    except getopt.GetoptError:
        print("cloudBackup.py <backup/restore> <source_directory/source_bucket:directory> <destination_bucket:directory/destination_directory>")
        sys.exit(2)





# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
