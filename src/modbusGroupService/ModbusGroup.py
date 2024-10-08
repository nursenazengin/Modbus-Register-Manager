from postgreService.Db import Postgres
from modbusGroupService.ModbusTable import ModbusTable
from dataclasses import dataclass, asdict
from flask import jsonify




@dataclass
class ModbusGroup:  
    fld_DataEditable: int
    fld_ReadModbusFunction: int
    fld_StartAddress: int
    fld_Quantity: int                             
    modbusRegister: list

    @staticmethod
    def fetchModelModbusGroup(DeviceModelId):
        connection = Postgres.connect()
        cursor = connection.cursor()
        
        cursor.execute('''SELECT dmg."fld_DataEditable", 
                   dmg."fld_ReadModbusFunction", 
                   MIN(dmt."fld_ModbusAddress") AS "fld_StartAddress",
                   MAX(dmt."fld_ModbusAddress") + 2 AS "fld_Quantiy"
            FROM public."tbl_DeviceModelModbusGroup" dmg
            INNER JOIN "tbl_DeviceModelModbusTable" dmt 
                    ON dmg."fld_Id" = dmt."fld_DeviceModelModbusGroupId"
            WHERE dmg."fld_DeviceModelId" = %s 
            GROUP BY dmg."fld_DataEditable", dmg."fld_ReadModbusFunction" 
                       
                       ''',(DeviceModelId,))
        result = cursor.fetchall()
        
        cursor.close()
        connection.close()
        return result

    
    @staticmethod
    def getModelModbusGroup(DeviceModelId):
        try:
            rows = ModbusGroup.fetchModelModbusGroup(DeviceModelId)
            modbusGroups = []
            

            for row in rows:
                modbusGroup = ModbusGroup(
                    fld_DataEditable=row[0],
                    fld_ReadModbusFunction=row[1],
                    fld_StartAddress=row[2],
                    fld_Quantity= row[3],  
                    modbusRegister=ModbusTable.getModelModbusTable(row[1])  
                
                )
                
                modbusGroups.append(asdict(modbusGroup))
                
            return (modbusGroups)
        

        except Exception as e:
            return jsonify({"error": str(e)})
        
    def getStartAddress(DeviceModelId):
        rows = ModbusGroup.fetchModelModbusGroup(DeviceModelId)
        for row in rows:
            return row[2]
        
        

    def getQuantity(DeviceModelId):
        rows = ModbusGroup.fetchModelModbusGroup(DeviceModelId)
        for row in rows:
            return row[3]

    def getModbusRegister(DeviceModelId):    
        register = ModbusTable.getModelModbusGroup(DeviceModelId)
        for reg in register:
            reg["ValueString"] = 5

        return jsonify(reg["ValueString"])    
    
