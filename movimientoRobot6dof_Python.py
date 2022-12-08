from vcScript import *
from vcHelpers.Robot2 import *

# Variables globales para las posiciones
robotPbandeja = [155.42, 382.17, 23.38]
robotPpiezas = [147.1+34, -333.7, -16.6]

offsetBPiezas = 356.9   # Distancia en x del robot de una bandeja de 54 a la otra
BandejaRecogida = 0   

tEsperaLlegadaPiezas = 2
tEsperaLlegadaBandeja = 5

i_bandeja = 0
ix_bandeja = 0
iy_bandeja = 0
i_piezas = 0
ix_piezas = 0
iy_piezas = 0

max_bandeja = 6
max_x_bandeja = 3
max_y_bandeja = 2

max_piezas = 12  # COMENTAR ESTO EN PRODUCCION!!!
#max_piezas = 54
max_x_piezas = 6
max_y_piezas = 9

paso_x_bandeja = 74
paso_y_bandeja = 75

paso_x_piezas = 34
paso_y_piezas = 39.1

toolOffset = 50

# Object handlers
robot = getRobot()
component = getComponent()

# Signals
signalVentosa = component.findBehaviour("Ventosa")
signalParada = component.findBehaviour("ParadaEmergencia")
signalMarcha = component.findBehaviour("MarchaNormal")
signalBandeja54Acabada = component.findBehaviour("Bandeja54Acabada")
signalBandejaRecogida = component.findBehaviour("BandejaRecogida")
signalPlacaDe6Done = component.findBehaviour("PlacaDe6Done")

def OnStart():
  pass
  
def OnRun():
  
  global i_piezas
  global i_bandeja
  global BandejaRecogida
  
  signalVentosa.signal(False)
  signalParada.signal(False)
  signalMarcha.signal(True)
  signalBandeja54Acabada.signal(False)
  signalBandejaRecogida.signal(0)
  signalPlacaDe6Done.signal(False)
  
  while not signalParada.Value:
    
    if signalMarcha.Value:
      
      # Pick
      iy_piezas = i_piezas // max_x_piezas
      ix_piezas = i_piezas % max_x_piezas
      
      posPick = [0,0,0]
      posPick[0] = robotPpiezas[0] - ix_piezas*paso_x_piezas - BandejaRecogida*offsetBPiezas
      posPick[1] = robotPpiezas[1] - iy_piezas*paso_y_piezas
      posPick[2] = robotPpiezas[2]
      
      Pick(robot,posPick,50)
      
      
      i_piezas += 1
      if i_piezas == max_piezas:
        i_piezas = 0
        signalBandeja54Acabada.signal(True)
        if BandejaRecogida == 0:
          BandejaRecogida +=1
          signalBandejaRecogida.signal(True)
        else: 
          BandejaRecogida += -1
          signalBandejaRecogida.signal(False)
      
      # Place
      iy_bandeja = i_bandeja // max_x_bandeja
      ix_bandeja = i_bandeja % max_x_bandeja
      
      posPlace = [0,0,0]
      posPlace[0] = robotPbandeja[0] + ix_bandeja*paso_x_bandeja
      posPlace[1] = robotPbandeja[1] + iy_bandeja*paso_y_bandeja
      posPlace[2] = robotPbandeja[2]
      
      Place(robot,posPlace,50)
      
      if signalBandeja54Acabada.Value: signalBandeja54Acabada.signal(False)
      
      i_bandeja += 1
      if i_bandeja == max_bandeja:
        i_bandeja = 0
        signalPlacaDe6Done.signal(True)
        robot.delay(0.5)
        signalPlacaDe6Done.signal(False)
        robot.delay(tEsperaLlegadaBandeja)

def Pick(robot,pos,aproxOffset):
  errorPieza = 0
  
  # Punto de aproximacion
  robot.jointMoveToPosition(pos[0],pos[1],pos[2]+aproxOffset+toolOffset,0,0,0,"irobot")
  robot.delay(0.3)
  
  # Punto en cuestion
  robot.linearMoveToPosition(pos[0],pos[1],pos[2]+toolOffset,0,0,0,"irobot")
  robot.delay(0.5)
  
  # Ejecutar lo que sea: cerrar pinza
  signalVentosa.signal(True)
  robot.delay(0.5)
  
  # Vuelta a pto. aprox
  robot.linearMoveToPosition(pos[0],pos[1],pos[2]+aproxOffset+toolOffset,0,0,0,"irobot")
  robot.delay(0.5)
  
  return errorPieza


def Place(robot,pos,aproxOffset):
  errorPieza = 0
  
  # Punto de aproximacion
  robot.jointMoveToPosition(pos[0],pos[1],pos[2]+aproxOffset+toolOffset,0,0,0,"irobot")
  robot.delay(0.3)
  
  # Punto en cuestion
  robot.linearMoveToPosition(pos[0],pos[1],pos[2]+toolOffset,0,0,0,"irobot")
  robot.delay(0.5)
  
  # Ejecutar lo que sea: abrir pinza
  signalVentosa.signal(False)
  robot.delay(0.5)
  
  # Vuelta a pto. aprox
  robot.linearMoveToPosition(pos[0],pos[1],pos[2]+aproxOffset+toolOffset,0,0,0,"irobot")
  robot.delay(0.5)
  
  return errorPieza