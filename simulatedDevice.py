import random
import datetime
import time
import sys
import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue
# String containing Hostname, Device Id & Device Key in the format
CONNECTION_STRING = "HostName=HackMx.azure-devices.net;DeviceId=TecDevice;SharedAccessKey=kAzQMK+9yMnDcM96oG9DF9pZPYYvy4JhbNINSCj43Wk="
# choose HTTP, AMQP or MQTT as transport protocol
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 1000
SEND_CALLBACKS = 0

def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    print ( "Confirmation[%d] received for message with result = %s" % (user_context, result) )
    map_properties = message.properties()
    print ( "    message_id: %s" % message.message_id )
    print ( "    correlation_id: %s" % message.correlation_id )
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )
    SEND_CALLBACKS += 1
    print ( "    Total calls confirmed: %d" % SEND_CALLBACKS )

def iothub_client_init():
    # prepare iothub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    # set the time until a message times out
    client.set_option("messageTimeout", MESSAGE_TIMEOUT)
    client.set_option("logtrace", 0)
    client.set_option("product_info", "HappyPath_Simulated-Python")
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        message_counter = 0

        while True:
			random_id =  random.randint(1, 4)
			random_capacity = random.random()
			date = "\""+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"\""
			msg_txt_formatted = "{\"capacidad\":" + str(random_capacity) + ", \"fecha\": "+ date +", \"id_bote\":" + str(random_id) + "}"
			print(msg_txt_formatted)
			message = IoTHubMessage(msg_txt_formatted)
			# optional: assign ids
			message.message_id = "message_%d" % message_counter
			message.correlation_id = "correlation_%d" % message_counter
			# optional: assign properties
			prop_map = message.properties()
			prop_text = "PropMsg_%d" % message_counter
			prop_map.add("Property", prop_text)

			client.send_event_async(message, send_confirmation_callback, message_counter)
			print ( "IoTHubClient.send_event_async accepted message [%d] for transmission to IoT Hub." % message_counter )

			status = client.get_send_status()
			print ( "Send status: %s" % status )
			time.sleep(30)

			status = client.get_send_status()
			print ( "Send status: %s" % status )

			message_counter += 1

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "Simulating a device using the Azure IoT Hub Device SDK for Python" )
    print ( "    Protocol %s" % PROTOCOL )
    print ( "    Connection string=%s" % CONNECTION_STRING )

    iothub_client_telemetry_sample_run()