import json, sched, time
import inquirer
import uuid
from ServiceRegistryAms import PullPublish
with open("ams-config.json") as json_data_file:
    config = json.load(json_data_file)
with open("topics-subs-config.json") as json_data_file:
    topics_subs = json.load(json_data_file)
import sys



questions = [
  inquirer.List('tenant', message="Select Tenant",choices=['eosc', 'egi','grnet']),
  inquirer.List('environment', message="Select Federation Registry Instance",choices=['dev','demo']),
  inquirer.List('service_state', message="Select Deployment Status",choices=['deployed','error'])
]

answers = inquirer.prompt(questions)
#print(answers)
pull_push_instances = []
config['pub_topic'] = answers['environment'] + config['pub_topic']

for topic_subs in topics_subs[answers['tenant']]:
    topic = topic_subs['topic']
    for sub in topic_subs['subs']:
        config['pull_topic'] = answers['environment'] + topic
        config['pull_sub'] = answers['environment'] + sub
        agent_id = (sub.split('_')).pop()
        pull_push_instances.append({"ams":PullPublish(config),"agent_id":agent_id})
        



# config['pull_topic'] = sys.argv[1] + config['pull_topic_' + sys.argv[2]] +'_'+ sys.argv[5]
# config['pull_sub'] = sys.argv[1] + config['pull_sub_'+ sys.argv[2]] + sys.argv[5]  + '_'+sys.argv[3]
# config['pub_topic'] = sys.argv[1] + config['pub_topic']
# ams1 = []

# ams = PullPublish(config)
# ams1.append(ams)
# print('msg={0}'.format(config))

s = sched.scheduler(time.time, time.sleep)
def pull_push(sc):
    print("started ",time.time())
    for pull_push_instance in pull_push_instances:
        ams = pull_push_instance['ams']
        agent_id = pull_push_instance['agent_id']
        msgs = ams.pull(1)
        print(msgs)
        print('msg={0}, agent_id={1}'.format(msgs,agent_id))
        pub_msgs = []
        for msg in msgs:
            data={'id':msg['id'],'state':'deployed','agent_id':agent_id}
            if (msg['protocol'] == 'oidc' and not msg['client_id'] ):
                print('i understand that client id is null')
                x = uuid.uuid1()
                data['client_id'] = str(x)
            if answers['service_state'] == 'error':
                data.state = 'error'
                data.status_code = 500
                data.error_description = 'sample error description'
            pub_msgs.append({'attributes':{},'data':data})
        if pub_msgs:
            print(pub_msgs)
            
            ams.publish(pub_msgs)
    print("finished ", time.time())
    s.enter(10, 1,pull_push, (sc,))
s.enter(10, 1, pull_push, (s,))
s.run()
