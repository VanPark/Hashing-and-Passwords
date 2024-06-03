import random
import time
import hashlib
import matplotlib.pyplot as plt

#Part (a): Hashing Arbitrary Inputs with SHA-256
def sha256_hash(input_str: str) -> str:
    return hashlib.sha256(input_str.encode()).hexdigest()



#Part (b): Hashing Two Strings with Hamming Distance of 1
def generate_hamming_distance_string(base_str: str) -> (str, str):
    # Convert the base string to a byte array
    base_bytes = bytearray(base_str.encode())
    
    # Flip the least significant bit of the first byte
    modified_bytes = bytearray(base_bytes)
    modified_bytes[0] ^= 0b00000001
    
    return base_str, modified_bytes.decode()

def hash_strings(str1: str, str2: str):
    print(f"Original String 1: {str1}\nOriginal String 2: {str2}")
    for i in range(10):
        str1 = sha256_hash(str1)
        str2 = sha256_hash(str2)
    print(f"Hashed String 1: {str1}\nHashed String 2: {str2}")

# Part (c): Finding Collisions in Truncated Hash Domains
def truncate_hash(hash_hex: str, bits: int) -> str:
    """Truncates the SHA-256 hash to the specified number of bits."""
    hex_length = bits // 4
    return hash_hex[:hex_length]

def find_collision(truncated_bits: int):
    """Finds a collision in the truncated hash domain."""
    hash_table = {}
    num_inputs = 0
    start_time = time.time()
    
    while True:
        input_str = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
        full_hash = sha256_hash(input_str)
        truncated_hash = truncate_hash(full_hash, truncated_bits)
        
        if truncated_hash in hash_table:
            collision_str = hash_table[truncated_hash]
            if collision_str != input_str:
                end_time = time.time()
                elapsed_time = end_time - start_time
                return collision_str, input_str, num_inputs, elapsed_time
        else:
            hash_table[truncated_hash] = input_str
        
        num_inputs += 1

def measure_collisions():
    """Measures the number of inputs and elapsed time to find collisions for various truncated hash sizes."""
    bits_list = list(range(8, 52, 2))
    num_inputs_list = []
    time_list = []
    
    for bits in bits_list:
        _, _, num_inputs, elapsed_time = find_collision(bits)
        num_inputs_list.append(num_inputs)
        time_list.append(elapsed_time)
    
    return bits_list, num_inputs_list, time_list

# Plotting the results
def plot_results(bits_list, num_inputs_list, time_list):
    """Plots the number of inputs and elapsed time to find collisions."""
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(bits_list, num_inputs_list, marker='o')
    plt.xlabel('Digest Size (bits)')
    plt.ylabel('Number of Inputs')
    plt.title('Number of Inputs vs Digest Size')

    plt.subplot(1, 2, 2)
    plt.plot(bits_list, time_list, marker='o')
    plt.xlabel('Digest Size (bits)')
    plt.ylabel('Elapsed Time (seconds)')
    plt.title('Elapsed Time vs Digest Size')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Part (a)
    print("Part (a): Hashing Arbitrary Inputs with SHA-256")
    print(sha256_hash("This is a test"))
    print()

    # Part (b)
    print("Part (b): Hashing Two Strings with Hamming Distance of 1")
    base_string = "This is a test"
    str1, str2 = generate_hamming_distance_string(base_string)
    hash_strings(str1, str2)
    print()

    # Part (c)
    print("Part (c): Finding Collisions in Truncated Hash Domains")
    truncated_bits = 16
    collision1, collision2, num_inputs, elapsed_time = find_collision(truncated_bits)
    print(f"Collision found:\nString 1: {collision1}\nString 2: {collision2}")
    print(f"Number of inputs: {num_inputs}\nElapsed time: {elapsed_time:.2f} seconds")
    print()

    # Measuring and plotting results
    bits_list, num_inputs_list, time_list = measure_collisions()
    plot_results(bits_list, num_inputs_list, time_list)