import re
import json
import subprocess
import sys

subprocess.run(["figlet", "  Flipreps"])

# Display the options to the user
print("--- FLIght Plan REceipt Printing System ---")
print("Options \n(1) Print custom (lesson plan, notes...)")
print("(2) Print FPLAN")

choice = input("Select an option (1/2): ")

if choice == "1":
    # quick copy-paste area so that i can copy lesson plan or additional notes and print them

    # User prompt
    print("Paste the raw data and press Ctrl+D (Ctrl+Z on Windows) when you're done:")
    raw_data = sys.stdin.read()

    # Remove non-printable characters
    # data = re.sub(r'[^\x20-\x7E\n]', '', raw_data)
    data = ''.join(c for c in raw_data if c.isprintable() or c == '\n')

    print("this is it")
    print(data)

    
    subprocess.run(["php", "printCUS.php", data])



elif choice == "2":
    # tool that grabs a SkyVector fplan pdf that the user grabbed with Ctrl+A over the whole document, and parses it into a format that makes it easy for a receipt printer to print over shell (usb lp kinda jazz)

    # Sample data (for testing)
    # with open('fplan4.txt', 'r') as file:
        # raw_data = file.read()

    # User prompt
    print("Paste the raw data and press Ctrl+D (Ctrl+Z on Windows) when you're done:")
    raw_data = sys.stdin.read()

    # Remove non-printable characters
    # data = re.sub(r'[^\x20-\x7E\n]', '', raw_data)
    data = ''.join(c for c in raw_data if c.isprintable() or c == '\n')
    

    # Find all occurrences of the "N....W...." pattern, this is how many legs we are doing FIX THIS BECAUSE I MAY BE IN COORDS S...W... OR S...E... OR N...E... (lol)
    pattern = r'N \d+°\d+\.\d+\'\nW \d+°\d+\.\d+\''
    matches = re.finditer(pattern, data)
    num_occurrences = len(list(matches)) - 1

    # Create a list of dictionaries, which will be all the legs
    dictionary_list = []

    # Iterate through the occurrences and create dictionaries
    for i in range(num_occurrences):
        dictionary = {
            'leg': i + 1, #done (by regex)
            'from': None, #done (by text grabbing)
            'to': None, #done (by text grabbing)
            'wind_direction': None,
            'wind_speed': None,
            'temp': None,
            'temp_deviation': None,
            'TAS': None, #done (by text grabbing)
            'Track': None, 
            'WCA': None,
            'TH': None,
            'Var': None,
            'Magnetic Heading': None, #done (by text grabbing)
            'Ground Speed': None, #done (by text grabbing)
            'Distance': None, #done (by text grabbing)
            'ETA': None, #done (mathematically)
            'CumETA': None #done (mathematically)
        }
        dictionary_list.append(dictionary)

    # Find the lines that match the "N...W..." pattern
    lines = re.finditer(pattern, data)

    # Get the line number of the termination of the last occurrence
    last_occurrence_index = -1
    for match in lines:
        last_occurrence_index = match.end()

    # Calculate the starting line for populating the TAS, Magnetic Heading, Ground Speed, and Distance values aka populate1
    populate1 = data.count('\n', 0, last_occurrence_index) + 2

    # Process lines containing TAS, Magnetic Heading, Ground Speed, Distance
    lines = data.split('\n')
    cumulative_eta = 0 # for later
    for i in range(populate1, populate1 + num_occurrences):
        values = lines[i].split()
        dictionary_list[i - populate1]['TAS'] = int(values[0])
        dictionary_list[i - populate1]['Magnetic Heading'] = values[1]
        dictionary_list[i - populate1]['Ground Speed'] = int(values[2])
        dictionary_list[i - populate1]['Distance'] = float(values[3])
        
        # Working out ETA and CumETA mathematically because it's tough to regex-pull them out 
        eta = (dictionary_list[i - populate1]['Distance'] / dictionary_list[i - populate1]['Ground Speed']) * 60
        # Calculate seconds and minutes
        total_minutes = int(eta)
        minutes = total_minutes % 60
        hours = total_minutes // 60
        seconds = int((eta - total_minutes) * 60)
        # Format ETA as "hours:minutes"
        dictionary_list[i - populate1]['ETA'] = '{:02d}:{:02d}'.format(minutes, seconds)

        cumulative_eta += eta
        cum_minutes = int(cumulative_eta)
        cum_seconds = int((cumulative_eta - cum_minutes) * 60)
        if cum_minutes >= 60:
            cum_hours = cum_minutes // 60
            cum_minutes %= 60
            dictionary_list[i - populate1]['CumETA'] = '{:02d}:{:02d}:{:02d}'.format(cum_hours, cum_minutes, cum_seconds)
        else:
            dictionary_list[i - populate1]['CumETA'] = '{:02d}:{:02d}'.format(cum_minutes, cum_seconds)


    # Working out TO and FROM: 
    # Read the first x*2 lines from the file where x is num_occurrences, this will get the icons from/to as well as the text of from/to
    adjusted_occurences = num_occurrences + 2
    file_lines = data.split('\n')
    input_data = '\n'.join(file_lines[:adjusted_occurences * 2])
    lines = input_data.split('\n')
    tofrom = lines[-adjusted_occurences:]
    tofrom_new = tofrom[:-1]
    #   DEBUGGING?
    # print(tofrom_new)

    # Find UserFix
    for i in range(len(tofrom_new) - 1):
        if tofrom_new[i] == "UserFix":
            tofrom_new[i] = input("New location name: ")

    # Update dictionary_list with new names
    for i in range(len(tofrom_new) - 1):
            dictionary_list[i]['from'] = tofrom_new[i]
            dictionary_list[i]['to'] = tofrom_new[i + 1]


    #   DEBUGGING?
    # for dictionary in dictionary_list:
    #    print(dictionary)

    # Convert the dictionary_list to a JSON-encoded string
    data_json = json.dumps(dictionary_list)
    # Run the PHP script and pass the JSON-encoded data as an argument
    subprocess.run(["php", "printFPL.php", data_json])