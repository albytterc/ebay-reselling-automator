import mysql.connector

# Connect to DB
mydb = mysql.connector.connect(
    host="buglehsljj3yjtsm5zbn-mysql.services.clever-cloud.com",
    user="uzlencznun28k5ip",
    password="rxH5dG9aAr4Rq99T7zaO",
    database="buglehsljj3yjtsm5zbn"
)

mycursor = mydb.cursor()

# Store SKU, Offer ID, Listing ID, URL 
# mycursor.execute("DROP TABLE IF EXISTS listing")
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS listing (id MEDIUMINT NOT NULL AUTO_INCREMENT, sku VARCHAR(255), offerId VARCHAR(255), listingId VARCHAR(255), url VARCHAR(255), status VARCHAR(255) DEFAULT 'Not Sold' , primary key (id) )")


def store_data(sku, offerId, listingId, url):
    # url = "https://www.amazon.com/Moto-Power-Unlocked-Smartphone-T-Mobile/dp/B08L5MN4LV/ref=sr_1_14?crid=1VCJ3UG6VQ86N&keywords=motorola+g+power&qid=1657210497&sprefix=motorola+g+power%2Caps%2C222&sr=8-14#renewedProgramDescriptionBtfSection"

    sql = "INSERT INTO listing (sku, offerId, listingId, url) VALUES (%s, %s, %s, %s)"
    val = (sku, offerId, listingId, url)
    mycursor.execute(sql, val)
    mydb.commit()


def clear_database():
    mycursor.execute("TRUNCATE TABLE listing;")


def see_listings():
    mycursor.execute("SELECT * FROM listing")
    result = mycursor.fetchall()
    print("LISTINGS")
    for x in result:
        print(f"Id: {x[0]} \nsku: {x[1]} \nofferid: {x[2]} \nlistingid: {x[3]} \nurl: {x[4]} \nstatus: {x[5]}")
        print("")


def update_status(url):
    sql = "UPDATE listing SET status = 'Sold' WHERE url = " + "'" + url + "' " + ""
    mycursor.execute(sql)
    mydb.commit()
    print(f"Status of {url[:80]}... updated")


def prompt_user():
    show_listings = input("Do you want to see your listings? (y/n): ")
    if show_listings == 'y':
        see_listings()

    to_update = input("Do you want to update the status of a listing? (y/n): ")
    if to_update == 'y':
        u = input("Enter the Amazon URL of a product you listed: ")
        update_status(u)
