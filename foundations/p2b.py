#!/usr/bin/python2

c = [0, 0, 0, 0] * 3

'''
c[0] = [2, -1, 3, 5]
c[1] = [4, 2, -4, 2]
c[2] = [1, -7, 3, 2]
c[3] = [-3, 1, 4, 3]
'''
c[0] = [2, -1, 3]
c[1] = [4, 2, -4]
c[2] = [1, -7, 3]

target = (2, 2)

cache = {}
count = 0

def findMinCost(row, col):
    global count
    if (row, col) in cache:
        return cache[(row, col)]
    if row == target[0] and col == target[1]:
        result = c[row][col]
    elif row == target[0]:
        result = c[row][col] + findMinCost(row, col + 1)
    elif col == target[1]:
        result = c[row][col] + findMinCost(row + 1, col)
    else:
        result = c[row][col] + min(findMinCost(row + 1, col), findMinCost(row, col + 1))

    cache[(row, col)] = result
    count += 1
    return result

if __name__ == '__main__':
    print('min cost = %d' %findMinCost(0, 0))
    print('count = %d' %count)
