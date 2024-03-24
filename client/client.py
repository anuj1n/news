import requests
import argparse

def login(url):
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    try:
        response = requests.post(url, data={'username': username, 'password': password})
        if response.status_code == 200:
            print("Login success")
        else:
            print("Login unsuccessful. Status code:", response.status_code)
    except requests.RequestException as e:
        print("An error occurred:", e)
    

def logout(url):
    response = requests.post(url)
    if response.status_code == 200:
        print("User logged out")
    else:
        print("No user logged in ", response.status_code)

def post_story(api_url):
        headline = input("Enter the headline of the story: ")
        category = input("Select the category of the story - pol art tech trivia: ")
        region = input("Select the region of the story - uk eu w: ")
        details = input("Enter the details of the story: ")
        payload = {
        "headline": headline,
        "category": category,
        "region": region,
        "details": details
         }
        
        response = requests.post(f"{api_url}/api/stories", json=payload)
        print(response.headers)
        if response.status_code == 201:
            print("Story posted successfully!")
        else:
            print("Failed to post the story. Error:", response.text)

def get_stories(api_url, params):
    response = requests.get(f"{api_url}/api/stories", params=params)
    if response.status_code == 200:
        stories = response.json().get('stories', [])
        for story in stories:
            print(story)  
    elif response.status_code == 404:
        print("No stories found.")
    else:
        print(f"Failed to fetch stories. Error: {response.text}")

def delete_story(api_url, story_key):
    response = requests.delete(f"{api_url}/api/stories/{story_key}/")
    print(response.text)

def register_to_directory(directory_url, agency_name, agency_url, agency_code):
    payload = {
        'agency_name': agency_name,
        'url': agency_url,
        'agency_code': agency_code
    }

    response = requests.post(f"{directory_url}/api/directory", data=payload)
    
    if response.status_code == 201:
        print("Registration successful!")
    else:
        print(f"Failed to register. Error: {response.text}")

def main():
    parser = argparse.ArgumentParser(description='Command-line news API client')
    parser.add_argument('-url', type=str, help='URL of the news API')
    parser.add_argument('-id', '--service_id', default=None, help='ID of the news service')
    parser.add_argument('-cat', '--category', default=None, help='News category')
    parser.add_argument('-reg', '--region', default=None, help='News region')
    parser.add_argument('-date', '--date', default=None, help='Date of the news (dd/mm/yyyy)')
    parser.add_argument('-command', choices=['login', 'logout', 'post', 'news', 'delete'], help='Command to execute')
    
    
    directory_url = "https://newssites.pythonanywhere.com"  
    agency_name = "Anujin Dorj News Agency"  
    agency_url = "https://ed20ad4.pythonanywhere.com"  
    agency_code = "AD03"  
    register_to_directory(directory_url, agency_name, agency_url, agency_code)

    args = parser.parse_args()
    api_url = args.url
    
    if args.command == 'login':
        login(api_url)
    if args.command == 'logout':
        logout(api_url)
    if args.command == 'post':
        post_story(api_url)
    if args.command == 'news':
        params = {}
        if args.category:
            params['story_cat'] = args.category
        if args.region:
            params['story_region'] = args.region
        if args.date:
            params['story_date'] = args.date
        get_stories(api_url, params)
    if args.command == 'delete':
        delete_story(api_url, args.story_key)
    
if __name__ == '__main__':
    main()