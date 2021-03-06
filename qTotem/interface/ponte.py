from PySide2.QtCore import QObject, Slot
from threading import Thread
from os import system

from paciente import paciente


def espeak(t: str):
    system(f'espeak -v pt-br "{t}"')


class Ponte(QObject):
    @Slot()
    def comecar(self):
        paciente.zeraDados()

    @Slot(int)
    def addPontos(self, pontos):
        paciente.pontosDePerguntas += pontos

    @Slot(result=int)
    def getPontos(self):
        return paciente.pontosTotal()

    @Slot(int)
    def setCovid(self, pergunta):
        paciente.covid[pergunta] = True

    @Slot(result=str)
    def getId(self):
        return str(paciente.id)

    @Slot(str, str)
    def publicarNoSite(self, grau, corNome):
        paciente.publicarNoSite(grau, corNome)

    @Slot(str)
    def falarTexto(self, t):
        espeakThread = Thread(target=espeak, args=(t,))
        espeakThread.daemon = True
        espeakThread.start()


ponte = Ponte()
