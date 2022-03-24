import pygame
from pygame.locals import *

pygame.init()

# VARIÁVEIS DE VALOR CONSTANTE

LARGURA = 800	
ALTURA =  600
display_surface = pygame.display.set_mode((LARGURA, ALTURA ))
pygame.display.set_caption('Damas')
image = pygame.image.load(r'C:\...\damas 800x600.jpg')

DARKGRAY = (64,64,64)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (100, 100, 100)
VERMELHO = (120, 0, 0)
VERDE_ESCURO = (0, 120, 0)
VERDE_CLARO = (0, 255, 0)
VERMELHO_CLARO = (255, 0, 0)
AZUL = (0, 0, 255)
COR_FUNDO = (54, 54, 54)
COR_TABULEIRO = (0, 31, 0)

# INICIANDO PROGRAMAÇÃO DO DISPLAY

display = pygame.display.set_mode((800, 600)) #Define o tamanho da janela e da escala de resolução do jogo 
pygame.display.set_caption('Jogo de Damas')
pygame.font.init()
clock = pygame.time.Clock()

# Classe principal

class Jogo:
	# Classe para tomar conta do status do jogo, que contem a matriz e peças do tabuleiro definida
	def __init__(self):
		self.status = 'Jogando'
		self.turno = 1
		self.jogadores = ('x', 'o')
		self.cedula_selecionada = None
		self.pulando = False
		self.matriz_jogadores = [['-','x','-','x','-','x','-','x'],
							    ['x','-','x','-','x','-','x','-'],
				  			    ['-','x','-','x','-','x','-','x'],
							    ['-','-','-','-','-','-','-','-'],
							    ['-','-','-','-','-','-','-','-'],
							    ['o','-','o','-','o','-','o','-'],
							    ['-','o','-','o','-','o','-','o'],
							    ['o','-','o','-','o','-','o','-']]

	
	def avalia_clique(self, pos):
		turno = self.turno % 2  #Verifica turno
		if self.status == "Jogando":
			linha, coluna = linha_clicada(pos), coluna_clicada(pos) # verifica se da para a peça pular para frente
			if self.cedula_selecionada:
				movimento = self.is_movimento_valido(self.jogadores[turno], self.cedula_selecionada, linha, coluna)
				if movimento[0]:
					self.jogar(self.jogadores[turno], self.cedula_selecionada, linha, coluna, movimento[1])
				elif linha == self.cedula_selecionada[0] and coluna == self.cedula_selecionada[1]:
					movs = self.movimento_obrigatorio(self.cedula_selecionada)
					if movs[0] == []:
						if self.pulando:
							self.pulando = False
							self.proximo_turno()
					self.cedula_selecionada = None
			else:#mostra a celula selecionada e mostra que nao tem mais movimento pra aquele turno pois ja foi feito o movimento
				if self.matriz_jogadores[linha][coluna].lower() == self.jogadores[turno]:
					self.cedula_selecionada = [linha, coluna]

	# VERIFICANDO SE UM MOVIMENTO REALIZADO PELO JOGADOR É VÁLIDO
	def is_movimento_valido(self, jogador, localizacao_cedula, linha_destino, coluna_destino):

		linha_originaria = localizacao_cedula[0]
		coluna_originaria = localizacao_cedula[1]

		obrigatorios = self.todos_obrigatorios()

		if obrigatorios != {}:# verifica se movimento obrigatorio é nulo se for nulo verifica se o movimento desejado é possível
			if (linha_originaria, coluna_originaria) not in obrigatorios:
				return False, None
			elif [linha_destino, coluna_destino] not in obrigatorios[(linha_originaria, coluna_originaria)]:
				return False, None

		movimento, pulo = self.movimentos_possiveis(localizacao_cedula)
		#Caso o movimento for possivel, retorna o movimento e se o jogar mover peca ele executa o movimento
		if [linha_destino, coluna_destino] in movimento:
			if pulo:
				if len(pulo) == 1:
					return True, pulo[0]
				else:
					for i in range(len(pulo)):
						if abs(pulo[i][0] - linha_destino) == 1 and abs(pulo[i][1] - coluna_destino) == 1:
							return True, pulo[i]

			if self.pulando:
				return False, None

			return True, None

		return False, None
		

	# RETORNA TODOS OS MOVIMENTOS OBRIGATÓRIOS DE UM TURNO
	def todos_obrigatorios(self): #verifica se tem movimento obrigatório, verificando por uma área proxima a peca
		todos = {}

		for r in range(len(self.matriz_jogadores)):
			for c in range(len(self.matriz_jogadores[r])):
				ob, pulos = self.movimento_obrigatorio((r, c))
				if  ob != []:
					todos[(r, c)] = ob
					

		return todos
		
	# RETORNA SE EXISTE UM MOVIMENTO POSSIVEL A SE FAZER COM A PEÇA
	def existe_possivel(self):#função que verifica se tem algum movimento possível  por uma área proxima a peça verificando a linha e a coluna se contem retorna true caso nao haja false
		for l in range(len(self.matriz_jogadores)):
			for c in range(len(self.matriz_jogadores[l])):
				if self.movimentos_possiveis((l, c))[0]:
					return True
		return False

	# RETORNA OS MOVIMENTOS OBRIGATÓRIOS DE UMA PEÇA QUE PODE SER JOGADA EM DETERMINADO TURNO
	def movimento_obrigatorio(self, localizacao_cedula): #Função que retorna os movimentos obrigatorios e executa seguindo a orientação do jogador
		obrigatorios = []
		posicao_cedula_pulada = []

		l = localizacao_cedula[0]
		c = localizacao_cedula[1]

		jogador = self.jogadores[self.turno % 2]
		index = self.jogadores.index(jogador)

		array = [jogador.lower(), jogador.upper(), '-']

		if self.matriz_jogadores[l][c].islower() and self.matriz_jogadores[l][c] == jogador and \
		self.turno % 2 == index:
				if l > 0: #Verifica se linha e coluna estão seguindo o tamanho da matriz para que não saia do tabuleiro
					if c < 7:#movimento Obrigatorio para a Direita peca branca 
						if self.matriz_jogadores[l - 1][c + 1].lower() not in array and jogador=='o':
							l_x = l - 1
							l_c = c + 1
							if l_x - 1 >= 0 and l_c + 1 <= 7:#comer peça a direita 
								if self.matriz_jogadores[l_x - 1][l_c + 1] == '-':
									obrigatorios.append([l_x - 1, l_c + 1])
									posicao_cedula_pulada.append((l_x, l_c))
					if c > 0:#movimento peca branca esquerda						#and jogador=='o ou x' bloqueia comer para traz
						if self.matriz_jogadores[l - 1][c - 1].lower() not in array and jogador=='o':
							l_x = l - 1
							l_c = c - 1
							if l_x - 1 >= 0 and l_c - 1 >= 0:#comer peça a esquerda
								if self.matriz_jogadores[l_x - 1][l_c - 1] == '-':
									obrigatorios.append([l_x - 1, l_c - 1])
									posicao_cedula_pulada.append((l_x, l_c))
							
				if l < 7:#Verifica se linha e coluna estão seguindo o tamanho da matriz para que não saia do tabuleiro
					if c < 7:#movimento Obrigatorio para a direta peca preta
						if self.matriz_jogadores[l + 1][c + 1].lower() not in array and jogador=='x':
							l_x = l + 1
							l_c = c + 1

							if l_x + 1 <= 7 and l_c + 1 <= 7:#comer peça direita
								if self.matriz_jogadores[l_x + 1][l_c + 1] == '-':
									obrigatorios.append([l_x + 1, l_c + 1])
									posicao_cedula_pulada.append((l_x, l_c))
					if c > 0:#movimento Obrigatorio para a esquerda peca preta 
						if self.matriz_jogadores[l + 1][c - 1].lower() not in array and jogador=='x':
							l_x = l + 1
							l_c = c - 1

							if l_x + 1 <= 7 and l_c - 1 >= 0:#comer peça esquerda
								if self.matriz_jogadores[l_x + 1][l_c - 1] == '-':
									obrigatorios.append([l_x + 1, l_c - 1])
									posicao_cedula_pulada.append((l_x, l_c))

		elif self.matriz_jogadores[l][c].isupper() and self.matriz_jogadores[l][c] == jogador.upper() and \
		self.turno % 2 == index:
		#retorna se ainda tem movimento obrigatório para fazer
			#MOVIMENTAÇÃO DA DAMA PARA COMER PEÇAS
			if not self.pulando and (jogador.lower() == 'x' and l !=8 )  or (jogador.lower() == 'o' and l != -1)  : #foi colocado diferente ou igual a 8 e diferente igual a -1 para poder comer se virar dama a partir da casa de dama e se transformar dama nao come outra peca para na casa coroação
				conta_linha = l
				conta_coluna = c
				while True:
					if conta_linha - 1 < 0 or conta_coluna - 1 < 0: break #verifica linha e coluna para não passar do tamanho da matriz 
					else:
						if self.matriz_jogadores[conta_linha - 1][conta_coluna - 1] not in array:
							l_x = conta_linha - 1
							l_c = conta_coluna - 1

							if l_x - 1 >= 0 and l_c - 1 >= 0:# Se linha e coluna maior ou igual a 0  seguindo os padroes  se movimento for feito seta a casa vazia e move a peça para local desejado
								if self.matriz_jogadores[l_x - 1][l_c - 1] == '-':
									posicao_cedula_pulada.append((l_x, l_c))
									while True:
										if l_x - 1 < 0 or l_c - 1 < 0:
											break
										else:
											if self.matriz_jogadores[l_x - 1][l_c - 1] == '-':
												obrigatorios.append([l_x - 1, l_c - 1])
											else:
												break
										l_x -= 1
										l_c -= 1
							break
					conta_linha -= 1
					conta_coluna -= 1

				conta_linha = l
				conta_coluna = c	
				#MOVIMENTOS OBRIGATÓRIOS QUANDO A PEÇA SE TRANSFORMA EM DAMA
				while True:
					if conta_linha - 1 < 0 or conta_coluna + 1 > 7: break
					else:
						if self.matriz_jogadores[conta_linha - 1][conta_coluna + 1] not in array:
							l_x = conta_linha - 1
							l_c = conta_coluna + 1
							#Verifica se tem mais de uma jogada obrigatoria se linha for maior ou igual a 0 ou coluna for menor que 7 
							if l_x - 1 >= 0 and l_c + 1 <= 7:
								if self.matriz_jogadores[l_x - 1][l_c + 1] == '-':# Se matriz linha -1 e coluna +1 estiver vazia mostra posicao que pode ser movimentada a peca
									posicao_cedula_pulada.append((l_x, l_c))
									while True:
										if l_x - 1 < 0 or l_c + 1 > 7: #verifica se não esta passando do limite da matriz se passar para
											break
										else:# se nao mostra se tem movimento obrigatório 
											if self.matriz_jogadores[l_x -1][l_c + 1] == '-':
												obrigatorios.append([l_x - 1, l_c + 1])
											else:
												break
										l_x -= 1
										l_c += 1
							break
					conta_linha -= 1
					conta_coluna += 1

				conta_linha = l
				conta_coluna = c
				while True:
					if conta_linha + 1 > 7 or conta_coluna + 1 > 7: break #conta linha e coluna se for maior que  7 para
					else:# se nao verifica se linha e coluna +1 tem movimento	
						if self.matriz_jogadores[conta_linha + 1][conta_coluna + 1] not in array:
							l_x = conta_linha + 1
							l_c = conta_coluna + 1
							if l_x + 1 <= 7 and l_c + 1 <= 7:#verifica se tem mais de uma jogada obrigatoria se linha ou coluna for menor ou igual a 7 retorna movimento obrigatorio
								if self.matriz_jogadores[l_x + 1][l_c + 1] == '-':# verifica se a casa objetiva esteja vazia se sim, pula pra casa desejada
									posicao_cedula_pulada.append((l_x, l_c))
									while True: #condição se tiver mais de um movimento obrigatorio ai repete ate acabar os movimentos obrigatórios
										if l_x + 1 > 7 or l_c + 1 > 7:
											break
										else:
											if self.matriz_jogadores[l_x + 1][l_c + 1] == '-':
												obrigatorios.append([l_x + 1, l_c + 1])
											else:
												break
										l_x += 1
										l_c += 1
							break
					conta_linha += 1
					conta_coluna += 1

				conta_linha = l
				conta_coluna = c
				while True:
					if conta_linha + 1 > 7 or conta_coluna - 1 < 0: break #Verifica se linha é maior que 7 e coluna é menor 0
					else:
						if self.matriz_jogadores[conta_linha + 1][conta_coluna - 1] not in array: #Verifica se linha +1 e coluna -1 se tem algo nela 
							l_x = conta_linha + 1
							l_c = conta_coluna - 1
							if l_x + 1 <= 7 and l_c - 1 >= 0: #movimentos obrigatorios quando linha for menor ou igual a 7 e coluna maior ou igual a 0
								if self.matriz_jogadores[l_x + 1][l_c - 1] == '-': # Verifica se casa destino esta vazia  e retorna caso peca pule para casa desejada
									posicao_cedula_pulada.append((l_x, l_c))
									while True:# retorna a função para repetição caso tenha movimento obrigatório
										if l_x + 1 > 7 or l_c - 1 < 0:
											break
										else:
											if self.matriz_jogadores[l_x + 1][l_c - 1] == '-':
												obrigatorios.append([l_x + 1, l_c - 1])
											else:
												break
										l_x += 1
										l_c -= 1
							break
					conta_linha += 1
					conta_coluna -= 1

		return obrigatorios, posicao_cedula_pulada

	# MOSTRA OS MOVIMENTOS POSSÍVEIS DE UMA PEÇA SELECIONADA
	def movimentos_possiveis(self, localizacao_cedula):
		movimentos, pulos = self.movimento_obrigatorio(localizacao_cedula)

		if movimentos == []:
			linha_atual = localizacao_cedula[0]
			coluna_atual = localizacao_cedula[1]
		#Move para baixo da matriz
			if self.matriz_jogadores[linha_atual][coluna_atual].islower(): 
				if self.matriz_jogadores[linha_atual][coluna_atual] == 'o':
					if linha_atual > 0:
						if coluna_atual < 7:#se coluna for maior que 0 permite mover peca para uma coluna  que seja menor que 0 se a linha for menor que 7// movimentação para a direita peça branca
							if self.matriz_jogadores[linha_atual - 1][coluna_atual + 1] == '-':
								movimentos.append([linha_atual - 1, coluna_atual + 1])
						if coluna_atual > 0:#se coluna for maior que 0 permite mover peca para uma coluna  que seja menor que 0 se a linha for maior que 0 // movimentação para a esquerda peça branca
							if self.matriz_jogadores[linha_atual - 1][coluna_atual - 1] == '-':
								movimentos.append([linha_atual - 1, coluna_atual - 1])
				elif self.matriz_jogadores[linha_atual][coluna_atual] == 'x':
					if linha_atual < 7:
						if coluna_atual < 7:#se coluna menor que 7 permite mover peca para uma linha  que seja menor que 7 se a linha for menor que 7// movimentação para a direita peça preta
							if self.matriz_jogadores[linha_atual + 1][coluna_atual + 1] == '-':
								movimentos.append([linha_atual + 1, coluna_atual + 1])
						if coluna_atual > 0:#se coluna maior que 0 e linha menor que 7 permite mover peça para uma linha que seja maior que 0// movimentação para a esquerda peça preta
							if self.matriz_jogadores[linha_atual + 1][coluna_atual - 1] == '-':
								movimentos.append([linha_atual + 1, coluna_atual - 1])
							#Verifica se local onde a peça vai ser movida está Vazio e permite o movimento 
			elif self.matriz_jogadores[linha_atual][coluna_atual].isupper():# retorna os movimentos da DAMA.
				conta_linha = linha_atual
				conta_coluna = coluna_atual
				while True:
					if conta_linha - 1 < 0 or conta_coluna - 1 < 0: break#Verifica se linha e coluna nao é menor que 0 se for para para nao sair da matriz
					else:
						if self.matriz_jogadores[conta_linha - 1][conta_coluna - 1] == '-': #verifica se casa (linha e coluna -1) está vazia 
							movimentos.append([conta_linha - 1, conta_coluna - 1]) #movimenta a peca para local desejado
						else: break
					conta_linha -= 1
					conta_coluna -= 1

				conta_linha = linha_atual
				conta_coluna = coluna_atual
				while True:
					if conta_linha - 1 < 0 or conta_coluna + 1 > 7: break #Verifica se linha nao é menor que 0 e coluna maior que 7 se for para para nao sair da matriz
					else:
						if self.matriz_jogadores[conta_linha - 1][conta_coluna + 1] == '-':# Verifica se casa está vazia 
							movimentos.append([conta_linha - 1, conta_coluna + 1])# movimenta a peca para local desejado
						else: break
					conta_linha -= 1
					conta_coluna += 1
				conta_linha = linha_atual
				conta_coluna = coluna_atual
				while True:
					if conta_linha + 1 > 7 or conta_coluna + 1 > 7: break#Verifica se linha nao é maior que 7 e coluna maior que 7 se for para para nao sair da matriz
					else:
						if self.matriz_jogadores[conta_linha + 1][conta_coluna + 1] == '-': #verifica se casa esta vazia 
							movimentos.append([conta_linha + 1, conta_coluna + 1])# executa movimento
						else: break
					conta_linha += 1
					conta_coluna += 1

				conta_linha = linha_atual
				conta_coluna = coluna_atual
				while True:
					if conta_linha + 1 > 7 or conta_coluna - 1 < 0: break#Verifica se linha nao é menor que 0 e coluna menor que 7 se for para para nao sair da matriz
					else:
						if self.matriz_jogadores[conta_linha + 1][conta_coluna - 1] == '-': # verifica se casa desejada está vazia	
							movimentos.append([conta_linha + 1, conta_coluna - 1]) #retorna movimento
						else: break
					conta_linha += 1
					conta_coluna -= 1
				
		return movimentos, pulos

	# EXECUTA UMA JOGADA
	def jogar(self, jogador, localizacao_cedula, linha_destino, coluna_destino, pulo): #executa sequencias para realizar o jogo, com as variaveis recebendo as suas alocações 
		linha_atual = localizacao_cedula[0]
		coluna_atual = localizacao_cedula[1]
		char = self.matriz_jogadores[linha_atual][coluna_atual]

		self.matriz_jogadores[linha_destino][coluna_destino] = char
		self.matriz_jogadores[linha_atual][coluna_atual] = '-'

		if pulo:# movimento de peça de pulo
			self.pulando = True

		if (jogador == 'x' and linha_destino == 7) or (jogador == 'o' and linha_destino == 0): #transforma a peça em Dama 
			if not self.pulando: #transforma em dama comendo peca
				self.matriz_jogadores[linha_destino][coluna_destino] = char.upper()
			elif not self.movimentos_possiveis((linha_destino, coluna_destino))[0]:
				self.matriz_jogadores[linha_destino][coluna_destino] = char.upper()
		
		if (jogador == 'x' and linha_destino == 7) or (jogador == 'o' and linha_destino == 0): #transforma a peça em Dama 
			if  self.pulando:# Transforma em dama andando com a peca
				self.matriz_jogadores[linha_destino][coluna_destino] = char.upper()
			elif self.movimentos_possiveis((linha_destino, coluna_destino))[0]:
				self.matriz_jogadores[linha_destino][coluna_destino] = char.upper()

		if pulo: #verifica se a casa é vazia se for executa jogada  para a peça se mover 
			self.matriz_jogadores[pulo[0]][pulo[1]] = '-'
			self.cedula_selecionada = [linha_destino, coluna_destino]
			self.pulando = True

		else:# se movimentos na peça selecionada terminou passa para o proximo turno, nisso verifica se tem vencedor
			self.cedula_selecionada = None
			self.proximo_turno()
		vencedor = self.verifica_vencedor()

		if vencedor != None: # se tiver vencedor acaba o jogo 
			self.status = 'Game Over'

	# PRÓXIMO TURNO
	def proximo_turno(self): 
		self.turno += 1

	# VERIFICA O VENCEDOR
	def verifica_vencedor(self):

		x = sum([contador.count('x') + contador.count('X') for contador in self.matriz_jogadores])
		o = sum([contador.count('o') + contador.count('O') for contador in self.matriz_jogadores])

		if x == 0:# se conta da soma de peca de x der 0 peca branca ganha o jogo
			return 'o'

		if o == 0:# se conta da soma de peca de o der 0 peca preta ganha o jogo
			return 'x'

		if x == 1 and o == 1: # se  sobrar uma peça de cada lado retorna empate 
			return 'Empate'

		if self.cedula_selecionada: #dependendo da peca selecionada retorna os movimentos possiveis 
			if not self.movimentos_possiveis(self.cedula_selecionada)[0]:
				if x == 1 and self.turno % 2 == 0:
					return 'o'
				if o == 1 and self.turno % 2 == 1:
					return 'x'

		if not self.existe_possivel(): # se nao exisistir movimentos possíveis de ambos os lados empata o jogo 
			return 'Empate'


		return None


	# DESENHAR TABULEIRO E PEÇAS
	def desenha(self):
		matriz = []

		for i in range(8):
			if i % 2 == 0:
				matriz.append(['-','#','-','#','-','#','-','#'])
			else:
				matriz.append(['#','-','#','-','#','-','#', '-'])

		y = 0
		for l in range(len(matriz)):
			x = 0
			for c in range(len(matriz[l])):
				if matriz[l][c] == '#':
					pygame.draw.rect(display, DARKGRAY, (x, y, 75, 75))
				else:
					pygame.draw.rect(display, BRANCO, (x, y, 75, 75))
				x += 75
			y += 75
