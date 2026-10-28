from app import take, unique_count

def preview(items, count):
    return take(items, count), unique_count(items)
