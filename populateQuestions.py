from random import sample
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netwars.settings')

import django
django.setup()

from ncqs.models import Question

def populate_test():
	question = "this  is my first question"
	choice_correct = "cchoice"
	choice1 = "choice 1"
	choice2 = 'choice 2'
	choice3 = 'choice3'
	qtype = 'EASY';
	Question.objects.get_or_create(question = question, choice_correct=choice_correct, choice1= choice1, choice2 = choice2,
	 choice3 = choice3, question_type = qtype)

	question = "this  is my second question"
	choice_correct = "cchoice"
	choice1 = "choice 1"
	choice2 = 'choice 2'
	choice3 = 'choice3'
	qtype = 'HARD';
	Question.objects.get_or_create(question = question, choice_correct=choice_correct, choice1= choice1, choice2 = choice2,
	 choice3 = choice3, question_type = qtype)

def getRandomQuestion():
	question = "What no. am i thinking of ?"
	choices = sample(range(1, 10000), 4)
	cchoice = choices[0]
	choices = choices[1:]
	return (question, choices, cchoice)

def getRandomHardQuestion():
	question = "What no. MMR is thinking of ?"
	choices = sample(range(1, 3000), 4)
	cchoice = choices[0]
	choices = choices[1:]
	return (question, choices, cchoice)



def populate_easy():
	for i in range(150):
		question, choices, cchoice = getRandomQuestion()
		Question.objects.get_or_create(question = question, choice_correct=cchoice, choice1= choices[0], choice2 = choices[1],
		 choice3 = choices[2])

def populate_hard():
	for i in range(50):
		question, choices, cchoice = getRandomHardQuestion()
		Question.objects.get_or_create(question = question, choice_correct=cchoice, choice1= choices[0], choice2 = choices[1],
		 choice3 = choices[2], question_type ="HARD")



if __name__ == '__main__':
	populate_hard();