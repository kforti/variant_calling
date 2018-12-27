import pexpect
import argparse
import sys

destination = "/home/kf78w"
files_to_push = ["albacore.py", "basecall_config.py", "commandline.py", "data_types.py", "utils.py"]
password = "List23222!"

def push_to_cluster(files, destination, password=password):
    command = "scp "
    for file in files:
        command += file + " "
    command += "kf78w@ghpcc06.umassrc.org:" + destination
    print(command)

    child = pexpect.spawn(command)
    child.delaybeforesend = 10
    child.expect("kf78w@ghpcc06.umassrc.org's password: ", timeout=None)
    child.sendline(password)
    child.expect(pexpect.EOF, timeout=10)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Files to push and destination to push to.')
    parser.add_argument('-f', '--files', type=str, nargs="*",
                        help='list the files you would like to push')
    parser.add_argument('-d', '--destination', type=str,
                        help='destination on the cluster')
    args = parser.parse_args()
    if args.files:
        files_to_push = args.files
    if args.destination:
        destination = args.destination

    push_to_cluster(files_to_push, destination)




