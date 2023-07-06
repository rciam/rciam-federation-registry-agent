
# README
Service Mock Deployer is a python implementation to mock the deployment of service requests submitted to Federation Registry. It can pull and publish messages from an ArgoMessagingService project using the argo-ams-library python library or connect directly to a local instance of Federation Registry.  
## Dependencies
Install the packages from the requirements.txt file
```shell
pip  install  -r  requirements.txt
```
## Running
### Setup Configuration Files
1. **config.json**: Configuration of the Federation Registry Instance. 
2. **ams_config.json**: Configuration of the AMS Instance.
3. **topics-subs-config.json**: Configuration for Topics and Subscriptions.
### Run Process
 ```
python3 run.py
```  
## Messages
### Service Request Messages
A Service Request Message has the following structure: (first message is a OIDC service and the second a SAML)
```python
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
			'email': 'mygrail@gmail.com'},
		{
			'type':'admin',
			'email':'myfail@gmail.com'
		}
	],
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
},
{
	'id': 7,
	'service_name': 'SAML Service',
	'service_description': 'This is a SAML service',
	'logo_uri': 'https://cdn.auth0.com/blog/duo-saml-exploit/saml.png',
	'policy_uri': 'https://policy_url.com',
	'integration_environment': 'production',
	'protocol': 'saml',
	'metadata_url': 'https://metadata_uri.com'
	'entity_id': 'entiry_id_uri',
	'deleted': false,
	'contacts': [{
			'type':'admin',
			'email': 'mygrail@gmail.com'
		},
		{
			'type':'admin',
			'email':'myfail@gmail.com'
		}
	]
}
```
### Deployment Response Messages

Here are 2 examples of messages. In the first one we have a successful deployment of a service request that also returns an external_id value and a client_id value that will overwrite the ones held in Federation Registry.
The second one is an unsuccessful deployment of a request. The agent_id property indicates that this is a response of one out of multiple deployment agents that has received  this request.
```python

	{
		'attributes':{},
		'data': {
			'id':1,
			'state':'deployed',
			'status_code':200,
			'external_id':'91231',
			'client_id': 'client_id123'
		}
	}
	
	{
		'attributes':{},
		'data': {
			'id':2,
			'state':'error',
			'error_description':'reason of the error'
			'status_code':500,
			'agent_id':2,
		}
	}
```
