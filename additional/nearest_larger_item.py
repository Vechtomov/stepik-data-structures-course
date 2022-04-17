from heapq import heappop, heappush

def solution_minheap(a):
    result = [0] * len(a)
    temp = []
    for i, el in enumerate(a):
        while len(temp) > 0 and temp[0][0] < el:
            e, j = heappop(temp)
            result[j] = i - j
        heappush(temp, (el, i))
    return result

def solution_stack(a):
    result = [0] * len(a)
    temp = []
    for i in range(len(a)-1, -1, -1):
        el = a[i]
        while len(temp) > 0 and temp[-1][0] < el:
            temp.pop()
        if len(temp) > 0:
            result[i] = temp[-1][1] - i
        temp.append((el, i))
    return result
