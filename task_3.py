import timeit

def build_shift_table(pattern):
    """Shift table for the Boyer-Moore algorithm (bad symbol heuristic)."""

    table = {}
    length = len(pattern)

    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)

    return table

def boyer_moore_search(text, pattern):
    """Boyer-Moore algorithm."""

    shift_table = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return - 1

def compute_lps(pattern):
    """LPS array for the Knuth-Morris-Pratt algorithm."""

    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    """Knuth-Morris-Pratt algorithm."""

    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1

def polynomial_hash(s, base=256, modulus=101):
    """Returns the polynomial hash of the string s."""

    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus

    return hash_value

def rabin_karp_search(main_string, substring):
    """Rabin-Karp algorithm."""

    substring_length = len(substring)
    main_string_length = len(main_string)
    
    base = 256 
    modulus = 101  
    
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

def texts_loader():
    with open("article_1.txt", "r", encoding="utf-8") as f:
        article_1 = f.read()
    with open("article_2.txt", "r", encoding="utf-8") as f:
        article_2 = f.read()
        
    return article_1, article_2

def run_benchmark():
    # Підрядки для пошуку (існуючі та вигадані)
    patterns = {
        "Article 1": {
            "existing": "алгоритми",
            "fake": "марсохід"
        },
        "Article 2": {
            "existing": "рекомендаційна система",
            "fake": "квантовий комп'ютер"
        }
    }

    texts = {
        "Article 1": article_1,
        "Article 2": article_2
    }

    algorithms = [
        ("Boyer-Moore", boyer_moore_search),
        ("KMP", kmp_search),
        ("Rabin-Karp", rabin_karp_search)
    ]

    print(f"{'Text':<10} | {'Pattern Type':<15} | {'Algorithm':<15} | {'Time (sec)':<15}")
    print("-" * 65)

    results = {}

    for text_name, text in texts.items():
        results[text_name] = {}
        for p_type, pattern in patterns[text_name].items():
            best_algo = None
            best_time = float('inf')
            
            for algo_name, algo_func in algorithms:
                # Вимірюємо час виконання (1000 запусків)
                timer = timeit.Timer(lambda: algo_func(text, pattern))
                time_taken = timer.timeit(number=1000)
                
                print(f"{text_name:<10} | {p_type:<15} | {algo_name:<15} | {time_taken:.6f}")
                
                if time_taken < best_time:
                    best_time = time_taken
                    best_algo = algo_name
            
            results[text_name][p_type] = best_algo
            print("-" * 65)

    print("\n--- Summary of Winners ---")
    for text_name, types in results.items():
        print(f"Text: {text_name}")
        for p_type, winner in types.items():
            print(f"  {p_type.capitalize()} pattern winner: {winner}")

if __name__ == "__main__":
    article_1, article_2 = texts_loader()
    run_benchmark()