#Função que mostra uma cor alertando o jogador que tem movimento obrigatório,caso haja area em volta da peça fica verde, se não vermelho
		if self.cedula_selecionada:
			obrigatorios = self.todos_obrigatorios()
			movs = self.movimentos_possiveis(self.cedula_selecionada)

			if obrigatorios != {}:
				if (self.cedula_selecionada[0], self.cedula_selecionada[1]) not in obrigatorios:
					x_vermelho = ALTURA / 8 * self.cedula_selecionada[1]
					y_vermelho = ALTURA / 8 * self.cedula_selecionada[0]

					pygame.draw.rect(display, VERMELHO_CLARO, (x_vermelho, y_vermelho, 75, 75))
					fonte = pygame.font.Font(None, 20)
					surface_texto, rect_texto = text_objects("Tem Movimento Obrigatorio", fonte, VERMELHO_CLARO)
					rect_texto.center = (700, ALTURA / 3)
					display.blit(surface_texto, rect_texto)
				else:
					if movs[0] == []:# se tem movimento obrigatorio para fazer fica verde claro se nao fica vermelho claro
						x_vermelho = ALTURA / 8 * self.cedula_selecionada[1]
						y_vermelho = ALTURA / 8 * self.cedula_selecionada[0]

						pygame.draw.rect(display, VERMELHO_CLARO, (x_vermelho, y_vermelho, 75, 75))
					else:
						for i in range(len(movs[0])):
							x_possivel = ALTURA / 8 * movs[0][i][1]
							y_possivel = ALTURA / 8 * movs[0][i][0]

							pygame.draw.rect(display, VERDE_CLARO, (x_possivel, y_possivel, 75, 75))
							
			else: # se tem pulo para comer peca para fazer fica verde claro se nao fica vermelho claro
				if self.pulando:
					x_vermelho = ALTURA / 8 * self.cedula_selecionada[1]
					y_vermelho = ALTURA / 8 * self.cedula_selecionada[0]


					pygame.draw.rect(display, VERMELHO_CLARO, (x_vermelho, y_vermelho, 75, 75))
				else:
					if movs[0] == []:# se tem movimento para fazer fica verde claro se nao fica vermelho claro
						x_vermelho = ALTURA / 8 * self.cedula_selecionada[1]
						y_vermelho = ALTURA / 8 * self.cedula_selecionada[0]

						pygame.draw.rect(display, VERMELHO_CLARO, (x_vermelho, y_vermelho, 75, 75))
					else:
						for i in range(len(movs[0])):
							x_possivel = ALTURA / 8 * movs[0][i][1]
							y_possivel = ALTURA / 8 * movs[0][i][0]

							pygame.draw.rect(display, VERDE_CLARO, (x_possivel, y_possivel, 75, 75))

		for l in range(len(self.matriz_jogadores)):
			for c in range(len(self.matriz_jogadores[l])):
				elemento = self.matriz_jogadores[l][c]
				if elemento != '-':
					x = ALTURA / 8 * c + ALTURA / 16
					y = ALTURA / 8 * l + ALTURA / 16
						#Desenho da peca de Dama quando x recebe upper para X peca recebe um diferencial para indicar que é dama
					if elemento.lower() == 'x':
						pygame.draw.circle(display, PRETO, (x, y), 20, 0)
						if elemento == 'X':
							pygame.draw.circle(display, BRANCO, (x, y), 10, 0)
							pygame.draw.circle(display, AZUL, (x, y), 5, 0)
					else:
						pygame.draw.circle(display, BRANCO, (x, y), 20, 0)
						if elemento == 'O':
							pygame.draw.circle(display, PRETO, (x, y), 10, 0)
							pygame.draw.circle(display, AZUL, (x, y), 5, 0)

		fonte = pygame.font.Font(None, 20)
		
		x = sum([contador.count('x') + contador.count('X') for contador in self.matriz_jogadores])
		o = sum([contador.count('o') + contador.count('O') for contador in self.matriz_jogadores])

		if self.status != 'Game Over':

			surface_texto, rect_texto = text_objects("Preto: " + str(12 - o), fonte, BRANCO)
			rect_texto.center = (650, 30)
			display.blit(surface_texto, rect_texto)

			surface_texto, rect_texto = text_objects("Branco: " + str(12 - x), fonte, BRANCO)
			rect_texto.center = (650, ALTURA - 30)
			display.blit(surface_texto, rect_texto)

			if self.turno % 2 == 1:
				surface_texto, rect_texto = text_objects("Turno do branco", fonte, BRANCO)
				rect_texto.center = (700, ALTURA / 2)
				display.blit(surface_texto, rect_texto)
			else:
				surface_texto, rect_texto = text_objects("Turno do Preto", fonte, BRANCO)
				rect_texto.center = (700, ALTURA / 2)
				display.blit(surface_texto, rect_texto)
		else:
			surface_texto, rect_texto = text_objects("Game Over", fonte, AZUL)
			rect_texto.center = (700, ALTURA / 3)
			display.blit(surface_texto, rect_texto)

