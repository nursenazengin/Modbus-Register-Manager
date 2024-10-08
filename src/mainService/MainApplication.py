from accessPointService.AccessPoint import AccessPoint
from modbusGroupService.ModbusGroup import ModbusGroup
from modbusGroupService.ModbusTable import ModbusTable
from deviceService.Device import Device
from pymodbus.client import ModbusTcpClient
from flask import Blueprint, jsonify 
from dataclasses import dataclass
import time
import json, redis
import struct
from redisService.ConnectionRedis import ConnectionRedis
from collections import defaultdict


mainBlueprint = Blueprint('main', __name__)
            

@dataclass
class Main:
    @mainBlueprint.route('/main/<AccessPointId>/<DeviceModelId>/<ModbusGroupId>', methods=['GET'])

    def readModbus(AccessPointId, DeviceModelId, ModbusGroupId):
        ModbusGroup.fetchModelModbusGroup(DeviceModelId)
        rows = AccessPoint.fetchAccessPoints()
        
        all_device_data = defaultdict(list)
        delay = 30
        start_time = time.time()

        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            if elapsed_time > delay:
                print("30 saniye süre doldu.")
                break
            
            for row in rows:
                ipAddresses = AccessPoint.getAccessPointIp()
                portNumbers = AccessPoint.getAccessPointPort()
                deviceIds = Device.getId(AccessPointId)  

                if not ipAddresses or not portNumbers or not deviceIds:
                    print("error: IP addresses, port numbers or device IDs are missing.")
                    continue  
                    
                i = 0  
                if i < len(ipAddresses):
                    try:
                        ipAddress = ipAddresses[i]
                        portNumber = portNumbers[i]
                        client = ModbusTcpClient(ipAddress, portNumber)
                        connection = client.connect()
                        if connection:
                            print({f"TCP connection is successful with IP address: {ipAddress} and port: {portNumber}"})
                            startAddress = ModbusGroup.getStartAddress(DeviceModelId)
                            count = ModbusGroup.getQuantity(DeviceModelId)
                            if startAddress is None or count is None:
                                print("Invalid start address.")
                                continue
                                                
                            startAddress = int(startAddress)
                            count = int(count)
                            for deviceId in deviceIds:
                                try:
                                    registers = client.read_holding_registers(startAddress, count, slave=1)
                                    if registers.isError():
                                        print({"error": f"Failed to read data from Modbus sensors: {registers.message}"})
                                        continue
                                    else:
                                        readData = registers.registers
                                        labelNames = ModbusTable.getLabelName(ModbusGroupId)
                                                            
                                        for index, value in enumerate(readData):
                                            packed_value = struct.pack('>H', value)
                                            floatData = struct.unpack('>f', packed_value + b'\x00\x00')[0]
                                                                
                                            if index >= len(labelNames):
                                                break  
                                                                
                                            device_data = {
                                                            'DataDescription': labelNames[index],
                                                            'DeviceId': deviceId,
                                                            'Value': floatData
                                                                }
                                                                
                                            all_device_data[deviceId].append(device_data)
                                except Exception as e:
                                    print(f"Data read error: {e}")
                                finally:
                                    client.close()
                        else:
                            print({f"TCP connection is unsuccessful with IP address: {ipAddress} and port: {portNumber}"})  
                        i = i + 1

                    except Exception as e:
                        print(f"Connection is unsuccessfull to {ipAddress}, {portNumber}")                       
                
                # Redis 
                if all_device_data: 
                    try:
                        ConnectionRedis.connectRedis()
                        redisKey = f"device_data_{AccessPointId}"
                        json_data = json.dumps({key: value for key, value in all_device_data.items()})
                        ConnectionRedis.setRedis(redisKey, json_data)
                        print(f"Key: {redisKey}, Value: {json_data}")
                    except redis.RedisError as e:
                        print(f"Data can't be written to Redis: {e}")
                else:
                    print("Data yok")

                time.sleep(1)

        return jsonify({key: value for key, value in all_device_data.items()})

