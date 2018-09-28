# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import xmltodict
import settings
import cpr_udtraek

from cpr_abonnement.cpr_abonnement import (
    pnr_subscription,
)


abo_dependencies = {
    'service_endpoint': settings.SP_ABO_SERVICE_ENDPOINT,
    'certificate': settings.SP_ABO_CERTIFICATE,
    'soap_request_envelope': settings.SP_ABO_SOAP_REQUEST_ENVELOPE,
    'system': settings.SP_ABO_SYSTEM,
    'user': settings.SP_ABO_USER,
    'service_agreement': settings.SP_ABO_SERVICE_AGREEMENT,
    'service': settings.SP_ABO_SERVICE
}


def get_cpr_delta_udtraek(sincedate):
    """ returns a dict like
    {
        "181229": {  # a date >= sincedate
            "1231621234": { # a cpr number
                 "key-0": "value-0",
                 # keys and values for example
                 "fornavn": "Jørgen",
                 "efternavn": "Jyde",
                 ...
                 "key-n": "value-n",
           },
        },
    }
    """
    return cpr_udtraek.delta(sincedate)


def add_cpr_subscription(pnr):
    result = change_cpr_subscription(
        pnr,
        settings.ADD_PNR_SUBSCRIPTION
    )
    return result == "ADDED"


def remove_cpr_subscription(pnr):
    result = change_cpr_subscription(
        pnr,
        settings.REMOVE_PNR_SUBSCRIPTION
    )
    return result == "REMOVED"


def get_all_subscribed_cprs():
    return []


def change_cpr_subscription(cpr, operation):
    cpr_abonnement_response_envelope = pnr_subscription(
         dependencies_dict=abo_dependencies,
         pnr=pnr,
         operation=operation
    )

    reply = xmltodict.parse(cpr_abonnement_response_envelope)

    operation_response_key = 'ns3:{}Response'.format(operation)

    return reply[
        'soap:Envelope'
    ][
        'soap:Body'
    ][  
        operation_response_key
    ][
        'ns3:Result'
    ]
    

