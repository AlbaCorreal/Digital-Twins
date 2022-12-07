from vcScript import *
from vcHelpers.Robot2 import *



def Pick(robot,pos,aproxOffset):
  errorPieza = 0
  
  # Punto de aproximacion
  robot.jointMoveToPosition(pos[0],pos[1],pos[2]+aproxOffset,0,0,0,"irobot")
  robot.delay(0.5)
  
  # Punto en cuestion
  robot.linearMoveToPosition(pos[0],pos[1],pos[2],0,0,0,"irobot")
  robot.delay(0.5)
  
  # Ejecutar lo que sea: cerrar pinza
  
  # Vuelta a pto. aprox
  robot.linearMoveToPosition(pos[0],pos[1],pos[2]+aproxOffset,0,0,0,"irobot")
  robot.delay(0.5)
  
  return errorPieza


def Place(robot,pos,aproxOffset):
  errorPieza = 0
  
  # Punto de aproximacion
  robot.jointMoveToPosition(pos[0],pos[1],pos[2]+aproxOffset,0,0,0,"irobot")
  robot.delay(0.5)
  
  # Punto en cuestion
  robot.linearMoveToPosition(pos[0],pos[1],pos[2],0,0,0,"irobot")
  robot.delay(0.5)
  
  # Ejecutar lo que sea: abrir pinza
  
  # Vuelta a pto. aprox
  robot.linearMoveToPosition(pos[0],pos[1],pos[2]+aproxOffset,0,0,0,"irobot")
  robot.delay(0.5)
  
  return errorPieza
  
  
def OnRun():
  
  # Definicion de ubicaciones de bandeja y piezas en el espacio respecto robot
  robotPbandeja = [185, 335, 50]
  robotPpiezas = [130, -340, 50]

  i_bandeja = 0
  ix_bandeja = 0
  iy_bandeja = 0
  i_piezas = 0
  ix_piezas = 0
  iy_piezas = 0

  max_bandeja = 6
  max_x_bandeja = 3
  max_y_bandeja = 2

  max_piezas = 54
  max_x_piezas = 6
  max_y_piezas = 9

  paso_x_bandeja = 74
  paso_y_bandeja = 75

  paso_x_piezas = 34
  paso_y_piezas = 39.1
  
  robot = getRobot()
  robot.driveJoints(0,0,90,0,0,0)
  robot.delay(0.5)
  
  print i_piezas
  
  Pick(robot,[200,0,0],50)
  
  while(1):
    
    # Pick
    iy_piezas = i_piezas // max_x_piezas
    ix_piezas = i_piezas % max_x_piezas
    
    posPick = [0,0,0]
    posPick[0] = robotPpiezas[0] - ix_piezas*paso_x_piezas
    posPick[1] = robotPpiezas[1] - iy_piezas*paso_y_piezas
    posPick[2] = robotPpiezas[2]
    
    Pick(robot,posPick,50)
    
    i_piezas += 1
    if i_piezas == max_piezas: i_piezas = 0
    
    # Place
    iy_bandeja = i_bandeja // max_x_bandeja
    ix_bandeja = i_bandeja % max_x_bandeja
    
    posPlace = [0,0,0]
    posPlace[0] = robotPbandeja[0] + ix_bandeja*paso_x_bandeja
    posPlace[1] = robotPbandeja[1] + iy_bandeja*paso_y_bandeja
    posPlace[2] = robotPbandeja[2]
    
    Place(robot,posPlace,50)
    
    i_bandeja += 1
    if i_bandeja == max_bandeja: i_bandeja = 0
   
  
  