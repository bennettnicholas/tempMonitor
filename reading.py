import time
import board
import adafruit_htu31d
import boto3
import datetime

i2c = board.I2C()  # uses board.SCL and board.SDA
htu = adafruit_htu31d.HTU31D(i2c)

# database setup
Table_Name='temp'
db = boto3.resource('dynamodb')
table = db.Table(Table_Name)
client = boto3.client('dynamodb')

#response = client.delete_table(TableName=Table_Name)
#response = client.create_table(TableName=Table_Name, AttributeDefinitions=[{'AttributeName':'index','AttributeType':'S'},],KeySchema=[{'AttributeName':'index','KeyType':'HASH'},], ProvisionedThroughput={
#        'ReadCapacityUnits': 123,
#        'WriteCapacityUnits': 123
#    })

while True:
    temperature, relative_humidity = htu.measurements 
    print("Temperature: %0.1f F" % ((temperature * 1.8) + 32))
    print("Humidity: %0.1f %%" % relative_humidity)
    print("")
    if datetime.datetime.now().strftime("%M") in ["00", "10", "20", "30", "40", "50" ]:
        table.put_item(
            Item={
                'index': datetime.datetime.now().strftime("%H:%M"),
                'timestamp': str(datetime.datetime.now().isoformat(timespec='seconds')),
                'Temperature':str(round(temperature*1.8+32,2)),
                'Humidity':str(relative_humidity)
            }
        )
    time.sleep(60)