# --- FUNÇÕES A SEREM UTILIZADAS  ---

# DEFINIR PADRÃO DE TEXTOS NA TELA
def text_objects(text, font, color):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()

# FUNÇÃO PARA CRIAR UM BOTÃO
def cria_botao(msg, sqr, cor1, cor2, cor_texto, acao=None):
	mouse = pygame.mouse.get_pos()
	clique = pygame.mouse.get_pressed()

	if sqr[0] + sqr[2] > mouse[0] > sqr[0] and sqr[1] + sqr[3] > mouse[1] > sqr[1]:
		pygame.draw.rect(display, cor2, sqr)
		if clique[0] == 1 and acao != None:
			acao()
	else:
		pygame.draw.rect(display, cor1, sqr)

	fontePequena = pygame.font.SysFont('comicsansms', 20)
	surface_texto, rect_texto = text_objects(msg, fontePequena, cor_texto)
	rect_texto.center = (sqr[0] + 60, sqr[1] + 20)
	display.blit(surface_texto, rect_texto)

# FUNÇÃO PARA IMPRIMIR OS CRÉDITOS
def creditos():
	sair = False
	while not sair:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				pygame.quit()
				quit()
			if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
				sair = True

		display.fill(PRETO)
		fonte = pygame.font.SysFont('comicsansms', 20)
		surface_texto, rect_texto = text_objects("Programador: João Ernesto R.A 11819806 ", fonte, BRANCO)
		rect_texto.center = ((LARGURA / 2), ALTURA / 3.2)
		display.blit(surface_texto, rect_texto)

		surface_texto, rect_texto = text_objects("Programador: Bruno Canisella R.A 11921168 ", fonte, BRANCO)
		rect_texto.center = ((LARGURA / 2), ALTURA / 4.5)
		display.blit(surface_texto, rect_texto)
		fonte = pygame.font.SysFont('comicsansms', 30)
		surface_texto, rect_texto = text_objects("Disciplina: Linguagens Formais e Autonomas", fonte, VERDE_CLARO)
		rect_texto.center = ((LARGURA / 2), ALTURA / 2.4
		)
		display.blit(surface_texto, rect_texto)
		fonte = pygame.font.SysFont('comicsansms', 20)
		surface_texto, rect_texto = text_objects("Professor: Claiton Luis", fonte, BRANCO)
		rect_texto.center = ((LARGURA / 2), ALTURA / 1.7)
		display.blit(surface_texto, rect_texto)
		surface_texto, rect_texto = text_objects("Versao Python: 10.2", fonte, VERMELHO_CLARO)
		rect_texto.center = ((LARGURA / 2), ALTURA / 1.5)
		display.blit(surface_texto, rect_texto)

		surface_texto, rect_texto = text_objects("Versao Pygame: 2.1.2", fonte, VERMELHO_CLARO)
		rect_texto.center = ((LARGURA / 2), ALTURA / 1.3)
		display.blit(surface_texto, rect_texto)

		voltar = fonte.render('Pressione qualquer tecla para voltar ao menu.', False, VERDE_CLARO)
		display.blit(voltar, (25, 550))

		pygame.display.update()
		clock.tick(15)

