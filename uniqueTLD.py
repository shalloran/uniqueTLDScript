import csv
import tldextract
from tqdm import tqdm

# GLOBALS
CSV_INPUT_FILE = input("Enter path to CSV file containing URLs: ")
CSV_OUTPUT_FILE = input("Enter path of CSV file to write de-duped URLs to: ")

def extractDomains(FILE_PATH):
    try:
        with open(FILE_PATH, 'r', newline='') as file:
            reader = csv.reader(file)
            urls = [row[0].strip() for row in reader if row]
            if not urls:
                print(f"No URLs found in the file {FILE_PATH}.")
                return []
    except FileNotFoundError:
        print(f"File {FILE_PATH} not found.")
        return []
    except Exception as e:
        print(f"Error reading file {FILE_PATH}: {e}")
        return []

    domains = set()
    # this is here to ensure that any mistakes can be caught
    review = set()
    
    for url in tqdm(urls, desc="Processing URLs... "):
        try:
            parsed_url = tldextract.extract(url) # urllib.parse.urlparse(url)
            if parsed_url.suffix and parsed_url.domain:
                domain = parsed_url.domain + '.' + parsed_url.suffix
                domains.add(domain)
            else:
                domains.add(f"{url} was incorrectly parsed, review")
        except Exception as e:
            print(f"Error parsing URL {url}: {e}")
    return list(domains)

def write_domains_to_file(domains, FILE_PATH):
    try:
        with open(FILE_PATH, 'w', newline='') as file:
            writer = csv.writer(file)
            for domain in domains:
                writer.writerow([domain])
    except Exception as e:
        print(f"Error writing to file {FILE_PATH}: {e}")

unique_domains = extractDomains(CSV_INPUT_FILE)
write_domains_to_file(unique_domains, CSV_OUTPUT_FILE)