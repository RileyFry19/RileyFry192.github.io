# This program takes input from a file and takes the data to make a print sheet.
# It takes displays the store name, patch name, quantity of pumpkins, price of pumpkins, and how much the store spent on pumpkins.
# It takes the quantity, price, and store cost and calculates how much in total a store has of each.

import datetime
oDate = ''
cPgctr = 0
cLinectr = 0

def main():
    pumpkinFileRead, pumpkinFileWrite, hStore, iStore, hPatch, iPatch, iRec, cMnQty, cMnStoreCost, cMjQty, cMjStoreCost, cGtQty, cGtStoreCost = init()
    while iRec != '':
        if hStore != iStore:
            cMjQty, cMjStoreCost, cMnQty, cMnStoreCost, hPatch = minorSubtotals(pumpkinFileWrite, hStore, hPatch, iPatch, cMjQty, cMjStoreCost, cMnQty, cMnStoreCost)
            cGtQty, cGtStoreCost, cMjQty, cMjStoreCost, hStore = majorSubtotals(pumpkinFileWrite, hStore, iStore, cGtQty, cGtStoreCost, cMjQty, cMjStoreCost)
        else:
            if hPatch != iPatch:
                cMjQty, cMjStoreCost, cMnQty, cMnStoreCost, hPatch = minorSubtotals(pumpkinFileWrite, hStore, hPatch, iPatch, cMjQty, cMjStoreCost, cMnQty, cMnStoreCost)
        iPatch, iQty, iPrice, cStoreCost, iStore, cMnQty, cMnStoreCost = calcs(iRec, cMnQty, cMnStoreCost)
        output(pumpkinFileWrite, iPatch, iQty, iPrice, cStoreCost, iStore)
        iRec, iStore, iPatch = read(pumpkinFileRead)
    cMjQty, cMjStoreCost, cMnQty, cMnStoreCost, hPatch = minorSubtotals(pumpkinFileWrite, hStore, hPatch, iPatch, cMjQty, cMjStoreCost, cMnQty, cMnStoreCost)
    cGtQty, cGtStoreCost, cMjQty, cMjStoreCost, hStore = majorSubtotals(pumpkinFileWrite, hStore, iStore, cGtQty, cGtStoreCost, cMjQty, cMjStoreCost)
    grandTotals(pumpkinFileWrite, cGtQty, cGtStoreCost)
    closing(pumpkinFileRead, pumpkinFileWrite)

def init():
    global oDate
    oDate = datetime.datetime.today().strftime('%b/%d/%Y')

    try:
        pumpkinFileRead = open(r'C:\Python\pumpkin.dat', 'r')
    except IOError:
        print("File Error. Program Terminated.")
        exit(0) 
    iRec, iStore, iPatch = read(pumpkinFileRead)

    try:
        pumpkinFileWrite = open(r'C:\Python\pumpkinrep.prt', 'w')
    except IOError:
        print("File Error. Program Terminated.")
        exit(0)

    hdgs(pumpkinFileWrite)

    cMnQty = 0
    cMnStoreCost = 0
    cMjQty = 0
    cMjStoreCost = 0
    cGtQty = 0
    cGtStoreCost = 0

    hStore = iStore
    hPatch = iPatch

    return pumpkinFileRead, pumpkinFileWrite, hStore, iStore, hPatch, iPatch, iRec, cMnQty, cMnStoreCost, cMjQty, cMjStoreCost, cGtQty, cGtStoreCost

def hdgs(pumpkinFileWrite):
    global cPgctr, oDate, cLineCtr
    cPgctr += 1
    pumpkinFileWrite.write("Date: " + oDate + format(" ", "14s") + "Great Pumpkin Ranch" + format(" ", "22s") + "Page: " + format(cPgctr, "2d") + "\n" + format(" ", "35s") + "Sales Report" +
                          "\n" + "" + "\n" + "Store Name" + format(" ", "9s") + "Patch Name" + format(" ", "11s") + "Quantity" + format(" ", "10s") + "Price" + format(" ", "7s") + "Store Cost" + "\n" + "")
    cLineCtr = 5

