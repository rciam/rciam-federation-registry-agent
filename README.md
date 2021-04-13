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
$ deployer_ssp -c example_deployers.config.json
```

### deployer_mitreid
deployer_mitreid requires the path of the ssp config file as an argument
```bash
$ deployer_mitreid -c example_mitre.config.json
```

## Configuration
Here is a description with the values that the mitreid and ssp conf file must include
example_deployers.config.json
```javascript
{
  "ssp": {
    "ams": {
      "host": "example.host.com",
      "project" : "ams-project-name-ssp",
      "pull_topic" : "ams-topic-ssp",
      "pull_sub" : "ams-sub-ssp",
      "token" : "ams-token-ssp",
      "pub_topic": "ams-publish-topic-ssp",
      "poll_interval": 1,
      "agent_id": "1"
    },
    "metadata_conf_file": "/path/to/ssp/metadata/file.php",
    "cron_secret": "SSP cron secret",
    "cron_url": "http://localhost/proxy/module.php/cron/cron.php",
    "cron_tag": "hourly",
    "request_timeout": 100
  },
  "mitreid": {
    "ams": {
      "host": "example.host.com",
      "project" : "ams-project-name-mitreid",
      "pull_topic" : "ams-topic-mitreid",
      "pull_sub" : "ams-sub-mitreid",
      "token" : "ams-token-mitreid",
      "pub_topic": "ams-publish-topic-mitreid",
      "poll_interval": 1,
      "agent_id": "1"
    },
    "issuer": "https://example.com/oidc" ,
    "refresh_token": "refresh token",
    "client_id": "client ID",
    "client_secret": "client secret"
  },
  "log_conf": "conf/logger.conf"
}
```

As shown above there are 2 main groups mitreid and ssp, for each group there are unique ams settings and service specific configuration values. The only global value is the `log_conf` path if you want to use the same logging configuration for both of the deployers. In case you need a different configuration for a deployer you can add log_conf in the scope of "mitreid" or "ssp"

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

