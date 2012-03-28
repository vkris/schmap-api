import sys
sys.path.append("..")
from schmap_api import client
# Username and password
obj = client(sys.argv[1],sys.argv[2])
li = []
#for line in open('handles_bb_latest.txt'):
#    li.append(line.strip())
li = [ 'gensent']
#li2 = ['gensent', 'WalkingDead_AMC']
#obj.analyze_list(li, "bb_mentioners","full_analysis")


#obj.analyze_account(li)
obj.catch_up()
