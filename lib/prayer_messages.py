import os
from typing import List

# NOTE: If import fails, remember to run `./generate_files.py`.
from constants import PRAYER_LOCATION


class PrayerChain:
    PRAYER_OUTPUT_FILE_NAME = "prayers_output.md"

    gendersPeoplePraying: List[str]
    messages: List[str]

    def __init__(self, gendersPeoplePraying, messages) -> None:
        self.gendersPeoplePraying = gendersPeoplePraying
        self.messages = messages

    def writeMessagesToFile(self):
        with open(PrayerChain.PRAYER_OUTPUT_FILE_NAME, "w") as prayerOutputFile:
            prayerOutputFile.writelines(self.messages)
        print(f'Wrote output to "{PrayerChain.PRAYER_OUTPUT_FILE_NAME}')

    def writeGendersPeoplePrayingToFile(self, todaysDate):
        PEOPLE_PRAYING_OUTPUT_FILE_NAME = f"prayer-history/{todaysDate}.md"
        with open(PEOPLE_PRAYING_OUTPUT_FILE_NAME, "w") as prayerOutputFile:
            prayerOutputFile.write(f"# {todaysDate}\n")
            prayerOutputFile.writelines(self.gendersPeoplePraying)
        print(f'Wrote output to "{PEOPLE_PRAYING_OUTPUT_FILE_NAME}')


class PrayerMessages:
    MALE_IDENTIFIER = "M"
    FEMALE_IDENTIFIER = "F"

    PRAYERER_PLACEHOLDER = "<PRAYERER>"
    PRAYEE_PLACEHOLDER = "<PRAYEE>"
    PRAYER_MESSAGE = f"""
Hey, {PRAYERER_PLACEHOLDER}! Hope you've been having a great week 🙂 Could you please pray for {PRAYEE_PLACEHOLDER} at least once this week?

Please tell them you are praying for them!

You can find their prayer here:
{PRAYER_LOCATION}

Thank you for praying for your brothers and sisters! 🙂
"""
    PRAYER_INPUT_FILE_NAME = "prayers_input.md"

    def readInPeoplePraying(prayer_input_file: str) -> List[str]:
        prayerInputPeople = []

        with open(prayer_input_file) as peoplePrayingFile:
            prayerInputLine = peoplePrayingFile.readline()
            gender_info = None
            while prayerInputLine and prayerInputLine != "":
                try:
                    if prayerInputLine.startswith(
                        f"## {PrayerMessages.MALE_IDENTIFIER}"
                    ):
                        gender_info = PrayerMessages.MALE_IDENTIFIER
                        continue

                    if prayerInputLine.startswith(
                        f"## {PrayerMessages.FEMALE_IDENTIFIER}"
                    ):
                        gender_info = PrayerMessages.FEMALE_IDENTIFIER
                        continue

                    if prayerInputLine.startswith(f"#"):
                        raise SyntaxError(
                            f'Invalid entry in "{prayer_input_file}": {prayerInputLine}'
                        )

                    prayerInputPeople.append([prayerInputLine.strip(), gender_info])
                finally:
                    prayerInputLine = peoplePrayingFile.readline()

        return prayerInputPeople

    def getNewPrayerOrder(
        peopleThatArePraying, currentPrayerOrder: List[str], oldOrders: List[str]
    ) -> bool:
        def checkIsUniqueOrder(newOrder) -> bool:
            newOrderRotations = [
                newOrder[x + 1 :] + newOrder[:x] for x in range(len(newOrder) + 1)
            ]
            return all([rotation not in oldOrders for rotation in newOrderRotations])

        if len(peopleThatArePraying) == 0:
            return checkIsUniqueOrder(currentPrayerOrder)

        for i in range(len(peopleThatArePraying)):
            currentPrayerOrder.append(peopleThatArePraying[i])
            orderIsValid = PrayerMessages.getNewPrayerOrder(
                peopleThatArePraying[:i] + peopleThatArePraying[i + 1 :],
                currentPrayerOrder,
                oldOrders,
            )
            if orderIsValid:
                return True
            currentPrayerOrder.pop()

        return False

    def loadOldOrders(genderIdentifier) -> List[List[str]]:
        genderOldOrders = []
        (path, _, files) = list(os.walk(os.sep.join([os.getcwd(), "prayer-history"])))[
            0
        ]
        for file in files:
            oldOrder = []

            with open(os.sep.join([path, file])) as oldPrayerFile:
                while not oldPrayerFile.readline().startswith(
                    f"## {genderIdentifier}\n"
                ):
                    pass
                while True:
                    prayerName = oldPrayerFile.readline()

                    if prayerName.startswith("##") or prayerName == "":
                        break

                    oldOrder.append(prayerName.strip())

            genderOldOrders.append(oldOrder)

        return genderOldOrders

    def loadGender(genderIdentifier, prayingPeople):
        oldOrders = PrayerMessages.loadOldOrders(genderIdentifier)
        genderOfPeoplePraying = list(
            map(
                lambda y: y[0],
                filter(lambda x: x[1] == genderIdentifier, prayingPeople),
            )
        )
        newPrayerOrder = []
        if PrayerMessages.getNewPrayerOrder(
            genderOfPeoplePraying, newPrayerOrder, oldOrders
        ):
            return newPrayerOrder

        raise Exception("No valid ordering found.")

    def getPrayerMessage(people):
        all_prayers_message_pieces = []
        for i in range(len(people)):
            prayerer = people[i]
            prayee = people[(i + 1) % len(people)]
            all_prayers_message_pieces.append(f"### Send this message to {prayerer}:")
            all_prayers_message_pieces.append(
                PrayerMessages.PRAYER_MESSAGE.replace(
                    PrayerMessages.PRAYERER_PLACEHOLDER, prayerer.split(" ")[0]
                ).replace(PrayerMessages.PRAYEE_PLACEHOLDER, prayee)
            )
        return "\n".join(all_prayers_message_pieces)

    def getPrayerChain() -> PrayerChain:
        peoplePraying = PrayerMessages.readInPeoplePraying(
            PrayerMessages.PRAYER_INPUT_FILE_NAME
        )
        genderMessages = []

        finishedGenderOrders = []
        for gender in [
            PrayerMessages.MALE_IDENTIFIER,
            PrayerMessages.FEMALE_IDENTIFIER,
        ]:
            finishedGenderOrder = PrayerMessages.loadGender(gender, peoplePraying)
            finishedGenderOrders.append(f"## {gender}\n")
            for personLine in finishedGenderOrder:
                finishedGenderOrders.append(f"{personLine}\n")
            allPeopleInGenderMsg = PrayerMessages.getPrayerMessage(finishedGenderOrder)
            genderMessages.append(allPeopleInGenderMsg)

        completeMessages = "\n".join(genderMessages)

        return PrayerChain(finishedGenderOrders, completeMessages)
