from platform import node
from robusta.api import *

@action
def free_disk_space(event: PrometheusKubernetesAlert):

    
    node = event.get_node()

    block_list: List[BaseBlock] = []
    exec_result = RobustaPod.exec_in_debugger_pod(
        pod_name="node-bash-pod", node_name=node.metadata.name,cmd="touch test.txt",debug_image="busybox"
    )

    block_list.append(MarkdownBlock(f"Command results for *touch test.txt* UPDATED"))
    block_list.append(MarkdownBlock(exec_result))

    finding = event.create_default_finding()
    event.add_enrichment(block_list)
