def binary_search_upper_bound(arr, target):
    """Binary search for sorted array with fractional numbers."""

    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2
        
        if arr[mid] < target:
            low = mid + 1
        else:
            upper_bound = arr[mid]
            high = mid - 1

    return (iterations, upper_bound)

if __name__ == "__main__":
    data = [0.1, 1.5, 2.4, 3.6, 3.6, 4.8, 5.9, 7.2, 9.1]

    target1 = 3.6
    result1 = binary_search_upper_bound(data, target1)
    print(f"Шукаємо {target1}: {result1}")
    
    target2 = 4.0
    result2 = binary_search_upper_bound(data, target2)
    print(f"Шукаємо {target2}: {result2}") 
    
    target3 = 10.0
    result3 = binary_search_upper_bound(data, target3)
    print(f"Шукаємо {target3}: {result3}") 
    
    target4 = -1.5
    result4 = binary_search_upper_bound(data, target4)
    print(f"Шукаємо {target4}: {result4}") 