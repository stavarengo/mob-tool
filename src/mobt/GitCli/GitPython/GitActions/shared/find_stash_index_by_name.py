from git import Repo


def find_stash_index_by_name(repo: Repo, stash_name: str) -> int | None:
    stash_list = repo.git.stash('list').split('\n')
    for idx, stash in enumerate(stash_list):
        if stash_name in stash:
            return idx
    return None
