package main

import (
	"bufio"
	"errors"
	"fmt"
	llog "log"
	"os"
	"time"
)

var (
	TESTCASE string
	DEBUG    = false
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

func Main(args []string) error {
	scanner := bufio.NewScanner(os.Stdin)

	var (
		C, P int
	)

	err := readline(scanner, "%d %d", &C, &P)
	if err != nil {
		return err
	}

	// TODO

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
