# mox_cpr_delta_mo

Mox agent for subscribing for updates from danish cpr registry and updating mo with results

This program should run once a day when updates from serviceplatformen are ready.

There is little to configure in the program other than the settings.ini which are divided into four sections

* mox settings - the overall program options
* cpr_udtraek settings - settings related to the delta dump from cpr/serviceplatformen
* cpr_abonnement settings  - settings related to putting cpr numbers into delta-dump-subscription
* mora settings - settings necessary for querying MO for cpr numbers for subscription and updating mo with the results of the delta dump

Here is a settings.ini file with sample values/explanations

You can specify the location of this file through the environment variable **MOX_CPR_DELTA_MO_CONFIG**

``` ini

    [settings]
    #mox settings
    #debug:10, #warn:30
    MOX_LOG_LEVEL = 10
    MOX_JSON_CACHE = var/myfile.json

    # cpr_udtraek settings
    ID_RSA_USER = the user account on the sftp-server
    SFTP_SERVER = the host name of the sftp server
    SFTP_SERVER_PORT = port of the sftp server, usually 22 like ssh 
    SFTP_SERVER_INIT_PATH = The path where the delta dump files are located
    SFTP_DOWNLOAD_PATH = the local temporary storage path
    ID_RSA_SP_PATH = local location of the private certificate used to contact SFTP_SERVER
    ID_RSA_SP_PASSPHRASE = password, if any, for the private certificate

    # cpr_abonnement settings
    SP_ABO_SERVICE_ENDPOINT =  Serviceplatformen endpoint
    SP_ABO_CERTIFICATE = certificate acc. to Serviceplatformen
    SP_ABO_SOAP_REQUEST_ENVELOPE = leave blank for bundled default
    SP_ABO_SYSTEM =  the uuid of the system
    SP_ABO_USER =  uuid of the user
    SP_ABO_SERVICE_AGREEMENT = uuid of the service aggreement
    SP_ABO_SERVICE = uuid of the service
    ADD_PNR_SUBSCRIPTION = AddPNRSubscription
    REMOVE_PNR_SUBSCRIPTION = RemovePNRSubscription
    GET_PNR_SUBSCRIPTIONS = GetAllFilters


    # mora settings 
    MORA_HTTP_BASE = MO http base - should end with '/service'
    MORA_ORG_UUID = The MO organisation uuid
    MORA_CA_BUNDLE = path to ca_bundle or False to opt out of ca verification

```
Running the program in a typical setup with a cron file wwhere You want to 
process changes since last time and set any new employes into subscription would be

``` bash

python -m mox_cpr_delta_mo --update-cpr-subscriptions

```

Program has help

``` bash

python -m mox_cpr_delta_mo --help

usage: __main__.py [-h] [--update-cpr-subscriptions] [--cpr-delta-update-mo]
                   [--cpr-delta-since CPR_DELTA_SINCE]

optional arguments:
  -h, --help            show this help message and exit
  --update-cpr-subscriptions
                        find subscriptions for all cpr-numbers, update
                        subscriptions for the ones that are missing in
                        subscrition, remove the ones missing in mora
  --cpr-delta-update-mo
                        retrieve data from cpr-kontoret and update mora
  --cpr-delta-since CPR_DELTA_SINCE
                        retrieve data from cpr-kontoret since this date given
                        as YYmmdd (181018)

```


Running the tests.

unittests:

```
python -m unittest discover tests 
```

integration tests - With suitable testdata in Mora tests can be run like

``` bash
python -m unittest discover tests -p 'integration_test*'
```

