"""Hashcode 2020 excercise

"""


from load import load_pizza_data as load_data

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
    for index, n_pizza_types in reversed(list(enumerate(pizza_types))):
        temp_residuals = residuals - n_pizza_types

        if temp_residuals >= 0:
            residuals = temp_residuals
            type_list.append(index)

    # Calcualte saturation - Number of feeded participants
    saturation = sum([pizza_types[idx] for idx in type_list])
    unsaturated_participants = participants - saturation

    return type_list, unsaturated_participants

def calculate_pizzas_recursive(participants, n_pizza_types, pizza_types):
    """ This function calculates the order list
        for pizzas, for a given number of participants.

        Recursive
        See: https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/
    """

    # No participants left
    if(n_pizza_types <= 0 or participants <= 0):
        return 0

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
    else:
        last_element_included = pizza_types[-1] +\
            calculate_pizzas_recursive(participants-pizza_types[-1],
                                       n_pizza_types-1,
                                       pizza_types[:-1])

        last_element_not_included = calculate_pizzas_recursive(participants,
                                                               n_pizza_types-1,
                                                               pizza_types[:-1])
        # Return the maximum of both cases because:
        # The maximum can never be exceed, so this is save, but the higher
        # the closer the addition until the maximum worked then
        return max(last_element_included,
                   last_element_not_included)

def write_data(types, filename):
    """ This functions creates a pizza order text file.
    """

    print('Write order to {}')



if __name__ == '__main__':
    SOURCE_PATH = '/media/paul/Daten/00_Data/google_hashcode_2020/a_example.in'
    SOURCE_PATH = '/media/paul/Daten/00_Data/google_hashcode_2020/b_small.in'
    # SOURCE_PATH = '/media/paul/Daten/00_Data/google_hashcode_2020/c_medium.in'
    # SOURCE_PATH = '/media/paul/Daten/00_Data/google_hashcode_2020/d_quite_big.in'
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

    feeded_people = calculate_pizzas_recursive(pizza_types_max, n_types, slice_list)
    print('\nOrdering pizza types in recursive calculation order: {}'.format(feeded_people))

    # Output result file for ordering
    # write_data(type_indexa, SOURCE_PATH)
