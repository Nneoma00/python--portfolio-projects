def generate_invoice():
    print("Welcome to the Command Line Invoice Generator")

    #save items: products/services since unknown, in an empty list
    #items is a list of tuples () including (product_name, qty, price_per_item, total_price)
    items = []

    #use an infinite while loop to get product names and prices until user says "done"
    while True:
        product_name = input("Enter product name: ")
        # if product_name == "done":
        #     break
        qty = int(input("Enter quantity: "))
        price_per_item = float(input("Enter price: "))

        total_price = qty * price_per_item
        items.append((product_name, qty, price_per_item, total_price))
        ask = input("Want to enter another product? Y/N: ").strip()
        if ask.lower() == "y":
            continue
        else:
            break 

#At this point, print the headings, i.e: how i want the invoice to look

    print("INVOICE")
    #Use the escape sequence (esc) OR backslash t (\t)to create tabs i.e: rows and columns?
    print("Item\t Qty\tPrice($) \tAmount")
    #Use 50 hyphens as an underline before looping through "items"
    print("-"*50)

    #initialize total amount. like total amoount of everything in invoice
    total_amount = 0

    #time to get values from the list of items. Values corresponding with product name, qty, etc
    for item in items:
        product_name, qty, price_per_item, total_price = item
        #Arrange variables to match the header
        print(f"{product_name}\t{qty}\t{price_per_item}\t{total_price}")

        #to be adding total_priceto total invoice bottomline with each iteration
        total_amount += total_price

    print("-"*50)
    print(f"Total amount: {total_amount}")
        
generate_invoice()
