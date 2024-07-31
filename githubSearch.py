import requests
import sys


def search_github_projects(language, platform, page=1, per_page=10):
    search_url = 'https://api.github.com/search/repositories'
    query = f'language:{language} platform:{platform}'
    params = {
        'q': query,
        'sort': 'stars',
        'order': 'desc',
        'page': page,
        'per_page': per_page
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()

        results = response.json()
        if results['total_count'] == 0:
            print(f"No repositories found for language '{language}' and platform '{platform}'.")
            return False

        print(f"\nRepositories (Page {page}):")
        for item in results['items']:
            print(f"- {item['name']}: {item['html_url']}")
            print(f"  Stars: {item['stargazers_count']}, Description: {item['description']}")
            print()

        return len(results['items']) == per_page  # True if there might be more results

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub API: {e}")
        sys.exit(1)


def main():
    language = input("Enter the programming language: ")
    platform = input("Enter the platform: ")
    per_page = 10
    page = 1

    while True:
        has_more = search_github_projects(language, platform, page, per_page)

        if not has_more:
            print("No more repositories to display.")
            break

        choice = input("Do you want to see more repositories? (y/n): ").lower()
        if choice != 'y':
            break

        page += 1


if __name__ == "__main__":
    main()