import json, sched, time
from ServiceRegistryAms import PullPublish
with open("config.json") as json_data_file:
    config = json.load(json_data_file)
ams = PullPublish(config)


s = sched.scheduler(time.time, time.sleep)
def pull_push(sc):
    msgs = ams.pull(1)
    print('msg={0}'.format(msgs))
    pub_msgs = []
    for msg in msgs:
        pub_msgs.append({'attributes':{},'data':{'id':msg['id'],'state':'deployed'}})
    if pub_msgs:
        ams.publish(pub_msgs)
    s.enter(3, 1,pull_push, (sc,))
s.enter(3, 1, pull_push, (s,))
s.run()
