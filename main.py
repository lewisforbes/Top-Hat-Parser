import csv
from os import listdir, mkdir
from os.path import isfile, join
from subprocess import call
from time import sleep

def exception(msg):
    print("ERROR")
    print(msg)
    sleep(3)
    raise Exception()

# generate formatted string from q details
def parse_q(q, correct_raw, ans):
    correct = []
    if correct_raw=="":
        correct_raw = "N/A"
    elif correct_raw=="0":
        correct_raw="ERROR"
    else:
        correct = correct_raw.split(",")
        try:
            correct = [int(q_i) for q_i in correct]
        except:
            exception("Correct column format is not valid: {}".format(correct_raw))
    
    
    q = q.replace("```", "\n```").replace("\n\n```", "\n```")
    output = "\n"+q
    for i, a in enumerate(ans):
        bold = "  "
        if i+1 in correct:
            bold = "**"
        output += "\n{}. {}{}{}".format(i+1, bold, a, bold)
    
    output += "\n\nCorrect: {}".format(correct_raw)

    return output

# installs node modules if required and joins processed csvs 
def init(dirname, outname, out_path):
    call("_converter\init.bat")
    mkdir(out_path)

    # join csvs
    fnames = [f for f in listdir(dirname) if isfile(join(dirname, f))]
    if len(fnames)==0:
        exception("No input files provided.")
    output = []
    first_file = True
    for fname in fnames:
        first_line = True
        f = open(dirname+fname, "r")
        for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
            if first_line and (not first_file):
                first_line = False
                continue
            output.append(line)
        if first_file:
            first_file = False
        
    with open(outname, 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(output)
    return outname


# input/output for the program
in_path="_converter/output/"
out_path="_converter/final_output/"

# user's input
user_path = "_converter/input/"
user_files = listdir(user_path)
try:
    user_files.remove("placeholder")
except:
    pass

if len(user_files)!=1:
    exception("Must provide exactly 1 input file. You've given {}.".format(len(user_files)))
user_fname = user_files[0]

# create input csv for program
joined_fname = out_path+"[joined] "+ user_fname
init(in_path, joined_fname, out_path)

# make data
f = open(joined_fname, "r")
first = True
i = 0
output = "## Questions from {}".format(user_fname)
for line in csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
    if first:
        first=False
        continue
    i+=1
    output += "\n### Question {}".format(i)
    output += parse_q(line[1], line[2], line[3:])
    output += "\n"

output = output.replace('\u2713', '') # remove rogue trailing character, strip() doesn't work
f.close()

f = open(out_path+"[parsed] " + user_fname.replace(".csv", ".md"), "w")
f.write(output)
f.close()

sleep(1)