import json, sched, time
import inquirer
import uuid
from ServiceRegistryAms.PullPublish import PullPublish
with open("topics-subs-config.json") as json_data_file:
    topics_subs = json.load(json_data_file)
with open("config.json") as json_data_file:
    agent_config = json.load(json_data_file)
with open("ams-config.json") as json_data_file:
    ams_config = json.load(json_data_file)
import requests
import base64
print(agent_config)
questions = [
  inquirer.List('tenant', message="Select Tenant",choices=agent_config['federation_tenants']),
  inquirer.List('environment', message="Select Federation Registry Instance",choices=agent_config['federation_devel_instances']+agent_config['federation_production_instances']),
  inquirer.List('service_state', message="Select Deployment Status",choices=['deployed','error'])
]

answers = inquirer.prompt(questions)
pull_push_instances = []

if answers['environment'] in agent_config['federation_production_instances']:
    config = ams_config['production']
else: 
    config = ams_config['devel']

config['pub_topic'] = answers['environment'] + config['pub_topic']
for topic_subs in topics_subs[answers['tenant']]:
    topic = topic_subs['topic']
    integration_environment = topic_subs['integration_environment']
    protocol = topic_subs['protocol']
    for  sub in topic_subs['subs']:
        config['pull_topic'] = answers['environment'] + topic
        config['pull_sub'] = answers['environment'] + sub
        deployer_name = ""
        if len(topic_subs['subs'])>1:
            deployer_name = (sub.split('_')).pop()
        pull_push_instances.append({"ams":PullPublish(config),"deployer_name":deployer_name,"integration_environment":integration_environment,"protocol":protocol})


s = sched.scheduler(time.time, time.sleep)
def pull_push(sc):
    print("started ",time.time())
    for pull_push_instance in pull_push_instances:
        
        ams = pull_push_instance['ams']
        
        deployer_name = pull_push_instance['deployer_name']
        
        msgs = ams.pull(1)
        print(msgs)
        print('msg={0}, deployer_name={1}'.format(msgs,deployer_name))
        pub_msgs = []
        for msg in msgs:
            data={'id':msg['id'],'deployer_name':deployer_name,'state':'deployed'}
            if answers['service_state']=='deployed':
                data['external_id'] = str(uuid.uuid1())
                print(data)
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
        headers={'x-api-key': agent_config['federation_key'],
            "content-type": "application/json"}
        )
    response =  json.loads(r.content)
    if(len(response['services']) >= 1):
        setStateArray = []
        amsResponses = []
        for service in response['services']:
            service = service['json']
            if(service['tenant']== answers['tenant']):
                setStateArray.append({'id':service['id'],'state':'waiting-deployment','protocol':service['protocol'],'tenant':service['tenant'],'integration_environment':service['integration_environment']})
                for mock_deployer in pull_push_instances:
                    if mock_deployer['protocol'] == service['protocol'] and mock_deployer['integration_environment'] == service['integration_environment']:
                        print(service)
                        external_id = uuid.uuid1()
                        external_id = str(external_id)
                        print(json.dumps({'id':service['id'],'state':'deployed' if answers['service_state']=='deployed' else 'error','status_code':200 if answers['service_state']=='deployed' else 500,'error_description':None if answers['service_state']=='deployed' else 'Mock Error','deployer_name':mock_deployer['deployer_name'],'external_id':external_id}).encode('utf-8'))
                        print({'message':{'attributes':{'key':'value'},'data':base64.b64encode(json.dumps({'id':service['id'],'state':'deployed' if answers['service_state']=='deployed' else 'error','status_code':200 if answers['service_state']=='deployed' else 500,'error_description':None if answers['service_state']=='deployed' else 'Mock Error','deployer_name':mock_deployer['deployer_name'],'external_id':external_id}).encode('utf-8')).decode('utf-8'),'messageId':"12312323"},"subscription":"projects/myproject/subscriptions/mysubscription"})
                        amsResponses.append({'message':{'attributes':{'key':'value'},'data':base64.b64encode(json.dumps({'id':service['id'],'state':'deployed' if answers['service_state']=='deployed' else 'error','status_code':200 if answers['service_state']=='deployed' else 500,'error_description':None if answers['service_state']=='deployed' else 'Mock Error','deployer_name':mock_deployer['deployer_name'],'external_id':external_id}).encode('utf-8')).decode('utf-8'),'messageId':"12312323"},"subscription":"projects/myproject/subscriptions/mysubscription"})
        if(len(setStateArray)>=1):
            print(setStateArray)
            requests.put('http://127.0.0.1:5000/agent/set_services_state', json=setStateArray,headers={'x-api-key': agent_config['federation_key']})
            requests.post('http://127.0.0.1:5000/ams/ingest',json={'messages':amsResponses},headers={'Authorization':agent_config['ams_auth_key'],'content-type': 'application/json'})
    s.enter(10,1,localhost_mock,(sc,))

if(answers['environment']!='local'):
    s.enter(1, 1, pull_push, (s,))
else:
    s.enter(1,1,localhost_mock,(s,))
s.run()
