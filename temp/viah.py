def amountPoliceGets(people):
    moving_dir = None
    accumulated_amount = 0
    money_to_police = 0

    while people:
        curr_person_dir , curr_person_amount = people.pop(0)

        if curr_person_dir == 1:
            if moving_dir == 1:
               accumulated_amount += curr_person_amount
            else:
                accumulated_amount = curr_person_amount
            moving_dir = 1
            
        
        if curr_person_dir == 0:
            if moving_dir == 1:
                money_to_police += accumulated_amount
                accumulated_amount = 0
            moving_dir = 0

        if curr_person_dir == -1:
            if moving_dir == 1:
                money_to_police += (accumulated_amount + curr_person_amount)
                moving_dir = 0
                accumulated_amount = 0

            elif moving_dir == 0:
                money_to_police += curr_person_amount
                moving_dir = 0
                accumulated_amount = 0

            elif moving_dir == -1:
                accumulated_amount += curr_person_amount
            
            else:
                moving_dir == -1
                accumulated_amount = curr_person_amount

    return money_to_police

people = [[1,3] , [-1,10], [1,4] , [0,7] , [-1, 12] , [-1,6]]

print(amountPoliceGets(people))


