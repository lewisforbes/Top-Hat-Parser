import csv
from os import listdir, remove
from os.path import isfile, join
from subprocess import call
from time import sleep

def exception(msg):
    print("ERROR")
    print(msg)
    sleep(3)
    raise Exception()

# generate formatted string from q details
def parse_q(q, ans):
    q = q.replace("```", "\n```").replace("\n\n```", "\n```")
    output = "\n"+q
    for i, a in enumerate(ans):
        bold = "  "
        if i==0:
            bold = "**"
        output += "\n{}. {}{}{}".format(i+1, bold, a, bold)
    return output

# installs node modules if required and joins processed csvs 
def init(dirname, outname):
    call("_converter\init.bat")

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
out_path="output/"

# user's input
user_path = "_converter/input/"
user_files = listdir(user_path)
if len(user_files)!=1:
    exception("Must provide exactly 1 input file. You've given {}.".format(len(user_files)))
user_fname = user_files[0]

# create input csv for program
joined_fname = out_path+"[joined] "+ user_fname
init(in_path, joined_fname)

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
    output += parse_q(line[1], line[3:])
    output += "\n"

output = output.replace('\u2713', '') # remove rogue trailing character, strip() doesn't work
f.close()

f = open(out_path+"[parsed] " + user_fname.replace(".csv", ".md"), "w")
f.write(output)
f.close()

# remove(joined_fname)
sleep(1)