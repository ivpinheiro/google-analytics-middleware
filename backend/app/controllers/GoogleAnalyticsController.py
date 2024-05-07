# Google Analytics imports
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    Filter,
    FilterExpression,
    RunReportRequest,
    RunRealtimeReportRequest
)

# Class imports
from .GoogleServicesAuthController import GoogleCloudServicesLogin

class GoogleAnalyticsController(GoogleCloudServicesLogin):
    def __init__(self, key, property_id, dimensions=None, metrics=None, filter_field_name=None, filter_in_list_filter=None, key_is_path = True):
        self.property_id = property_id
        self.dimensions = dimensions or []
        self.metrics = metrics or []
        self.filter_field_name = filter_field_name or ""
        self.filter_in_list_filter = filter_in_list_filter or []
        super().__init__(key, key_is_path)

    def connect_analytics_ga4_api(self):
        client = BetaAnalyticsDataClient(credentials=super().create_google_service_credential_for_ga4())
        return client

    def connect_analytics_ua_api(self):
        return super().create_google_service_credential_for_ua()
    
    def get_google_analytics_data_ga4(self, start_date_, end_date_):
        try:
            client = self.connect_analytics_ga4_api()
            dimensions = [Dimension(name=dimension_name) for dimension_name in self.dimensions]
            metrics = [Metric(name=metric_name) for metric_name in self.metrics]
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                dimensions=dimensions,
                metrics=metrics,
                date_ranges=[DateRange(start_date=start_date_, end_date=end_date_)],
            )
            response = client.run_report(request=request)
            if response.row_count > 0:
                return response
            else:
                return (), (), ()
        except Exception as e:
            print(f"Ocorreu um erro ao acessar a API do Google Analytics: {e}")
            return None

    def get_google_analytics_data_real_time_ga4(self):
        try:
            client = self.connect_analytics_ga4_api()
            dimensions = [Dimension(name=dimension_name) for dimension_name in self.dimensions]
            metrics = [Metric(name=metric_name) for metric_name in self.metrics]
            if (len(self.filter_in_list_filter) > 0 and len(self.filter_field_name) > 0):
                dimension_filter = FilterExpression(filter=Filter(field_name=self.filter_field_name, in_list_filter=Filter.InListFilter(values=self.filter_in_list_filter)))
            else:
                dimension_filter = None

            request = RunRealtimeReportRequest(
                property=f"properties/{self.property_id}",
                dimensions=dimensions,
                metrics=metrics,
                dimension_filter=dimension_filter
            )
            response = client.run_realtime_report(request=request)

            if response and response.row_count > 0:
                return response.rows, response.dimension_headers, response.metric_headers
            else:
                return (), (), ()
        except Exception as e:
            raise RuntimeError(f"Ocorreu um erro ao acessar a API do Google Analytics: {e}")
        
    def get_google_analytics_data_ua(self, start_date_, end_date_, pageToken = None):
        try:
            analytics = self.connect_analytics_ua_api()     
            response = analytics.reports().batchGet(
                body = {
                    "reportRequests": [
                        {
                        "viewId": self.property_id,
                        "dateRanges": [{'startDate': start_date_, 'endDate': end_date_}],
                        "metrics": self.metrics,
                        "dimensions": self.dimensions,
                        "pageToken": pageToken
                        }
                    ]
                }
            ).execute()
            
            if response:
                return response
            else:
                return (), (), ()
        except Exception as e:
            raise RuntimeError(f"Ocorreu um erro ao acessar a API do Google Universal Analytics: {e}")