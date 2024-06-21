import json
import os

def printError(text):
	print("[ERROR]:",text)
def printInfo(text):
	print("[INFO]:",text)


def printTable(data,title=False):
	maxwidth = 0
	n,m = len(data),len(data[0])
	for i in range(n):
		for j in range(m):
			data[i][j] = str(data[i][j])

	data_matrix = []
	for i in data:
		data_matrix.extend([len(j) for j in i])
	maxwidth_arr = []
	for i in range(m):
		maxwidth += max(data_matrix[i::m])
		maxwidth_arr.append(max(data_matrix[i::m]))
	maxwidth += m+1
	print("-"*maxwidth)
	if title:
		title_row = data.pop(0)
		for d in range(m):
			max_space = maxwidth_arr[d]
			datalen = len(title_row[d])
			space = max_space-datalen
			spacei = space//2
			print("|{0}{1}{2}".format(" "*spacei,title_row[d]," "*(space - spacei)),end="")
		print("|")
		print("-"*maxwidth)
	for row in data:
		for i in range(m):
			max_space = maxwidth_arr[i]
			datalen = len(row[i])
			d = row[i]
			space = max_space - datalen
			print("|{}".format(d+" "*space),end="")
		print("|")
	print("-"*maxwidth)
DIRNAME = os.path.dirname(os.path.abspath(__file__))

FILENAME = os.path.join(DIRNAME,"voters.obj")
#printTable([["new table","working table"],["very good table","happy go lucky"]],title=True)
if not os.path.exists(FILENAME):
	printError("{} not found.".format(FILENAME))
	exit()
with open(FILENAME) as f:
	data = json.load(f)
	f.close()
#print(data["information"])
printTable([[" "*10+data["information"]["desc"]+" "*10]])

cands = data["candidates"]
printInfo("Total Voters are {}".format(len(data["voters"])))
for key,vals in cands.items():
	print("\n\n\n",key.upper())
	data = [["Sno.","Candidate","Vote(s)"]]
	sno = 1
	d =[]
	maxi = 0
	for cand in vals.values():
		data.append([sno,cand["name"],len(cand["voters"])])
		sno += 1
		if len(cand["voters"])>=maxi:
			d.clear() if len(cand["voters"])>maxi else None
			d.append(cand["name"])
			maxi = len(cand["voters"])
	printTable(data,title=True)
	if len(d) == 1:
		print("[WINNER]:",d[0],"(With {0} vote{1})".format(maxi,"s" if maxi>1 else ""))
	else:
		print("Winner cannot be decided since {0} have {1} vote{2}".format(", ".join(d),maxi,"s" if maxi>1 else ""))
os.system("pause")

