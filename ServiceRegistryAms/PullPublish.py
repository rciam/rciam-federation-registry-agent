import json
from argparse import ArgumentParser
from argo_ams_library import ArgoMessagingService,AmsMessage, AmsException

class PullPublish():
    def __init__(self,config):
        self.pull_sub = config['pull_sub']
        self.pub_topic = config['pub_topic']
        self.pull_topic = config['pull_topic']
        self.ams = ArgoMessagingService(endpoint=config['host'], token=config['token'], project=config['project'])

    def pull(self,nummsgs):
        messages = []
        try:
            if not self.ams.has_sub(self.pull_sub):
                self.ams.create_sub(self.pull_sub,self.pull_topic)
        except AmsException as e:
            print(e)
            raise SystemExit(1)

        # try to pull number of messages from subscription. method will
        # return (ackIds, AmsMessage) tuples from which ackIds and messages
        # payload will be extracted.
        ackids = list()
        for id, msg in self.ams.pull_sub(self.pull_sub, nummsgs):
            data = msg.get_data()
            msgid = msg.get_msgid()
            attr = msg.get_attr()
            messages.append(json.loads(data.decode("utf-8")))
            #print('msgid={0}, data={1}, attr={2}'.format(msgid, data, attr))
            ackids.append(id)
        return messages, ackids

    def ack(self,ackids):
        # pass list of extracted ackIds to AMS Service so that
        # it can move the offset for the next subscription pull
        # (basically acknowledging pulled messages)
        if ackids:
            self.ams.ack_sub(self.pull_sub, ackids)

    def publish(self,messages):
        # messages = [{data:[{id:1},{state:'deployed'}],attributes=''}]
        try:
            if not self.ams.has_topic(self.pub_topic):
                self.ams.create_topic(self.pub_topic)
        except AmsException as e:
            print(e)
            raise SystemExit(1)

        # publish one message to given topic. message is constructed with
        # help of AmsMessage which accepts data and attributes keys.
        # data is Base64 encoded, attributes is dictionary of arbitrary
        # key/value pairs
        msg = AmsMessage()
        msglist = []
        for message in messages:
            msglist.append(msg(data=json.dumps(message['data']),attributes={}))


        try:
            ret = self.ams.publish(self.pub_topic, msglist)
            print(ret)
        except AmsException as e:
            print(e)
