import os
import json
import pyodbc
from typing import Union
from pydantic import BaseModel
import datetime

print(f"pyodbc.drivers() {pyodbc.drivers()}") 

class AirSample(BaseModel):

    device_id: str
    sample: int
    sample_time: datetime.datetime

class DbService:



    def __init__(self):
            # self.sgp40JSON = json.dumps(self.sgp40)
        self.connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]
        self.TABLE_AIRGP40 = "AIRSGP40"
        self.DB_NAME="cpdashboard"
        return

    def root(self):
        print(f"Root of {self.TABLE_AIRGP40} API")
        try:
            conn = self.get_conn()
            cursor = conn.cursor()

            # Table should be created ahead of time in production app.
            cursor.execute(f"""
                IF  NOT EXISTS (SELECT * FROM sys.objects 
                            WHERE    object_id = OBJECT_ID(N'{self.TABLE_AIRGP40}') AND type in (N'U'))
                BEGIN
                    CREATE TABLE {self.TABLE_AIRGP40} (
                        ID int NOT NULL PRIMARY KEY IDENTITY,
                        device_id VARCHAR(25) NOT NULL,
                        sample int,
                        sample_time DATETIME
                    );
                END
            """)
            conn.commit()
            # # Same device can only make one sample at a particular timestamp
            cursor.execute(f"""
                        IF IndexProperty(Object_Id(N'{self.TABLE_AIRGP40}'), 'dev_sample_idx', 'IndexID') Is Null
                        BEGIN 
                            CREATE UNIQUE INDEX dev_sample_idx ON {self.TABLE_AIRGP40} (device_id DESC, sample_time DESC); 
                        END
                        """)
            conn.commit()
        except Exception as e:
            # Table may already exist
            print(e)
        return f"{self.TABLE_AIRGP40} API"

    def get_air_samples(self, device_id: str):
        rows = []
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM airsgp40 WHERE device_id=N'{device_id}'")
            rows = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
            
            # for row in cursor.fetchall():
            #     print(row.ID, row.device_id, row.sample, row.sample_time)

        return rows

    def get_air_sample(self, device_id: str, sample_time: datetime):
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.TABLE_AIRGP40} WHERE device_id = ? AND sample_time = ?", device_id, sample_time)

            row = cursor.fetchone()
            return f"{row.ID}, {row.device_id}, {row.sample}, {row.sample_time}"

    def create_air_sample(self, item: AirSample):
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {self.TABLE_AIRGP40} (device_id, sample, sample_time) VALUES (?, ?, ?)", item.device_id, item.sample, item.sample_time)
            conn.commit()
        ret = item.model_dump()
        return ret

    def get_conn(self):
        conn = pyodbc.connect(self.connection_string)
        return conn