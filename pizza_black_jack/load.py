"""
    This functions load data from given datasets.
"""

def load_pizza_data(source):
    """
    This function loads a text file as dataset
    from a source path. The data structure is
    supposed to be like:
    <15 4
    2 3 5 6>

    Parameters
    ----------
    source : String
        Global path to text file to be loaded.

    Returns
    -------
    participants : Int
        Number of people to be ordered for.
    n_types : int
        Number of pizza types available.
    n_type_slices : list[int]
        Number of slices per pizza type.

    """

    print('Load data: {}'.format(source))

    with open(source, 'r') as file:
        content = file.read().splitlines()

    # Read first line
    line = content[0].split(' ')
    participants = int(line[0])
    n_types = int(line[1])

    # Read second line
    line = content[-1].split(' ')
    n_type_slices = [int(val) for val in line]

    # Check validity of input file
    if len(n_type_slices) != n_types:
        raise ValueError('Input file corrupted!')

    return participants, n_types, n_type_slices
