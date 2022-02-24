from re import I
import sys
import time as tt
from itertools import cycle

TESTCASE = sys.argv[1] if len(sys.argv) > 1 else ""
DEBUG = True

"""
    C: number of contributors
    P: number of projects
    contributors: K(name), V(contributor)
    projects: K(name), V(project)
"""


def main():
    # PARSE
    C, P = sys.stdin.readline().strip().split(" ")
    C, P = int(C), int(P)
    contributors = {}
    projects = {}

    for _ in range(C):
        name, N = sys.stdin.readline().strip().split(" ")
        N = int(N)
        skills = []
        for _ in range(N):
            innn = sys.stdin.readline().strip()
            print(innn)
            name, L = innn.split(" ")
            L = int(L)
            skills.append(Skill(name, L))
        contributors[name] = Contributor(name, skills)

    for _ in range(P):
        name, D, S, B, R = sys.stdin.readline().strip().split(" ")
        D, S, B, R = int(D), int(S), int(B), int(R)
        skills = []
        for _ in range(P):
            name, L = sys.stdin.readline().strip().split(" ")
            L = int(L)
            skills.append(Skill(name, L))
        projects[name] = Project(name, D, S, B, skills)

    for c in contributors:
        log(c)

    for p in projects:
        log(p)

    # SOLUTION


class Contributor:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Skill:
    def __init__(self, name, level):
        self.name = name
        self.leve = level

    def __str__(self):
        return ""

    def __repr__(self):
        return self.name


class Project:
    def __init__(self, name, duration, score, best_before, skills):
        self.name = name
        self.duration = duration
        self.score = score
        self.best_before = best_before
        self.skills = skills

    def __str__(self) -> str:
        return self.name


def log(message, force=False):
    if DEBUG or force:
        print(f"{TESTCASE:12.12}\t{message}")


if __name__ == "__main__":
    start = tt.perf_counter()
    log("------------------------ START", True)
    main()
    log(
        f"------------------------ FINISH @ {tt.perf_counter() - start:.6f}s", True)
