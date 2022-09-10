from utilities import *

isoDate = "2022-09-10T15:30:00-04:00"
expectedEpoch = 1662838200
expectedMMDDYYYY = "09/10/2022"
def test_isoDateToEpoch():
    epoch = isoDateStringToEpoch(isoDate)
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