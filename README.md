Farm-Direct

Farm-Direct is a farmer-to-customer web platform that streamlines the process of buying and selling agricultural produce. It’s designed to empower farmers and consumers by enabling direct market access, inventory tracking, and secure transactions — all within a polished and user-friendly interface.

🚀 Features

Multilingual Support: UI supports English, Marathi, and Hindi, making the platform accessible to a wider audience.

Farmer Module: Farmers can add products, manage their inventory, and track their listings seamlessly.

Customer Module: Customers can browse products, apply filters, sort items, and add produce to their cart.

Interactive Cart & Checkout: A smooth cart management system, along with a modal-style checkout experience.

Banking Integration: Both farmers and customers can manage their bank details directly from the app.

AI-Generated Descriptions: Product descriptions are generated dynamically using a language model (e.g., Gemini API).

Real-time Insights Simulation: Mock market data and insights panels to give users a feel for live market updates.

Engaging UI/UX: Includes toast notifications, loading spinners, micro-interactions, transitions, and animations.

📂 File Structure & Descriptions

frontend.html
This file contains the full client-side UI for Farm-Direct. It integrates Bootstrap, JavaScript, and custom styles to create a responsive and interactive dashboard. The page offers a multilingual splash screen, farmer and customer modules, real-time product listing, cart functionality, and dynamic UI components like notifications and loading states.

index.html
A Jinja2 template used in the Flask backend project. It serves as the landing / home page and includes a hero section, feature cards (Farmer, Customer, Direct Market Access), and call-to-action buttons for registration and login. Structured using Bootstrap for responsiveness, and designed for template inheritance ({% extends "base.html" %}).

🛠️ Tech Stack

Frontend: HTML, CSS, Bootstrap, JavaScript

Backend: Flask (Python)

Templating: Jinja2

Data Storage: (If you have one — mention here, e.g., PostgreSQL / SQLite / MySQL)

AI / ML (if used): (Mention the model or API for generating descriptions)

Other Tools: (List any other libraries or APIs you integrated)

✅ Setup & Run

Clone the repository:

git clone https://github.com/AryaPatil0406/Farm-Direct.git  
cd Farm-Direct  


Create and activate a virtual environment:

python3 -m venv venv  
source venv/bin/activate    # On Windows: venv\Scripts\activate  


Install dependencies:

pip install -r requirements.txt  


Run the Flask app:

flask run  


Then open http://localhost:5000 in your browser.

💡 Future Enhancements

Add user authentication for farmers/customers.

Implement real-time backend data to replace mock market insights.

Integrate payment gateway to enable secure transactions.

Build analytics dashboard for farmers to track sales and demand.

Use a database (if not already) to persist user data and product catalogs.
