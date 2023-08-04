import webbrowser
import json
import os
import time

import moduleinstaller

try:
    import schedule
    import selenium
except ImportError:
    moduleinstaller.install_modules(['schedule', 'selenium'])

no_classes = True
num_classes = None
path = None

days = {'monday' : [], 'tuesday' : [], 'wednesday' : [], 'thursday' : [], 'friday' : []}

def open_url(url):
    webbrowser.open_new_tab(url)
    print(f'{time.asctime()}: Opened a new tab.')

def make_schedule():
    for Classes in range(num_classes):
        schedule.every().monday.at(days['monday'][Classes][1]).do(open_url, url = days['monday'][Classes][0])
        schedule.every().monday.at(days['tuesday'][Classes][1]).do(open_url, url = days['tuesday'][Classes][0])
        schedule.every().wednesday.at(days['wednesday'][Classes][1]).do(open_url, url = days['wednesday'][Classes][0])
        schedule.every().thursday.at(days['thursday'][Classes][1]).do(open_url, url = days['thursday'][Classes][0])
        schedule.every().friday.at(days['friday'][Classes][1]).do(open_url, url = days['friday'][Classes][0])

path = os.path.normpath(__file__ + os.sep + os.pardir + os.sep + os.pardir + os.sep + 'res')
os.makedirs(path, exist_ok=True)

file = path + os.sep + 'config.json'

try:
    savedschedule = open(file, 'r')
except FileNotFoundError:
    savedschedule = open(file, 'w+')
char = savedschedule.read(1)
savedschedule.close()

#no previous schedule
if not char:
    print('Looks like you don\'t have a schedule.')

    #loop for try/except
    while no_classes:

        #create schedule
        try:
            num_classes = int(input('Enter the number of classes you take per day: '))
            print(f'You take {num_classes} classes.')

            #iterates through the days of the week
            for day in days:
                #inputs to determine class time + link
                for Class in range(num_classes):
                    class_link = input(f'Enter the link for class {Class+1} of {num_classes} on {day} (ex https://www.zoom.us/j/738912): ')
                    class_time = input(f'Enter the time for class {Class+1} of {num_classes} on {day} (ex. 08:25 or 22:45): ')

                    #if class time was not formatted correctly
                    if len(class_time) < 5:
                        class_time = '0' + class_time

                    days[day].append((class_link, class_time))

            #actually starts to schedule everything
            make_schedule()

            #breaks out of the loop
            no_classes = False

        #input given was not an integer
        except ValueError:
            print('it has to be an integer dumdum')
            continue
        
    #confirmation with no errors
    print('Successfully scheduled everything!')

    #saves created schedule to json file
    with open(file, 'w') as openedfile:
        info = {'schedule' : days, 'number of classes' : num_classes}
        json.dump(info, openedfile)
        openedfile.close()

#schedule found in json file
else:
    print('You already have a schedule.')

    #copies previous schedule to dictionary
    with open(file, 'r') as savedschedule:
        data = []
        for line in savedschedule:
            data.append(json.loads(line))

        num_classes = data[0]["number of classes"]
        days = data[0]["schedule"]
        
        savedschedule.close()

    #schedules again
    make_schedule()

    print('Scheduled all classes. Waiting...')

#waits for pending tasks and runs them
while True:
    schedule.run_pending()
    time.sleep(1)