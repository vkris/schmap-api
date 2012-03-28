import json

east_states = ["Alabama","Connecticut","Delaware","Florida","Georgia","Illinois","Indiana","Kentucky","Maine","Maryland","Massachusetts","Michigan","Mississippi","New Hampshire","New Jersey","New York State","North Carolina","Ohio","Pennsylvania","Rhode Island","South Carolina","Tennessee","Vermont","Virginia","Washington","DC","West Virginia","Wisconsin"]
east_of_missisipi = [ x.lower() for x in east_states]
source_id = {"WEST":-1005142, "EAST":-1005141}
_SIZE_=5000
final = {}
final['rules'] = []
final2={}
final2['rules'] = []
for account in open("/tmp/hawaii_followers_data.json"):
    data = json.loads(account)
    profiled_users = data['profiled_users']
    dataset_name = data['dataset_name']

    for user in profiled_users:
        xid =  user['xid']
        city_or_town = user['city_or_town']
        twitter_loc= user['twitter_loc']
        us_state = user['us_state']
        screen_name = user['screen_name']
        try:
            if ( len(us_state) >= 1):
                if us_state.lower() in east_of_missisipi:
                    #print dataset_name +"\t" + screen_name + "\t" + str(xid) + "\t"+ us_state +"\tEAST" +"\t"+twitter_loc
                    #print str(xid)+","+str(source_id['EAST'])
                    #print "from:"+screen_name
                    rule_hash = {}
                    rule_hash['value'] = "from:"+screen_name
                    rule_hash['tag'] = "hta_east_follower"
                    if (len(final['rules']) < _SIZE_):
                        final['rules'].append(rule_hash)
                    else:
                        final2['rules'].append(rule_hash)
                else:
                    #print str(xid)+","+str(source_id['WEST'])
                    #print "from:"+ screen_name
                    rule_hash = {}
                    rule_hash['value'] = "from:"+screen_name
                    rule_hash['tag'] = "hta_west_follower"
                    if (len(final['rules']) < _SIZE_):
                        final['rules'].append(rule_hash)
                    else:
                        final2['rules'].append(rule_hash)
                    #print dataset_name +"\t" + screen_name + "\t" + str(xid) + "\t"+ us_state +"\tWEST"+ "\t"+twitter_loc
            else:
                pass
                #print dataset_name +"\t" + screen_name + "\t" + str(xid) + "\t NOT_FOUND\t NIL"
        except TypeError,e:
            pass
            #print user
        except UnicodeEncodeError,ex:
            print user

#print json.dumps(final)
print json.dumps(final2)

