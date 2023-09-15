def amountPoliceGets(people):
    queue = []
    money = 0
    while people:
        q = people.pop(0)
        print(q)
        if not queue:
            queue.append(q)
        else:
            if q[0] != queue[-1][0] and queue[-1][0] != 0:
                col_money = queue[-1][1] + q[1]
                money = money + col_money
                queue.append([0,col_money])
            elif q[0] != queue[-1][0] and queue[-1][0] == 0:
                money += q[1]
                queue.append([0,q[1]])
            elif q[0] == queue[-1][0]:
                queue.append(q)
    return money

# people = [[1,3] , [1,10], [1,4] , [1,7] , [1, 12] , [1,6]]

people = [[1,3] , [-1,10], [1,4] , [0,7] , [-1, 12] , [-1,6]]
print(amountPoliceGets(people))
