async def next_product(products, index):
    try:
        return products[index + 1]
    except IndexError:
        return False


async def previous_product(products, index):
    try:
        if index == 0:
            return False
        return products[index - 1]
    except IndexError:
        return False
