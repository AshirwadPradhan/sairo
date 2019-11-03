import yaml
from uhashring import HashRing
from check_health import CheckHealth

class ClusterNodes:

    @staticmethod
    def get_cluster_nodes() -> list:
        cluster_nodes: list = []

        with open('clusterconfig.yaml', 'r') as file_handle:
            cluster_nodes = yaml.load(file_handle, Loader=yaml.FullLoader)
        
        return cluster_nodes

class NodeRing:

    def __init__(self):
        self._nodes = None
        self._load_cluster_nodes()

    def _load_cluster_nodes(self):

        cluster_nodes: list = ClusterNodes.get_cluster_nodes()
        self._nodes: list = cluster_nodes

    def get_nodes(self, bucket_name: str) -> dict:

        hash_ring = HashRing(self._nodes)
        _cp_hr = hash_ring
        replica_nodes = {'member_nodes':[],
                        'backup_nodes':[]}
        target_node = str()

        for _ in range(0,3):

            if CheckHealth.check(_cp_hr.get(bucket_name)['hostname']):
                target_node = _cp_hr.get(bucket_name)['hostname']
                replica_nodes['member_nodes'].append(target_node)
                _cp_hr.remove_node(target_node)
            else:
                _cp_hr.remove_node(target_node)
        
        for _ in range(0,2):
            #works only for 5 node cluster
            #assumption is that the 1st node of the member nodes is always reachable.
            if CheckHealth.check(_cp_hr.get(bucket_name)['hostname']):
                target_node = _cp_hr.get(bucket_name)['hostname']
                replica_nodes['backup_nodes'].append(target_node)
                _cp_hr.remove_node(target_node)
            else:
                _cp_hr.remove_node(target_node)

        return replica_nodes


if __name__ == '__main__':

    nr = NodeRing()
    print(nr.get_nodes('truouiyuuibe'))
    print(nr.get_nodes('trvevergibe'))
    print(nr.get_nodes('triergegbe'))
    print(nr.get_nodes('tribyjykyke'))
    print(nr.get_nodes('tribmbbmbme'))
    print(nr.get_nodes('trizczzcvbe'))
