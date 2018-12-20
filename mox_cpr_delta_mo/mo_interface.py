# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
import logging
from .settings import (
    MORA_HTTP_BASE,
    MORA_ORG_UUID,
    MORA_CA_BUNDLE,
    SAML_API_TOKEN,
)

logger = logging.getLogger("mox_cpr_delta_mo")

mora_headers = {
    "SESSION": SAML_API_TOKEN
}


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
        r = requests.get(
            url,
            headers=mora_headers,
            params=params,
            verify=MORA_CA_BUNDLE
        )
        r.status_code == requests.codes.ok or r.raise_for_status()
        return r
    except Exception:
        logger.exception(url)


def mora_post(url, **params):
    url = mora_url(url)
    try:
        r = requests.post(
            url,
            headers=mora_headers,
            verify=MORA_CA_BUNDLE,
            **params
        )
        r.status_code == requests.codes.ok or r.raise_for_status()
        return r
    except Exception:
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
    # skip if no changes
    relevant_changes = {
        "validity": {"from": fromdate},
    }
    if not {"fornavn", "mellemnavn", "efternavn"} <= set(changes.keys()):
        return False
    elif changes["mellemnavn"]:
        relevant_changes["name"] = (
            "%(fornavn)s %(mellemnavn)s %(efternavn)s" % changes
        )
    else:
        relevant_changes["name"] = "%(fornavn)s %(efternavn)s" % changes

    list_of_edits = []

    for e in mora_eployees_from_cpr(pnr):
        list_of_edits.append({
            "type": "employee",
            "uuid": e["uuid"],
            "data": relevant_changes,
        })

    mora_post(
        url="{BASE}/details/edit",
        json=list_of_edits,
    )
