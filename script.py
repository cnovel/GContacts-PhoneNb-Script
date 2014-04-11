################################
# Work under CC BY 4.0 license #
#      by Cyril NOVEL          #
################################

import csv
import codecs
import cStringIO
import sys

class UTF8Recoder:
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
    def __iter__(self):
        return self

class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# If two numbers have the same label,  Google stores them
# in the same cell, with separator :::
def separateAndProcess(stringNumbers):
  noSpaceNumbers = stringNumbers.replace(" ", "")
  numbers = noSpaceNumbers.split(":::")
  stringToReturn = ""
  i = 0
  while i < len(numbers):
    processedNb = numberProcessing(numbers[i])
    if (i == len(numbers) -1):
      stringToReturn += processedNb
    else:
      stringToReturn += processedNb + " ::: "
    
    i += 1

  return stringToReturn



# Process the phone number
def numberProcessing(stringNb):
  stringFrmtd = stringNb.replace(" ", "")
  frenchNumber = False
  ukNumber = False
  # there is no space to worry about in the new string
  if stringFrmtd[0] == "+":
    #international number here
    if stringFrmtd[1] == "3":
      # obviously its +33 something so French number !
      frenchNumber = True
    else:
      ukNumber = True

  elif stringFrmtd[0] == "0" and stringFrmtd[1] == "0":
    #international number here again
    stringFrmtd = "+" + stringFrmtd[2:] # we remove the 00
    if stringFrmtd[1] == "3":
      # obviously its +33 something so French number !
      frenchNumber = True
    else:
      ukNumber = True

  elif len(stringFrmtd) == 10:
    # 10 numbers, guess it's french
    frenchNumber = True
    stringFrmtd = "+33" + stringFrmtd[1:] # we remove the 0

  elif len(stringFrmtd) == 11:
    # 11 numbers, guess it's uk
    ukNumber = True
    stringFrmtd = "+44" + stringFrmtd[1:] # we remove the 0

  if frenchNumber:
    nb = stringFrmtd[0] + stringFrmtd[1] + stringFrmtd[2] + " " + stringFrmtd[3] + " " + stringFrmtd[4] + stringFrmtd[5]  + " " + stringFrmtd[6] + stringFrmtd[7]  + " " + stringFrmtd[8] + stringFrmtd[9] + " " + stringFrmtd[10] + stringFrmtd[11]
    return nb

  elif ukNumber:
    nb = stringFrmtd[0] + stringFrmtd[1] + stringFrmtd[2] + " " + stringFrmtd[3] + stringFrmtd[4] + stringFrmtd[5] + stringFrmtd[6] + " " + stringFrmtd[7]  + stringFrmtd[8] + stringFrmtd[9] + stringFrmtd[10] + stringFrmtd[11] + stringFrmtd[12]
    return nb 

  else:
    print stringNb + " wasn't recognised and so wasn't processed."
    return stringNb

def csvPhonesNb(arrayFirstLine):
  csvPhonesNbIndex
  i = 0
  while i < len(arrayFirstLine):
    if ("Phone" in arrayFirstLine[i] and "Value" in arrayFirstLine[i]):
      csvPhonesNbIndex.append(i)
    i += 1

  return csvPhonesNbIndex

def testProcessing():
  number1 = "06 32 30 45 67"
  number2 = "0745322134"
  number3 = "+33 6 54 78 43 26"
  number4 = "+33654784326"
  number5 = "00 33 6 45 36 78 54"

  number6 = "07456093456"
  number7 = "074 560 934 56"
  number8 = "00 44 745609 3456"
  number9 = "+447456093456"

  nb1 = numberProcessing(number1)
  nb2 = numberProcessing(number2)
  nb3 = numberProcessing(number3)
  nb4 = numberProcessing(number4)
  nb5 = numberProcessing(number5)
  nb6 = numberProcessing(number6)
  nb7 = numberProcessing(number7)
  nb8 = numberProcessing(number8)
  nb9 = numberProcessing(number9)

  print nb1
  print nb2
  print nb3
  print nb4
  print nb5
  print nb6
  print nb7
  print nb8
  print nb9


if len(sys.argv) != 3:
  sys.exit("Too few or too many arguments!")

try:
  csvFile = open(sys.argv[1], 'rb')
except IOError:
    print "Could not open file!"
    sys.exit("Exiting script.")

with csvFile:
  ouputFile = open(sys.argv[2], 'wb')

  reader = UnicodeReader(csvFile)
  writer = UnicodeWriter(ouputFile,quoting=csv.QUOTE_ALL)

  i = 0
  csvPhonesNbIndex = []

  print "Start the processing..."
  for row in reader:
    if i == 0:
      i = 1
      csvPhonesNbIndex = csvPhonesNb(row)
      #print csvPhonesNbIndex
      writer.writerow(row)
    else:
      newRow = row
      j = 0
      while j < len(csvPhonesNbIndex):
        index = csvPhonesNbIndex[j]
        if row[index] != "": # we can process the string
          newRow[index] = separateAndProcess(row[index])
        j += 1

      writer.writerow(newRow)

  print "All done!"

  csvFile.close()