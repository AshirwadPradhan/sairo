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

    def get_nodes(self, bucket_name: str) -> str:

        hash_ring = HashRing(self._nodes)
        member_nodes = []

        for _ in range(0,3):
            target_node = hash_ring.get(bucket_name)['hostname']
            member_nodes.append(target_node)
            hash_ring.remove_node(target_node)

        return member_nodes


if __name__ == '__main__':

    nr = NodeRing()
    print(nr.get_nodes('truouiyuuibe'))
    print(nr.get_nodes('trvevergibe'))
    print(nr.get_nodes('triergegbe'))
    print(nr.get_nodes('tribyjykyke'))
    print(nr.get_nodes('tribmbbmbme'))
    print(nr.get_nodes('trizczzcvbe'))
