from github import Github

from dexi import config


g = Github(config.GITHUB_TOKEN, per_page=config.DEFAULT_PAGE_SIZE)


# for repo in g.get_user().get_repos():
#     print(repo.name)

repo = g.get_repo("slicelife/ros-service")
pulls = repo.get_pulls(state='open', sort='created', base='master')
for pr in pulls:
    import pdb
    pdb.set_trace()
    print(pr.number)
    print(pr.title)
    print(pr.created_at)
    print(pr.state)
    print(pr.updated_at)
    print(pr.url)
    print([r for r in pr.get_reviews()])



import pdb
pdb.set_trace()
