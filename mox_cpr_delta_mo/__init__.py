# -- coding: utf-8 --
#
# Copyright (c) 2018, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .mo_interface import (
    mora_get_all_cpr_numbers,
    mora_update_person_by_cprnumber,
)

from .cpr_interface import (
    cpr_get_delta_udtraek,
    cpr_add_subscription,
    cpr_remove_subscription,
    cpr_get_all_subscribed,
)

__all__ = [
    "mora_get_all_cpr_numbers",
    "mora_update_person_by_cprnumber",
    "cpr_get_delta_udtraek",
    "cpr_add_subscription",
    "cpr_remove_subscription",
    "cpr_get_all_subscribed",
]
