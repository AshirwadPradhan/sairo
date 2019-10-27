from datetime import datetime
class SairoObject:

    def __init__(self, object_key, bucket, file_bin, metadata, md5_hash):

        self._object_key = object_key
        self._KIND = 'storage#object'
        self._bucket = bucket
        self._version_id = 0
        self._file_bin = file_bin
        self._metadata = metadata
        self._object_id = None
        self._time_created = datetime.now
        self._md5_hash = md5_hash
        self._self_link = None
    
    @property
    def object_key(self):

        return self._object_key
    
    @property
    def kind(self):

        return self._KIND

    @property
    def version_id(self):

        return self._version_id
    
    @version_id.setter
    def version_id(self, version_id: int):

        self._version_id = version_id
    
    @property
    def file_bin(self):

        return self._file_bin
    
    @property
    def metadata(self):

        return self._metadata
    
    @property
    def bucket(self):

        return self._bucket
    
    @property
    def object_id(self):

        return self._object_id

    @property
    def time_created(self):
        
        return self._time_created
    
    @property
    def md5_hash(self):

        return self._md5_hash
    
    @bucket.setter
    def bucket(self, bucket):

        self._bucket = bucket

    @property
    def self_link(self):
        return self._self_link
    
    @self_link.setter
    def self_link(self, object_link: str):
        self._self_link = object_link
    
    def delete(self):
        """Deletes the object and it's metadata"""
        pass

    def get(self):
        """"Retrieves the object"""
        pass
