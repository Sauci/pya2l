import os.path

from mktestdocs import check_md_file


def test_markdown():
    check_md_file(fpath=os.path.join(os.path.dirname(__file__), '..', 'README.md'), memory=True)
