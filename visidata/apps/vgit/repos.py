from visidata import vd, VisiData, Sheet, Column, AttrColumn, date, vlen, asyncthread, Path, namedlist, PyobjSheet, modtime, AttrDict

from .gitsheet import GitSheet

@VisiData.api
def guess_git(vd, p):
    if (p/'.git').is_dir():
        return dict(filetype='git')


@VisiData.api
def open_git(vd, p):
    return GitRepos(p.name, source=p)


@VisiData.api
def git_repos(vd, p, args):
    return GitRepos(p.name, source=p)


class GitLinesColumn(Column):
    def __init__(self, name, cmd, *args, **kwargs):
        super().__init__(name, cache=True, **kwargs)
        cmdparts = cmd.split()
        if cmdparts[0] == 'git':
            cmdparts = cmdparts[1:]
        self.gitargs = cmdparts + list(args)

    def calcValue(self, r):
        gitdir = GitSheet(source=r).gitPath
        return list(self.sheet.git_lines('--git-dir', gitdir, *self.gitargs))


class GitAllColumn(GitLinesColumn):
    def calcValue(self, r):
        gitdir = GitSheet(source=r).gitPath
        return self.sheet.git_all('--git-dir', gitdir, *self.gitargs).strip()



class GitRepos(GitSheet):
    help = '''
        # git repos
        A list of git repositories under `{sheet.source}`

        - `Enter` to open the status sheet for the current repo
    '''
    rowtype = 'repos'  # rowdef: Path
    columns = [
        Column('repo', type=str, width=30),
        GitAllColumn('branch', 'git rev-parse --abbrev-ref HEAD', width=8),
        GitLinesColumn('stashes', 'git stash list', type=vlen, width=8),
        GitLinesColumn('cached', 'git diff --cached', type=vlen, width=8),
        GitLinesColumn('branches', 'git branch --no-color', type=vlen, width=8),
        Column('modtime', type=date, getter=lambda c,r: modtime(r)),
    ]
    nKeys = 1

    def iterload(self):
        import glob
        for fn in glob.glob('**/.git', root_dir=self.source, recursive=True):
            yield Path(fn).parent


    def openRow(self, row):
        return vd.open_git(row)

    def openCell(self, col, row):
        val = col.getValue(row)
        return PyobjSheet(getattr(val, '__name__', ''), source=val)
