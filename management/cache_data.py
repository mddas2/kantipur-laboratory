from django.core.cache import cache

def cached_function():
    # Try to get data from the cache
    cached_data = cache.get('my_cached_data')
    
    if cached_data is None:
        # Data not in cache, simulate fetching from a data source
        data = {'message': 'Data fetched from the data source.'}
        
        # Store data in cache for 60 seconds
        cache.set('my_cached_data', data, 60)
    else:
        data = cached_data
    
    return data
