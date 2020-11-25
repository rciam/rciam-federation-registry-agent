# rciam-federation-registry-agent

***Rciam federation registry agent*** main objective is to sync data between rciam federation registry with satosa and mitreId respectively.
This python library includes a module named `ServiceRegistryAms/` to pull and publish messages from Argo messaging service using the argo-ams-library,
an API module named `MitreidConnect/` to communicate with the api of the mitreId.
The main standalone scripts that are used to deploy updates to the third party services are under `bin/`:

* `deployer_ssp` for simple saml php
* `deployer_mitreid` for mitreid

## Installation

First install the packages from the requirements.txt file
```bash
pip install -r requirements.txt
```

Install rciam-federation-registy-agent
```bash
pip install rciam-federation-registry-agent
```

## Usage

### deployer_ssp
deployer_ssp requires the path of the ssp config file as an argument
```bash
$ deployer_ssp -c example_ssp.config.json
```

Here is a description with the values that the ssp conf file must include
example_ssp.config.json
```javascript
{
  "host": "example.host.com",
  "project" : "ams-project-name",
  "pull_topic" : "ams-topic",
  "pull_sub" : "ams-sub",
  "token" : "ams-token",
  "pub_topic": "ams-publish-topic",
  "metadata": "/path/to/ssp/metadata/file.php",  // deployer_ssp only
  "metadata_key": "ssp-metadata-key",  // deployer_ssp only
  "ssp_url": "http://localhost/proxy/module.php/cron/cron.php",  // deployer_ssp only
  "log_conf": "conf/logger.conf",
  "time_interval": 1  // Poll ams time interval
}
```

### deployer_mitreid
deployer_mitreid requires the path of the ssp config file as an argument
```bash
$ deployer_mitreid -c example_mitre.config.json
```

Here is a description with the values that the mitreid conf file must include
example_ssp.config.json
```javascript
{
  "host": "example.host.com",
  "project" : "ams-project-name",
  "pull_topic" : "ams-topic",
  "pull_sub" : "ams-sub",
  "token" : "ams-token",
  "pub_topic": "ams-publish-topic",
  "agent_id": "agent_num",
  "mitreid_url": "https://example.com/oidc" ,
  "mitreid_refresh_token": "oauth.mitreid.refresh.token",
  "mitreid_client_id": "mitre.id.client.id",
  "mitreid_client_secret": "mitreid.client.secret",
  "log_conf": "conf/logger.conf",
  "time_interval": 1  // Poll ams time interval
}
```

### ServiceRegistryAms
Use ServiceRegistryAms as an manager to pull and publish messages from ams
```python
from ServiceRegistryAms.PullPublish import PullPublish

with open('config.json') as json_data_file:
  config = json.load(json_data_file)
  ams = PullPublish(config)

  message = ams.pull(1)
  ams.publish(args)
```


### MitreidConnect
Use MitreidConnect as an api manager to communicate with mitreId
- First obtain an access token and create the mitreId API client (find refreshTokenGrant under `Utils` directory)
```python
  access_token = refreshTokenGrant(issuer_url, refresh_token, client_id, client_secret)
  mitreid_agent = mitreidClientApi(issuer_url, access_token)
```

- Use the following functions to create, delete and update a service on mitreId
```
  response = mitreid_agent.createClient(mitreid_msg)
  response = mitreid_agent.updateClientById(external_id, mitreid_msg)
  response = mitreid_agent.deleteClientById(external_id)
```

## License

[Apache](http://www.apache.org/licenses/LICENSE-2.0)

