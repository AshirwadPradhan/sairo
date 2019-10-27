from obs.persist.serializer import BucketSerializer
from obs.sairo_bucket import SairoBucket
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

    def __init__(self, sairo_object):
        pass
