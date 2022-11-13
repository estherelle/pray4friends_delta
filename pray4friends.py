import os

from typing import List

PEOPLE = [
    ['Petros Yeung', 'M'],
    ['Sophia Wang', 'F'],
    ['Johnny Wu', 'M'],
    ['Sylvia Yang', 'F'],
    ['Jenny Huang', 'F'],
    ['Esther Liao', 'F'],
    ['Ann Shan', 'F'],
    ['Kevin Yang', 'M'],
    ['Jennifer Huang', 'F'],
    ['Amy Lee', 'F'],
    ['Kathleen Hu', 'F'],
    ['Nathan Ruiz', 'M']
]

PRAYER_LOCATION='https://docs.google.com/document/d/1m0obS7Me-RhNqVale8zCBVQEiEvjr3nfPxZWpa_IUuY/edit#heading=h.479mxvgve6ve'

PRAYERER='<PRAYERER>'
PRAYEE='<PRAYEE>'

PRAYER_MESSAGE = f'''
Hey, {PRAYERER}! Hope you've been having a great week 🙂 Could you please pray for {PRAYEE} at least once this week?

Please tell them you are praying for them!

You can find their prayer here:
{PRAYER_LOCATION}

Thank you for praying for your brothers and sisters! 🙂
'''

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

def printPrayerMessage(people):
    for i in range(len(people)):
        prayerer = people[i]
        prayee = people[(i + 1) % len(people)]
        print(f'### Send this message to {prayerer}:')
        print(PRAYER_MESSAGE.replace(PRAYERER, prayerer.split(" ")[0]).replace(PRAYEE, prayee))

for gender in ['M', 'F']:
    printPrayerMessage(loadGender(gender, PEOPLE))
