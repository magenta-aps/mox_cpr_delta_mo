# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
You must set MORA_HTTP_BASE="http://<some-mo>/service"
and
MORA_TEST_PNR="<some pnr>"
in the environment

You Can set:
MORA_ORG_UUID

For these tests to run, as it must have a live mo with
a name it is allowed to change. Will try to change back.

"""
import os
import requests
import unittest
import mox_cpr_delta_mo.mo_interface as mo


def get_org_uuid():
    return requests.get(os.environ["MORA_HTTP_BASE"] + "/o/").json()[0]["uuid"]


class TestMoxCprDeltaMo(unittest.TestCase):

    def setUp(self):
        if not {"MORA_HTTP_BASE", "MORA_TEST_PNR"} <= os.environ.keys():
            self.fail(__doc__)
        mo.MORA_HTTP_BASE = os.environ["MORA_HTTP_BASE"]
        mo.MORA_ORG_UUID = os.environ.get("MORA_ORG_UUID", get_org_uuid())
        mo.MORA_DIVIDED_NAME = False

    def test_mora_get_all_cpr_numbers(self):
        "get both cpr numbers in the system"
        self.assertIn(
            os.environ["MORA_TEST_PNR"],
            mo.mora_get_all_cpr_numbers()
        )

    def test_mora_update_person_by_cprnumber(self):
        "rename Person to 'Mo Minsk Mohsen' and back again"
        old_data = mo.mora_eployees_from_cpr(os.environ["MORA_TEST_PNR"])
        mo.mora_update_person_by_cprnumber(
            fromdate="2018-09-10",
            pnr=os.environ["MORA_TEST_PNR"],
            changes={
                'fornavn': "Mo",
                'mellemnavn': "Minsk",
                'efternavn': "Mohsen"
            },
        )
        employees = mo.mora_eployees_from_cpr(os.environ["MORA_TEST_PNR"])
        self.assertEqual(["Mo Minsk Mohsen"], [e["name"] for e in employees])
        mo.mora_update_person_by_cprnumber(
            fromdate="2018-09-10",
            pnr=os.environ["MORA_TEST_PNR"],
            changes={
                'fornavn': old_data[0]["name"].rsplit(" ", maxsplit=1)[0],
                'mellemnavn': "",
                'efternavn': old_data[0]["name"].rsplit(" ", maxsplit=1)[1]
            }
        )
        employees = mo.mora_eployees_from_cpr(os.environ["MORA_TEST_PNR"])
        self.assertEqual([old_data[0]["name"]], [e["name"] for e in employees])

    def test_mora_update_person_by_cprnumber_divided_name(self):
        "rename Person to 'Mo Minsk Mohsen' and back again"
        mo.MORA_DIVIDED_NAME = True
        self.test_mora_update_person_by_cprnumber()
