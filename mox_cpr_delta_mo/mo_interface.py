# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
import logging
from settings import MORA_HTTP_BASE, MORA_ORG_UUID, MORA_CA_BUNDLE

logger = logging.getLogger("mox_cpr_delta_mo")


def mora_url(url):
    """format url like
    {BASE}/o/{ORG}/e
    params like
    {'limit':0, 'query':''}
    """
    url = url.format(BASE=MORA_HTTP_BASE, ORG=MORA_ORG_UUID)
    logger.debug(url)
    return url


def mora_get(url, **params):
    url = mora_url(url)
    try:
        return requests.get(url, params=params, verify=MORA_CA_BUNDLE)
    except Exception as e:
        logger.exception(url)


def mora_post(url, **params):
    url = mora_url(url)
    try:
        return requests.post(url, params=params, verify=MORA_CA_BUNDLE)
    except Exception as e:
        logger.exception(url)


def mora_get_all_cpr_numbers():
    alluuids = [
        e["uuid"] for e in mora_get("{BASE}/o/{ORG}/e").json()["items"]
    ]
    return [
        mora_get("{BASE}/e/" + uuid + "/").json().get("cpr_no")
        for uuid in alluuids
    ]


def mora_eployees_from_cpr(pnr):
    uuids_from_cpr = [
        e["uuid"]
        for e in mora_get("{BASE}/o/{ORG}/e", query=pnr).json()["items"]
    ]
    return [
        e
        for e in [
            mora_get("{BASE}/e/" + uuid + "/").json()
            for uuid in uuids_from_cpr
        ]
        if e.get("cpr_no") == pnr
    ]


def mora_update_person_by_cprnumber(fromdate, pnr, changes):
    relevant_changes = {}
    # skip if no changes
    if not {"fornavn", "mellemnavn", "efternavn"} <= set(changes.keys()):
        return False
    elif changes["mellemnavn"]:
        relevant_changes["navn"] = (
            "%(fornavn)s %(mellemnavn)s %(efternavn)s" % changes
        )
    else:
        relevant_changes["navn"] = "%(fornavn)s %(efternavn)s" % changes

    for e in mora_eployees_from_cpr(pnr):
        mora_post(
            # lets say type defaults to 'employee'
            url="{BASE}/e/" + e["uuid"] + "/edit",
            data=relevant_changes,
            validity={"from": fromdate},
        )
