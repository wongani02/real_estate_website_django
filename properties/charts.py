from chartit import DataPool, Chart
from django.db.models import Sum
from properties.models import PropetyViews, Likes



# Return string of total number of property views
def sum_views(pk):
    sum = PropetyViews.objects.filter(property__id=pk).aggregate(total_views=Sum('views'))['total_views']

    return 'Total Views: {}'.format(sum)

def create_properties_views_chart(pk, p_name):
    # Create data pool with data we want to retrieve
    property_data = DataPool(series=[
        {
            'options': {
                'source': PropetyViews.objects.filter(property__id=pk)
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
                    'type': 'spline',
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
            },
            'subtitle': {
                'text': sum_views(pk)
            },
            'legend': {
                'shadow': True,
                'reversed': True
            },
            'plotOptions': {
                'line': {
                    'boarderWidth': 10,
                    'borderRadius': 5,
                }
            }
        }
    )

    # Return chart
    return cht


def create_properties_likes_chart(request):
    property_data_2 = DataPool(series=[
        {
            'options': {
                'source': Likes
            },
            'terms': ['property', 'date',]
        }
    ])
    
    # Create chart object
    cht = Chart(
        datasource=property_data_2,
        series_options=[
            {
                'options': {
                    'type': 'column',
                    'stacking': False,
                },
                'terms': {
                    'date': ['property_id',]
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

    return cht
