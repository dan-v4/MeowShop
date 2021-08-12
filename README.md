# MeowShop
Discord bot for small-scale e-commerce. Essentially creates a shop for your server. Utilizes MongoDB for the database.

## Shop Setup
1. First, I recommend setting up a private text channel where only you (server owner) and MeowShop have permissions to read and send messages.  
![image](https://user-images.githubusercontent.com/85653267/129054069-7fd30cd7-b902-4dcf-9b7d-8de923920d55.png)  
![image](https://user-images.githubusercontent.com/85653267/129054121-54461656-332f-417c-9cd9-5abcff7b458f.png)  
2. Next, use `$setup <currency code> <shipping cost>`. Currency code must be defined in [ISO 4217](https://www.xe.com/iso4217.php). Cryptocurrencies are currently unsupported.  
![image](https://user-images.githubusercontent.com/85653267/129058434-3ef49aff-dcd1-49aa-bddb-8e9a576048ac.png)  
3. Add a payment method. Use `$addpayment <payment type> <payment instruction>`. It is highly recommended to instruct customers to attach a note/message when sending a payment.  
![image](https://user-images.githubusercontent.com/85653267/129059243-56ce30e7-59fc-46c2-88c5-d374bdf2b53a.png)  
4. Check your shop info using `$info` to verify.  
![image](https://user-images.githubusercontent.com/85653267/129059630-52fb77a7-a27b-4b95-b58b-7c0953fcbc66.png)  

**Notes**:
1. The default prefix is `$`,
2. The shop search code is blurred in the photos. However, you should share the shop search code to server members in order for them to buy from the shop.

## Adding products to the shop  
1. After setting up your shop, it's time to add products to your shop. Use `$addp <item name> <price> <count> <*desciption>`.  
![image](https://user-images.githubusercontent.com/85653267/129062463-b192efbc-6d02-464e-995b-45164b5d4451.png)  
Currently, the item name can only be one word. To set a longer name use `$setname <item id> <new name>` after using `$addp`.  
2. To check your product list use `$products`. Additionally, you can use `$products <server code>` to check product list in DMs.  
![image](https://user-images.githubusercontent.com/85653267/129063204-9ceb874b-b4cc-4a69-a426-29796c0da442.png)  


## Commands
Default Prefix: `$`  
  
**Owner commands:**  
Commands for server owner. Guild only commands. It is recommended to setup a private channel with permissions for MeowShop and server owner for the use of these commands.  
  
* `$setup <currency code> <shipping cost>` - Setup server shop. Must be used before shop is initialized.  
* `$setprefix <new prefix>` - Setup server prefix. Default prefix and DM prefix is `$`.  
* `$confirm <order code>` - Confirm order has been paid. Use after payment is received.  
* `$refund <order code>` - Confirm refund request. Use when payment has been refunded to the user.  
* `$addp <item name> <price> <count> <*desciption>` - Add a product for sale.  
* `$delp <item id>` - Delete a product.  
* `$setname <item id> <new name>` - Set item name. Can be used to change item name to multiple words.  
* `$setdesc <item id> <new description>` - Set item description.  
* `$setcount <item id> <new count>` - Set item count.  
* `$setprice <item id> <new price>` - Set item price.  
* `$setcurrency <currency code>` - Set shop currency.  
* `$setshipping <shipping cost>` - Set shop shipping price.  
* `$addpayment <payment type> <payment instruction>` - Add payment option.  
* `$delpayment <payment type>` - Delete payment option.  
  
**User commands:** 
Commands for buyer. DM only commands. `products` and `info` can be used within the server.  
  
* `$info <server code>` - Server shop info.  
* `$products <server code>` - Show products for sale. Can be used without <server code> within a server.
* `$payments <server code>` - Show payment methods.  
* `$add <server code> <item id> <quantity>` - Add an item to your cart.  
* `$remove <server code> <item id> <quantity>` - Remove items from your cart.  
* `$cart <server code>` - Show cart.  
* `$checkout <server code>` - Checkout cart.  
* `$cancel <order code>` - Cancel your order. Use when payment has not been sent yet.  
* `$rrefund <order code>` - Request a refund. Use when payment is sent.  

