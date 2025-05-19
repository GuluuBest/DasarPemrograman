def tempConvertion(value, fromTemp="C", toTemp="K") :
    #put your function here
    if (fromTemp == toTemp) :
        print("the temperature is same")
        return
    
    if (fromTemp not in ("C","K","R","F") 
        or toTemp not in ("C","K","R","F")
        ):
        print("we are not cover this specific temperature")
        return
    
    # Here, we will use celcius as the base temperature
    if (fromTemp == "C"):
        baseTemp = value
    elif (fromTemp == "R"):
        baseTemp = 5/4 * value
    elif (fromTemp == "F"):
        baseTemp = (value-32) * 5/9
    else:
        baseTemp = value - 273.15
    
    if (toTemp == "C"):
        tempConv = baseTemp
    elif (toTemp == "R") :
        tempConv = 4/5 * baseTemp
    elif (toTemp == "F"):
        tempConv = (9/5 + baseTemp) + 32
    else:
        tempConv = baseTemp + 273.15
    

    print("Convertion from",outputFormat(value),longName(fromTemp),
          "is",outputFormat(tempConv),longName(toTemp))

def longName(shortName) :
    output = {
        "K" : "Kelvin",
        "R" : "Rankine",
        "C" : "Celcius",
        "F" : "Fahrenheit"
    }

    return output[shortName]

def outputFormat(value) :
    degree_symbol = u'\N{DEGREE SIGN}'
    return str(round(value,3))+degree_symbol

