# Blink - The Wooden Store

The web-based platform is designed for the seamless sale of wooden products, incorporating multiple roles with distinct responsibilities to ensure efficient operations and a positive customer experience.

Administrator (Super Admin):
The Super Admin oversees the entire system, managing user roles, permissions, and system settings. They are responsible for financial transactions, system configurations, and ensuring overall security measures are in place.

Manager:
The Manager plays a crucial role in daily operations, overseeing employees and managing product requirements. They collaborate with Product Makers to create wooden products based on specific criteria outlined by either the Manager or Admin.

Product Maker:
Product Makers are tasked with crafting wooden products as per the specifications provided by the Manager or Admin. Once the products are ready, they submit them to Quality Assurance (QA) for thorough testing.

Quality Assurance (QA):
The QA team rigorously tests the wooden products for quality, functionality, and adherence to predefined standards. They approve or reject products based on their findings, ensuring only high-quality items reach the inventory.

Delivery Person:
Delivery Personnel are responsible for ensuring timely and accurate delivery of orders to customers. They pick the products from the warehouse based on available stocks and coordinate with the Manager for efficient order fulfillment.

Warehouse Owner:
The Warehouse Owner manages the storage and organization of inventory in the warehouse. They track stock levels, coordinate with the Manager for replenishment, and ensure smooth operations within the warehouse facility.

Customer (End User):
Customers access the online platform to browse a wide range of wooden products. They can explore different categories and subcategories, view product variants and prices, apply filters for customized searches, place orders, track delivery statuses, and provide feedback on their overall experience.

Key Features:

Product Creation and Management: Collaboration between Managers and Product Makers to create and add new wooden products to the inventory.
Inventory Management: Managers oversee stock levels, product attributes, variants, categories, and subcategories to ensure a well-organized inventory.
Order Processing: Managers process customer orders, coordinating with Delivery Personnel for timely order fulfillment.
Delivery Management: Delivery Personnel pick products from the warehouse and deliver them to customers, providing delivery status updates.
Financial Management: Managers handle expense tracking, ledger entries, and financial transactions within the system.
User Management: Admins or Managers create and manage user accounts, assigning roles and permissions as needed to streamline operations.
In essence, this web-based application facilitates a smooth and efficient process for selling wooden products online, from product creation to delivery, while providing customers with a user-friendly experience and ensuring quality standards are met throughout.
 
### Refere link below to check functionality and use of code functions.

https://docs.google.com/spreadsheets/d/1-o7KIyzILiTkdL2W-5vtvBnvsVJGQ93pHBjymeZBqFk/edit?usp=sharing


## Setup for new database

# run fixtures 

#### python manage.py loaddata admin_fixture.json
#### python manage.py loaddata states.json


