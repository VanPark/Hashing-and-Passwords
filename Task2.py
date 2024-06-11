import fitz  # PyMuPDF
import bcrypt
import nltk
from nltk.corpus import words
import concurrent.futures
import time
import math

# Step 1: Extract password hashes from PDF
def extract_hashes_from_pdf(pdf_path):
    hashes = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text()
            for line in text.splitlines():
                if '$2b$' in line:  # identify lines with bcrypt hashes
                    hashes.append(line.strip())
    #print(hashes)
    return hashes

# Step 2: Generate list of possible passwords
nltk.download('words')
word_list = [word for word in words.words() if 6 <= len(word) <= 10]

# Helper function to split list into chunks
def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

# Step 3: Function to check password chunks
def check_password_chunk(chunk, full_hash):
    for word in chunk:
        if bcrypt.checkpw(word.encode('utf-8'), full_hash.encode('utf-8')):
            return word
    return None

# Step 4: Crack the hashes with parallel processing of the dictionary
def crack_password(user_hash, word_list, num_threads):
    start_time = time.time()
    user, full_hash = user_hash.split(':')[0], user_hash.split(':', 1)[1]
    
    chunks = split_list(word_list, num_threads)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_chunk = {executor.submit(check_password_chunk, chunk, full_hash): chunk for chunk in chunks}
        for future in concurrent.futures.as_completed(future_to_chunk):
            result = future.result()
            if result:
                end_time = time.time()
                return (user, result, end_time - start_time)
    return (user, None, None)

# Step 5: Main function with parallel processing for users and dictionary
def main(pdf_path, num_threads):
    hashes = extract_hashes_from_pdf(pdf_path)
    cracked_results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_hash = {executor.submit(crack_password, user_hash, word_list, num_threads): user_hash for user_hash in hashes}
        for future in concurrent.futures.as_completed(future_to_hash):
            user_hash = future_to_hash[future]
            try:
                result = future.result()
                cracked_results.append(result)
            except Exception as exc:
                print(f"{user_hash} generated an exception: {exc}")

    for result in cracked_results:
        user, password, time_taken = result
        if password:
            print(f"User: {user}, Password: {password}, Time taken: {time_taken:.2f} seconds")
        else:
            print(f"User: {user}, Password not found")

if __name__ == "__main__":
    pdf_path = 'shadow.pdf'
    num_threads = 8  # Adjust this number based on your CPU cores and desired parallelism
    main(pdf_path, num_threads)