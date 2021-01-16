import serial
from time import sleep

cnt=0
def readout():
    global cnt
    if(ser.in_waiting > 0):
        while(ser.in_waiting > 0):
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            sleep(1/120)
    else:
        ser.write(b'M119\n')
        cnt+=1
        print('M119 sent the '+str(cnt)+'th time')
        sleep(0.01)

print('Connecting to Arduino...')
ser = serial.Serial('/dev/ttyACM0', 250000, timeout=0.01)
sleep(2)
print('Arduino connected and ready!')
# ser.flushInput()
# ser.flushOutput()

while True:
    readout()
#     line = ser.readline().decode('utf-8').rstrip()
#     if len(line)>0:
#         print(line)
#     else: #ser.inWaiting()==False:
#         ser.write(b'M119\n')
#         cnt+=1
#         print('M119 sent the '+str(cnt)+'th time')
#         sleep(0.01)