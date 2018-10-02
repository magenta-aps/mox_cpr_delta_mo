import functools
import unittest
import logging
import mox_cpr_delta_mo.__main__ as mox

mox.mora_get_all_cpr_numbers = lambda:["0101621234","0202621234"] 
mox.mora_update_person_by_cprnumber = lambda fromdate, pnr, changes: None
mox.get_cpr_delta_udtraek = lambda sincedate: {sincedate:{"0101621234":{'fornavn':"Bent"}}}
mox.add_cpr_subscription = lambda pnr: True
mox.remove_cpr_subscription = lambda pnr: False
mox.get_all_subscribed_cprs = lambda: ["0101621234","0303631234"] 

logstash=[]
def logger(*args, **kwargs):
    logstash.append((args, kwargs))

mox.logger.debug=functools.partial(logger, logging.DEBUG)

class TestMoxCprDeltaMo(unittest.TestCase):
    def setUp(self):
        logstash.clear()

    def test_update_cpr_subscriptions(self):
        mox.update_cpr_subscriptions()
        self.assertEqual(logstash[0], ((10, 'update_cpr_subscriptions started'), {}))
        self.assertEqual(logstash[-1], ((10, 'update_cpr_subscriptions ended'), {}))

