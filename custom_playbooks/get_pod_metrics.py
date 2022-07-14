from robusta.api import *
from prometheus_api_client import PrometheusConnect


@action
def free_disk_space(pod_event: PodEvent):

    # Get pod metrics CPU and memory.

    labels = {
        "pod": pod_event.get_pod().metadata.name,
        "namespace": pod_event.get_pod().metadata.namespace,
    }
    metrics_enrichment = create_metrics_enrichment(
        item_type=ResourceChartItemType.Pod,
        labels=labels
    )
    pod_event.add_enrichment(metrics_enrichment)


def create_metrics_enrichment(
    item_type: ResourceChartItemType,
    labels: Dict[Any, Any],
):
    cpu_usage_pod_query = 'sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{namespace="$namespace", pod=~"$pod"})'
    promql_query = __prepare_promql_query(labels, cpu_usage_pod_query)
    cpu_query_output = run_prom_query(promql_query)
    #mem_usage_pod_query = 'sum(container_memory_working_set_bytes{job="kubelet", metrics_path="/metrics/cadvisor", pod=~"$pod", container!="", image!=""})',
    #promql_query = __prepare_promql_query(labels, mem_usage_pod_query)
    #mem_query_output = run_prom_query(promql_query)

    block_list: List[BaseBlock] = []
    #block_list.append(MarkdownBlock(f"Command results for *{params.bash_command}:*"))
    block_list.append(MarkdownBlock(f"Pod CPU Usage"))
    block_list.append(MarkdownBlock(cpu_query_output))

    #block_list.append(MarkdownBlock(f"Pod Memory Usage"))
    #block_list.append(MarkdownBlock(mem_query_output))

    return block_list


def __prepare_promql_query(provided_labels: Dict[Any, Any], promql_query_template: str) -> str:
    labels = defaultdict(lambda: "<missing>")
    labels.update(provided_labels)
    template = Template(promql_query_template)
    promql_query = template.safe_substitute(labels)
    return promql_query


def run_prom_query(prom_query):
    prometheus_base_url = PrometheusDiscovery.find_prometheus_url()
    prom = PrometheusConnect(url=prometheus_base_url, disable_ssl=True)
    result = prom.custom_query(query=prom_query)
    return result
