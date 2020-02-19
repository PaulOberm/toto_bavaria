"""Hashcode 2020 excercise

"""
from load import load_pizza_data as load_data, write_data

def calculate_pizzas_dumb(participants, n_pizza_types, pizza_types):
    """Determine pizza types and number of feeded
       participants.

    Parameters
    ----------
    participants : Int
        Number of people to be feeded by pizza.
    n_pizza_types : type
        Description of parameter `n_pizza_types`.
    pizza_types : type
        Description of parameter `pizza_types`.

    Returns
    -------
    type
        Description of returned object.

    """

    residuals = participants
    type_list = []
    for index, n_pizzas in reversed(list(enumerate(pizza_types))):
        temp_residuals = residuals - n_pizzas

        if temp_residuals >= 0:
            residuals = temp_residuals
            type_list.append(index)

    # Calcualte saturation - Number of feeded participants
    saturation = sum([pizza_types[idx] for idx in type_list])
    unsaturated_participants = participants - saturation

    return type_list[::-1], unsaturated_participants

def calculate_pizzas_recursive(participants, n_pizza_types, pizza_types):
    """ This function calculates the order list
        for pizzas, for a given number of participants.

        Recursive
        See: https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/
    """

    # No participants left
    if(n_pizza_types <= 0 or participants <= 0):
        return 0, None

    # If weight of the nth item is more than Knapsack of capacity
    # W, then this item cannot be included in the optimal solution
    if(pizza_types[-1] > participants):
        return calculate_pizzas_recursive(participants,
                                          n_pizza_types-1,
                                          pizza_types[:-1])

    # If it fits: Always do a binary split to include it or not
    # By doing so, the case where no element at all is a solution is checked,
    # which seems quite senseless
    # A lot of stuff is calculated way to often by doing so
    temp, temp_idx = calculate_pizzas_recursive(participants-pizza_types[-1],
                                                n_pizza_types-1,
                                                pizza_types[:-1])
    last_element_included = pizza_types[-1] + temp

    last_element_not_included, _ = calculate_pizzas_recursive(participants,
                                                              n_pizza_types-1,
                                                              pizza_types[:-1])
    # Return the maximum of both cases because:
    # The maximum can never be exceed, so this is save, but the higher
    # the closer the addition until the maximum worked then
    if last_element_included >= last_element_not_included:
        print(n_pizza_types-1)
        return last_element_included, n_pizza_types-1
    else:
        return last_element_not_included, None

def calculate_pizzas_dynamic(participants, n_pizza_types, pizza_types):
    K = [[0 for x in range(participants+1)] for x in range(n_pizza_types+1)]

    # Build table K[][] in bottom up manner
    for i in range(n_pizza_types+1): # y-direction
        for w in range(participants+1): # x-direction --> Swapped in matrix
            participants_discrepancy = w-pizza_types[i-1]
            if(i==0 or w==0):
                K[i][w] = 0
            elif participants_discrepancy >= 0:  # Index w-wt[i-1] always greater than 0, getting back to residual participants, for them
                K[i][w] = max(pizza_types[i-1] + K[i-1][participants_discrepancy], K[i-1][w])
            else:
                K[i][w] = K[i-1][w]
            print(str(K[i][w]) + ' ', end='')
        print(' ')

    max_participants = K[n_pizza_types][participants]

    index_list = []
    current_person = max_participants
    while(current_person > 0):
        # Find row number where current_person is upper limited
        print(current_person)
        type_idx = min([idx for idx, l in enumerate(K) if l[current_person]==current_person])
        print('idx', type_idx)
        index_list.append(type_idx-1)
        current_person = current_person - pizza_types[type_idx-1]

    return max_participants, len(index_list), index_list[::-1]



if __name__ == '__main__':
    SOURCE_PATH = '/media/paul/Daten/00_Data/google_hashcode_2020/a_example.in'
    SOURCE_PATH = '/media/paul/Daten/00_Data/google_hashcode_2020/b_small.in'
    SOURCE_PATH = '/media/paul/Daten/00_Data/google_hashcode_2020/c_medium.in'
    SOURCE_PATH = '/media/paul/Daten/00_Data/google_hashcode_2020/d_quite_big.in'
    # SOURCE_PATH = '/media/paul/Daten/00_Data/google_hashcode_2020/e_also_big.in'

    # Load data from dataset
    pizza_types_max, n_types, slice_list = load_data(SOURCE_PATH)
    # pizza_types_max, n_types, slice_list = 15, 4, [2, 3, 5, 6]
    print('Number of participants: {}'.format(pizza_types_max))
    print('Number of pizza types: {}'.format(n_types))
    print('List of pizza_types per pizza: {}'.format(slice_list))

    # Calculate number of pizzas for number of participants
    type_indexa, unfeeded = calculate_pizzas_dumb(pizza_types_max, n_types, slice_list)
    print('\nOrdering pizza types: {}'.format(type_indexa))
    print('Number of residuals (unfeeded): {}'.format(unfeeded))
    print('Percentage: {} %'.format(unfeeded*100/pizza_types_max))

    # feeded_people, _ = calculate_pizzas_recursive(pizza_types_max, n_types, slice_list)
    # print('\nOrdering pizza types in recursive calculation order: {}'.format(feeded_people))

    feeded_people, n_types_rec, pizza_indexa = calculate_pizzas_dynamic(pizza_types_max, n_types, slice_list)
    print('\nOrdering pizza types: {}'.format(pizza_indexa))
    print('\nNumber of feeded people: {}'.format(feeded_people))

    # Output result file for ordering
    write_data(len(type_indexa), type_indexa, SOURCE_PATH+'_dumb_out.txt')
    write_data(n_types_rec, pizza_indexa, SOURCE_PATH+'_dynamic_out.txt')
