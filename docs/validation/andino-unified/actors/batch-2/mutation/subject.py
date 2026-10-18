def page(items, index, size):
    start = index * (size - 1)
    return items[start:start + size]
