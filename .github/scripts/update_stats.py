import urllib.request
import json
import re
import os

def get_stats(username):
    headers = {'User-Agent': 'Mozilla/5.0'}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers['Authorization'] = f'token {token}'
        
    # Get user's own repos to calculate total forks
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    req = urllib.request.Request(repos_url, headers=headers)
    with urllib.request.urlopen(req) as response:
        repos = json.loads(response.read().decode())

    total_forks = sum(repo.get('forks_count', 0) for repo in repos)

    # Get repos starred by the user to calculate total stars given
    starred_url = f"https://api.github.com/users/{username}/starred?per_page=100"
    req_starred = urllib.request.Request(starred_url, headers=headers)
    with urllib.request.urlopen(req_starred) as response:
        starred = json.loads(response.read().decode())
        
    total_stars = len(starred)
    
    return total_stars, total_forks

def update_readme(stars, forks):
    readme_path = 'README.md'
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme = f.read()

    # Update stars badge
    readme = re.sub(
        r'(badge/STARS-)\d+(-black)',
        f'\\g<1>{stars:02d}\\g<2>',
        readme
    )
    
    # Update forks badge
    readme = re.sub(
        r'(badge/FORKS-)\d+(-black)',
        f'\\g<1>{forks:02d}\\g<2>',
        readme
    )

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme)

if __name__ == '__main__':
    username = 'biswa16-dev'
    stars, forks = get_stats(username)
    print(f"Total Stars: {stars}, Total Forks: {forks}")
    update_readme(stars, forks)
