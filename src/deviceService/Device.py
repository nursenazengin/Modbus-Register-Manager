from dataclasses import dataclass, asdict
from postgreService.Db import Postgres
from modbusGroupService.ModbusGroup import ModbusGroup



@dataclass
class Device:
    fld_Id: int
    fld_FirmId: int
    fld_DeviceName: str
    fld_Description: str
    fld_DeviceSerialNr: str
    fld_DeviceModelTypeId: int
    fld_AccessPointId: int
    fld_DeviceOrganizationId: int
    fld_DeviceModelId: int
    fld_DeviceCategoryId: int
    fld_DeviceSlaveId: int
    fld_DeviceTimezoneId: int
    fld_Latitude: float
    fld_Longitude: float
    modbusGroups: list 

    @staticmethod
    def fetchDevices(AccessPointId):
        connection = Postgres.connect()
            
        cursor = connection.cursor()
        cursor.execute('''SELECT "fld_Id", "fld_FirmId", "fld_DeviceName", "fld_Description", 
                        "fld_DeviceSerialNr", "fld_DeviceModelTypeId", "fld_AccessPointId", 
                        "fld_DeviceOrganizationId", "fld_DeviceModelId", "fld_DeviceCategoryId", 
                        "fld_DeviceSlaveId", "fld_DeviceTimezoneId", "fld_Latitude", "fld_Longitude", 
                        "fld_DeviceDaylight", "fld_LocationName" FROM "tbl_Device" WHERE "fld_AccessPointId" = %s 
                        AND "fld_Active" = true AND "fld_Deleted"= false''', (AccessPointId,))
            
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data
        
    @staticmethod
    
    def getDevices(AccessPointId):
        devices = []
        try:
            rows = Device.fetchDevices(AccessPointId)
            
            
            for row in rows:

                device = Device(
                    fld_Id=row[0],
                    fld_FirmId=row[1],
                    fld_DeviceName=row[2],
                    fld_Description=row[3],
                    fld_DeviceSerialNr=row[4],
                    fld_DeviceModelTypeId=row[5],
                    fld_AccessPointId=row[6],
                    fld_DeviceOrganizationId=row[7],
                    fld_DeviceModelId=row[8],
                    fld_DeviceCategoryId=row[9],
                    fld_DeviceSlaveId=row[10],
                    fld_DeviceTimezoneId=row[11],
                    fld_Latitude=row[12],
                    fld_Longitude=row[13],
                    modbusGroups=ModbusGroup.getModelModbusGroup(row[8])
                )
            
                
                devices.append(asdict(device))  

            return (devices)
        
        except Exception as e:
            print(type(e))
            return ({"error": str(e)})
        
    

    @staticmethod
    def getId(AccessPointId):
        rows = Device.fetchDevices(AccessPointId)
        ids = []
        if rows:
            for row in rows:
                ids.append(row[0])
        return ids
    
