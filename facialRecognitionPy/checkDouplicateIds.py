import os
import pickle

#Origin folder
KNOWN_IDS_DIR = 'knownIds'

#Global variables
checkedFileInfo = []
knownFiles = []
folderForFile = []
deleteFiles = []
indexOfFiles = 0
shouldBeId = 0

#Convert string to list
def ConvertToList(string) :
    if '-' in string :
        li = list(string.split('-'))
        return li
    else :
        li=[]
        li[:0]=string
        return li

#Function to convert list to string 
def ConvertToString(s) : 
    # initialize an empty string
    str1 = '-'  
    # return string  
    return (str1.join(s))

#Function used to replace incorrect id with a new id
def ReIdentify(string, newId, folder) :
    print(type(string))
    if folder == "y" and "-" not in string :
        id = newId
        id = ConvertToString(id)
    else :
        id = ConvertToList(string)
        id.pop(0)
        id.insert(0, newId)
        id = ConvertToString(id)
    return id

#Custom function that sortes the origin folder
def BetterNumberStrSort(list) :
    li2 = []
    li3 = []
    sortedList = []
    for string in list :
        dict = {
            'id': '',
        }
        if '-'in string :
            li = string.split('-')
            dict['id'] = li[0]
            dict['string'] = li[1]
            li2.append(dict)
        else :
            li = string
            dict['id'] = li
            li = []
            li.append(string)
            li2.append(dict)
        li3.append(int(li[0]))
    li3.sort()
    li4 = []
    for dict in li2 :
        li4.append([value for value in dict.values()][0])
    for i in li3 :
        check = li2[li4.index(str(i))]
        li5 = []
        for val in check.values() :
            li5.append(val)
        li5String = ConvertToString(li5)
        sortedList.append(li5String)
    return sortedList 

sortedKnownIdsDir = BetterNumberStrSort(os.listdir(KNOWN_IDS_DIR))

#Check files in the origin folder
for name in sortedKnownIdsDir :
    for filename in os.listdir(f'{KNOWN_IDS_DIR}/{name}') :
        fileInfo = pickle.load(open(f'{KNOWN_IDS_DIR}\{name}\{filename}', 'rb'))

        checkedFileInfo.append(fileInfo)
        knownFiles.append(filename)
        folderForFile.append(f'{KNOWN_IDS_DIR}/{name}/')

        indexOfFiles = knownFiles.index(filename)

#Compare files against each other 
for file in knownFiles :
    currentFile = knownFiles.index(file)
    fileCheck = currentFile
    while fileCheck < indexOfFiles :
        checkIfDouplicate = (checkedFileInfo[currentFile] == checkedFileInfo[fileCheck + 1]).all()
        print(f'{checkIfDouplicate}\t{currentFile}=={fileCheck + 1}')
        if checkIfDouplicate == True :
            if [f'{folderForFile[fileCheck + 1]}{knownFiles[fileCheck + 1]}', knownFiles[fileCheck + 1], folderForFile[fileCheck + 1]] not in deleteFiles :
                deleteFiles.append([f'{folderForFile[fileCheck + 1]}{knownFiles[fileCheck + 1]}', knownFiles[fileCheck + 1], folderForFile[fileCheck + 1]])
        fileCheck += 1
    print()

#If there is found any douplicate files inform user and delete them
if len(deleteFiles) > 0 :
    print(f'There has been located {len(deleteFiles)} douplicate file(s)')
    for i in deleteFiles :
        os.remove(i[0])
        print(f'"{i[0]}" has been removed')
        knownFiles.pop(knownFiles.index(i[1]))
        folderForFile.pop(folderForFile.index(i[2]))
        indexOfFiles = len(knownFiles) - 1

#Rename incorrectly named folders and files and delete empty ones
for name in sortedKnownIdsDir :
    nameToId = []
    nameToId = list(name.split('-'))[0]
    #Rename folders
    if nameToId != str(shouldBeId) :
        shouldBeFolderName = ReIdentify(name, str(shouldBeId), "y")
        print(f'The folder name "{name}" is incorrectly named, it should be "{shouldBeFolderName}"')
        try :
            os.rename(f'{KNOWN_IDS_DIR}/{name}', f'{KNOWN_IDS_DIR}/{shouldBeFolderName}')
            name = shouldBeFolderName
            print(f'The folder has now been renamed to "{shouldBeFolderName}"')
        except :
            print('Rename faild')

    #Delete empty folders
    if os.listdir(f'{KNOWN_IDS_DIR}/{name}') == [] :
        print(f'The folder "{name}" is empty')
        os.removedirs(f'{KNOWN_IDS_DIR}\{name}')
        print(f'The folder "{name}" has been removed')
    #Rename files
    else :
        for filename in os.listdir(f'{KNOWN_IDS_DIR}/{name}') :
            nameToId = list(filename.split('-'))[0]
            if nameToId != str(shouldBeId) :
                shouldBeFileName = ReIdentify(filename, str(shouldBeId), "n")
                print(f'The file "{filename}" is incorrectly named, it should be "{shouldBeFileName}"')
                try :
                    os.rename(f'{KNOWN_IDS_DIR}/{name}/{filename}', f'{KNOWN_IDS_DIR}/{name}/{shouldBeFileName}')
                    filename = shouldBeFileName
                    print(f'The folder has now been renamed to "{shouldBeFileName}"')
                except :
                    print('Rename faild')
        shouldBeId += 1