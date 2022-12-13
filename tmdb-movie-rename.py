import os, sys, configparser, argparse
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
parser.add_argument('path', help='movie file to be renamed and moved')

args = parser.parse_args()

# Check source file
movieFile = args.path
if not os.path.isfile(movieFile):
    print("No such file.")
    exit();

movieFileExtension = os.path.splitext(movieFile)[1]

# Check for config in user config directory
configFile = os.path.expanduser("~/.config/tmdb-movie-rename/config.ini")
if not os.path.isfile(configFile):
    print("No config file found.")
    exit();

config = configparser.ConfigParser()
config.read(configFile)

# Set API key
tmdb.API_KEY = config["TMDB"]["ApiKey"]

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
for index, directory in enumerate(config["Target Directories"]):
    print(f'{index + 1} - {directory.upper()}')
    print(f'{bcolors.OKGREEN}{config["Target Directories"][directory]}{bcolors.ENDC}\n')
    targetDirectories.append(config["Target Directories"][directory])

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
os.rename(movieFile, finalTarget)
print("Finished!")