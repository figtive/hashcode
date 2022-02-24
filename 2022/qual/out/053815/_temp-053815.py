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

    contributors_skill = {}
    # contributors_skill[skill_name][skill_level][contributor_name] = the contributor obj
    # {css: {
    #   {2: maria}
    # }

    def bump_level(contributor, skill_name):
        curr_level = contributor.skills[skill_name].level
        contributor.skills[skill_name].level += 1
        del contributors_skill[skill_name][curr_level][contributor.name]
        if curr_level + 1 not in contributors_skill[skill_name]:
            contributors_skill[skill_name][curr_level + 1] = {}
        contributors_skill[skill_name][curr_level +
                                       1][contributor.name] = contributor

    for _ in range(C):
        name, N = sys.stdin.readline().strip().split(" ")
        N = int(N)
        skills = {}
        for _ in range(N):
            nameS, L = sys.stdin.readline().strip().split(" ")
            L = int(L)
            skills[nameS] = Skill(nameS, L)
        contributors[name] = Contributor(name, skills)
        # optimizer
        for _, s in skills.items():
            if s.name not in contributors_skill:
                contributors_skill[s.name] = {}
            if s.level not in contributors_skill[s.name]:
                contributors_skill[s.name][s.level] = {}
            contributors_skill[s.name][s.level][name] = contributors[name]

    for _ in range(P):
        name, D, S, B, R = sys.stdin.readline().strip().split(" ")
        D, S, B, R = int(D), int(S), int(B), int(R)
        skills = []
        for _ in range(R):
            nameS, L = sys.stdin.readline().strip().split(" ")
            L = int(L)
            skills.append(Skill(nameS, L))
        projects[name] = Project(name, D, S, B, skills)

    # log(contributors)
    # log(projects)

    # SOLUTION
    project_selected = []
    for T in range(50000):
        for _, project in projects.items():
            # check if project has not been selected
            if project.start_day < 0:
                for required_skill in project.skills:
                    for _, contributor in contributors.items():
                        # check if contributor is ready to work
                        if not contributor.pending_assignment and (contributor.current_project is None or contributor.current_project.start_day + contributor.current_project.duration > T):
                            for _, contributor_skill in contributor.skills.items():
                                if required_skill.name == contributor_skill.name:
                                    if contributor_skill.level >= required_skill.level:
                                        contributor.current_skill_name = required_skill.name
                                        contributor.current_project = project
                                        contributor.pending_assignment = True
                                        project.contributors.append(
                                            contributor)
                                        break
                            else:
                                continue
                            break
                if len(project.contributors) == len(project.skills):
                    project_selected.append(project)
                    for contributor in project.contributors:
                        # if previous project's required skill level is +1, bump skill level
                        bump_level(contributor, contributor.current_skill_name)
                        contributor.pending_assignment = False
                    project.start_day = T
                else:
                    for contributor in project.contributors:
                        contributor.current_skill_name = None
                        contributor.current_project = None
                        contributor.pending_assignment = False
                    project.contributors = []

    # OUTPUT
    print(len(project_selected), file=sys.stderr)
    for project in project_selected:
        print(project.name, file=sys.stderr)
        print(
            " ".join([c.name for c in project.contributors]), file=sys.stderr)


class Contributor:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills  # skill map
        self.current_project = None
        self.current_skill_name = None
        self.pending_assignment = False

    def __str__(self):
        return self.name + " " + str(self.skills)

    def __repr__(self):
        return self.name + " " + str(self.skills)


class Skill:
    def __init__(self, name, level):
        self.name = name
        self.level = level

    def __str__(self):
        return self.name + "@" + str(self.level)

    def __repr__(self):
        return self.name + "@" + str(self.level)


class Project:
    def __init__(self, name, duration, score, best_before, skills):
        self.name = name
        self.duration = duration
        self.score = score
        self.best_before = best_before
        self.skills = skills  # list of skills
        self.contributors = []
        self.start_day = -1

    def __str__(self) -> str:
        return self.name + " " + str(self.duration) + " " + str(self.score) + " " + str(self.best_before) + " " + str(self.skills)

    def __repr__(self) -> str:
        return self.name + " " + str(self.duration) + " " + str(self.score) + " " + str(self.best_before) + " " + str(self.skills)


def log(message, force=False):
    if DEBUG or force:
        print(f"{TESTCASE:20.20}\t{message}")


if __name__ == "__main__":
    start = tt.perf_counter()
    log("------------------------ START", True)
    main()
    log(
        f"------------------------ FINISH @ {tt.perf_counter() - start:.6f}s", True)
