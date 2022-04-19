import json, sched, time
import inquirer
import uuid
from ServiceRegistryAms.PullPublish import PullPublish
with open("ams-config.json") as json_data_file:
    config = json.load(json_data_file)
with open("topics-subs-config.json") as json_data_file:
    topics_subs = json.load(json_data_file)
import sys
import requests
import base64




# ample_string = "GeeksForGeeks is the best"
# sample_string_bytes = sample_string.encode("ascii")

# base64_bytes = base64.b64encode(sample_string_bytes)
# base64_string = base64_bytes.decode("ascii")

questions = [
  inquirer.List('tenant', message="Select Tenant",choices=['eosc', 'egi','grnet']),
  inquirer.List('environment', message="Select Federation Registry Instance",choices=['dev','demo','localhost']),
  inquirer.List('service_state', message="Select Deployment Status",choices=['deployed','error'])
]

answers = inquirer.prompt(questions)
pull_push_instances = []

config['pub_topic'] = answers['environment'] + config['pub_topic']
for topic_subs in topics_subs[answers['tenant']]:
    topic = topic_subs['topic']
    integration_environment = topic_subs['integration_environment']
    protocol = topic_subs['protocol']
    for sub in topic_subs['subs']:
        config['pull_topic'] = answers['environment'] + topic
        config['pull_sub'] = answers['environment'] + sub
        agent_id = (sub.split('_')).pop()
        pull_push_instances.append({"ams":PullPublish(config),"agent_id":agent_id,"integration_environment":integration_environment,"protocol":protocol})
            

# print(pull_push_instances)

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
            data={'id':msg['id'],'agent_id':agent_id,'state':'deployed'}
            if (msg['protocol'] == 'oidc' and not msg['client_id'] ):
                print('i understand that client id is null')
                x = uuid.uuid1()
                data["client_id"] = str(x)
            if answers['service_state'] == 'error':
                data["state"] = 'error'
                data["status_code"] = 500
                data["error_description"] = 'Mock Error'
            pub_msgs.append({'attributes':{},'data':data})
        if pub_msgs:
            print(pub_msgs)
            
            ams.publish(pub_msgs)
    print("finished ", time.time())
    s.enter(10, 1,pull_push, (sc,))

def localhost_mock(sc):
    print("Getting services")
    r = requests.get('http://127.0.0.1:5000/agent/get_new_configurations',
        headers={'x-api-key': 'banana',
            "content-type": "application/json"}
        )
    response =  json.loads(r.content)
    if(len(response['services']) >= 1):
        setStateArray = []
        amsResponses = []
        for service in response['services']:
            service = service['json']
            # print(service['tenant'])
            # print(service)
            if(service['tenant']== answers['tenant']):
                setStateArray.append({'id':service['id'],'state':'waiting-deployment','protocol':service['protocol'],'tenant':service['tenant'],'integration_environment':service['integration_environment']})
                for mock_deployer in pull_push_instances:
                    if mock_deployer['protocol'] == service['protocol'] and mock_deployer['integration_environment'] == service['integration_environment']:
                        print(json.dumps({'id':service['id'],'state':'deployed' if answers['service_state']=='deployed' else 'error','status_code':200 if answers['service_state']=='deployed' else 500,'error_description':None if answers['service_state']=='deployed' else 'Mock Error','agent_id':mock_deployer['agent_id']}).encode('utf-8'))
                        amsResponses.append({'message':{'attributes':{'key':'value'},'data':base64.b64encode(json.dumps({'id':service['id'],'state':'deployed' if answers['service_state']=='deployed' else 'error','status_code':200 if answers['service_state']=='deployed' else 500,'error_description':None if answers['service_state']=='deployed' else 'Mock Error','agent_id':mock_deployer['agent_id']}).encode('utf-8')).decode('utf-8'),'messageId':"12312323"},"subscription":"projects/myproject/subscriptions/mysubscription"})
        if(len(setStateArray)>=1):
            print(setStateArray)
            requests.put('http://127.0.0.1:5000/agent/set_services_state', json=setStateArray,headers={'x-api-key': 'banana'})
            requests.post('http://127.0.0.1:5000/ams/ingest',json={'messages':amsResponses},headers={'Authorization':'banana','content-type': 'application/json'})
    s.enter(10,1,localhost_mock,(sc,))

if(answers['environment']!='localhost'):
    s.enter(1, 1, pull_push, (s,))
else:
    s.enter(1,1,localhost_mock,(s,))
s.run()
