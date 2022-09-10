import sys

# CLI Args:
# python fetchDataAndGenerateInvoice.py {isDebug}
# isDebug: debug mode is ON if anything other than "0" or undefined is passed in.

isDebug = sys.argv[1] != "0" if len(sys.argv) > 1 else False

if isDebug:
    print("Debug mode on.")

def printDebug(message):
    if isDebug:
        print(message)

if __name__ == "__main__":
    printDebug("Fetching data from Toggl")

    printDebug("Generating template")

    