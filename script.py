################################
# Work under CC BY 4.0 license #
#      by Cyril NOVEL          #
################################
import csv

# Process the phone number
def numberProcessing(stringNb):
  newNumber
  if stringNb[0] == "+":
    space = False
    for(c in stringNb):
      if c == " ":
        space = True

    if !space:
      if (stringNb[1] == 3 and stringNb[2] == 3):
        # french number
        newNumber = "+33 "
        newNumber += stringNb[3]
        i = 4
        while i < len(stringNb):
          if i%2 == 0:
            newNumber += " " + stringNb[i]
          else:
            newNumber += stringNb[i]
          i += 1

        return newNumber

      elif (stringNb[1] == 4 and stringNb[2] == 4):
        # UK number
        newNumber = "+44 "
        newNumber += stringNb[3]
        i = 4
        while i < len(stringNb):
          if i%7 == 0:
            newNumber += " " + stringNb[i]
          else:
            newNumber += stringNb[i]
          i += 1

        return newNumber

      else:
        return stringNb

    else:
      return stringNb

  else:
    space = False
    for(c in stringNb):
      if c == " ":
        space = True

    if space:
      return stringNb
    else:
      if len(stringNb) == 10:
        # french number
        newNumber = "+33 "
        newNumber += stringNb[1]
        i = 2
        while i < len(stringNb):
          if i%2 == 0:
            newNumber += " " + stringNb[i]
          else:
            newNumber += stringNb[i]
          i += 1

        return newNumber

      elif len(stringNb) == 11:
        # UK number
        newNumber = "+44 "
        newNumber += stringNb[1]
        i = 2
        while i < len(stringNb):
          if i%5 == 0:
            newNumber += " " + stringNb[i]
          else:
            newNumber += stringNb[i]
          i += 1

        return newNumber

      else:
        return stringNb

def csvPhonesNb(arrayFirstLine):
  csvPhonesNbIndex
  i = 0
  while i < len(arrayFirstLine):
    if ("Phone" in arrayFirstLine[i] and "Value" in arrayFirstLine[i]):
      csvPhonesNbIndex.append(i)
    i += 1

  return csvPhonesNbIndex


csvFile = open('google.csv', 'rb')
reader = csv.reader(csvFile)
writer = csv.writer(open('output.csv', 'wb'))
i = 0
csvPhonesNbIndex
for row in reader:
  if i == 0:
    i = 1
    csvPhonesNbIndex = csvPhonesNb(row)
    writer.writerow(row)
  else:
    newRow = row
    j = 0
    while j < len(csvPhonesNbIndex):
      index = csvPhonesNbIndex[j]
      if row[index] != "" # we can process the string
        newRow[index] = numberProcessing(row[index])
      j += 1

    writer.writerow(newRow)

csvFile.close()