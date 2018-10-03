# mox_cpr_delta_mo

Mox agent for subscribing for updates from danish cpr registry and updating mo with results

This program should run once a day when updates from serviceplatformen are ready.

There is little to configure in the program other than the settings.py which are divided into four sections

* mox settings - the overall program options
* cpr_udtraek settings - settings related to the delta dump from cpr/serviceplatformen
* cpr_abonnement settings  - settings related to putting cpr numbers into delta-dump-subscription
* mora settings - settings necessary for querying MO for cpr numbers for subscription and updating mo with the results of the delta dump

``` python

    # mox settings
    #debug:10, #warn:30
    MOX_LOG_LEVEL = 10

    # cpr_udtraek settings
    ID_RSA_USER = "sftpcpr"  # the user account on the sftp-server
    SFTP_SERVER = "10.0.3.82"  # the host name of the sftp server
    SFTP_SERVER_PORT = 22  # port of the sftp server, usually 22 like ssh 
    SFTP_SERVER_INIT_PATH = "/home/sftpcpr/cpr-files" # The path where the delta dump files are located
    SFTP_DOWNLOAD_PATH = "/tmp/cpr-files/"  # the local temporary storage path
    ID_RSA_SP_PATH = "/home/me/.ssh/id_rsa"  # local location of the private certificate used to contact SFTP_SERVER
    ID_RSA_SP_PASSPHRASE = ""  # password, if any, for the private certificate

    # cpr_abonnement settings
    SP_ABO_SERVICE_ENDPOINT = "http://10.0.3.89/endpoint"  # Serviceplatformen endpoint
    SP_ABO_CERTIFICATE = "certificate.crt"  # certificate acc. to Serviceplatformen
    SP_ABO_SOAP_REQUEST_ENVELOPE = ""  # xml envelope - leave blank for bundled default
    SP_ABO_SYSTEM = "0fb8a2c0-c6e2-11e8-8724-234888bfbd3a"  # the uuid of the system
    SP_ABO_USER = "0fb8a2c0-c6e2-11e8-8724-234888bfbd3a"  # uuid of the user
    SP_ABO_SERVICE_AGREEMENT = "0fb8a2c0-c6e2-11e8-8724-234888bfbd3a"  # uuid of the service aggreement
    SP_ABO_SERVICE = "0fb8a2c0-c6e2-11e8-8724-234888bfbd3a"  # uuid of the service
    ADD_PNR_SUBSCRIPTION = ""  # name of action (for envelope)
    REMOVE_PNR_SUBSCRIPTION = ""  # name of action (for envelope)

    # mora settings 
    MORA_HTTP_BASE = "http://10.0.3.161:5000/service"  # MO http base - should end with '/service'
    MORA_ORG_UUID = "0fb8a2c0-c6e2-11e8-8724-234888bfbd3a"  # The MO organisation uuid

```

