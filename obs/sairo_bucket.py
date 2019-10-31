from datetime import datetime
class SairoBucket:
    
    def __init__(self, name):
        
        self._name = name
        self._KIND = "storage#bucket"
        self._time_created = datetime.now
        self._time_updated = datetime.now
        self._object_list = {}
        
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

        if new_obj not in self._object_list:
            self._object_list[new_obj] = new_obj
            print(f'Adding {new_obj} to the {self._name} buckets object list')
    
    def del_object_list(self, obj: str):

        if obj in self._object_list:
            self._object_list.pop(obj)
            print(f'Deleting {obj} from the {self._name} buckets object list')

    
    def delete(self):
        """Deletes the bucket"""
        pass

    def get(self):
        """Gets metadata about the bucket"""
        pass
