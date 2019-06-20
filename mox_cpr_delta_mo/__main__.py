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
import os
import json

from mox_cpr_delta_mo import (
    mora_get_all_cpr_numbers,
    mora_update_person_by_cprnumber,
    cpr_get_delta_udtraek,
    cpr_add_subscription,
    cpr_remove_subscription,
    cpr_get_all_subscribed,
)

from mox_cpr_delta_mo.settings import (
    MOX_LOG_LEVEL,
    MOX_LOG_FILE,
    MOX_JSON_CACHE,
    SFTP_DOWNLOAD_PATH
)

# set warning-level for all loggers
[
    logging.getLogger(i).setLevel(logging.WARNING)
    for i in logging.root.manager.loggerDict
]

logging.basicConfig(
    format='%(levelname)s %(asctime)s %(name)s %(message)s',
    level=MOX_LOG_LEVEL,
    filename=MOX_LOG_FILE
)
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
    # let python do the Y2K math
    nextdate = datetime.datetime.strptime(sincedate, "%y%m%d")

    for date, citizens in cpr_get_delta_udtraek(sincedate).items():
        logger.info("processing %d items for %s", len(citizens), date)

        # let python do the Y2K math
        fromdate = datetime.datetime.strptime(date, "%y%m%d")
        fromdatestr = fromdate.strftime("%Y-%m-%d")

        for pnr, changes in citizens.items():
            mora_update_person_by_cprnumber(fromdatestr, pnr, changes)

    nextdate = datetime.datetime.now()
    return nextdate.strftime("%y%m%d")


def read_cache(path):
    if not os.path.exists(path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        cache = {}
    else:
        cache = json.load(open(path))
    return cache


def write_cache(path, cache):
    json.dump(cache, open(path, "w"))


if __name__ == "__main__":

    cache = read_cache(MOX_JSON_CACHE)
    parser = argparse.ArgumentParser()

    if not os.path.exists(SFTP_DOWNLOAD_PATH):
        os.makedirs(SFTP_DOWNLOAD_PATH)

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
        "given as YYmmdd (181018)",
        type=str,
        default=cache.get("nextdate", "181018")
    )

    args = parser.parse_args()
    logger.info("starting program with args: %r", args)

    if args.update_cpr_subscriptions:
        logger.info("start adding new subscritions")
        try:
            update_cpr_subscriptions()
        except Exception as e:
            logger.exception(e)
        logger.info("end adding new subscritions")

    if args.cpr_delta_update_mo:
        logger.info("start updating os2mo - updates since %s",
                    args.cpr_delta_since)
        try:
            cache["nextdate"] = cpr_delta_update_mo(args.cpr_delta_since)
        except Exception as e:
            logger.exception(e)
        logger.info("end updating os2mo")

    write_cache(MOX_JSON_CACHE, cache)
