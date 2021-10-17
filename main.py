import os, re
from typing import List

arg_directory = "mc-logs"

class log_reader():
    def __init__(self, directory) -> None:
        self.dir_list = self.find_log_files(directory)

    def find_log_files(self, directory):
        dir_list = os.listdir(directory)
        return_list = []
        for item in dir_list:
            if item == "latest.log":
                pass
            #elif os.path.isfile(item):
            else:
                return_list.append(item)
        return return_list

    def find_log_line(self, string, compiled_regex):
        match = compiled_regex.match(string)

def main():
    dir_list = log_reader(arg_directory).dir_list
    #print(dir_list)

    filename_regex = re.compile(r"(\d{4})-(\d{2})-(\d{2})") # Year, Month, Day
    fileline_regex_1 = re.compile(r"\[(\d{2}):(\d{2}):(\d{2})] \[Client thread/INFO]: Connecting to (.+), (\d+)") # Hour, Minute, Second, ServerAddress, Port   ## Used when joining a server
    fileline_regex_2 = re.compile(r"\[(\d{2}):(\d{2}):(\d{2})] \[Client thread/INFO]: Stopping!") # Hour, Minute, Second                                        ## Used when Minecraft closes
    fileline_regex_3 = re.compile(r"\[(\d{2}):(\d{2}):(\d{2})] \[Client thread/INFO]: Stopping worker threads") # Hour, Minute, Second                          ## Used when you disconnect from a server
    fileline_regex_4 = re.compile(r"\[(\d{2}):(\d{2}):(\d{2})] \[main/INFO]: Setting user: (.+)") # Hour, Minute, Second, Username                              ## Used when the game first starts
    fileline_regex_5 = re.compile(r"\[(\d{2}):(\d{2}):(\d{2})] \[Client thread/INFO]: \[CHAT] (.+) joined the game") # Hour, Minute, Second, Username           ## Used to detect that you have joined a multiplayer session and that the usernames match

    session_open = False
    session_start_time = []
    username = ""

    for item in dir_list:
        matches = filename_regex.match(item)
        if matches != None:
            date_year = matches.group(1)
            date_month = matches.group(2)
            date_day = matches.group(3)

        file_item = open(item,"r")
        for line in file_item:

            #Find when Minecraft Opens
            result = log_reader.find_log_line(line,fileline_regex_4)
            if result != None:
                username = result.group(4)

            #Find when the user attempted connection
            result = log_reader.find_log_line(line,fileline_regex_1)
            if result != None:
                hour = result.group(1)
                minute = result.group(2)
                second = result.group(3)
                serveraddr = result.group(4)
                serverport = result.group(5)

                is_attempting_connection = True

            if is_attempting_connection:
                result = log_reader.find_log_line(line,fileline_regex_5)
                if result != None:
                    hour = result.group(1)
                    minute = result.group(2)
                    second = result.group(3)
                    conn_username = result.group(4)

                if conn_username ==  username:
                    is_attempting_connection = False
                    is_connected = True
                    session_start_time = [hour, minute, second]

if __name__ == '__main__':
    main()
elif __name__ != '__main__':
    print("This is meant to be run as a standalone script, please try again.")