

all: students countries focus dinner tutorial abstract

students:
	@echo Student/General
	@./students.py| sort | uniq -c

countries:
	@echo Countries
	@./countries.py|sort | uniq -c | sort -nr

focus:
	@echo Focus Demo
	@./focus.py|sort |uniq -c

dinner:
	@echo Dinner
	@./dinner.py|sort |uniq -c | sort -nr

tutorial:
	@echo Tutorial
	@./tutorial.py|sort |uniq -c | sort -nr

abstract:
	@echo Abstract
	@./abstract.py|sort |uniq -c | sort -nr
