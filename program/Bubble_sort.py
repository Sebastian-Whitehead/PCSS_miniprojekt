def countPoints(scores: [int], n: int) -> [int]:
    points = []
    for n in range(n):
        points.append(scores.count(n))
    return points

def bubble_sort(scores):
    #den kigger på de 2 første, finder den højeste værdi og sætter den øverst. Kigger på 2 og 3 og finder den højeste, og til sidst 3 og 4

    n = len(scores)
    for i in range (n - 1): #number of comparisons
        flag = 0 #set flag to 0, when flag is zero again it stops

        for j in range(n - 1):
            if scores[j] > scores[j+1]:
                temp = scores[j] # make a temporary list to save the new order, which is the same as the current index
                scores[j] = scores[j+1] #change the current index to j+1,
                scores[j+1] = temp #change j+1 to temporary, which is j.
                flag = 1

        if flag == 0:
            break
    return scores


if __name__ == '__main__':
    scores = [0, 2, 3, 2, 1, 0, 1, 3, 1, 1, 1, 2]
    points = countPoints(scores)
    print(points)
    sortedPoints = bubble_sort(points)
    print(sortedPoints)