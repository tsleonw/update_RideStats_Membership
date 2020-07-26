from zipfile import ZipFile
from shutil import copy

manifest = ["waAPIClient.py",
            "URSMConfig.py",
            "updateRideStatsMembership.py",
            "updateRideStats.zip",
            "rideStatsClient.py",
            "updateRideStats.sh",
            "readme.txt",
            ]
targetDirectory = "/Users/tslcw/UpdateRideStats/Test/"

def copyFiles(manifest, targetDirectory):
    for file in manifest:
        newFile = copy(file,targetDirectory)
        print("created file:  ", newFile)

def createZipFile():
    """
    create a zip file of the files needed to update the membership list in rideStats.
    """
    zip = ZipFile('UpdateRideStats.zip', 'w')
    zip.write('rideStatsClient.py')
    zip.write('updateRideStats.sh')
    zip.write('updateRideStatsMembership.py')
    zip.write('URSMConfig.py')
    zip.write("waAPIClient.py")
    zip.write("readme.txt")
    zip.close()

if __name__ == "__main__":
    createZipFile()
    copyFiles(manifest, targetDirectory)
