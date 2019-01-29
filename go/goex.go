package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func main() {

	reader := bufio.NewReader(os.Stdin)

	for {

		//read
		text, _ := reader.ReadString('\n')

		//log
		log.Print("get message :", text)

		//send
		fmt.Print(text)
	}

}
