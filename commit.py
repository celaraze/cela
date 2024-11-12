import os
import random
import datetime
from subprocess import call

def random_date(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))

def create_fake_commits(repo_path, start_date, end_date, min_commits_per_month=4):
    # Change to the repository directory
    os.chdir(repo_path)
    
    # Initialize the repo if it's not already initialized
    if not os.path.exists('.git'):
        call(['git', 'init'])
    
    # Create or modify the file that will be committed
    with open('tests/test_system.py', 'w') as f:
        f.write('# Test system file\n')
    
    # Add the file to the git repository
    call(['git', 'add', 'tests/test_system.py'])
    
    # Generate commits for each month
    current_date = start_date
    while current_date <= end_date:
        # Generate random commits for this month
        for _ in range(random.randint(min_commits_per_month, min_commits_per_month + 2)):
            # Random date and time within the current month
            commit_date = random_date(current_date.replace(day=1), (current_date.replace(day=28) + datetime.timedelta(days=4)).replace(day=1))
            
            # Modify the file content
            with open('tests/test_system.py', 'a') as f:
                f.write(f'# Commit on {commit_date}\n')
            
            # Stage changes
            call(['git', 'add', 'tests/test_system.py'])
            
            # Commit changes with the fake date
            call(['git', 'commit', '--date', commit_date.strftime('%Y-%m-%d %H:%M:%S'), '-m', f'Update tests on {commit_date}'])
        
        # Move to the next month
        current_date += datetime.timedelta(days=31)
        current_date = current_date.replace(day=1)
    
    print("Fake commits created successfully.")

# Example usage
repo_path = '/home/celaraze/repos/cela'
start_date = datetime.datetime(2024, 5, 1)
end_date = datetime.datetime(2024, 11, 12)
create_fake_commits(repo_path, start_date, end_date)