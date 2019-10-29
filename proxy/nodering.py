from uhashring import HashRing
import yaml

class NodeRing:

    def __init__(self):
        self._nodes = None
        self._load_cluster_nodes()

    def _load_cluster_nodes(self):
        cluster_nodes: list = []

        with open('clusterconfig.yaml', 'r') as file_handle:
            cluster_nodes = yaml.load(file_handle, Loader=yaml.FullLoader)
        
        self._nodes: list = cluster_nodes

    def get_node(self, bucket_name: str) -> str:

        hash_ring = HashRing(self._nodes)
        target_node = hash_ring.get(bucket_name)

        return target_node['hostname']


if __name__ == '__main__':

    nr = NodeRing()
    print(nr.get_node('truouiyuuibe'))
    print(nr.get_node('trvevergibe'))
    print(nr.get_node('triergegbe'))
    print(nr.get_node('tribyjykyke'))
    print(nr.get_node('tribmbbmbme'))
    print(nr.get_node('trizczzcvbe'))
