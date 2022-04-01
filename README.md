# rciam-federation-registry-agent

**RCIAM Federation Registry Agent** main objective is to sync data between RCIAM Federation Registry and
Keycloak/MITREid Connect/SimpleSAMLphp.
This python library includes a module named `ServiceRegistryAms/` to pull and publish messages from ARGO Messaging
Service using the argo-ams-library, an API module named `MitreidConnect/` to communicate with the API of the MITREid, an
API module named `Keycloak/` to communicate with the API of the Keycloak.
The main standalone scripts that are used to deploy updates to the third party services are under `bin/`:

- `deployer_keycloak` for Keycloak
- `deployer_mitreid` for MITREid
- `deployer_ssp` for SimpleSAMLphp

## Installation

First install the packages from the requirements.txt file

```bash
pip install -r requirements.txt
```

Install rciam-federation-registry-agent

```bash
pip install rciam-federation-registry-agent
```

## Usage

### deployer_keycloak

deployer_keycloak requires the path of the config file as an argument

```bash
deployer_keycloak -c example_deployers.config.json
```

### deployer_mitreid

deployer_mitreid requires the path of the config file as an argument

```bash
deployer_mitreid -c example_deployers.config.json
```

### deployer_ssp

deployer_ssp requires the path of the config file as an argument

```bash
deployer_ssp -c example_deployers.config.json
```

## Configuration

Here is a description with the values that the MITREid and SSP conf file must include
example_deployers.config.json

```json
{
  "keycloak": {
    "ams": {
      "host": "example.host.com",
      "project": "ams-project-name-mitreid",
      "pull_topic": "ams-topic-mitreid",
      "pull_sub": "ams-sub-mitreid",
      "token": "ams-token-mitreid",
      "pub_topic": "ams-publish-topic-mitreid",
      "poll_interval": 1,
      "agent_id": "1"
    },
    "issuer": "https://example.com/oidc",
    "refresh_token": "refresh token",
    "client_id": "client ID",
    "client_secret": "client secret",
    "default_client_scopes": []
  },
  "mitreid": {
    "ams": {
      "host": "example.host.com",
      "project": "ams-project-name-mitreid",
      "pull_topic": "ams-topic-mitreid",
      "pull_sub": "ams-sub-mitreid",
      "token": "ams-token-mitreid",
      "pub_topic": "ams-publish-topic-mitreid",
      "poll_interval": 1,
      "agent_id": "1"
    },
    "issuer": "https://example.com/oidc",
    "refresh_token": "refresh token",
    "client_id": "client ID",
    "client_secret": "client secret"
  },
  "ssp": {
    "ams": {
      "host": "example.host.com",
      "project": "ams-project-name-ssp",
      "pull_topic": "ams-topic-ssp",
      "pull_sub": "ams-sub-ssp",
      "token": "ams-token-ssp",
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
  "log_conf": "conf/logger.conf"
}
```

As shown above there are 2 main groups MITREid and SSP, for each group there are unique AMS settings and service
specific configuration values. The only global value is the `log_conf` path if you want to use the same logging
configuration for both of the deployers. In case you need a different configuration for a deployer you can add log_conf
in the scope of "MITREid" or "SSP"

### ServiceRegistryAms

Use ServiceRegistryAms as a manager to pull and publish messages from AMS

```python
from ServiceRegistryAms.PullPublish import PullPublish

with open('config.json') as json_data_file:
  config = json.load(json_data_file)
  ams = PullPublish(config)

  message = ams.pull(1)
  ams.publish(args)
```

### Keycloak

Use Keycloak as an API manager to communicate with Keycloak

- First obtain an access token and create the Keycloak API Client (find clientCredentialsGrant under `Utils` directory)

```python
  access_token = clientCredentialsGrant(issuer_url, client_id, client_secret)
  keycloak_agent = KeycloakClientApi(issuer_url, access_token)
```

- Use the following functions to create, delete and update a service on clientCredentialsGrant

```python
  response = keycloak_agent.createClient(keycloak_msg)
  response = keycloak_agent.updateClientById(external_id, keycloak_msg)
  response = keycloak_agent.deleteClientById(external_id)
```

### MITREid Connect

Use MITREid Connect as an API manager to communicate with MITREid

- First obtain an access token and create the MITREid API Client (find refreshTokenGrant under `Utils` directory)

```python
  access_token = refreshTokenGrant(issuer_url, refresh_token, client_id, client_secret)
  mitreid_agent = mitreidClientApi(issuer_url, access_token)
```

- Use the following functions to create, delete and update a service on MITREid

```python
  response = mitreid_agent.createClient(mitreid_msg)
  response = mitreid_agent.updateClientById(external_id, mitreid_msg)
  response = mitreid_agent.deleteClientById(external_id)
```

## License

[Apache](http://www.apache.org/licenses/LICENSE-2.0)
