import sys
sys.path.append("..")
from schmap_api import client
# Username and password, client ID
obj = client(sys.argv[1],sys.argv[2], sys.argv[3])

'''
#li = ['gensent','WalkingDead_AMC','BroadwalkEmpHBO']
li=[]
for line in open('/Users/vivekris/Desktop/NHL/Network/all.txt'):
    li.append(line.strip())
obj.analyze_list(li, "nhl_network_all","full_analysis")

'''
li= []
#for line in open('/tmp/followers.dat'):
    #li.append(line.strip())
#obj.analyze_list(li, "toyota-followers","full_analysis")
#obj.analyze_list(li, "toyota-followers","profiled_dataset")

#obj.analyze_(li)
obj.analysis_type="profiled_dataset"
obj.catch_up()
