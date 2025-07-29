# data_store.py
class Data:
    def __init__(self):
        self.Data = []
    def read(self):
        return self.Data
    def write(self, new_data):
        self.Data = new_data

job_data = Data()
scenario_data = Data()
