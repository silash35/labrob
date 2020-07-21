#Constantes medicas, só devem ser alteradas 1 vez
temperaturaMax = 0
saturacaoMin = 0
pressaoMin = 0
pressaoMax = 0

class Paciente:

    def __init__(self):
        self.temperatura = 0
        self.pressao = 0
        self.saturacao = 0
        # Não tem maneira melhor,e mais escalável de calcular o grau de emergência do que com pontos
        self.pontosDePerguntas = 0
        self.id = 0

        self.covid = [False,False,False,False,False]
        #0- Teve tosse seca
        #1- Febre alta por 5 dias ou mais
        #2- dificuldade de respirar
        #3- diarreia
        #4- contato com alguém que teve covid

    def zeraDados(self):
        self.temperatura = 0
        self.pressao = 0
        self.saturacao = 0
        self.pontosDePerguntas = 0
        self.id = self.id + 1
        self.covid = [False,False,False,False,False]

    def getDados(self):
        #código leitura da GPIO

        # Como essa função vai rodar em Loop, 
        # talvez ela pegue dados errados da GPIO, e não 
        # queremos que ela sobrescreva os dados antigos
        # caso os dados antigos sejam mais "graves"
        temp = 0
        press = 0 
        satura = 0
        if(temp > self.temperatura):
            self.temperatura = temp
        if(press > self.pressao):
            self.pressao = press
        if(satura < self.saturacao):
            self.saturacao = satura

    def pontosTotal(self):
        #código calcular total de pontos
        pTemp = 0
        if(self.temperatura > temperaturaMax):
            pTemp = 10

        pPress = 0
        if(self.pressao > pressaoMax or self.pressao < pressaoMin):
            pPress = 10

        pSatura = 0
        if(self.saturacao < saturacaoMin):
            pSatura = 10

        return (self.pontosDePerguntas + pTemp + pPress + pSatura)

    def publicarNoSite(self):
        f = open('./site/templates/users/'+str(self.id)+'.html','wt')
        f.write('''
        <div class="card hoverable">
    <div class="card-image waves-effect waves-block waves-light">
      <!-- Card Image -->
      <img class="activator" src="static/images/users/'''+calculaGrau(self.pontosTotal())[2]+'''.png">
    </div>
    <div class="card-content activator" style="cursor:pointer">
      <!-- Card Title -->
      <span class="card-title grey-text text-darken-4">'''+str(self.id)+'''</span>
    </div>
    <div class="card-reveal">
      <!-- Card Reveal Content -->
      <span class="card-title grey-text text-darken-4">'''+str(self.id)+'''<i class="material-icons right">close</i></span>

      <p>
        '''+ str(calculaGrau(self.pontosTotal())[0]) +'''
      </p>

      <p class="center">
	Temperatura: '''+str(self.temperatura)+'''<br>
	Pressão: '''+str(self.pressao)+'''<br>
	Saturação: '''+str(self.saturacao)+'''<br>
      </p>
      <p>
	<strong>Dados Covid:</strong><br>
        Tosse seca: '''+ str(self.covid[0]) +''' <br>
        Febre alta (+5 dias): '''+ str(self.covid[1]) +''' <br>
        dificuldade de respirar: '''+ str(self.covid[2]) +''' <br>
        diarreia: '''+ str(self.covid[3]) +''' <br>
        contato com alguém que teve covid: '''+ str(self.covid[4]) +''' <br>
      </p>
      <div class="center">
        <button class=" green btn" onclick="excluir('''+ str(self.id) +''')">Finalizar</button>
      </div>
    </div>
  </div>
        ''')
        f.close()

paciente = Paciente()

def calculaGrau(pontos):
    grau = 'Não Urgente'
    cor = '#ffffff'
    corNome = 'branco'

    if(pontos <= 10):
        cor = '#1c5cff'
        grau = "Não Urgente"
        corNome = 'azul'
    elif(pontos <= 20):
        cor = '#1fd158'
        grau = 'Pouco Urgente'
        corNome = 'verde'
    elif(pontos <= 30):
        cor = '#f5d800'
        grau = 'Urgente'
        corNome = 'amarelo'
    elif(pontos <= 40):
        cor = '#ff6f00'
        grau = 'Muito Urgente'
        corNome = 'laranja'
    elif (pontos > 40):
        cor = '#ff1500'
        grau = 'Emergência'
        corNome = 'vermelho'
    else:
        pass #ERRO
    return [grau, cor, corNome]