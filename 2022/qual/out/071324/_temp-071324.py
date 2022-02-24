from math import floor
import sys
import time as tt

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
    projects = []

    contributors_s_level = {}
    # contributors_s_level[skill_name][skill_level][contributor_name] = the contributor obj
    # {css: {
    #   {2: maria}
    # }
    contributors_skill = {}
    # contributors_skill[contributor_name] = the contributor's name

    def bump_level(contributor, skill_name):
        curr_level = contributor.skills[skill_name].level
        contributor.skills[skill_name].level += 1
        del contributors_s_level[skill_name][curr_level][contributor.name]
        if curr_level + 1 not in contributors_s_level[skill_name]:
            contributors_s_level[skill_name][curr_level + 1] = {}
        contributors_s_level[skill_name][curr_level +
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
            if s.name not in contributors_s_level:
                contributors_s_level[s.name] = {}
            if s.level not in contributors_s_level[s.name]:
                contributors_s_level[s.name][s.level] = {}
            contributors_s_level[s.name][s.level][name] = contributors[name]
            if s.name not in contributors_skill:
                contributors_skill[s.name] = []
            contributors_skill[s.name].append(name)

    for _ in range(P):
        name, D, S, B, R = sys.stdin.readline().strip().split(" ")
        D, S, B, R = int(D), int(S), int(B), int(R)
        skills = []
        for _ in range(R):
            nameS, L = sys.stdin.readline().strip().split(" ")
            L = int(L)
            skills.append(Skill(nameS, L))
        projects.append(Project(name, D, S, B, skills))

    MAX_T = 0
    if TESTCASE == "a_an_example":
        MAX_T = 50_000
        projects.sort(key=lambda x: x.best_before, reverse=False)
        projects.sort(key=lambda x: x.score, reverse=True)
    if TESTCASE == "b_better_start_small":
        MAX_T = 50_000
        projects.sort(key=lambda x: x.best_before, reverse=False)
        projects.sort(key=lambda x: x.score, reverse=True)
        projects.sort(key=lambda x: x.duration, reverse=False)
    if TESTCASE == "c_collaboration":
        MAX_T = 50_000
        projects.sort(key=lambda x: x.best_before, reverse=False)
        projects.sort(key=lambda x: x.score, reverse=True)
    if TESTCASE == "d_dense_schedule":
        MAX_T = 50_000
        projects.sort(key=lambda x: x.best_before, reverse=False)
        projects.sort(key=lambda x: x.score, reverse=True)
    if TESTCASE == "e_exceptional_skills":
        MAX_T = 50_000
        projects.sort(key=lambda x: x.best_before, reverse=False)
        projects.sort(key=lambda x: x.score, reverse=True)
    if TESTCASE == "f_find_great_mentors":
        MAX_T = 50_000
        projects.sort(key=lambda x: x.best_before, reverse=False)
        projects.sort(key=lambda x: x.score, reverse=True)

    # SOLUTION
    project_selected = []
    for T in range(MAX_T):
        if T % 1000 == 0:
            log(f"T: {T}/{MAX_T} ({T/MAX_T*100:.2f}%)")
        for project in projects:
            # check if project has not been selected
            if project.start_day < 0 and project.best_before - floor(0.80 * project.duration) > T:
                for required_skill in project.skills:
                    for contributor_name in contributors_skill[required_skill.name]:
                        contributor = contributors[contributor_name]
                        # check if contributor is ready to work
                        if not contributor.pending_assignment and (contributor.current_project is None or contributor.current_project.start_day + contributor.current_project.duration >= T):
                            will_be_assigned = False
                            if contributor.skills[required_skill.name].level >= required_skill.level:
                                will_be_assigned = True
                            elif contributor.skills[required_skill.name].level >= required_skill.level - 1:
                                for mentor in project.contributors:
                                    if required_skill.name in mentor.skills and mentor.skills[required_skill.name].level >= required_skill.level:
                                        will_be_assigned = True
                                        break
                            if will_be_assigned:
                                contributor.current_skill_name = required_skill.name
                                contributor.current_project = project
                                contributor.pending_assignment = True
                                contributor.should_bump = contributor.skills[
                                    required_skill.name].level <= required_skill.level
                                project.contributors.append(contributor)
                                break

                if len(project.contributors) == len(project.skills):
                    project_selected.append(project)
                    for contributor in project.contributors:
                        # if previous project's required skill level is +1, bump skill level
                        if contributor.should_bump:
                            bump_level(
                                contributor, contributor.current_skill_name)
                        contributor.pending_assignment = False
                    project.start_day = T
                else:
                    for contributor in project.contributors:
                        contributor.current_skill_name = None
                        contributor.current_project = None
                        contributor.pending_assignment = False
                        contributor.should_bump = False
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
        self.should_bump = False

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
