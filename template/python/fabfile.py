import os
from pathlib import Path

from fabric import task

# cd to project dir
os.chdir(Path(__file__).parent.absolute())


@task
def dev_setup(c):
    c.run("pip install --require-hashes -r requirements.txt")
    c.run("pip install --no-deps --editable .")


@task
def generate_requirements(c):
    c.run("pip-compile -q -o requirements-prod.txt", pty=True)
    c.run("pip-compile -q -o requirements.txt --extra dev", pty=True)


@task
def update_package(c, package: str):  # no idea if this is the best approach
    c.run(f"pip-compile -P {package} -q -o requirements-prod.txt", pty=True)
    c.run(f"pip-compile -P {package} -q -o requirements.txt --extra dev", pty=True)
    print("""
!!! NEED TO RUN !!!
fab dev-setup
""")


@task
def mypy(c):
    c.run("mypy src", pty=True)


@task
def ruff(c):
    c.run("ruff check", pty=True)


@task
def test(c):
    c.run("pytest", pty=True)


@task(
    ruff,
    mypy,
    test,
)
def check(_):
    pass
