# Copyright (c) 2021 Steven
import procwatch

app = 'python'
procClient=procwatch.procwatch(app)

memoryInMb = procClient.getMemoryMb() # return int

memoryInKb = procClient.getMemoryKb() # return int

runningTime = procClient.getRunningTime() # return str

# return dict of all processes with app name
runningProcs = procClient.getRunningProcs()

# return dict of all running application in the format {'app': ['proccess': rss]}
allRunningApps = procClient.runningApps

print(allRunningApps[procClient.appName])
