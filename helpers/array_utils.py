def bubble_sort(arr, d=True):
    """
    Sorts an array using bubble sort algorithm.
    
    Args:
        arr: Array to sort
        d: True for ascending order, False for descending
        
    Returns:
        Sorted array
    """
    sorted = False
    while not sorted:
        sorted = True
        for i in range(0, len(arr) - 1):
            if d:
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    sorted = False
            else:
                if arr[i] < arr[i + 1]:
                    arr[i + 1], arr[i] = arr[i], arr[i + 1]
                    sorted = False
    return arr

def get_2D_row(r, a):
    """
    Gets a specific row from a 2D array.
    
    Args:
        r: Row index
        a: 2D array
        
    Returns:
        The specified row
    """
    return [row for row in a[r]]

def get_2D_col(c, a):
    """
    Gets a specific column from a 2D array.
    
    Args:
        c: Column index
        a: 2D array
        
    Returns:
        The specified column
    """
    return [row[c] for row in a] 