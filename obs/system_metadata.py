from datetime import datetime

class SystemMetadata:
    
    def __init__(self, content_length, content_type, content_md5):
        self._content_length = content_length
        self._content_type = content_type
        # self._last_modified = self._get_last_modified_time()
        self._creation_date: str = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self._content_md5 = content_md5
        self._x_version_id = None
    
    @property
    def content_length(self):
        return self._content_length
    
    @property
    def content_type(self):
        return self._content_type
    
    # @property
    # def last_modified(self):
    #     return self._last_modified
    
    @property
    def creation_date(self):
        return self._creation_date
    
    @property
    def content_md5(self):
        return self._content_md5

    @property
    def x_version_id(self):
        return self._x_version_id
    
    def get(self) -> dict:
        return {'content_length':self._content_length,
                'content_type':self._content_type,
                'creation_date':self._creation_date,
                'content_md5':self._content_md5, }
        

    # def _get_last_modified_time(self):
    #     pass

if __name__ == '__main__':

    sm = SystemMetadata(45, 'bla bla', 'efeufbiufuiu3fff348r394yy9')
    print(sm.get())