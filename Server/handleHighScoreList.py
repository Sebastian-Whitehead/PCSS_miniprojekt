import json, random


# Load the data from the txt-file using JSON.
# Return an empty list if the file is empty
def loadScores(fileName):
    try:
        with open(fileName) as json_file:
            return json.load(json_file)
    except:
        return []


# Insert the data into the old high score list,
# using split inserting.
# (Slice the list in two until the desired location has been found
def insertScore(data, oldScoreList):
    # Iterate all new scores
    for newScore in data:
        newValue = newScore[1]  # Get the value from the new score

        compareList = list(oldScoreList)  # Copy the score list to comparing list

        # Insert the element if the old list is empty
        if len(compareList) < 1:
            oldScoreList.insert(0, newScore)  # Insert current element
            continue  # Continue to next iteration

        # Cut the compare list in half
        while len(compareList) > 0:

            # Get comparing data
            compareIndex = int(len(compareList) / 2)  # Get the index of comparing score
            actualElement = compareList[compareIndex]  # Get the actual element of comparing
            compareValue = actualElement[1]  # Get the value of comparing
            actualIndex = oldScoreList.index(actualElement)  # Get the actual index of the element

            # Check if the values are the same
            if compareValue == newValue:
                oldScoreList.insert(actualIndex, newScore)  # Insert the score at the current index
                break  # Break the while loop

            # Compare the value with the new value
            if compareValue > newValue:
                compareList = compareList[:compareIndex]  # Get the first part of the list
            else:
                compareList = compareList[compareIndex + 1:]  # Get the second part of the list

            # Insert the new value into the score list at the correct index
            if len(compareList) < 1:
                if compareValue < newValue: actualIndex += 1  # Add one to place it behind the compare element
                oldScoreList.insert(actualIndex, newScore)  # Insert the current score in the score list

    return oldScoreList  # return the updated list


# Update the txt file with the new data
# - Load file with old high score list
# - Insert the given data into the list
# - Overwrite the next high score list in the same txt-file
def saveScores(fileName, scoreList):
    oldScoreList = loadScores(fileName)  # Load file
    updatedScoreList = insertScore(scoreList, oldScoreList)  # Insert data into score list

    # Save the updated list as json
    with open(fileName, 'w') as outfile:
        json.dump(updatedScoreList, outfile)

    print(f'Save data..')


# Test the program with manufactured data.
# Save and load data
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
