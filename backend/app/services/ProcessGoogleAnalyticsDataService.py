
class ProcessGoogleAnalyticsDataService():
    def __init__(self, data) -> None:
        self.data = data
    
    def process_google_analytics_data_ga4(self):
        rows = self.data.rows
        dimension_headers = self.data.dimension_headers
        metric_headers = self.data.metric_headers
        object_data = {}
        for index_dimension_header, dimension in enumerate(dimension_headers):
            object_data[dimension.name] = [row.dimension_values[index_dimension_header].value for row in rows]
        for index_metric_header, metric in enumerate(metric_headers):
            object_data[metric.name] = [row.metric_values[index_metric_header].value for row in rows]
        return object_data
    
    def process_google_analytics_data_ua(self):
        report = self.data["reports"][0]
        columnHeader = report["columnHeader"]
        dimensions = columnHeader["dimensions"]
        metrics = [entry["name"] for entry in columnHeader["metricHeader"]["metricHeaderEntries"]]
        data = report["data"]["rows"]
        rows = [entry["dimensions"] + entry["metrics"][0]["values"] for entry in data]        
        return rows, dimensions, metrics