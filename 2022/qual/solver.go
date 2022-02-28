package main

import (
	"bufio"
	"errors"
	"fmt"
	llog "log"
	"os"
	"sort"
	"time"
)

var (
	TESTCASE string
	DEBUG    = true
)

func main() {
	start := time.Now()
	TESTCASE = os.Args[1]

	log("------------------------ START", true)
	err := Main(os.Args[1:])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		log(fmt.Sprintf("------------------------ FAIL @ %s", time.Since(start)), true)
		os.Exit(1)
	}
	log(fmt.Sprintf("------------------------ FINISH @ %s", time.Since(start)), true)
}

type Contributor struct {
	Name              string
	Skills            map[string]*Skill
	CurrentProject    *Project
	CurrentSkillName  string
	PendingAssignment bool
	ShouldBump        bool
}

func NewContributor() *Contributor {
	return &Contributor{
		Skills: make(map[string]*Skill),
	}
}

type Skill struct {
	Name  string
	Level int
}

func NewSkill() *Skill {
	return &Skill{}
}

type Project struct {
	Name         string
	Duration     int
	Score        int
	BestBefore   int
	Skills       []*Skill
	Contributors []*Contributor
	StartDay     int
}

func NewProject() *Project {
	return &Project{
		Skills:       make([]*Skill, 0),
		Contributors: make([]*Contributor, 0),
		StartDay:     -1,
	}
}

// ByProject returns true if p1 < p2 semantically.
type ByProject func(p1, p2 *Project) bool

type projectSorter struct {
	projects []*Project
	by       ByProject
}

func (by ByProject) Stable(projects []*Project) {
	s := projectSorter{
		projects: projects,
		by:       by,
	}

	sort.Stable(s)
}

func (s projectSorter) Len() int {
	return len(s.projects)
}

func (s projectSorter) Less(i, j int) bool {
	return s.by(s.projects[i], s.projects[j])
}

func (s projectSorter) Swap(i, j int) {
	s.projects[i], s.projects[j] = s.projects[j], s.projects[i]
}

