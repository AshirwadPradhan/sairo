import os
from persist.serializer import BucketSerializer
from persist.serializer import ObjectSerializer
from sairo_bucket import SairoBucket
from sairo_objects import SairoObject

OBS_BUCKET_DIR = '~/.sairo'

class PersistBucketHandler:

    def __init__(self):

        self._bhobj = None
    
    def persist(self, sairo_bucket: SairoBucket) -> bool:

        bs = BucketSerializer()
        self._bhobj = sairo_bucket

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

    def __init__(self):
        self._ohobj = None
    
    def persist(self, sairo_object: SairoObject) -> bool:

        self._ohobj: SairoObject = sairo_object

        self._ohobj.version_id = self.determine_version()
        object_path = os.path.join(OBS_BUCKET_DIR, self._ohobj.bucket, self._ohobj.object_key)
        self._ohobj.self_link = os.path.join(object_path, 
                                self._ohobj.object_key+str(self._ohobj.version_id)+'.pk')        

        objs = ObjectSerializer()
        bucks = BucketSerializer()

        if objs.serialize(self._ohobj):

            bucket_path = os.path.join(OBS_BUCKET_DIR, sairo_object.bucket)
            buck_ser_path = os.path.join(bucket_path, sairo_object.bucket+'.pk')
            print(f'Reading bucket {buck_ser_path}....')
            bucket_obj: SairoBucket = bucks.deserialize(buck_ser_path)
            bucket_obj.object_list = self._ohobj.object_key

            if bucks.serialize(bucket_obj):
                print(f'Bucket {bucket_obj.name} updated with {self._ohobj.object_key}')
            else:
                print(f'ERROR:Bucket {bucket_obj.name} CANNOT be updated with {self._ohobj.object_key}')

            return True
        else:
            return False
    
    def read(self, serial_object_path: str, object_name: str) -> SairoObject:
        
        bs = ObjectSerializer()
        list_files = os.listdir(serial_object_path)
        tmp_path = serial_object_path+'/'+object_name+str(len(list_files))+'.pk'
        print(tmp_path)
        return bs.deserialize(tmp_path)
    
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


