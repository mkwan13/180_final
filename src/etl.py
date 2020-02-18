import sys
from collections import Counter

revert = 0
revert_pairs = {}
edits = {}
mutual_revert_pairs = {}
mutual_revert_users = {}
user_edits = {}
lineLabels = {}
lineAuthors = {}

def readFile():
    global user_edits
    global revert_pairs
    global lineLabels
    global lineAuthors
    global revert
    global edits
    for ln in open(file, 'r', encoding = 'utf-8'):
        if not '^^^_' in ln:
            title = ln.strip()
            lineLabels[title] = []
            lineAuthors[title] = []
            revert_pairs[title] = []
            continue
        
        parts = ln.strip().split(' ')
        if len(parts) < 4:
            continue
        if parts[3] not in user_edits:
            user_edits[parts[3]] = 1
        else:
            user_edits[parts[3]] += 1
            
        if parts[1] == '1':
            revert += 1
            lineLabels[title].append(int(parts[2]))
            lineAuthors[title].append(parts[3])
            continue
        line = getLine(title, int(parts[2]))
        if line != None:
            revertedU = parts[3]
            revertingU = lineAuthors[title][line-1]
            if revertedU == revertingU:
                continue
            pair = revertedU + "~!~" + revertingU
            if pair not in revert_pairs[title]:
                revert_pairs[title].append(pair)
				
def getMutual(title):
    global revert_users
    global mutual_revert_users
    mutual_revert_users[title] = []
    mutual_revert_pairs[title] = []
    for pair in revert_pairs[title]:
        #print(revert_pairs)
        parts = pair.split('~!~')
        if parts[1] + '~!~' + parts[0] in revert_pairs[title]:
            sorted_pair = ""
            if parts[0] < parts[1]:
                sorted_pair = parts[0] + "~!~" + parts[1]
            else:
                sorted_pair = parts[1] + "~!~" + parts[0]
            mutual_revert_pairs[title].append(sorted_pair)
            if parts[1] not in mutual_revert_users[title]:
                mutual_revert_users[title].append(parts[1])
            if parts[0] not in mutual_revert_users[title]:
                mutual_revert_users[title].append(parts[0])		
				
def getLine(title, label):
    global lineLabels
    for line, ll in reversed(list(enumerate(lineLabels[title]))):
        if lineLabels[title][line] == label:
			return line 
		
def calc_m(title):
    global revert_pairs
    global user_edits
    edit_min_list = []
    score = 0
    for pair in list(set(revert_pairs[title])):
        parts = pair.split("~!~")
        u1 = parts[0]
        u2 = parts[1]
        if user_edits[u1]<user_edits[u2]:
            edit_min = user_edits[u1]
        else:
            edit_min = user_edits[u2]
        edit_min_list.append(edit_min)
        
    if len(edit_min_list) > 0:
        max_edit_min = max(edit_min_list)
    else:
        max_edit_min = 0
    for pair in list(set(mutual_revert_pairs[title])):
        parts = pair.split("~!~")
        u1 = parts[0]
        u2 = parts[1]
        if u1 not in mutual_revert_users[title]:
            mutual_revert_users[title].append(u1)
        if u2 not in mutual_revert_users[title]:
            mutual_revert_users[title].append(u2)
    score += sum(edit_min_list)
    score -= max_edit_min
    score *= len(mutual_revert_users)
    return score