func Main(args []string) error {
	scanner := bufio.NewScanner(os.Stdin)

	var (
		C, P         int
		contributors map[string]*Contributor
		projects     []*Project

		contributorSLevel map[string]map[int]map[string]*Contributor
		contributorSkill  map[string][]*Contributor
	)

	bumpLevel := func(contributor *Contributor, skillName string) {
		skill := contributor.Skills[skillName]
		delete(contributorSLevel[skill.Name][skill.Level], contributor.Name)

		skill.Level++

		if _, ok := contributorSLevel[skill.Name][skill.Level]; !ok {
			contributorSLevel[skill.Name][skill.Level] = make(map[string]*Contributor)
		}
		contributorSLevel[skill.Name][skill.Level][contributor.Name] = contributor

	}

	contributors = make(map[string]*Contributor)
	projects = make([]*Project, 0)
	contributorSLevel = make(map[string]map[int]map[string]*Contributor)
	contributorSkill = make(map[string][]*Contributor)

	err := readline(scanner, "%d %d", &C, &P)
	if err != nil {
		panic(err)
	}

	for c := 0; c < C; c++ {
		contributor := NewContributor()
		var N int
		err = readline(scanner, "%s %d", &contributor.Name, &N)
		if err != nil {
			panic(err)
		}

		for n := 0; n < N; n++ {
			skill := NewSkill()
			err = readline(scanner, "%s %d", &skill.Name, &skill.Level)
			if err != nil {
				panic(err)
			}

			// optimizer
			if _, ok := contributorSLevel[skill.Name]; !ok {
				contributorSLevel[skill.Name] = make(map[int]map[string]*Contributor)
			}
			if _, ok := contributorSLevel[skill.Name][skill.Level]; !ok {
				contributorSLevel[skill.Name][skill.Level] = make(map[string]*Contributor)
			}
			contributorSLevel[skill.Name][skill.Level][contributor.Name] = contributor
			if _, ok := contributorSkill[skill.Name]; !ok {
				contributorSkill[skill.Name] = make([]*Contributor, 0)
			}
			contributorSkill[skill.Name] = append(contributorSkill[skill.Name], contributor)

			contributor.Skills[skill.Name] = skill
		}

		contributors[contributor.Name] = contributor
	}

	for p := 0; p < P; p++ {
		project := NewProject()
		var R int
		err = readline(scanner, "%s %d %d %d %d", &project.Name, &project.Duration, &project.Score, &project.BestBefore, &R)
		if err != nil {
			panic(err)
		}

		for r := 0; r < R; r++ {
			skill := NewSkill()
			err = readline(scanner, "%s %d", &skill.Name, &skill.Level)
			if err != nil {
				panic(err)
			}
			project.Skills = append(project.Skills, skill)
		}

		projects = append(projects, project)
	}

	// TODO: heuristics

	MAX_T := 0
	switch TESTCASE {
	case "a_an_example":
		MAX_T = 50000
		ByProject(func(p1, p2 *Project) bool {
			return p1.BestBefore < p2.BestBefore
		}).Stable(projects)
		ByProject(func(p1, p2 *Project) bool {
			return p1.Score > p2.Score
		}).Stable(projects)
	case "b_better_start_small":
		MAX_T = 50000
		ByProject(func(p1, p2 *Project) bool {
			return p1.BestBefore < p2.BestBefore
		}).Stable(projects)
		ByProject(func(p1, p2 *Project) bool {
			return p1.Score > p2.Score
		}).Stable(projects)
		ByProject(func(p1, p2 *Project) bool {
			return p1.Duration < p2.Duration
		}).Stable(projects)
	case "c_collaboration":
		MAX_T = 50000
		ByProject(func(p1, p2 *Project) bool {
			return p1.BestBefore < p2.BestBefore
		}).Stable(projects)
		ByProject(func(p1, p2 *Project) bool {
			return p1.Score > p2.Score
		}).Stable(projects)
	case "d_dense_schedule":
		MAX_T = 50000
		ByProject(func(p1, p2 *Project) bool {
			return p1.BestBefore < p2.BestBefore
		}).Stable(projects)
		ByProject(func(p1, p2 *Project) bool {
			return p1.Score > p2.Score
		}).Stable(projects)
	case "e_exceptional_skills":
		MAX_T = 50000
		ByProject(func(p1, p2 *Project) bool {
			return p1.BestBefore < p2.BestBefore
		}).Stable(projects)
		ByProject(func(p1, p2 *Project) bool {
			return p1.Score > p2.Score
		}).Stable(projects)
	case "f_find_great_mentors":
		MAX_T = 50000
		ByProject(func(p1, p2 *Project) bool {
			return p1.BestBefore < p2.BestBefore
		}).Stable(projects)
		ByProject(func(p1, p2 *Project) bool {
			return p1.Score > p2.Score
		}).Stable(projects)
	}

	// SOLUTION
	projectSelected := make([]*Project, 0)
	for T := 0; T < MAX_T; T++ {
		if T%1000 == 0 {
			log(fmt.Sprintf("T: %d/%d (%.2f%%)", T, MAX_T, float32(T)/float32(MAX_T)*100))
		}
		for _, project := range projects {
			// check if project has not been selected
			if project.StartDay < 0 && project.BestBefore-int(0.80*float32(project.Duration)) > T {
				for _, requiredSkill := range project.Skills {
					for _, contributor := range contributorSkill[requiredSkill.Name] {
						// check if contributor is ready to work
						if !contributor.PendingAssignment && (contributor.CurrentProject == nil || contributor.CurrentProject.StartDay+contributor.CurrentProject.Duration >= T) {
							willAssign := false
							if contributor.Skills[requiredSkill.Name].Level >= requiredSkill.Level {
								willAssign = true
							} else if contributor.Skills[requiredSkill.Name].Level >= requiredSkill.Level-1 {
								for _, mentor := range project.Contributors {
									if skill, ok := mentor.Skills[requiredSkill.Name]; ok && skill.Level >= requiredSkill.Level {
										willAssign = true
										break
									}
								}
							}

							if willAssign {
								contributor.CurrentSkillName = requiredSkill.Name
								contributor.CurrentProject = project
								contributor.PendingAssignment = true
								contributor.ShouldBump = contributor.Skills[requiredSkill.Name].Level <= requiredSkill.Level
								project.Contributors = append(project.Contributors, contributor)
								break
							}
						}
					}
				}

				if len(project.Contributors) == len(project.Skills) {
					projectSelected = append(projectSelected, project)
					for _, contributor := range project.Contributors {
						if contributor.ShouldBump {
							bumpLevel(contributor, contributor.CurrentSkillName)
						}
						contributor.PendingAssignment = false
					}
					project.StartDay = T
				} else {
					for _, contributor := range project.Contributors {
						contributor.CurrentSkillName = ""
						contributor.CurrentProject = nil
						contributor.PendingAssignment = false
						contributor.ShouldBump = false
					}
				}
			}
		}
	}

	// OUTPUT
	fmt.Println(len(projectSelected))
	for _, project := range projectSelected {
		fmt.Println(project.Name)
		for i, contributor := range project.Contributors {
			fmt.Print(contributor.Name)
			if i != len(project.Contributors)-1 {
				fmt.Print(" ")
			} else {
				fmt.Println()
			}
		}
	}

	return nil
}

func readline(scanner *bufio.Scanner, format string, a ...interface{}) error {
	var line string
	if scanner.Scan() {
		line = scanner.Text()
	} else {
		return errors.New("readline: reached EOF")
	}

	_, err := fmt.Sscanf(line, format, a...)
	if err != nil {
		return err
	}

	return nil
}

func log(msg string, force ...bool) {
	if DEBUG || (len(force) > 0 && force[0]) {
		llog.Printf("%20.20s %s\n", TESTCASE, msg)
	}
}

func vlog(msg string, force ...bool) {
	if DEBUG || (len(force) > 0 && force[0]) {
		log(fmt.Sprintf("%#v", msg), force...)
	}
}
