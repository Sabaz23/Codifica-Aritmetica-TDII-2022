#   Luca Sabatino S4833215
#   Codifica.py
#   2022
#   Codifica aritmetica di una stringa di bit

import sys
import array as arr
from dataclasses import dataclass
import math
import random

#La struct Interval contiene gli estremi di un intervallo

@dataclass
class Interval:
    intervalStart: float
    intervalEnd: float

interval0 = Interval(0.0,0.0) #Intervallo per il simbolo 0
interval1 = Interval(0.0,0.0) #Intervallo per il simbolo 1

#Calcola la differenza tra gli estremi di un intervallo (l'ampiezza)
def CalculateDiff(intervalStart,intervalEnd): 
    return intervalEnd - intervalStart

#   Questa formula serve per calcolare la fine di un segmento della codifica aritmetica
#   S = Estremo iniziale dell'intervallo
#   P = Probabilità del simbolo
#   R = Ampiezza dell'intervallo

def rangeFormula(S,P,R): 
    return S +(P*R)

#   Questa funzione è il fulcro della codifica, calcolando l'ampiezza degli intervalli di 0 e 1 basandosi sulle loro probabilità
#   intervalStart = inizio dell'intervallo da codificare
#   intervalEnd = fine dell'intervallo da codificare
#   probability = array di probabilità dei simboli
#   symbol = simbolo da codificare (0 o 1)

def ArithmeticCoding(intervalStart,probability,intervalRange,symbol):
    global interval0
    global interval1
    intervalEnd = rangeFormula(intervalStart,probability[symbol],intervalRange)
    if(symbol == 0):
        interval0.intervalStart = intervalStart
        interval0.intervalEnd = intervalEnd
    else:
        interval1.intervalStart = intervalStart
        interval1.intervalEnd = intervalEnd
    return intervalEnd

#   Funzione main

if __name__ == "__main__":
    #n0 e n1 sono variabili temporanee finalizzate al calcolo ricorsivo delle probabilità durante l'inserimento
    n0 = 0
    n1 = 0
    probability = arr.array('f',[0.5,0.5])  #Inizialmente, sono equiprobabili
    if(len(sys.argv) != 2): #In input va inserito un numero intero che rappresenta la lunghezza della stringa di bit
        print("Usage: python3 Codifica.py <len>")
        sys.exit(1)
    bits = ''
    for i in range(int(sys.argv[1])):
        temp = str(random.randint(0,1)) #La stringa di bit viene generata casualmente
        bits += temp
    bitLength = int(sys.argv[1])
    print("Bits: " + bits)
    i = 1
    for element in bits:
            if float(element) == 0:
                n0 += 1
            else:
                n1 += 1
            probability[0] = n0 / i #Calcolo della probabilità del simbolo 0
            probability[1] = n1 / i #Calcolo della probabilità del simbolo 1
            print("Probability of 0: \n" + str(round(probability[0],2)))
            print("Probability of 1: \n" + str(round(probability[1],2)))
            i += 1

    #   IntervalRange è il risultato della differenza della lunghezza, e inizialmente viene fatto usando 0
    #   (l'inizio assoluto dell'intervallo e la probabilità di 0)
    intervalRange = CalculateDiff(0,probability[0])
    previousEnd = ArithmeticCoding(0,probability,intervalRange,0)
    previousEnd = ArithmeticCoding(previousEnd,probability,intervalRange,1)

    intervalRange = CalculateDiff(interval1.intervalStart,interval1.intervalEnd)
    previousEnd = ArithmeticCoding(interval1.intervalStart,probability,intervalRange,0)
    previousEnd = ArithmeticCoding(previousEnd,probability,intervalRange,1)

    #   Interval0 start e interval1 end rappresentano la lunghezza dell'intervallo di codifica.
    #   Il valore medio è la media tra i due estremi, e sarà il singolo valore double che codifica il messaggio
    finalDouble = (interval0.intervalStart + interval1.intervalEnd)/2  

    print("FinalDouble: " + str(finalDouble))
    
    #   Expected è il valore dato da log(1/Ampiezza)/Lunghezza del messaggio
    #   L'entropia viene calcolata utilizzando la sua formula, che è la sommatoria delle probabilità dei simboli
    #   moltiplicate per il logaritmo in base 2 di 1 / la loro probabilità
    #   Se esiste solo un valore (stringa di soli 1 o soli 0,), l'entropia sarà 0
    if probability[0] == 0 or probability[1] == 0:
        Expected = 0
        Entropy = 0
    else:
        Expected = (math.log2(1/CalculateDiff(interval0.intervalStart,interval1.intervalEnd)))/bitLength
        Entropy = probability[0] * math.log2(1/probability[0]) + probability[1] * math.log2(1/probability[1])
    print("Expected: " + str(Expected))
    print("Entropy: " + str(Entropy))



    