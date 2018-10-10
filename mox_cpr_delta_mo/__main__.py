# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import datetime
import logging

from mox_cpr_delta_mo import (
    mora_get_all_cpr_numbers,
    mora_update_person_by_cprnumber,
    cpr_get_delta_udtraek,
    cpr_add_subscription,
    cpr_remove_subscription,
    cpr_get_all_subscribed,
)
from settings import MOX_LOG_LEVEL

# set warning-level for all loggers
[
    logging.getLogger(i).setLevel(logging.WARNING)
    for i in logging.root.manager.loggerDict
]

logging.basicConfig(level=MOX_LOG_LEVEL)
logger = logging.getLogger("mox_cpr_delta_mo")
logger.setLevel(logging.DEBUG)


def update_cpr_subscriptions():
    "add or remove subscriptions according to mora data"
    logger.debug("update_cpr_subscriptions started")
    must_subscribe = set(mora_get_all_cpr_numbers())
    are_subscribed = set(cpr_get_all_subscribed())
    add_set = must_subscribe - are_subscribed
    remove_set = are_subscribed - must_subscribe
    for pnr in remove_set:
        cpr_remove_subscription(pnr)
    for pnr in add_set:
        cpr_add_subscription(pnr)
    logger.debug("update_cpr_subscriptions ended")


def cpr_delta_update_mo(sincedate):
    for date, citizens in cpr_get_delta_udtraek(sincedate).items():
        # let python do the Y2K math
        fromdate = datetime.datetime.strptime(date, "%y%m%d").strftime(
            "%Y-%m-%d"
        )
        for pnr, changes in citizens.items():
            mora_update_person_by_cprnumber(fromdate, pnr, changes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--update-cpr-subscriptions",
        help="find subscriptions for all cpr-numbers, update "
        "subscriptions for the ones "
        "that are missing in subscrition, remove the ones missing in mora",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--cpr-delta-update-mo",
        help="retrieve data from cpr-kontoret and update mora",
        action="store_true",
        default=True,
    )
    parser.add_argument(
        "--cpr-delta-since",
        help="retrieve data from cpr-kontoret since this date "
        "given as YYmmdd (180921)",
        type=str,
        default="180927",
    )

    args = parser.parse_args()

    if args.update_cpr_subscriptions:
        update_cpr_subscriptions()

    if args.cpr_delta_update_mo:
        cpr_delta_update_mo(args.cpr_delta_since)
