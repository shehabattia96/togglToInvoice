from utilities import *

isoDate = "2022-06-20T18:56:34Z"
expectedEpoch = 1655751394
expectedMMDDYYYY = "06/20/2022"
def test_isoDateToEpoch():
    epoch = isoDateStringToEpochSeconds(isoDate)
    assert epoch == expectedEpoch, f"Expected {expectedEpoch}. Got {epoch}"
def test_epochToIsoDate():
    isoDate = epochToIsoDateString(expectedEpoch)
    assert isoDate == isoDate, f"Expected {isoDate}. Got {isoDate}"
def test_epochToMMDDYYYYDate():
    mMDDYYYY = epochToMMDDYYYYString(expectedEpoch)
    assert mMDDYYYY == expectedMMDDYYYY, f"Expected {expectedMMDDYYYY}. Got {mMDDYYYY}"

if __name__ == "__main__":
    test_isoDateToEpoch()
    test_epochToIsoDate()
    test_epochToMMDDYYYYDate()
    print("Done test_utilities")