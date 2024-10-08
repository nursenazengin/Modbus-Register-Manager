from postgreService.Db import Postgres
from dataclasses import dataclass,asdict


@dataclass
class ModbusTable:    
                                      
    fld_Id: int 
    fld_DataDescription: str
    fld_LabelId: int
    fld_LabelUnit: str
    fld_ModbusAddress: int
    fld_DataTypeId: int
    fld_DataEndian: str
    fld_LabelName: str
    fld_LabelDataTypeId: int
    modbusRegisters = []

    @staticmethod
    def fetchModelModbusTable(ModbusGroupId):
        connection = Postgres.connect()
        cursor = connection.cursor()
        cursor.execute('''SELECT dmt."fld_Id", dmt."fld_DataDescription", dmt."fld_LabelId", dmt."fld_LabelUnit", 
                       dmt."fld_ModbusAddress", dmt."fld_DataTypeId", dmt."fld_DataEndian", l."fld_LabelName", l."fld_LabelDataTypeId"  FROM "tbl_DeviceModelModbusTable" dmt JOIN "tbl_Label" l ON dmt."fld_LabelId" = l."fld_Id" 
                       WHERE "fld_DeviceModelModbusGroupId" = %s
                        ''', (ModbusGroupId,))
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data
    

    @staticmethod
    def getModelModbusTable(ModbusGroupId):
        rows = ModbusTable.fetchModelModbusTable(ModbusGroupId)

        for row in rows:
            modbusTable = ModbusTable(
                fld_Id= row[0],
                fld_DataDescription= row[1],
                fld_LabelId= row[2],
                fld_LabelUnit= row[3],
                fld_ModbusAddress= row[4],
                fld_DataTypeId= row[5],
                fld_DataEndian= row[6],
                fld_LabelName=row[7],
                fld_LabelDataTypeId=row[8], 
            )

            
            ModbusTable.modbusRegisters.append(asdict(modbusTable))

        return (ModbusTable.modbusRegisters)
    

    @staticmethod
    def getLabelName(ModbusGroupId):
        rows = ModbusTable.fetchModelModbusTable(ModbusGroupId)
        labelNames = []
        if rows:
            for row in rows:
                labelNames.append(row[7])
        return labelNames
    

        
