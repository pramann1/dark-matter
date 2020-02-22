import sys
import os
import time
import os.path
from swpag_client import Team
from shutil import move

if len(sys.argv) != 3:
    sys.exit("Please pass correct number of arguments. TEAM(IP(ARG1), FLAG_TOKEN(ARG2))")

t = Team(sys.argv[1], sys.argv[2])


def submitStub(flags):
    list = []
    for flag in flags:
        if flag in ['flagNAME69', 'flagNAME2']:
            list.append('correct')
    return list


def submitFlags(flags):
    correct = 0
    flagResponse = []
    try:
        print(flags)
        flagResponse = t.submit_flag(flags)
        # flagResponse = submitStub(flags)
    except Exception:
        print ("Error submitting flags.")
    for response in flagResponse:
        if response.startswith('correct'):
            correct = correct + 1
    print("Submitted [" + str(len(flags)) + "] flags. [" + str(correct) + "] were correct.")


def processLine(line):
    newList = []
    pruneString = line.split("FLG")
    for x in pruneString:
        newList.append('FLG' + x)
    return newList


directory = os.path.normpath("flags")
while True:
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                f = open(os.path.join(subdir, file), 'r')
                flags = []
                for line in f:
                    submitFlags((processLine(line)))
                f.close()
                move(os.path.join(subdir, file), 'archivedFlags\\archived_' + file)
                # os.remove(os.path.join(subdir, file))
    print("scanning for files in pool...")
    time.sleep(1)
