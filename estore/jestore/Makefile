
.PHONY: compile run debug build test


compile:
	@rm -rf bin/* && javac -g -d bin -cp lib/*:bin src/org/rt/*/*.java

run:
	@java -cp bin:lib/* org.rt.worker.Worker 10

debug:
	jdb -classpath bin:lib/* -sourcepath src org.rt.worker.Worker 10

build:
	@rm -rf bin/* && javac -d bin -cp lib/*:bin src/org/rt/*/*.java

build_c:
	sudo docker build -t droopp/jestore_async:0.1.0 .
	sudo docker push droopp/jestore_async:0.1.0

test:
	# @tr '\n' '\tncm\t' < test/data.d | java -cp bin:lib org.rt.worker.Worker
	@cat test/array_data.d | java -cp bin:lib org.rt.worker.Worker 10
