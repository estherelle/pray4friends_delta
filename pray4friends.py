import os

from datetime import datetime
from typing import List

PRAYER_LOCATION='https://bible.com'

PRAYERER='<PRAYERER>'
PRAYEE='<PRAYEE>'

PRAYER_MESSAGE = f'''
Hey, {PRAYERER}! Hope you've been having a great week 🙂 Could you please pray for {PRAYEE} at least once this week?

Please tell them you are praying for them!

You can find their prayer here:
{PRAYER_LOCATION}

Thank you for praying for your brothers and sisters! 🙂
'''
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
            .replace(PRAYERER, prayerer.split(" ")[0])
            .replace(PRAYEE, prayee))
    return '\n'.join(all_prayers_message_pieces)

prayerInputPeople = []

with open('prayers_input.txt') as peoplePrayingFile:
  person = peoplePrayingFile.readline()
  while person and person != '':
    prayerInputPeople.append(person.strip().split(','))
    person = peoplePrayingFile.readline()

genderMessages = []
todaysDate = datetime.now().strftime("%m-%d-%Y")

finishedGenderOrders = [f'# {todaysDate}\n']
for gender in ['M', 'F']:
    finishedGenderOrder = loadGender(gender, prayerInputPeople)
    finishedGenderOrders.append(f'## {gender}\n')
    for person in finishedGenderOrder:
      finishedGenderOrders.append(f'{person}\n')
    genderMessage = getPrayerMessage(finishedGenderOrder)
    genderMessages.append(genderMessage)

completeMessage = '\n'.join(genderMessages)

with open(PRAYER_OUTPUT_FILE_NAME, 'w+') as prayerOutputFile:
  prayerOutputFile.write(completeMessage)

with open(f'prayer-history/{todaysDate}.md', 'w+') as prayerOutputFile:
  for line in finishedGenderOrders:
    prayerOutputFile.writelines(line)

print(f'Script complete. Wrote output to "{PRAYER_OUTPUT_FILE_NAME}"')
