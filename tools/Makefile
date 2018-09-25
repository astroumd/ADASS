

all: students countries dinner tutorial abstract focus comm demo financial companion proceedings date diet \
	adass-0 adass-1 adass-2 adass-3 count

students:
	@echo Student/General
	@./counter.py 1 |sort | uniq -c

countries:
	@echo Countries
	@./counter.py 12 |sort | uniq -c | sort -nr

dinner:
	@echo Dinner
	@./counter.py 23 |sort | uniq -c | sort -nr

tutorial:
	@echo Tutorial
	@./counter.py 22 |sort | uniq -c | sort -nr

abstract:
	@echo Abstract
	@./counter.py 28 |sort | uniq -c | sort -nr

abstract2:
	@echo Abstract2
	@./counter.py 29 demo financial companion

focus:
	@echo Focus DemoTalk
	@./counter.py 25 |sort | uniq -c

comm:
	@echo Commercial DemoTable
	@./counter.py 26 |sort | uniq -c | sort -nr

demo:
	@echo Astro DemoTable
	@./counter.py 27 |sort | uniq -c | sort -nr

financial:
	@echo Financial
	@./counter.py 18 |sort | uniq -c | sort -nr

companion:
	@echo Companion
	@./counter.py 19 |sort | uniq -c | sort -nr

proceedings:
	@echo Proceedings
	@./counter.py 20 |sort | uniq -c | sort -nr

date:
	@echo RegDate
	@./counter.py 0 |sort | uniq -c | sort -k 2

diet:
	@echo Diet
	@./counter.py 16 |sort | uniq -c | sort -nr


adass-0:
	./counter.py -1 > adass-0.txt

adass-1:
	./emails2018.py > adass-1.txt

adass-2:
	./adass2018.py > adass-2.txt

adass-3:
	./abstracts.py > adass-3.txt

count:
	@echo Counted `cat adass-0.txt | wc -l` participants

#       our dropbox keeps a pretty recent update to the 3 registration sheets
#       or grab the 3 files from our LOC google drive folder "registration" and
#       symlink with 'reg' since that's a hardcoded name here 
reg:
	ln -sf ~/Dropbox/adass2018 reg

# commit
gitci:
	git ci adass-0.txt adass-1.txt adass-2.txt adass-3.txt

# undo (shit happens)
gitco:
	git co adass-0.txt adass-1.txt adass-2.txt adass-3.txt

# get new/old names
diff:
	git diff adass-0.txt
