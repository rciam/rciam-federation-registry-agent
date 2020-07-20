import json, sched, time
from ServiceRegistryAms import PullPublish
with open("config.json") as json_data_file:
    config = json.load(json_data_file)
ams = PullPublish(config)
#ams.test([{'attributes':{},'data':{'id':1,'state':'deployed'}},{'attributes':{},'data':{'id':2,'state':'deployed'}},{'attributes':{},'data':{'id':3,'state':'deployed'}}])

s = sched.scheduler(time.time, time.sleep)
def pull_push(sc):
    msgs = ams.pull(1)
    pub_msgs = []
    for msg in msgs:
        pub_msgs.append({'attributes':{},'data':{'id':msg['id'],'state':'deployed'}})
    if pub_msgs:
        ams.publish(pub_msgs)
    s.enter(3, 1,pull_push, (sc,))
s.enter(3, 1, pull_push, (s,))
s.run()

# Create an object of Birds class & call a method of it
