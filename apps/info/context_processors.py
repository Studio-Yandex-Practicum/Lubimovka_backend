import datetime
import os

import git


def admin_index(request):
    extra_context = {}
    route = request.path.split("/")[1]
    if route == "admin":
        repo = git.Repo(os.getcwd())
        branch = repo.head.reference
        last_commit = str(branch.commit)[:7]
        commit_date = datetime.datetime.fromtimestamp(branch.commit.committed_date)
        last_tag = repo.tags[-1]
        tag = str(last_tag) if branch.commit == last_tag.commit else None
        environment = str(branch).split("/")[0]

        if environment == "master":
            if tag:
                extra_context["tag"] = tag
            extra_context["commit_date"] = commit_date
            extra_context["last_commit"] = last_commit
            extra_context["type"] = "master"
        elif environment == "develop":
            extra_context["commit_date"] = commit_date
            extra_context["last_commit"] = last_commit
            extra_context["type"] = "develop"
        else:
            extra_context["environment"] = environment
            extra_context["commit_date"] = commit_date
            extra_context["last_commit"] = last_commit
            extra_context["type"] = "test"

    return extra_context
