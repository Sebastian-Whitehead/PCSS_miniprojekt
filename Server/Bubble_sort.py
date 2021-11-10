import random

def countPoints(scores: [int]) -> [int]:
    points = []
    n = max(scores)
    for x in range(n):
        summed = scores.count(x)
        points.append(summed)
    return points

def bubble_sort(scores):
    #den kigger på de 2 første, finder den højeste værdi og sætter den øverst. Kigger på 2 og 3 og finder den højeste, og til sidst 3 og 4

    n = len(scores)
    for i in range (n - 1): #number of comparisons
        flag = 0 #set flag to 0, when flag is zero again it stops

        for j in range(n - 1):
            if scores[j][1] > scores[j+1][1]:
                temp = scores[j] # make a temporary list to save the new order, which is the same as the current index
                scores[j] = scores[j+1] #change the current index to j+1,
                scores[j+1] = temp #change j+1 to temporary, which is j.
                flag = 1

        if flag == 0:
            break
    return scores


if __name__ == '__main__':
    names = ['name0', 'name1', 'name2', 'name3']
    scores = []
    for i in range(50):
        n = random.randint(0, len(names))
        scores.append(n)

    points = countPoints(scores)
    packedScores = list(zip(names, scores))
    print(f'{packedScores=}')
    sortedPoints = bubble_sort(packedScores)
    print(f'{sortedPoints=}')