def read(pumpkinFile):
    iRec = pumpkinFile.readline()
    iStore = str(iRec[0:10])
    iPatch = str(iRec[10:11])
    if iPatch == "N":
        iPatch = "North"
    elif iPatch == "S":
        iPatch = "Skunk Creek"
    elif iPatch == "B":
        iPatch = "Back 40"
    return iRec, iStore, iPatch

def minorSubtotals(pumpkinFileWrite, hStore, hPatch, iPatch, cMjQty, cMjStoreCost, cMnQty, cMnStoreCost):
    global cLineCtr
    pumpkinFileWrite.write("\n" + format(hStore, "10s") + format(" ", "1s") + "Minor:" + format(" ", "2s") + format(hPatch, "11s") + format(" ", "12s") + format(cMnQty, "6,d") + format(" ", "20s") + format(cMnStoreCost, "12,.2f") + "\n" + "")

    cMjQty += cMnQty
    cMjStoreCost += cMnStoreCost
    cMnQty = 0
    cMnStoreCost = 0

    hPatch = iPatch

    cLineCtr += 2
    if cLineCtr > 55:
        hdgs(pumpkinFileWrite)
    return cMjQty, cMjStoreCost, cMnQty, cMnStoreCost, hPatch

def majorSubtotals(pumpkinFileWrite, hStore, iStore, cGtQty, cGtStoreCost, cMjQty, cMjStoreCost):
    global cLineCtr
    pumpkinFileWrite.write("\n" + format(hStore, "10s") + format(" ", "1s") + "Major:" + format(" ", "22s") + format(cMjQty, "9,d") + format(" ", "20s") + format(cMjStoreCost, "12,.2f") + "\n" + "")
    cGtQty += cMjQty
    cGtStoreCost += cMjStoreCost
    cMjQty = 0
    cMjStoreCost = 0

    hStore = iStore

    cLineCtr += 2
    if cLineCtr > 55:
        hdgs(pumpkinFileWrite)
    return cGtQty, cGtStoreCost, cMjQty, cMjStoreCost, hStore

def calcs(iRec, cMnQty, cMnStoreCost):
    iPatch = str(iRec[10:11])
    if iPatch == "N":
        iPatch = "North"
    elif iPatch == "S":
        iPatch = "Skunk Creek"
    elif iPatch == "B":
        iPatch = "Back 40"
    iQty = int(iRec[11:14])
    iPrice = float(iRec[14:18])/100
    cStoreCost = iQty * iPrice
    iStore = str(iRec[0:10])
    cMnQty += iQty
    cMnStoreCost += cStoreCost
    return iPatch, iQty, iPrice, cStoreCost, iStore, cMnQty, cMnStoreCost

def output(pumpkinFileWrite, iPatch, iQty, iPrice, cStoreCost, iStore):
    global cLineCtr
    pumpkinFileWrite.write("\n" + format(iStore, "10s") + format(" ", "9s") + format(iPatch, "11s") + format(" ", "15s") + format(iQty, "3d") + 
                           format(" ", "11s") + format(iPrice, "3,.2f") + format(" ", "9s") + format(cStoreCost, "8,.2f") + "\n" + "")
    cLineCtr += 2
    if cLineCtr > 55:
        hdgs(pumpkinFileWrite)

def grandTotals(pumpkinFileWrite, cGtQty, cGtStoreCost):
    pumpkinFileWrite.write("\n" + format(" ", "3s") + "Grand Totals" + format(" ", "22s") + format(cGtQty, "11,d") + format(" ", "18s") + format(cGtStoreCost, "14,.2f"))

def closing(pumpkinFileRead, pumpkinFileWrite):
    pumpkinFileRead.close()
    pumpkinFileWrite.close()

main()