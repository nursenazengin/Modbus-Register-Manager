from flask import Blueprint, jsonify
from postgreService.Db import Postgres
from deviceService.Device import Device
from dataclasses import dataclass,asdict


accessPointBlueprint = Blueprint('access_point', __name__)

@dataclass
class AccessPoint:
    fld_Id: int
    fld_FirmId: int
    fld_AccessPointName: str
    fld_Description: str
    fld_CommunicationType: int
    fld_CommunicationMethod: int
    fld_ProtocolId: int
    fld_AccessPointIp: int
    fld_AccessPointPort: int
    fld_ConfigurationPort: int
    fld_AccessPointSerialNr: int
    fld_AccessPointTimeout: int
    fld_AccessPointQueryRetryCnt: int
    devicesData: list

    @staticmethod
    def fetchAccessPoints():
        # Veritabanına bağlan
        connection = Postgres.connect()
        if connection is None:
            return None

        cursor = connection.cursor()
        cursor.execute('SELECT "fld_Id", "fld_FirmId", "fld_AccessPointName", "fld_Description", "fld_CommunicationType", "fld_CommunicationMethod", "fld_ProtocolId", "fld_AccessPointIp", "fld_AccessPointPort", "fld_ConfigurationPort", "fld_AccessPointSerialNr", "fld_AccessPointTimeout", "fld_AccessPointQueryRetryCnt" FROM "tbl_AccessPoint" WHERE "fld_Active" = true AND "fld_Deleted"= false AND "fld_FirmId" = 1 AND "fld_CommunicationType" = 0 AND "fld_CommunicationMethod" = 0 AND "fld_ProtocolId" = 0')
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data

    @accessPointBlueprint.route('/accessPoints', methods=['GET'])
    def getAccessPoints():
        accessPoints = []
        rows = AccessPoint.fetchAccessPoints()
        
        if rows:
            accessPoints = [
                AccessPoint(
                    fld_Id=row[0],
                    fld_FirmId=row[1],
                    fld_AccessPointName=row[2],
                    fld_Description=row[3],
                    fld_CommunicationType=row[4],
                    fld_CommunicationMethod=row[5],
                    fld_ProtocolId=row[6],
                    fld_AccessPointIp=row[7],
                    fld_AccessPointPort=row[8],
                    fld_ConfigurationPort=row[9],
                    fld_AccessPointSerialNr=row[10],
                    fld_AccessPointTimeout=row[11],
                    fld_AccessPointQueryRetryCnt=row[12],
                    devicesData= Device.getDevices(row[0]) 
                )
                for row in rows
            ]         
            return jsonify(accessPoints)
        

        else:
            return jsonify({"error": "Unable to fetch data"})
        
    @staticmethod
    def getAccessPointIp():
        rows = AccessPoint.fetchAccessPoints()
        ipAddresses = []
        ipAddresses.append('10.45.36.10')
        if rows:
            for row in rows:
                ipAddresses.append(row[7])
                

        return ipAddresses
            
        
    
    @staticmethod
    def getAccessPointPort():
        rows = AccessPoint.fetchAccessPoints()
        portNumbers = []
        portNumbers.append(502)
        if rows:
            for row in rows:
                portNumbers.append(row[8])
        return portNumbers
            
 
