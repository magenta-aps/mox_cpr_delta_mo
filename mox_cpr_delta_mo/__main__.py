import argparse

from mox_cpr_delta_mo import get_all_cpr_numbers
from mox_cpr_delta_mo import update_cpr_number
from mox_cpr_delta_mo import get_cpr_delta

def update_subscriptions():
    pass

def cpr_delta_update_mo(sincedate):
    for date,citizens in get_cpr_delta(sincedate).items():
        print(date)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--update-subscriptions", 
        help="report subscriptions for all cpr-numbers, update subscriptions for the ones "
             "that are missing in subscrition, remove the ones missing in mora", 
        action="store_true", 
        default=False
    )
    parser.add_argument(
        "--cpr-delta-update-mo", 
        help="retrieve data from cpr-kontoret and update mora",
        action="store_true", 
        default=True
    )
    parser.add_argument(
        "--cpr-delta-since", 
        help="retrieve data from cpr-kontoret since this date "
             "given as YYmmdd (180921)" ,
        type=str,
        default="180927"
    )

    args = parser.parse_args()

    if args.update_subscriptions:
        update_subscriptions()

    if args.cpr_delta_update_mo:
        cpr_delta_update_mo(args.cpr_delta_since)

    
