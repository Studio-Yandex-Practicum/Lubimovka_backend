import datetime
import os

import git


def admin_index(request):
    extra_context = {}
    if request.path != "/":
        route = request.path.split("/")[1]
        if route == "admin":
            repo = git.Repo(os.getcwd())
            branch = repo.head.reference
            last_commit = str(branch.commit)[:7]
            commit_date = datetime.datetime.fromtimestamp(branch.commit.committed_date)
            environment = str(branch).split("/")[0]

            extra_context["commit_date"] = commit_date
            extra_context["last_commit"] = last_commit
            extra_context["environment"] = environment

            if environment == "master":
                if repo.tags:
                    last_tag = repo.tags[-1]
                    tag = str(last_tag) if branch.commit == last_tag.commit else None
                    if tag:
                        extra_context["tag"] = tag
            elif environment != "develop":
                extra_context["branch"] = str(branch)
                extra_context["environment"] = "test"

        return extra_context
