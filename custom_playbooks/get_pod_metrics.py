from robusta.api import *
from custom_playbooks.helpers import prom_query_runner

@action
def get_pod_metrics(pod_event: PodEvent):

    # Get pod metrics CPU and memory.
    labels = {
        "pod": pod_event.get_pod().metadata.name,
        "namespace": pod_event.get_pod().metadata.namespace,
    }
    metrics_enrichment = prom_query_runner.create_metrics_enrichment(
        item_type=ResourceChartItemType.Pod,
        labels=labels
    )
    pod_event.add_enrichment(metrics_enrichment)

