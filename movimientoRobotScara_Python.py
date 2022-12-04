# Este script va asociado como PythonScpript al comportamiento del robot Scara
# Falta:
# - Definir pos de bandeja respecto base del robot (actualmente aleatoria)
# - Definir pos de la primera posicion de medicion respecto base de la bandeja (actualmente 0,0,0)
# - Definir comportamiento del sensor acoplado

from vcScript import *
from vcHelpers.Robot2 import *

# Definicion de puntos
posBandeja = [150, 0, 0]
offsetx = 0
offsety = 0
offsetz = 0
pasox = 75
pasoy = 74

print "Puntos a alcanzar por el robot Scara (Omrom)"

bandejaPpieza1 = list(posBandeja)
bandejaPpieza1[0] = bandejaPpieza1[0] + offsetx
bandejaPpieza1[1] = bandejaPpieza1[1] + offsety
bandejaPpieza1[2] = bandejaPpieza1[2] + offsetz
print bandejaPpieza1

bandejaPpieza2 = [0,0,0]
bandejaPpieza2[0] = bandejaPpieza1[0] + pasox
bandejaPpieza2[1] = bandejaPpieza1[1]
bandejaPpieza2[2] = bandejaPpieza1[2]
print bandejaPpieza2

bandejaPpieza3 = [0,0,0]
bandejaPpieza3[0] = bandejaPpieza2[0]
bandejaPpieza3[1] = bandejaPpieza2[1] + pasoy
bandejaPpieza3[2] = bandejaPpieza2[2]
print bandejaPpieza3

bandejaPpieza4 = [0,0,0]
bandejaPpieza4[0] = bandejaPpieza3[0] - pasox
bandejaPpieza4[1] = bandejaPpieza3[1]
bandejaPpieza4[2] = bandejaPpieza3[2]
print bandejaPpieza4

bandejaPpieza5 = [0,0,0]
bandejaPpieza5[0] = bandejaPpieza4[0]
bandejaPpieza5[1] = bandejaPpieza4[1] + pasoy
bandejaPpieza5[2] = bandejaPpieza4[2]
print bandejaPpieza5

bandejaPpieza6 = [0,0,0]
bandejaPpieza6[0] = bandejaPpieza5[0] + pasox
bandejaPpieza6[1] = bandejaPpieza5[1]
bandejaPpieza6[2] = bandejaPpieza5[2]
print bandejaPpieza6

def MoveToMeasurePoint(robot,pos,aproxOffset):
  errorPieza = 0
  
  # Punto de aproximacion
  robot.jointMoveToPosition(pos[0],pos[1],pos[2]+aproxOffset,0,0,0,"irobot")
  robot.delay(0.5)
  
  # Punto en cuestion
  robot.linearMoveToPosition(pos[0],pos[1],pos[2],0,0,0,"irobot")
  robot.delay(0.5)
  
  # Ejecutar medicion (sacar alguna señal con medicion buena o mala)
  
  # Vuelta a pto. aprox
  robot.linearMoveToPosition(pos[0],pos[1],pos[2]+aproxOffset,0,0,0,"irobot")
  robot.delay(0.5)
  
  return errorPieza
  
  
def MoveAllMeasurePoints(robot):
  MoveToMeasurePoint(robot,bandejaPpieza1,50)
  MoveToMeasurePoint(robot,bandejaPpieza2,50)
  MoveToMeasurePoint(robot,bandejaPpieza3,50)
  MoveToMeasurePoint(robot,bandejaPpieza4,50)
  MoveToMeasurePoint(robot,bandejaPpieza5,50)
  MoveToMeasurePoint(robot,bandejaPpieza6,50)


def OnRun():
  robot = getRobot()
  robot.driveJoints(0,0,0,0,0,0)
  robot.delay(0.5)
  
  ocupado = 1
  piezas_medidas = 0
  
  
  while not ocupado:
    llegan_piezas = 0
      
  if not piezas_medidas and ocupado:
    MoveAllMeasurePoints(robot)
    robot.driveJoints(0,0,0,0,0,0)
    robot.delay(0.5)
    piezas_medidas = 1
  