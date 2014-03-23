################################
# Work under CC BY 4.0 license #
#      by Cyril NOVEL          #
################################
import csv
import codecs
import cStringIO

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


# Process the phone number
def numberProcessing(stringNb):
  if stringNb[0] == "+":
    space = False
    for c in stringNb:
      if c == " ":
        space = True

    if not space:
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
    for c in stringNb :
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
ouputFile = open('output.csv', 'wb')

reader = UnicodeReader(csvFile)
writer = UnicodeWriter(ouputFile,quoting=csv.QUOTE_ALL)

i = 0
csvPhonesNbIndex = []

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
      if row[index] != "": # we can process the string
        newRow[index] = numberProcessing(row[index])
      j += 1

    writer.writerow(newRow)

csvFile.close()