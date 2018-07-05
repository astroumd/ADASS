

all: students countries focus dinner tutorial

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
