import os
from obs.persist.serializer import BucketSerializer
from obs.persist.serializer import ObjectSerializer
from obs.sairo_bucket import SairoBucket
from obs.sairo_objects import SairoObject

OBS_BUCKET_DIR = '/home/dominouzu/sairo'

class PersistBucketHandler:

    def __init__(self, bucket_object: SairoBucket):

        self._bhobj = bucket_object
    
    def persist(self) -> bool:

        bs = BucketSerializer()

        try:

            if bs.serialize(self._bhobj):
                return True
            else:
                return False
        
        except FileNotFoundError:
            raise FileNotFoundError
    
    def read(self, serial_bucket_path: str) -> SairoBucket:

        bs = BucketSerializer()
        return bs.deserialize(serial_bucket_path)


class PersistObjectHandler:

    def __init__(self, sairo_object: SairoObject):
        self._ohobj = sairo_object
    
    def persist(self) -> bool:

        self._ohobj.version_id = self.determine_version()
        object_path = os.path.join(OBS_BUCKET_DIR, self._ohobj.bucket, self._ohobj.object_key)
        self._ohobj.self_link = os.path.join(object_path, 
                                self._ohobj.object_key+str(self._ohobj.version_id)+'.pk')        

        objs = ObjectSerializer()
        if objs.serialize(self._ohobj):
            return True
        else:
            return False
    
    def read(self, serial_object_path: str) -> SairoObject:
        
        bs = ObjectSerializer()
        return bs.deserialize(serial_object_path)
    
    def determine_version(self) -> int:
        
        object_path = os.path.join(OBS_BUCKET_DIR, self._ohobj.bucket, self._ohobj.object_key)
        file_list = os.listdir(object_path)

        if len(file_list) > 0:
            current_version = 0
            for fl in file_list:
                if fl.endswith('.pk'):
                    current_version = current_version + 1
            
            return current_version+1

        else:
            return 1


