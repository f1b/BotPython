from datetime import datetime


def WriteLog(ex:Exception, data):
    path = "logs\\ALLlogs.txt"
    time = datetime.now()
    file = open(path,'a')
    if (ex != None):
        file.write("["+str(time.day)+'.'+str(time.month)+'.'+str(time.year)+'  '+
                str(time.hour)+':'+str(time.minute)+':'+str(time.second)+"] "+ str(ex.args) +" "+str(data)+"\n")
    else:
        file.write("["+str(time.day)+'.'+str(time.month)+'.'+str(time.year)+'  '+
                str(time.hour)+':'+str(time.minute)+':'+str(time.second)+"] "+" "+str(data)+"\n")
    file.close()