# FUNÇÃO PARA IMPRIMIR AS REGRAS DO JOGO DE DAMAS
def regras():
	sair = False

	while not sair:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				sair = True
				pygame.quit()
				quit()
			if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
				sair = True

		display.fill(PRETO)

		fonte = pygame.font.SysFont('comicsansms', 20)

		info1 = fonte.render('O jogo de damas eh praticado em um tabuleiro em uma matriz 8x8,.', False, (BRANCO))
		info2 = fonte.render('o objetivo do jogo é capturar todas as pecas do oponente.', False, (BRANCO))
		info3 = fonte.render('A peca anda só para frente, uma casa de cada vez, na diagonal,', False, (BRANCO))
		info4 = fonte.render('e quando a peça atinge o final do tabuleiro ela vira uma dama.', False, (BRANCO))
		info5 = fonte.render('A dama é uma peca de movimentos mais amplos. Ela anda para frente e para tras.', False, (BRANCO))
		info6 = fonte.render('A captura e obrigatoria, não podendo passar a vez', False, (BRANCO))
		info7 = fonte.render('A peca da dama podem capturar tanto para frente como para tras.', False, (BRANCO))
		info8 = fonte.render('A peca sem ser dama captura só para frente', False, (BRANCO))
		info9 = fonte.render('Vence quem ficar com peças sobrando no tabuleiro', False, (BRANCO))
		info10 = fonte.render('O empate vem quando se passa mais de 10 turnos e sobra uma peça de cada jogador.', False, (BRANCO))
		
		game1 = fonte.render('Durante o jogo, ao clicar em uma peca, sera exibido em verde os movimentos', False, (BRANCO))
		game2 = fonte.render('possiveis da mesma, caso fique vermelha, significa que', False, (BRANCO))
		game3 = fonte.render('ela nao tem movimentos possiveis ou o turno pertence ao outro jogador.', False, (BRANCO))

		voltar = fonte.render('Pressione qualquer tecla para voltar ao menu.', False, VERDE_CLARO)

		display.blit(info1, (5, 65))
		display.blit(info2, (5, 95))
		display.blit(info3, (5, 115))
		display.blit(info4, (5, 145))
		display.blit(info5, (5, 165))
		display.blit(info6, (5, 195))
		display.blit(info7, (5, 215))
		display.blit(info8, (5, 245))
		display.blit(info9, (5, 265))
		display.blit(info10, (5, 295))
		
		display.blit(game1, (5, 315))
		display.blit(game2, (5, 335))
		display.blit(game3, (5, 360))
		display.blit(voltar, (25, 550))

		pygame.display.update()
		clock.tick(60)

