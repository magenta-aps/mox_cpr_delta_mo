# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import functools
import unittest
import logging
import mox_cpr_delta_mo.mo_interface as mo


logstash=[]
def logger(*args, **kwargs):
    logstash.append((args, kwargs))

mo.logger.debug=functools.partial(logger, logging.DEBUG)

class TestMoxCprDeltaMo(unittest.TestCase):
    def setUp(self):
        logstash.clear()

    def test_mora_get_all_cpr_numbers(self):
        # Anders And and Fedtmule
        self.assertEqual(mo.mora_get_all_cpr_numbers(),[
            '1011101010', 
            '0101001010',
        ]) 


    def test_mora_update_person_by_cprnumber(self):
        mo.mora_update_person_by_cprnumber(
            fromdate="2018-09-10",
            pnr='1011101010',
            changes={
                'fornavn':"Mo",
                'mellemnavn':"Minsk",
                'efternavn':"Mohsen"
            }
        )
        pass




