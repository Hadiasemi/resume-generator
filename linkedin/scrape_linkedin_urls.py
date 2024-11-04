import json
import sys
import os
import threading
from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from typing import List
import random

# Lock for thread-safe operations
lock = threading.Lock()

def get_login() -> tuple:
    password = "qwertyuiop123!@#$%!a"
    with open("gmails.txt", "r") as f:
        gmails = [elem for elem in f.readlines() if not '-' in elem]

    email = random.choice(gmails).strip()
    return email, password

def setup_driver():
    try:
        email, password = get_login()
        driver = webdriver.Chrome()
        actions.login(driver, email, password)
        return driver
    except WebDriverException as e:
        print(f"Error setting up driver: {e}")
        return None

def person_to_json(person: Person) -> dict:
    """
    Convert a Person object from linkedin-scraper to a dictionary.
    
    Args:
        person (Person): The Person object to convert.

    Returns:
        dict: Dictionary representation of the Person object.
    """
    person_dict = {
        'linkedin_url': person.linkedin_url,
        'name': person.name,
        'about': person.about,
        'location': person.location,
        'open_to_work': person.open_to_work,
        'experiences': [
            {
                'institution_name': exp.institution_name,
                'linkedin_url': exp.linkedin_url,
                'website': exp.website,
                'industry': exp.industry,
                'type': exp.type,
                'headquarters': exp.headquarters,
                'company_size': exp.company_size,
                'founded': exp.founded,
                'from_date': exp.from_date,
                'to_date': exp.to_date,
                'description': exp.description,
                'position_title': exp.position_title,
                'duration': exp.duration,
                'location': exp.location
            } for exp in person.experiences
        ],
        'education': [
            {
                'institution_name': edu.institution_name,
                'linkedin_url': edu.linkedin_url,
                'website': edu.website,
                'industry': edu.industry,
                'type': edu.type,
                'headquarters': edu.headquarters,
                'company_size': edu.company_size,
                'founded': edu.founded,
                'from_date': edu.from_date,
                'to_date': edu.to_date,
                'description': edu.description,
                'degree': edu.degree
            } for edu in person.educations
        ],
        'accomplishments': [
            {
                'institution_name': acc.institution_name,
                'linkedin_url': acc.linkedin_url,
                'website': acc.website,
                'industry': acc.industry,
                'type': acc.type,
                'headquarters': acc.headquarters,
                'company_size': acc.company_size,
                'founded': acc.founded,
                'category': acc.category,
                'title': acc.title
            } for acc in person.accomplishments
        ],
        'skills': person.skills,
        'interests': [
            {
                'institution_name': intst.institution_name,
                'linkedin_url': intst.linkedin_url,
                'website': intst.website,
                'industry': intst.industry,
                'type': intst.type,
                'headquarters': intst.headquarters,
                'company_size': intst.company_size,
                'founded': intst.founded,
                'title': intst.title
            } for intst in person.interests
        ],
        'contacts': person.contacts,
        'also_viewed_urls': person.also_viewed_urls
    }

    return person_dict

def scrape_profiles_in_thread(urls: List[str], output_dir: str, batch_size: int, thread_id: int, shared_persons_json: List[dict]):
    driver = setup_driver()
    if not driver:
        print(f"Thread {thread_id}: Driver setup failed.")
        return

    for i, url in enumerate(urls):
        try:
            person = Person(url, driver=driver, close_on_complete=False)
            person_data = person_to_json(person)
            
            with lock:
                if person_data['linkedin_url'] not in {p['linkedin_url'] for p in shared_persons_json}:
                    shared_persons_json.append(person_data)
                    
                    if len(shared_persons_json) % batch_size == 0:
                        start_index = len(shared_persons_json) - batch_size
                        batch_filename = os.path.join(output_dir, f"batch_{start_index}_{start_index + batch_size}.json")
                        with open(batch_filename, 'w') as batch_file:
                            json.dump(shared_persons_json[start_index:start_index + batch_size], batch_file, indent=4)
                        print(f"Thread {thread_id}: Batch saved to {batch_filename}")
        except Exception as e:
            print(f"Thread {thread_id}: {url} failed")

    driver.quit()

def get_scraped_urls_and_data(output_dir: str) -> (set, List[dict]):
    scraped_urls = set()
    all_scraped_data = []

    # Read final_output.json if it exists
    final_output_path = os.path.join(output_dir, "final_output.json")
    if os.path.exists(final_output_path):
        with open(final_output_path, 'r') as f:
            data = json.load(f)
            for person in data:
                if person['linkedin_url'] not in scraped_urls:
                    all_scraped_data.append(person)
                    scraped_urls.add(person['linkedin_url'])

    # Read batch files
    for filename in os.listdir(output_dir):
        if filename.startswith("batch_") and filename.endswith(".json"):
            with open(os.path.join(output_dir, filename), 'r') as f:
                batch_data = json.load(f)
                for person in batch_data:
                    if person['linkedin_url'] not in scraped_urls:
                        all_scraped_data.append(person)
                        scraped_urls.add(person['linkedin_url'])

    return scraped_urls, all_scraped_data

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_filename> <output_directory> <batch_size>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_directory = sys.argv[2]
    batch_size = int(sys.argv[3])

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(input_filename, 'r') as infile:
        urls = list({url.strip() for url in infile.readlines() if url.strip()})

    # Get already scraped URLs and data
    scraped_urls, shared_persons_json = get_scraped_urls_and_data(output_directory)
    print(len(urls), len(scraped_urls))
    # Remove already scraped URLs from the input
    urls = [url for url in urls if url not in scraped_urls]
    print(len(urls))
    num_threads = min(4, len(urls))  # Adjust the number of threads as needed
    chunk_size = len(urls) // num_threads
    threads = []

    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_threads - 1 else len(urls)
        thread_urls = urls[start:end]
        thread = threading.Thread(target=scrape_profiles_in_thread, args=(thread_urls, output_directory, batch_size, i + 1, shared_persons_json))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    final_output_filename = os.path.join(output_directory, "final_output.json")
    with open(final_output_filename, 'w') as final_file:
        json.dump(shared_persons_json, final_file, indent=4)
    print(f"Final output saved to {final_output_filename}")

    print(f"Scraping completed. Data saved to {output_directory}.")