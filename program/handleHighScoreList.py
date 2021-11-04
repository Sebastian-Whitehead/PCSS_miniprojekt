import json, random


def loadScores(fileName):
    try:
        with open(fileName) as json_file:
            return json.load(json_file)
    except:
        return []


def insertScore(data, oldScoreList):
    # Iterate all new scores
    for newScore in data:
        compareList = list(oldScoreList)  # Copy the score list to comparing list

        if len(compareList) < 1: oldScoreList.insert(0, newScore)

        # Cut the compare list in half
        while len(compareList) > 0:
            newValue = newScore[1]  # Get the value from the new score

            # Get compareing data
            compareIndex = int(len(compareList) / 2)  # Get the index of comparing score
            compareValue = compareList[compareIndex][1]  # Get the value of comparing score

            # Check if the values are the same
            if compareValue == newValue:
                compareScore = [x for x in oldScoreList if x[1] == compareValue][0]
                finalIndex = oldScoreList.index(compareScore)
                # Insert the score at the current index
                oldScoreList.insert(finalIndex, newScore)
                break

            # Compare the value with the new value
            if compareValue > newValue:
                compareList = compareList[:compareIndex]  # Get the first part of the list
            else:
                compareList = compareList[compareIndex + 1:]  # Get the second part of the list

            # Insert the new value into the score list at the correct index
            if len(compareList) < 1:
                compareScore = [x for x in oldScoreList if x[1] == compareValue][0]
                finalIndex = oldScoreList.index(compareScore)
                if compareValue < newValue: finalIndex += 1
                oldScoreList.insert(finalIndex, newScore)
                continue

    return oldScoreList


def saveScores(fileName, scoreList):
    oldScoreList = loadScores(fileName)  # Load file

    # Insert data into score list
    scoreList = insertScore(scoreList, oldScoreList)

    # Update the score list
    updatedScoreList = scoreList

    # Save the updated list as json
    with open(fileName, 'w') as outfile:
        json.dump(updatedScoreList, outfile)


def programTesting(data, printOut):
    fileName = 'allTimeHighScore.txt'

    saveScores(fileName, data)
    highScore = loadScores(fileName)

    if printOut:
        for currentScore in reversed(highScore): print(currentScore)


if __name__ == '__main__':

    programTesting([
        ['Tonko', 10123],
        ['Rebecca', -1051],
        ['Charlotte', 13],
        ['Sebsastian', 12],
        ['Tobias', 15]
    ], False)

    programTesting([
        ['Tonko', 154],
        ['Rebecca', -42],
        ['Charlotte', 45],
        ['Sebsastian', 56],
        ['Tobias', 483]
    ], False)

    # Make manufactured big data
    bigData = []
    for x in range(100):
        name = str(int(random.random() * 10))
        score = int(random.random() * 100)
        bigData.append([name, score])
    programTesting(bigData, True)
