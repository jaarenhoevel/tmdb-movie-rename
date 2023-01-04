import os, configparser, argparse
import tmdbsimple as tmdb

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser(description='Rename movie files with the help of TMDB database.')
parser.add_argument('directory', help='Directory containing the movie file to be renamed and moved')

args = parser.parse_args()

# Check source directory
directory = args.directory
if not os.path.isdir(directory):
    print("No such directory.")
    exit()

# Check for config in user config directory
configFile = os.path.expanduser("~/.config/tmdb-movie-rename/config.ini")
if not os.path.isfile(configFile):
    print("No config file found.")
    exit();

config = configparser.ConfigParser()
config.read(configFile)

# Set API key
tmdb.API_KEY = config["TMDB"]["ApiKey"]

# Get list of files in directory
files = os.listdir(directory)

# Filter out non-movie files
movieFiles = [f for f in files if f.endswith(('.mkv', '.mp4', '.avi', '.m4v'))]

## Check if there is a clear largest file
largestFile = max(movieFiles, key=lambda x: os.path.getsize(os.path.join(directory, x)))
largestFileSize = os.path.getsize(os.path.join(directory, largestFile))

# Check if there are any other files within selected margin of the size of the largest file
closeSizeFiles = [f for f in movieFiles if abs(os.path.getsize(os.path.join(directory, f)) - largestFileSize) / largestFileSize <= float(config["General"]["SimilarFileSizeMargin"])]

if len(closeSizeFiles) == 1:
    # Use largest file
    movieFile = largestFile
    print(f'Selected file: {movieFile} ({largestFileSize / 1024 / 1024 / 1024:.2f} GiB)')
else:
    # Sort list of files by size
    movieFiles.sort(key=lambda x: os.path.getsize(os.path.join(directory, x)), reverse=True)
    
    # Print list of files for user to select from
    print("Select a movie file:")
    for index, file in enumerate(movieFiles):
        fileSize = os.path.getsize(os.path.join(directory, file))
        if abs(fileSize - largestFileSize) / largestFileSize <= float(config["General"]["SimilarFileSizeMargin"]):
            # Highlight file if it is within selected margin of the size of the largest file
            print(f'{index + 1} - {bcolors.OKGREEN}{file}{bcolors.ENDC} ({fileSize / 1024 / 1024 / 1024:.2f} GiB)')
        else:
            print(f'{index + 1} - {file} ({fileSize / 1024 / 1024 / 1024:.2f} GiB)')

    selectedIndex = int(input(">>> ")) - 1
    movieFile = movieFiles[selectedIndex]

# Get movie file extension
movieFileExtension = os.path.splitext(movieFile)[1]

# Ask for movie name 
print("Movie name:")
search = tmdb.Search()
search.movie(query=input(">>> "))

# Print all results
print("\nResults:")
for index, movie in enumerate(search.results):    
    print(f'{index + 1} - {movie["title"]} ({movie["release_date"][:4]})')
    print(f'{bcolors.OKGREEN}{movie["overview"]}{bcolors.ENDC}\n')

print("Select a movie:")
selectedIndex = int(input(">>> ")) - 1

# Generate name from selected movie
selectedMovie = search.results[selectedIndex]
newName = f'{selectedMovie["title"]} ({selectedMovie["release_date"][:4]})'

print("\n\nAppend 3D MVC suffix to file name? [y/N]")
appendSuffix = input(">>> ");
if  appendSuffix == "y" or appendSuffix == "Y":
    newName += config["General"]["Kodi3DSuffix"]

newName += movieFileExtension

# Let user check new name
print(f'\n\nNew file name is "{newName}". Is this correct? [Y/n]')
correct = input(">>> ")
if correct == "n" or correct == "N":
    print("Exiting...")
    exit()

# Print target directories
targetDirectories = []
print("\n\nMove file to directory? [Skip]")
for index, tDirectory in enumerate(config["Target Directories"]):
    print(f'{index + 1} - {tDirectory.upper()}')
    print(f'{bcolors.OKGREEN}{config["Target Directories"][tDirectory]}{bcolors.ENDC}\n')
    targetDirectories.append(config["Target Directories"][tDirectory])

targetDirectorySelection = input(">>> ")
if targetDirectorySelection != "":
    targetDirectory = targetDirectories[int(targetDirectorySelection) - 1]
else:
    targetDirectory = os.path.abspath(os.getcwd())

finalTarget = targetDirectory + "/" + newName

if os.path.isfile(finalTarget):
    print("Target file already exists. Exiting...")
    exit()

print(f'\n\nTarget: "{finalTarget}". Move/Rename file? [Y/n]')
confirm = input(">>> ")
if confirm == "n" or confirm == "N":
    print("Exiting...")
    exit()

print("\n\nRenaming file...")
os.rename(directory + "/" + movieFile, finalTarget)
print("Finished!")