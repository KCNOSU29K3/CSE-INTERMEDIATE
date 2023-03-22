"""
Discount program
"""
from textwrap import dedent


def calc_price(prices:list[float], discount_percent:float, gst_rate_percent:float = 5.0):
    """
    Calculates price
    """
    total = 0.0
    for i in prices:
        total += i

    total_discount = total*(discount_percent/100)
    total_gst = (total - total_discount) * (gst_rate_percent/100)
    reciept = f"""
    Item price 1: {prices[0]:.2f}
    Item price 2: {prices[1]:.2f}
    Item price 3: {prices[2]:.2f}

    total: {total:.2f}
    discount % : {discount_percent:.2f}
    total saved: {total_discount:.2f}
    gst: {total_gst:.2f}
    total: {total - total_discount + total_gst:.2f}
    """

    return(dedent(reciept))
    pass

def main():
    """
    main function
    """
    prices = []
    for i in range(3):
        prices.append(float(input(f"Please enter price {i+1}\n$")))
    
    discount_percent = float(input("What is the percentage of the discount?\n"))

    print(calc_price(prices, discount_percent))


if __name__ == "__main__":
    main()