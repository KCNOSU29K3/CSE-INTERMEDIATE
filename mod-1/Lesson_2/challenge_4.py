from challenge_4_module import calc_price, draw_square

def main():
    costs = [9.00, 10.99]
    discount = 50


    print("assuming a cost list of {} and a discount of {}%, the total price will be {}".format(costs, discount, calc_price(costs, discount)))


    draw_square(4, 50, 0, (0, 0), "red")
    input("")


if __name__ == "__main__":
    main()