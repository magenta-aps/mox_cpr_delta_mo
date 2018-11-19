import os
import pathlib
import configparser

inipaths = [p for p in [
        pathlib.Path(os.environ.get("MOX_CPR_DELTA_MO_CONFIG", "")),
        pathlib.Path("") / "settings.ini",
        pathlib.Path(__file__).absolute() / "settings.ini",
    ] if p.is_file()
]

if not len(inipaths):
    raise FileNotFoundError
else:
    inifile = inipaths[0]

config = configparser.ConfigParser(defaults={
    "MOX_LOG_LEVEL": "10",
    "MOX_JSON_CACHE": "var/myfile.json",
    "ADD_PNR_SUBSCRIPTION": "AddPNRSubscription",
    "REMOVE_PNR_SUBSCRIPTION": "RemovePNRSubscription",
    "GET_PNR_SUBSCRIPTIONS": "GetAllFilters",
})

config.read(str(inifile))
settings = config["settings"]


MOX_LOG_LEVEL = int(settings["MOX_LOG_LEVEL"])
MOX_JSON_CACHE = settings["MOX_JSON_CACHE"]
ID_RSA_USER = settings["ID_RSA_USER"]
SFTP_SERVER = settings["SFTP_SERVER"]
SFTP_SERVER_PORT = int(settings["SFTP_SERVER_PORT"])
SFTP_SERVER_INIT_PATH = settings["SFTP_SERVER_INIT_PATH"]
SFTP_DOWNLOAD_PATH = settings["SFTP_DOWNLOAD_PATH"]
ID_RSA_SP_PATH = settings["ID_RSA_SP_PATH"]
ID_RSA_SP_PASSPHRASE = settings["ID_RSA_SP_PASSPHRASE"]
SP_ABO_SERVICE_ENDPOINT = settings["SP_ABO_SERVICE_ENDPOINT"]
SP_ABO_CERTIFICATE = settings["SP_ABO_CERTIFICATE"]
SP_ABO_SOAP_REQUEST_ENVELOPE = settings["SP_ABO_SOAP_REQUEST_ENVELOPE"]
SP_ABO_SYSTEM = settings["SP_ABO_SYSTEM"]
SP_ABO_USER = settings["SP_ABO_USER"]
SP_ABO_SERVICE_AGREEMENT = settings["SP_ABO_SERVICE_AGREEMENT"]
SP_ABO_SERVICE = settings["SP_ABO_SERVICE"]
ADD_PNR_SUBSCRIPTION = settings["ADD_PNR_SUBSCRIPTION"]
REMOVE_PNR_SUBSCRIPTION = settings["REMOVE_PNR_SUBSCRIPTION"]
GET_PNR_SUBSCRIPTIONS = settings["GET_PNR_SUBSCRIPTIONS"]
MORA_HTTP_BASE = settings["MORA_HTTP_BASE"]
MORA_ORG_UUID = settings["MORA_ORG_UUID"]
MORA_CA_BUNDLE = bool(settings["MORA_CA_BUNDLE"])
