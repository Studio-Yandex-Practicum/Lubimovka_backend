import datetime
import os

import git


def admin_versioning(request):
    extra_context = {}
    if request.path[1:6] == "admin":
        repo = git.Repo(os.getcwd())
        branch = repo.head.reference
        last_commit = str(branch.commit)[:7]
        commit_date = datetime.datetime.fromtimestamp(branch.commit.committed_date)

        extra_context["commit_date"] = commit_date
        extra_context["last_commit"] = last_commit
        extra_context["branch"] = str(branch)
        if repo.tags:
            last_tag = repo.tags[-1]
            tag = str(last_tag) if branch.commit == last_tag.commit else None
            if tag:
                extra_context["tag"] = tag

        return extra_context
