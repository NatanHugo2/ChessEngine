import speech_recognition as sr
import pydub
from pydub import AudioSegment
from pydub.utils import make_chunks
import chess
board = chess.Board()
rec = sr.Recognizer()
mic = sr.Microphone
def ajeitar_texto(texto):
    ajeitando = texto.replace('Bispo','B').replace('bispo','B').replace('cavalo','N').replace('Cavalo','N').replace('Rainha','Q').replace('rainha','Q').replace( 'Torre','R').replace('torre','R').replace('Peão','').replace('peão','').replace('Rei','K').replace('rei','K').replace('Na','').replace('na','').replace(' ','').replace('Captura','x').replace('captura','x').replace('A','a').replace('C','c').replace('D','d').replace('de','d').replace('De','d').replace('E','e').replace('F','f').replace('G','g').replace('H','h').replace('Xeque','+').replace('xeque','+').replace('cheque','+').replace('Cheque','+').replace('Shrek','+').replace('S','f').replace('shrek','+').replace('Hey','K').replace('de','D').replace('quatro','4').replace('um','1').replace('três','3').replace('dois','2').replace('cinco','5').replace('seis','6').replace('sete','7').replace('oito','8').replace('mate','#').replace('Mate','#').replace('Roque','O-O').replace('Grande','-O').replace('roque','O-O').replace('rock','O-O').replace('Rock','O-O').replace('grande','-O')
    ajeitando_dividido = ajeitando.split('x')
    contador = 0
    ajeitado = [] 
    for i in ajeitando_dividido:
      lista_i = list(i)
      for j in lista_i:
        if contador == 0:
          ajeitado += j
          contador += 1
          pass
        else:
          if j == 'B':
            lista_i[contador] = 'b'
            ajeitado += lista_i[contador]   
          else:
            contador += 1
            ajeitado += j
      if len(ajeitando_dividido) == 2:
        ajeitado += 'x'
    if len(ajeitando_dividido) == 2:
      ajeitado.pop(-1)
    ajeitado = ''.join(ajeitado)
    return ajeitado
while (board.is_checkmate() == False) and (board.is_fivefold_repetition() == False ) and( board.is_seventyfive_moves() == False) and (board.is_stalemate() == False):
    print(board)
    print('Esses são os movimentos legais:', board.legal_moves)
    print('Fale seu movimento:',end='')
    try:
      with sr.Microphone(0) as mic:
        rec.adjust_for_ambient_noise(mic)
        audio = rec.listen(mic)
        texto = rec.recognize_google(audio, language="pt-BR")
        print(texto)
        print(ajeitar_texto(texto))
      board.push_san(ajeitar_texto(texto))
    except Exception as e:
       print('Você falou algo que não deu pra entender ou fez um movimento inválido')
if (board.is_fivefold_repetition() == False ) and( board.is_seventyfive_moves() == False) and (board.is_stalemate() == False):
  print('Cheque Mate! ')
  board
else:
  print('Deu Empate!')
  board
