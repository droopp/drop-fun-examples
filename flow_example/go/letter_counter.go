package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func main() {

	reader := bufio.NewReader(os.Stdin)

	flag.Parse()
	s := flag.Arg(0)

	f, _ := strconv.Atoi(s)

	for {

		//read
		msg, _ := reader.ReadString('\n')

		if msg == "" {

			os.Exit(0)
		}

		//log
		log.Print("get message :", msg)

		s := strings.Split(msg, ",")

		n := len(s[2])

		if n > f {

			//send
			fmt.Print("tag:exist,", strings.Join(s[1:], ","))

		} else {

			//send
			fmt.Print(strings.Join(s[1:], ","))

		}

	}

}
