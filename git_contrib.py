from git import Repo
from lib_git import get_file_stats_by_author_by_day

branch_name = "master"
repo = Repo('C:\Users\illiminable\Documents\src\GitPython')

stats = get_file_stats_by_author_by_day(repo, branch_name)

print "hello"



