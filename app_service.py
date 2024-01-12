import json


class AppService:
    
    sgp40 = [
        {
            "created_at": "2024-01-05T23:35:01",
            "value":30
        },
        {
            "created_at": "2024-01-06T23:35:01",
            "value":40
        },
        {
            "created_at": "2024-01-07T23:35:01",
            "value":50
        }
    ]

    def __init__(self):
        self.sgp40JSON = json.dumps(self.sgp40)

    def get_sgp40s(self):
        return self.sgp40JSON

    def create_sgp40(self,sgp40):
        sgp40Data = json.loads(self.sgp40JSON)
        sgp40Data.append(sgp40)
        self.sgp40JSON = json.dumps(sgp40Data)
        return self.sgp40JSON

    def update_sgp40(self, request_sgp40):
        sgp40Data = json.loads(self.sgp40JSON)
        for sgp40 in sgp40Data:
            if sgp40["created_at"] == request_sgp40['created_at']:
                sgp40.update(request_sgp40)
                return json.dumps(sgp40Data);
        return json.dumps({'message': 'sgp40 created_at not found'});

    def delete_sgp40(self, request_sgp40_created_at):
        sgp40Data = json.loads(self.sgp40JSON)
        for sgp40 in sgp40Data:
            if sgp40["created_at"] == request_sgp40_created_at:
                sgp40Data.remove(sgp40)
                return json.dumps(sgp40Data);
        return json.dumps({'message': 'sgp40 created_at not found'});

    
