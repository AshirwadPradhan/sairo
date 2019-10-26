from datetime import datetime

class SystemMetadata:
    
    def __init__(self, content_length, content_type):
        self._content_length = content_length
        self._content_type = content_type
        self._last_modified = self._get_last_modified_time()
        self._creation_date = datetime.now
        self._content_md5 = None
        self._x_version_id = None
    
    @property
    def content_length(self):
        return self._content_length
    
    @property
    def content_type(self):
        return self._content_type
    
    @property
    def last_modified(self):
        return self._last_modified
    
    @property
    def creation_date(self):
        return self._creation_date
    
    @property
    def content_md5(self):
        return self._content_md5
    
    @property
    def x_version_id(self):
        return self._x_version_id

    def _get_last_modified_time(self):

        pass