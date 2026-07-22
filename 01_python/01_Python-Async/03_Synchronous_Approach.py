import time

def fetch_data_sync(site_id):
    print(f"Starting download from Site {site_id}...")
    time.sleep(2)  # Simulates waiting for a network response
    print(f"Finished downloading from Site {site_id}!")
    return f"Data from Site {site_id}"

def main_sync():
    start_time = time.time()
    
    # Tasks run one after the other
    result1 = fetch_data_sync(1)
    result2 = fetch_data_sync(2)
    result3 = fetch_data_sync(3)
    
    end_time = time.time()
    print(f"\nAll downloads completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    main_sync()

# Total Runtime: ~6 seconds (2 seconds + 2 seconds + 2 seconds). # Check `04_Asynchronous_Approach.py`` file, this will take 2 seconds