#!/usr/bin/env python3

import os

from argparse import ArgumentParser
from datetime import datetime
from typing import List
# NOTE: If import fails, remember to run `./generate_files.py`.
from constants import PRAYER_LOCATION

MALE_IDENTIFIER='M'
FEMALE_IDENTIFIER='F'

PRAYERER_PLACEHOLDER='<PRAYERER>'
PRAYEE_PLACEHOLDER='<PRAYEE>'
PRAYER_MESSAGE = f'''
Hey, {PRAYERER_PLACEHOLDER}! Hope you've been having a great week 🙂 Could you please pray for {PRAYEE_PLACEHOLDER} at least once this week?

Please tell them you are praying for them!

You can find their prayer here:
{PRAYER_LOCATION}

Thank you for praying for your brothers and sisters! 🙂
'''
PRAYER_INPUT_FILE_NAME='prayers_input.md'
PRAYER_OUTPUT_FILE_NAME='prayers_output.md'

def getNewPrayerOrder(peopleThatArePraying, currentPrayerOrder: List[str], oldOrders: List[str]) -> bool:
    def checkIsUniqueOrder(newOrder) -> bool:
        newOrderRotations = [newOrder[x+1:] + newOrder[:x] for x in range(len(newOrder) + 1)]
        return all([rotation not in oldOrders for rotation in newOrderRotations])

    if len(peopleThatArePraying) == 0:
        return checkIsUniqueOrder(currentPrayerOrder)

    for i in range(len(peopleThatArePraying)):
        currentPrayerOrder.append(peopleThatArePraying[i])
        orderIsValid = getNewPrayerOrder(peopleThatArePraying[:i] + peopleThatArePraying[i+1:], currentPrayerOrder, oldOrders)
        if orderIsValid:
            return True
        currentPrayerOrder.pop()

    return False


def loadOldOrders(genderIdentifier) -> List[List[str]]:
    genderOldOrders = []
    (path, _, files) = list(os.walk(os.sep.join([os.getcwd(), 'prayer-history'])))[0]
    for file in files:
        oldOrder = []

        with open(os.sep.join([path, file])) as oldPrayerFile:
            while not oldPrayerFile.readline().startswith(f'## {genderIdentifier}\n'):
                pass
            while True:
                prayerName = oldPrayerFile.readline()

                if prayerName.startswith('##') or prayerName == '':
                    break

                oldOrder.append(prayerName.strip())

        genderOldOrders.append(oldOrder)

    return genderOldOrders


def loadGender(genderIdentifier, prayingPeople):
    oldOrders = loadOldOrders(genderIdentifier)
    genderOfPeoplePraying = list(map(lambda y: y[0], filter(lambda x: x[1] == genderIdentifier, prayingPeople)))
    newPrayerOrder = []
    if getNewPrayerOrder(genderOfPeoplePraying, newPrayerOrder, oldOrders):
        return newPrayerOrder

    raise Exception('No valid ordering found.')

def getPrayerMessage(people):
    all_prayers_message_pieces = []
    for i in range(len(people)):
        prayerer = people[i]
        prayee = people[(i + 1) % len(people)]
        all_prayers_message_pieces.append(f'### Send this message to {prayerer}:')
        all_prayers_message_pieces.append(
          PRAYER_MESSAGE
            .replace(PRAYERER_PLACEHOLDER, prayerer.split(" ")[0])
            .replace(PRAYEE_PLACEHOLDER, prayee))
    return '\n'.join(all_prayers_message_pieces)

def parse_args():
    def convert_datetime_arg(input_date_string: str):
        month, day, year = input_date_string.split('/')
        return datetime(*[int(x) for x in [f'20{year}', month, day]])

    parser = ArgumentParser(
        description='Generate a chain of prayer messages for a group to get everyone to prayer for each other.',
    )
    parser.add_argument(
        '-d',
        '--date',
        required=False,
        type=convert_datetime_arg,
        help='The date the prayers were created on. Used to store the resulting ordering in a local file. Defaults to today. Format: MM/DD/YY',
        default=datetime.now())
    return parser.parse_args()


def main():
    args = parse_args()

    prayerInputPeople = []

    with open(PRAYER_INPUT_FILE_NAME) as peoplePrayingFile:
        prayerInputLine = peoplePrayingFile.readline()
        gender_info = None
        while prayerInputLine and prayerInputLine != '':
            try:
                if prayerInputLine.startswith(f'## {MALE_IDENTIFIER}'):
                    gender_info = MALE_IDENTIFIER
                    continue

                if prayerInputLine.startswith(f'## {FEMALE_IDENTIFIER}'):
                    gender_info = FEMALE_IDENTIFIER
                    continue

                if prayerInputLine.startswith(f'#'):
                    raise SyntaxError(f'Invalid entry in "{PRAYER_INPUT_FILE_NAME}": {prayerInputLine}')

                prayerInputPeople.append([prayerInputLine.strip(), gender_info])
            finally:
                prayerInputLine = peoplePrayingFile.readline()

    genderMessages = []
    todaysDate = args.date.strftime("%Y-%m-%d")

    finishedGenderOrders = [f'# {todaysDate}\n']
    for gender in [MALE_IDENTIFIER, FEMALE_IDENTIFIER]:
        finishedGenderOrder = loadGender(gender, prayerInputPeople)
        finishedGenderOrders.append(f'## {gender}\n')
        for personLine in finishedGenderOrder:
            finishedGenderOrders.append(f'{personLine}\n')
        allPeopleInGenderMsg = getPrayerMessage(finishedGenderOrder)
        genderMessages.append(allPeopleInGenderMsg)

    completeMessage = '\n'.join(genderMessages)

    with open(PRAYER_OUTPUT_FILE_NAME, 'w') as prayerOutputFile:
        prayerOutputFile.write(completeMessage)

    with open(f'prayer-history/{todaysDate}.md', 'w') as prayerOutputFile:
        for line in finishedGenderOrders:
            prayerOutputFile.writelines(line)

    print(f'Script complete. Wrote output to "{PRAYER_OUTPUT_FILE_NAME}"')

main()