# FUNÇÃO PARA IMPRIMIR A TELA DO VENCEDOR
def tela_vencedor(vencedor):
	sair = False

	while not sair:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				sair = True
				pygame.quit()
				quit()
			if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
				sair = True

		display.fill(PRETO)

		fonte = pygame.font.SysFont('comicsansms', 50)

		surface_texto, rect_texto = None, None

		if vencedor == "empate":
			surface_texto, rect_texto = text_objects("EMPATE!", fonte, BRANCO)
		elif vencedor == "x":
			surface_texto, rect_texto = text_objects("VITORIA DO  PRETO", fonte, BRANCO)
		elif vencedor == "o":
			surface_texto, rect_texto = text_objects("VITORIA DO BRANCO", fonte, BRANCO)

		rect_texto.center = ((LARGURA / 2), ALTURA / 3)
		display.blit(surface_texto, rect_texto)

		fonte = pygame.font.Font(None, 30)
		voltar = fonte.render('Pressione qualquer tecla para voltar ao menu.', False, VERDE_CLARO)

		display.blit(voltar, (25, 550))

		pygame.display.update()
		clock.tick(60)

# TELA DO MENU
def menu_jogo():
	while True:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				pygame.quit()
				quit()
		
			display_surface.fill(BRANCO)
			display_surface.blit(image, (0, 0))
		
			fonte = pygame.font.SysFont('comicsansms', 50)
			surface_texto, rect_texto = text_objects("Jogo de Damas", fonte, BRANCO)
			rect_texto.center = ((LARGURA / 2), ALTURA / 3)
			display.blit(surface_texto, rect_texto)

			cria_botao("INICIAR",(LARGURA - 760, ALTURA / 2, 120, 40), VERDE_CLARO, VERDE_ESCURO, BRANCO, loop_jogo)
			cria_botao("MANUAL",(LARGURA - 560, ALTURA / 2, 120, 40), BRANCO, CINZA, PRETO, regras)
			cria_botao("CREDITOS",(LARGURA - 360, ALTURA / 2, 120, 40), BRANCO, CINZA, PRETO, creditos)
			cria_botao("SAIR",(LARGURA - 160, ALTURA / 2, 120, 40), VERMELHO_CLARO, VERMELHO, BRANCO, sair)
			pygame.display.update()

# SAIR DO JOGO	
def sair():
	pygame.quit()
	quit()
# FUNÇÕES AUXILIARES NO LOOP DO JOGO
def coluna_clicada(pos):
	x = pos[0]
	for i in range(1, 8):
		if x < i * ALTURA / 8:
			return i - 1
	return 7

def linha_clicada(pos):
	y = pos[1]
	for i in range(1, 8):
		if y < i * ALTURA / 8:
			return i - 1
	return 7

# LOOP DA TELA DO JOGO DE DAMAS
def loop_jogo():
	sair = False

	jogo = Jogo()

	while not sair:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				sair = True
				pygame.quit()
				quit()
			if evento.type == pygame.MOUSEBUTTONDOWN:
				jogo.avalia_clique(pygame.mouse.get_pos())

		display.fill(PRETO)
		jogo.desenha()

		vencedor = jogo.verifica_vencedor()

		if vencedor is not None:
			sair = True
			tela_vencedor(vencedor)

		pygame.display.update()
		clock.tick(60)

menu_jogo()
pygame.quit()
quit()
