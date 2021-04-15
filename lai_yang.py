print("The Execution of Lai-Yang Algorithm for 2 Processes and 3 Time Nodes Only")
no_processes = 2
processes = []

for i in range(0, no_processes):
    amount = int(input("Enter the initial value for P{}: ".format(i+1)))
    processes.append(amount)

p1 = processes[0]
p2 = processes[1]

def calculate_arr_sum(arr):
    sum = 0
    for i in arr:
        sum = sum + i
    return sum

initial_sys_value = calculate_arr_sum(processes)
print("Initial Global State = {}".format(initial_sys_value))

no_timestamps = int(input("Enter total number of timestamps: "))
no_messages = int(input("Enter total number of messages: "))

def processMessage(ts, msg, p1, p2):
    if msg['fromProcess']==1:
        if(ts==msg['startTime']):
            p1 = p1 - msg['value']
        elif(ts==msg['endTime']):
            p2 = p2 + msg['value']
    elif msg['fromProcess']==2:
        if(ts==msg['startTime']):
            p2 = p2 - msg['value']
        elif(ts==msg['endTime']):
            p1 = p1 + msg['value']
    return p1,p2
    

def setTimestamps():
    global p1,p2
    print("==========================")
    print("|  Timestamp" + "   P1   " + "   P2 |")
    timestamps = []
    for i in range(0, no_timestamps):
        for j in range(0, no_messages):
            if(messages[j]['startTime'] > i and messages[j]['endTime'] > i):
                break
            else:
                p1, p2 = processMessage(i, messages[j], p1, p2)
        timestamp = {}
        timestamp['index'] = i
        timestamp['p1_value'] = p1
        timestamp['p2_value'] = p2
        if len(timestamps) == 0:
            timestamps = [timestamp]
        else:
            timestamps.append(timestamp)
                
        print("==========================")
        print("|   T" + str(i+1) + "  |  " + str(p1) + "  |  " + str(p2) + "  |")
    return timestamps


def recordLocalSnapshot(red_message, ts_arr):
    startTime = red_message['startTime']
    endTime = red_message['endTime']
    if ((startTime > -1) and (endTime > 1) and (startTime < len(ts_arr)) and (endTime < len(ts_arr))):
        print("Local State P1: {}".format(ts_arr[startTime]['p1_value']))
        print("Local State P2: {}".format(ts_arr[endTime - 1]['p2_value']))
        return ts_arr[startTime]['p1_value'] + ts_arr[endTime]['p2_value']
    return 0


def sentP1_P2(red_msg, msg_arr):
    redStartTime = red_msg['startTime']
    sum = 0
    for i in range(0, len(msg_arr)):
        if(msg_arr[i]['fromProcess'] == 1 and msg_arr[i]['startTime'] <= redStartTime):
            sum = sum + msg_arr[i]['value']
    print("Total messages sent from P1 to P2 = {}".format(sum))
    return sum


def recvP1_P2(red_msg, msg_arr):
    redEndTime = red_msg['endTime']
    sum = 0
    for i in range(0, len(msg_arr)):
        if(msg_arr[i]['fromProcess'] == 1 and msg_arr[i]['endTime'] <= redEndTime):
            sum = sum + msg_arr[i]['value']
    print("Total messages received from P1 to P2 = {}".format(sum))
    return sum


def sentP2_P1(red_msg, msg_arr):
    redEndTime = red_msg['endTime']
    sum = 0
    for i in range(0, len(msg_arr)):
        if(msg_arr[i]['fromProcess'] == 2 and msg_arr[i]['startTime'] <= redEndTime):
            sum = sum + msg_arr[i]['value']
    print("Total messages sent from P2 to P1 = {}".format(sum))
    return sum


def recvP2_P1(red_msg, msg_arr):
    redStartTime = red_msg['startTime']
    sum = 0
    for i in range(0, len(msg_arr)):
        if(msg_arr[i]['fromProcess'] == 2 and msg_arr[i]['endTime'] <= redStartTime):
            sum = sum + msg_arr[i]['value']
    print("Total messages received from P1 to P2 = {}".format(sum))
    return sum


def recordChannelStates(red_msg, msg_arr):
    ch12 = sentP1_P2(red_msg, msg_arr) - recvP1_P2(red_msg, msg_arr)
    ch21 = sentP2_P1(red_msg, msg_arr) - recvP2_P1(red_msg, msg_arr)
    return ch12 + ch21


def verifyConsistentStates(red_msg, ts_arr, msg_arr):
    global p1,p2
    totalInitialValue = p1 + p2
    print(totalInitialValue)
    localSnapshot = recordLocalSnapshot(red_msg, ts_arr)
    channelState = recordChannelStates(red_msg, msg_arr)
    totalSnapshotValue = localSnapshot + channelState

    if(totalInitialValue == totalSnapshotValue):
        print("Total Initial Value {} == Total Snapshot Value {}".format(totalInitialValue, totalSnapshotValue))
        print("Initial system value is EQUAL to snapshot value hence it is a consistant global state.")
    else:
        print("Total Initial Value {} != Total Snapshot Value {}".format(totalInitialValue, totalSnapshotValue))
        print("Initial system value is NOT EQUAL to snapshot value hence it is a consistant global state.")


for i in range(0, int(no_messages)):
    data = {}
    data['message'] = i+1
    print("Enter values for message{}: ".format(i+1))
    amount = int(input("Enter amount: "))
    data['value'] = amount
    fromProcess = int(input("From Process[1 or 2]: "))
    data['fromProcess'] = fromProcess
    toProcess = int(input("To Process[1 or 2]: "))
    data['toProcess'] = toProcess
    startTime = int(input("Start Timestamp[1-{}]: ".format(no_timestamps)))
    data['startTime'] = startTime
    endTime = int(input("End Timestamp[1-{}]: ".format(no_timestamps)))
    data['endTime'] = endTime
    if i==0:
        messages = [data]
    else:
        messages.append(data)

ts_arr = setTimestamps()
red_index = int(input("Enter RED message index[1-{}]: ".format(no_messages)))
red_message = messages[red_index-1]
verifyConsistentStates(red_message, ts_arr, messages)
print("===============THE END=================")
k=input("press close to exit")
if k=='close':
    exit()