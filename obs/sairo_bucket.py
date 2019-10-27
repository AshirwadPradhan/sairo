from datetime import datetime
class SairoBucket:
    
    def __init__(self, name):
        
        self._name = name
        self._KIND = "storage#bucket"
        self._time_created = datetime.now
        self._time_updated = datetime.now
        self._object_list = []
        
    @property
    def name(self):
        
        return self._name

    @property
    def kind(self):

        return self._KIND
    
    @property
    def time_created(self):

        return self._time_created
    
    @property
    def time_updated(self):

        return self._time_updated
    
    @time_updated.setter
    def time_updated(self, time: datetime):

        self._time_updated = time
    
    @property
    def object_list(self):

        return self._object_list
    
    @object_list.setter
    def object_list(self, new_obj: str):
        self._object_list.append(new_obj)
    
    def delete(self):
        """Deletes the bucket"""
        pass

    def get(self):
        """Gets metadata about the bucket"""
        pass
