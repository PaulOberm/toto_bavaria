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
    participants : int
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


def write_data(n_types, type_list, filename):
    """
    This functions creates a pizza order text file.
    For example:
    <3
    0 2 3>

    Parameters
    ----------
    n_types : int
        Number different pizza types
    type_list: List[int]
        List of selected input types by type_index
    filename: String
        Full global path name of output file with
        extension

    """

    print('Write order to {}'.format(filename))

    temp_string = " ".join(str(t) for t in type_list)
    with open(filename, 'w') as file:
        file.write(str(n_types) + '\n')
        file.write(temp_string)
