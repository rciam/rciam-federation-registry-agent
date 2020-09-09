Service Deployer is a python implementation for pulling and publishing messages from an ArgoMessagingService project using the argo-ams-libray python library.

### Dependencies
We need to install the argo-ams-libray
`pip install argo-ams-library`

### Running

1. Configure the config.json file
```
        {
          "host": "msg-devel.argo.grnet.gr",
          "project" : "rciam-service-registry",
          "pull_topic" : "tasks",
          "token" : "token",
          "pull_sub" : "service-deployer",
          "pub_topic": "updates"
        }
```
2. Initialize PullPublish
```
          from ServiceRegistryAms import PullPublish
            with open("config.json") as json_data_file:
          config = json.load(json_data_file)
          ams = PullPublish(config)
```

3. Pulling messages from ams
Using ams.pull() returns requested messages if available
```
          messages = ams.pull(number_of_desired_messages)
```

Messages have the following structure: (first message is a oidc service and the seccond a saml)
```
          messages = [
            {
              'id': 5,
              'protocol':'oidc',
              'client_id':'client5',
              'id_token_timeout_seconds': 600,
              'clear_access_tokens_on_refresh': True,
              'access_token_validity_seconds': 3600,
              'device_code_validity_seconds': 10000,
              'contacts': [
                {
                  'type':'admin',
                  'email': 'mygrail@gmail.com'
                },
                {
                  'type':'admin',
                  'email':'myfail@gmail.com'
                }],
              'deleted': False,
              'service_name':'Client Name',
              'scope': ['email', 'name'],
              'logo_uri': 'https://logo.jpg',
              'redirect_uris': ['https://redirecturi.com'],
              'refresh_token_validity_seconds': 28800,
              'code_challenge_method':'plain',
              'policy_uri': 'https://policy_uri.com',
              'allow_introspection': True,
              'service_description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean in ex in tellus congue co: .',
              'integration_environment':'development',
              'reuse_refresh_tokens': True,
              'grant_types': ['implicit'],
              'client_secret':'secret'  
            }
            ,
            {
              id: 7,
              service_name: 'Saml Service',
              service_description: 'This is a saml service',
              logo_uri: 'https://cdn.auth0.com/blog/duo-saml-exploit/saml.png',
              policy_uri: 'https://policy_url.com',
              integration_environment: 'production',
              protocol: 'saml',
              metadata_url: 'https://metadata_uri.com',
              entity_id: 'entiry_id_uri',
              deleted: false,
              contacts: [{
                  'type':'admin',
                  'email': 'mygrail@gmail.com'
                },
                {
                  'type':'admin',
                  'email':'myfail@gmail.com'
                }
              ]
            }

          ]
```


4. Publishing Deployment Updates

To publish the deployment updates we use the ams.publish(args) function. The argument must follow the folliwing syntax.
**Note: state can be "deployed" or "error" **

```
        args = [
          {
            'attributes':{},
            'data': {
              'id':1,
              'state':'deployed'
            }
          },
          {
            'attributes':{},
            'data': {
              'id':2,
              'state':'deployed'
            }
          }
          ,{
            'attributes':{},
            'data': {
              'id':3,
              'state':'error'
            }
          }
        ]
```
