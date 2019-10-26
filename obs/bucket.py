from datetime import datetime
class Bucket:
    
    def __init__(self, name):
        
        self._name = name
        self._KIND = "storage#bucket"
        self._time_created = datetime.now
        self._time_updated = None
        self._object_list = None
        
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
    
    @property
    def object_list(self):

        return self._object_list
    
    def delete(self):
        """Deletes the bucket"""
        pass

    def get(self):
        """Gets metadata about the bucket"""
        pass
