import sys
sys.path.append("..")
from schmap_api.client import SchmapAPIClient
obj = SchmapAPIClient(sys.argv[1],sys.argv[2])
li = [ 'gensent', 'WalkingDead_AMC']
#li2 = ['gensent', 'WalkingDead_AMC']
#obj.analyze_list(li, "test_list")

#obj.analyze_account(li)
obj.catch_up()
