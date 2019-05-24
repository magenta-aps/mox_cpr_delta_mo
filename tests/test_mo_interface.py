#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest
import functools
import logging
import mox_cpr_delta_mo.mo_interface as mo

sent = {}
http = {}


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data




class TestMoInterface(unittest.TestCase):

    def setUp(self):
        def mora_get(url, **params):
            return http.get(url)
        def mora_post(url, **params):
            sent.setdefault("post", {})[url] = params
        def logger(*args, **kwargs):
            sent.setdefault("log", []).append((args, kwargs))
        self.maxDiff = None
        sent.clear()
        http.clear()
        mo.mora_get = mora_get
        mo.mora_post = mora_post
        mo.logger.debug = functools.partial(logger, logging.DEBUG)

    def test_mora_update_person_by_cprnumber_no_valid_changes(self):
        mo.mora_update_person_by_cprnumber("2525-01-01", "1234561234", {"Me": "No"})
        self.assertEqual(
            {'log': [((10, 'no name changes for %s', '1234561234'), {})]},
            sent
        )

    def test_mora_update_person_by_cprnumber_valid_changes(self):

        # must ask for th person behind pnummer 0906340000
        http["{BASE}/o/{ORG}/e"] = MockResponse({
            "items": [{"name": "Anders And",
                      "uuid": "53181ed2-f1de-4c4a-a8fd-ab358c2c454a"}
        ]}, 200)

        # must ask for employee to check that query hit cpr
        http['{BASE}/e/53181ed2-f1de-4c4a-a8fd-ab358c2c454a/'] = MockResponse({
            "cpr_no": "0906340000",
            "name": "Anders And",
            "org": {"name": "Aarhus Universitet",
                    "user_key": "AU",
                    "uuid": "456362c4-0ee4-4e5e-a72c-751239745e62"},
            "user_key": "andersand",
            "uuid": "53181ed2-f1de-4c4a-a8fd-ab358c2c454a"
        }, 200)

        # call the function
        mo.mora_update_person_by_cprnumber(
            "2525-01-01T00:00:00Z",
            "0906340000",
            {"fornavn": "Robert", "mellemnavn": "", "efternavn": "Jakobsen"}
        )

        # make sure we logged changes and posted them to mo
        self.assertEqual({
            'log': [((10,
                       '%s has changes in name',
                       '53181ed2-f1de-4c4a-a8fd-ab358c2c454a'), {})],
            'post': {
                '{BASE}/details/edit': {
                    'json': [{
                    'data': {'name': 'Robert Jakobsen',
                             'validity': {'from': '2525-01-01T00:00:00Z'}},
                    'type': 'employee',
                    'uuid': '53181ed2-f1de-4c4a-a8fd-ab358c2c454a'}],
                    'params': {'force': 1}
                 }
             }
        }, sent)

