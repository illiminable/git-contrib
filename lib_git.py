from git import Repo
from datetime import datetime
from os.path import splitext


def _to_datetime(timestamp):
    return datetime.fromtimestamp(int(timestamp))

def _display_date(timestamp):
    return _to_datetime(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def _accumulate_extension_by_author_stats(data, commit):
    root_daily_author_node = data["daily_by_author"]
    total_author_node = data["total_by_author"]
    commit_datetime = _to_datetime(commit.committed_date)
    commit_date = commit_datetime.date()
    date_node = root_daily_author_node.setdefault(commit_date, {})

    author = commit.author
    daily_author_node = date_node.setdefault(author, {})
    total_author_node = total_author_node.setdefault(author, {})

    for filename, stats in commit.stats.files.items():
        filename_no_ext, file_extension = splitext(filename)
        daily_extension_node = daily_author_node.setdefault(file_extension, {"file_count": 0, "insertions": 0, "deletions": 0, "file_set": set()})
        total_extension_node = total_author_node.setdefault(file_extension, {"file_count": 0, "insertions": 0, "deletions": 0, "file_set": set()})
        daily_extension_node['insertions'] += stats['insertions']
        daily_extension_node['deletions'] += stats['deletions']
        daily_extension_node['file_count'] += 1
        daily_extension_node['file_set'].add(filename.lower())
        total_extension_node['insertions'] += stats['insertions']
        total_extension_node['deletions'] += stats['deletions']
        total_extension_node['file_count'] += 1
        total_extension_node['file_set'].add(filename.lower())

    return data

def get_file_stats_by_author_by_day(repo, branch_name):
    commits = repo.iter_commits(branch_name)

    data = {"file_stats": { "daily_by_author": {}, "total_by_author": {}, "": {} }}
    for commit in commits:
        _accumulate_extension_by_author_stats(data["file_stats"], commit)

    return data