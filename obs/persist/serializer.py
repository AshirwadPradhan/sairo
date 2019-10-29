import pickle
import os
from sairo_bucket import SairoBucket
from sairo_objects import SairoObject

OBS_BUCKET_DIR = '/home/dominouzu/sairo'

class ObjectSerializer:

    def __init__(self):
        pass


    def serialize(self, sairo_object: SairoObject) -> bool:

        if isinstance(sairo_object, SairoObject):

            bucket_name = sairo_object.bucket
            object_name = sairo_object.object_key
            serial_file = sairo_object.self_link

            try:

                with open(serial_file, 'wb') as file_handler:
                    print(f'Serializing {object_name} to {serial_file}...')
                    pickle.dump(sairo_object, file_handler)
                
                return True

            except pickle.PicklingError:
                print(f'Cannot pickle {object_name} object')

                return False
            
            except FileNotFoundError:
                print(f'The bucket {bucket_name} or object {object_name} is missing')

                return False
        
        else:

            raise TypeError('Cannot serialize objects that are not SairoObject')
            return False
    

    def deserialize(self, sairo_object: str) -> SairoObject or None:
        '''
        @params 
        sairo_object -> complete path to the object pickle file.
        '''

        try:
            with open(sairo_object, 'rb') as file_handler:
                sairo_object = pickle.load(file_handler)

            return sairo_object

        except pickle.UnpicklingError:
            print(f'Cannot unpickle the {sairo_object}')

            return None
        
        except FileNotFoundError:
            print(f'Pickled file {sairo_object} not found')

            return None


class BucketSerializer:

    def __init__(self):
        pass
        
        
    def serialize(self, sairo_bucket: SairoBucket) -> bool:

        if isinstance(sairo_bucket, SairoBucket):

            serial_bucket_dir = OBS_BUCKET_DIR+'/'+sairo_bucket.name
            serial_bucket_file = serial_bucket_dir+'/'+sairo_bucket.name+'.pk'
            
            if os.path.exists(serial_bucket_dir):
                try:

                    with open(serial_bucket_file, 'wb') as file_handler:
                        pickle.dump(sairo_bucket, file_handler)
                
                        return True

                except pickle.PicklingError:
                    print(f'Cannot pickle {sairo_bucket.name} bucket')

                    return False

            else:
                raise FileNotFoundError
        
        else:
            print('Cannot serialize object which are not SairoBucket')

            return False
    
    def deserialize(self, sairo_bucket: str) -> SairoBucket or None:
        '''
        @params sairo_bucket : complete path to bucket pickle file
        '''

        try:
            with open(sairo_bucket, 'rb') as file_handler:
                sairo_object = pickle.load(file_handler)

            return sairo_object

        except pickle.UnpicklingError:
            print(f'Cannot unpickle the {sairo_bucket}')

            return None
        
        except FileNotFoundError:
            print(f'Pickled file {sairo_bucket} not found')

            return None

