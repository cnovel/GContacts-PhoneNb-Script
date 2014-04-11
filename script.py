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
  stringFrmtd = stringNb.replace(" ", "")
  frenchNumber = false
  ukNumber = false
  # there is no space to worry about in the new string
  if stringFrmtd[0] == "+"
    #international number here
    if stringFrmtd[1] == 3:
      # obviously its +33 something so French number !
      frenchNumber = True
    else:
      ukNumber = True

  elif stringFrmtd[0] == "0" and stringFrmtd[1] == "0":
    #international number here again
    stringFrmtd = "+" + stringFrmtd[2:] # we remove the 00
    if stringFrmtd[1] == 3:
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
    return stringNb

def csvPhonesNb(arrayFirstLine):
  csvPhonesNbIndex
  i = 0
  while i < len(arrayFirstLine):
    if ("Phone" in arrayFirstLine[i] and "Value" in arrayFirstLine[i]):
      csvPhonesNbIndex.append(i)
    i += 1

  return csvPhonesNbIndex


csvFile = open('test.csv', 'rb')
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