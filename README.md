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
