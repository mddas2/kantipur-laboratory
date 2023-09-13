import datetime
import nepali_datetime
from django.template.defaulttags import register

@register.filter
def get_NepaliDate(date):
    try:
        dt = datetime.date(date.year,date.month,date.day)
        nepali_date = nepali_datetime.date.from_datetime_date(dt)
        return nepali_date
        # return nepali_date.strftime('%K-%n-%D (%k %N %G)')   
    except:
        return date