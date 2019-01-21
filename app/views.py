from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from django.views.generic import View
from django.core.management import call_command
from django.template import Template, Context

import os, io, csv

userCredentials = {
	'abc' : '0000'
}

players = []
index = 0

class Login(View):
	def get(self, request):
		html = render_to_string('login.html')
		return HttpResponse(html, status=200)

	def post(self, request):
		data = request.POST
		username = data['username']
		password = data['password']

		if username in userCredentials:
			if userCredentials[username] == password:
				return HttpResponse(render_to_string('landingPage.html'), status=200)
		
		return HttpResponse(render_to_string('invalidLogin.html'), status=200)

class PlayerFile(View):
	def post(self, request):
		global index, players
		index = 0
		players.clear()

		file = request.FILES

		if file:
			file = file['filename']
			if file.name[-3:] == 'csv':
				temp = file.read().decode('utf-8').split('\n')
				for p in temp:
					if len(p) > 1:
						p = p.rstrip('\r')
						players.append(p)
						print(p)
				print(players)

				context = {
					'name' : str(players[index])
				}
				return render(request, 'playerInfo.html', context, status=200)

		return HttpResponse('Please upload a valid csv file', status = 200)

class Player(View):
	def post(self, request):
		global index, players
			
		if(index < len(players)):
			# UPDATE THAT PLAYER INFO
			data = request.POST
			string = str(players[index]) + ',' + data['lastscore'] + ',' + data['balls'] + ',' + data['sixes']
			print(string)
			players[index] = string
			index = index + 1

			# IF MORE PLAYERS REMAINING
			if(index < len(players)):
				context = {
					'name' : str(players[index])
				}
				return render(request, 'playerInfo.html', context, status=200)
		return HttpResponse(render_to_string('exit.html'), status=200)

class Exit(View):
	def get(self, request):
		# ALL INFO COLLECTED, TERMINATE
		print(players)
		header = 'Player Name' + ',' + 'Last Game Score' + ',' + 'Balls Played' + ',' + '6s Hits'
		with open('final.csv', 'w') as final:
			final.write(header + '\n')

			for p in players:
				final.write(p + '\n')
		
		with open('final.csv', 'rb') as final:
			response = HttpResponse(final, content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename = final.csv'
			return response
