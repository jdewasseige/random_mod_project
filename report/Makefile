COMPILER=latexmk
NAME=report

all: $(NAME).tex
	$(COMPILER) -pdf -pdflatex="pdflatex -shell-escape -enable-write18" \
		-use-make -auxdir=auxFile -outdir=auxFile $(NAME).tex ;
	cp auxFile/*.pdf ./
	
show: $(NAME).pdf
	make all;
	open $(NAME).pdf

clean:
	rm -rf ./auxFile
