# Importing Necessary packages
import getpass
import datetime
import platform
from pathlib import Path
import pickle
import pyzipper
import os

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Firstly, getting OS details of this system. It would be useful later
present_os = platform.system()

## Greeting the user
try:
    user_name = getpass.getuser()
    print("Hello {}!!. \nHope you're having a great day.".format(user_name.capitalize()))
except:
    print("Hello there!!. \nHope you're having a great day.")

# Asking user the date for which content needs to be added to diary.
## Giving options such as Today, yesterday and a custom date.
print("Please enter the date for which you want to add contents:\n1: for Today, 0 for Yesterday. Else, write a custom date of your choise in format: DD/MM or D/M. Add year if necessary")

while True:
    user_inp = input()
    if user_inp == '1':
        input_date = datetime.date.today()
        break
    elif user_inp == '0':
        input_date = datetime.date.today() - datetime.timedelta(days=1)
        break
    else:
        try:  # before formatting the custom date user might have entered, checking its integrity.
            if int(user_inp.split('/')[1]) >= 1 or int(user_inp.split('/')[1]) <= 12:  # Month entered should be between 1-12
                if int(user_inp.split('/')[0]) >= 1 or int(user_inp.split('/')[0]) <= 31:  # Date entered should be between 1-31
                    # Converting the input into datetime format
                    try:  # checking if we have year entered by user
                        if len(user_inp.split("/")[2]) <4: # Checking if length of year (as string) = 4
                            print("Enter the year correctly")
                        elif len(user_inp.split("/")[2]) == 4:
                            input_date = datetime.datetime.strptime(user_inp,"%d/%m/%Y")
                            break
                    except:  # if we don't have year, taking the current year.
                        input_date = datetime.datetime.strptime(user_inp+"/"+str(datetime.datetime.today().year),"%d/%m/%Y")
                        break

                else:
                    print("Try again")
            else:
                print("Try again")
        except:
            print("Try again")

## correctly formating the datetime interpreted to be pushed as filename
input_date_formated = input_date.strftime("%Y-%m-%d")  # YYYY-MM-DD format for diary item's name

# Taking content to be dumped into the diary file from user
print("Start entering your inputs (if you want to end, simply type 'END'/ 'end' on a new line): ")
content_list = []  # for storing multi line input
while True:
    line = input()
    if line.lower() == 'end':
        break
    content_list.append(line)
print("Got it!")
content = "\n".join(content_list)  # Converting list to string.

# Setting up the target directory in which we would dump these diary note files.
## For this, we would (by default) store it inside a folder named '{user_name}_diary_content' inside the system's Documents folder.
## But, the exact path of this is different for different OSes. let's define those.
## Let's first check if we have some directory defined from our previous run, saved in same directory as this file
try:
    with open('diary_input.pickle', 'rb') as f:
        target_dir,password = pickle.load(f)  # We would save/ retrive the target directory & password (to be used for encrypting the zip file)
except:  # in case, we don't have this pickle file (1st run)
    # In such cases, we are considering Documents/{user_name}_diary_content as default
    if present_os == 'Linux':
        target_dir = '/home/{}/Documents'.format(user_name)
    elif present_os.lower().startswith('darwin'):
        target_dir = '/Users/{}/Documents'.format(user_name)
    elif present_os == 'Windows':
        target_dir = Path("C:/Users")/user_name/"Documents".format(user_name) 

# So by default, this program would use documents folder to save a target folder for saving all the diary content files, but giving user the option to change it...

print("Using the directory: '{}'.".format(target_dir)+" I would save the directory: {}_diary_contents in this.".format(user_name))
print("Would I proceed with this?")
user_input = input("Y/n: ") 
while True:
    try:
        if user_input.lower() == 'n':
            user_inp_dir = input("Enter the new directory (I would save yourname_diary_contents here): ")
            dir_obj = Path(user_inp_dir)
            if dir_obj.is_dir():  # Checking if the entered directory actually exists. if yes, we would save it for next consecutive runs 
                target_dir = dir_obj
                break
            else:
                print("Enter a valid directory")
        elif user_input.lower() == 'y':
            print("Ok!")
            break
        else:
            print("Enter either y/n")
    except:
        print("Try again")


# Creating that target directory, if not present. In target_dir selected, we add {user_name}_diary_content
target_dir_actual = target_dir+"/"+user_name+"_diary_contents"  # this directory is the one in which we'll dump diary files
target_dir_obj = Path(target_dir)
target_dir_obj.parent.mkdir(parents=True, exist_ok=True)

# Pushing the newly created file here.
with open(target_dir+'/'+input_date_formated, 'w', encoding='utf-8') as f1:
    f1.write(content)


# Now creating a .zip protected file to be pushed to Google drive
## Taking password from the saved pickle file (from 2nd run)
## We would save this file in target_dir

if 'password' in globals():
    print("Hey, I have your previously used password, would you like to go ahead with the same or change it?:")  # In case of password already present (from 2nd run), we would ask user to continue or to change it.
    while True:
        user_inp = input("Type 'C' to change or 'N' to continue")
        if user_inp.lower() == 'c':
            password = input("Enter a suitable, strong password for your export zip file: ")
            break
        elif user_inp.lower() == 'n':
            break
        else:
            print("Invalid response. Please try again.")

print("Zipping & encoding your export.")
passbytes = password.encode('utf-8')
# Pickling this & the target directory to make sure we don't have to ask it to user again.
## it would be saved in the target_dir
with open('diary_input.pickle','wb') as f2:
    pickle.dump([target_dir,password],f2)

## Encrypting the target zip for securing it before storing it on gdrive.
zip_file_name = 'diary_content_webpush.zip'  # Desired name for the zip file. You can change it here if you want.
with pyzipper.AESZipFile(Path(target_dir)/zip_file_name, 'w',compression=pyzipper.ZIP_LZMA, 
                             encryption=pyzipper.WZ_AES) as zf:
    zf.setpassword(passbytes)
    for root, dirs, files in os.walk(target_dir_actual):
        for file in files:
            file_path = Path(root) / file
            # Calculate the relative path to maintain folder structure
            arcname = file_path.relative_to(target_dir_actual)
            zf.write(file_path, arcname)

# Connecting to Google drive
## Please replace the following variables with your own values.
scopes = ['https://www.googleapis.com/auth/drive.file']
file_name = zip_file_name
file_path = target_dir+'/'+zip_file_name
gdrive_folder_id = 'google_drive_folder_id'  # change this with your target folder id of your google drive. 
## (from the newly created folder URL, folder id is the thing after /folders/)

def get_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes).run_local_server(port=0)
        with open('token.json', 'w') as f:
            f.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def call_google():
    service = get_service()
    media = MediaFileUpload(file_path, mimetype='application/zip')

    # Check if file already exists in the folder
    existing = service.files().list(
        q=f"name='{file_name}' and '{gdrive_folder_id}' in parents and trashed=false",
        fields="files(id)"
    ).execute().get('files', [])

    if existing:
        service.files().update(fileId=existing[0]['id'], media_body=media).execute()
        print("File updated.")
    else:
        service.files().create(body={'name': file_name, 'parents': [gdrive_folder_id]}, media_body=media).execute()
        print("File uploaded.")


# Asking user if he/she wants to use Google API to upload this zip to cloud now?. Or exit the program.
while True:
    print("Do you want to backup the diary on cloud?:")
    c_backup = input("Y/n")
    if c_backup.lower() == 'y':
        call_google()  # If yes, it would connect to the google drive API
        break
    elif c_backup.lower() == 'n':
        print("Got it!\n have a great day ahead!")
        break
    else:
        print("Invalid response, Please try again..")

