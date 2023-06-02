from chartit import DataPool, Chart
from properties.models import PropetyViews, Likes


def create_views_chart(request):
    # Create data pool with data we want to retrieve
    property_data = DataPool(series=[
        {
            'options': {
                'source': PropetyViews
            },
            'terms': ['views', 'date',]
        }
    ])

    # Create chart object
    cht = Chart(
        datasource=property_data,
        series_options=[
            {
                'options': {
                    'type': 'column',
                    'stacking': False,
                },
                'terms': {
                    'date': ['views',]
                }
                
            }
        ],
        chart_options={
            'title': {
                'text': 'Property Views'
            },
            'xAxis': {
                'title': {
                    'text': 'Date'
                }
            },
            'yAxis': {
                'title': {
                    'text': 'Number of Views'
                }
            }
        }
    )

    property_data_2 = DataPool(series=[
        {
            'options': {
                'source': Likes
            },
            'terms': ['property', 'date',]
        }
    ])

    # Create chart object
    cht2 = Chart(
        datasource=property_data_2,
        series_options=[
            {
                'options': {
                    'type': 'column',
                    'stacking': False,
                },
                'terms': {
                    'date': ['property',]
                }
                
            }
        ],
        chart_options={
            'title': {
                'text': 'Property Likes'
            },
            'xAxis': {
                'title': {
                    'text': 'Date'
                }
            },
            'yAxis': {
                'title': {
                    'text': 'Number of Likes'
                }
            }
        }
    )

    # Return chart
    return cht, cht2

def create_likes_chart(request):
    pass