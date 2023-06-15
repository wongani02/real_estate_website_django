from chartit import DataPool, Chart
from django.db.models import Sum
from properties.models import PropetyViews, Likes, Property
from django.utils.dateparse import parse_date
from django.utils.dateformat import format as format_date



# Return string of total number of property views
def sum_views(pk):
    sum = PropetyViews.objects.filter(property__id=pk).aggregate(total_views=Sum('views'))['total_views']

    return 'Total Views: {}'.format(sum)

# Return total number of property likes
def sum_likes(pk):
    """
    Since 'Likes' model does not have an incremental integer field like 'Property Views',
    just get the aggregate sum of an property column
    """
    sum = Likes.objects.filter(property__id=pk).count()

    return 'Total Likes: {}'.format(sum)

def create_properties_views_chart(pk):
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


def create_properties_likes_chart(pk):
    property_data_2 = DataPool(series=[
        {
            'options': {
                'source': Likes.objects.filter(property__id=pk)
            },
            'terms': ['date', 'count']
        }
    ])

    # Create chart object
    cht = Chart(
        datasource=property_data_2,
        series_options=[
            {
                'options': {
                    'type': 'spline',
                    'stacking': False,
                },
                'terms': {
                    'date': [
                        'count'
                    ]
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
                },
                'crosshair': 'true'
            },
            'yAxis': {
                'title': {
                    'text': 'Number of Likes'
                }
            },
            'subtitle': {
                'text': sum_likes(pk)
            },
        }
    )

    return cht


def get_months(date_obj):
    unique_months = set()

    for date_str in date_obj:
        try:
            # Parse input string into date object
            _date = parse_date(date_str)

            # Get the months name from the date object
            month_name = format_date(_date, "F")

            # Add the months name to the set
            unique_months.add(month_name)
        except ValueError:
            print("Invalid date format: ", date_str)
    
    # Convert the set to a list
    unique_months_list = list(unique_months)

    return unique_months_list

def destructure_date_objects(objs):
    formatted_dates=[]

    for date_obj in objs:
        formatted_date=date_obj.strftime("%Y-%m-%d")
        formatted_dates.append(formatted_date)

    return formatted_dates



def all_property_views_chart(request):
    def month_name(month_num):
        names = {
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul',
            8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        }
        return names[month_num]

    # Get date objects from database
    objs=destructure_date_objects(PropetyViews.objects.values_list('date', flat=True))
    
    # Get month from date objects
    months = get_months(objs)
    
    # Create data pool with data we want to retrieve
    property_data = DataPool(series=[
        {
            'options': {
                'source': PropetyViews.objects.filter(property__agent__username=request.user.username)
            },
            'terms': [
                'views', 
                'date',
                # 'property'
            ]
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
            },
            'subtitle': {
                'text': sum_views(request.user.pk)
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
        },
        # x_sortf_mapf_mts=(None, month_name, False)
    )

    # Return chart
    return cht
