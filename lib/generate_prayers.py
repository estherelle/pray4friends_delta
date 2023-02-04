#!/usr/bin/env python3

from argparse import ArgumentParser
from datetime import datetime

from prayer_messages import PrayerMessages


def parse_args():
    def convert_datetime_arg(input_date_string: str):
        month, day, year = input_date_string.split("/")
        return datetime(*[int(x) for x in [f"20{year}", month, day]])

    parser = ArgumentParser(
        description="Generate a chain of prayer messages for a group to get everyone to prayer for each other.",
    )
    parser.add_argument(
        "-d",
        "--date",
        required=False,
        type=convert_datetime_arg,
        help="The date the prayers were created on. Used to store the resulting ordering in a local file. Defaults to today. Format: MM/DD/YY",
        default=datetime.now(),
    )
    return parser.parse_args()


def main():
    args = parse_args()

    prayerChain = PrayerMessages.getPrayerChain()
    prayerChain.writeMessagesToFile()
    prayerChain.writeGendersPeoplePrayingToFile(args.date.strftime("%Y-%m-%d"))

    print(f"Script complete.")


main()
