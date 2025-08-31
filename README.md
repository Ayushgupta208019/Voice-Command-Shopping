# Voice Command Shopping Assistent

## Deployed Link:- https://voiceassistent.pythonanywhere.com/

## How to use
https://github.com/user-attachments/assets/0fb29b18-f9ea-4461-a184-4fc871c3d691

## Discription:-

This project prototype is designed for hands-free shopping. 

With this project, users can add, remove, and check out their products using voice commands, eliminating the need to click on the "Add to Cart," "Remove from Cart," and "Check Out" buttons. 

It helps users save time searching for products, as they can simply send a voice message, and if the product is available on the list, it will appear in the suggestion list.

## Tech Stack

**Client:** HTML, CSS, JavaScript

**Server:** Flask/Django, flask-cors

**NLP:** spacy, NumPy

**Voice Command:** Web Speech API (JavaScript) for browser-based voice recognition.


## Features

### Speech-to-Text:

- Use Web Speech API (for browser) or Google Speech-to-Text API (for advanced accuracy, multilingual).

### NLP Understanding:

- Use spaCy to parse sentences.

- Add/Remove Items:

   - “Add bananas”
    - “Remove milk”

- Parse numbers from sentences → "Add 3 oranges" → quantity=3.

    - Example: "I want to buy 2 apples" → {action: "add", item: "apple", quantity: 2}.

### Quantity Management:

- Parse numbers from sentences → "Add 3 oranges" → quantity=3.

### Multilingual Support:

- Currently Support Two Languages "ENGLISH", "HINDI".

### Smart Suggestions
- Suggest multiple products that matches the product name.

## WorkFlow Diagram
<img width="1622" height="851" alt="Image" src="https://github.com/user-attachments/assets/42c1fe05-2eea-427f-989e-1b3a0eeacf3a" />

## Run at Local Server
      open app.py file
      python app.py  --run at terminal

      open index.html file in chrome browser

## Detail Approach, Challanges and Future Improvement & Scalability

### Project Approach: Voice-Activated Shopping Assistant

#### 1\. Project Overview & Core Objective

**Elevator Pitch:** This is a full-stack web application that allows users to manage a shopping cart using voice commands. It's designed to provide a hands-free, intuitive shopping experience by interpreting natural language to add, remove, and check out items.

**Core Objective:** To build a functional prototype of a voice-first e-commerce interface, demonstrating skills in frontend development, backend API creation, and basic Natural Language Processing (NLP).

-----

#### 2\. System Architecture

The application follows a classic client-server architecture, composed of three distinct layers:

1.  **Frontend (Client-Side):** This is the user interface that runs in the browser. It's built with vanilla HTML, CSS, and JavaScript. Its primary responsibilities are:

      * Displaying the product list, shopping cart, and checkout history.
      * Capturing user voice input via the browser's **Web Speech API**.
      * Communicating with the backend via asynchronous **REST API calls (`fetch`)**.

2.  **Backend (Server-Side):** This is the "brain" of the application, built with Python and the Flask micro-framework. It's a stateless API server responsible for:

      * Serving the product catalog.
      * Processing all business logic.
      * Managing the shopping cart session.
      * Performing Natural Language Processing on the voice commands.

3.  **Data Layer:** The data storage is intentionally simple for this prototype and is handled in three ways:

      * **Product Catalog:** A static `products.json` file on the server, acting as our product database.
      * **Shopping Cart State:** An **in-memory Python list** on the backend. This means the cart is temporary and resets if the server restarts.
      * **Checkout History:** The browser's **`localStorage`**. This makes the history persistent for a user on their specific browser.

-----

#### 3\. Technology Stack

My choice of technologies was guided by the goal of rapid prototyping and leveraging the right tools for the job.

  * **Backend:**

      * **Python:** Chosen for its simplicity and powerful libraries, especially for NLP.
      * **Flask:** A lightweight web framework, perfect for building RESTful APIs without unnecessary bloat.
      * **spaCy:** A modern and efficient NLP library used for **entity recognition** (identifying the product names in a command).
      * **Flask-CORS:** Middleware to handle Cross-Origin Resource Sharing, essential for allowing the frontend to communicate with the backend API.

  * **Frontend:**

      * **HTML5, CSS3, Vanilla JavaScript:** Chosen to demonstrate core web development skills without framework overhead. It keeps the frontend light and fast.
      * **Web Speech API:** A browser-native API for handling speech-to-text conversion.

  * **Data Format:**

      * **JSON:** The standard data interchange format for communication between the frontend and backend.

-----

#### 4\. Detailed Execution Flow (User Journey)

Let's walk through the most common user action: **"Add two T-shirts to the cart."**

1.  **Voice Capture (Frontend):** The user clicks "Start Recording." The browser's Web Speech API listens and transcribes the audio into the text string `"add two t-shirts to the cart"`.

2.  **API Request (Frontend):** The JavaScript `onresult` event handler takes this string and sends it in a `POST` request to the backend's `/process_voice` endpoint.

3.  **Intent Recognition (Backend):** The Flask server receives the request.

      * The `detect_intent()` function uses regular expressions (e.g., `r"\b(add|buy)\b"`) to quickly classify the user's primary goal as `"add"`.

4.  **Entity Extraction (Backend):**

      * The `extract_quantity()` function finds the word "two" and converts it to the integer `2`.
      * The `extract_item()` function uses **spaCy** to parse the text, identify `"t-shirts"` as a noun (the entity), and extracts it.

5.  **Business Logic (Backend):**

      * The system loads the product list from `products.json`.
      * It uses a `best_match()` scoring function to find the product that most closely matches the extracted item "t-shirts" (in this case, "T-shirt").
      * It then checks the in-memory `shopping_cart`. If "T-shirt" is already present, it increases its quantity by 2. If not, it adds it as a new item with a quantity of 2.

6.  **API Response (Backend):** The server sends a JSON response back confirming the action, e.g., `{"intent": "add", "added": "T-shirt", "qty": 2}`.

7.  **UI Update (Frontend):**

      * The JavaScript `fetch` promise resolves, receiving the confirmation.
      * It then triggers the `refreshCart()` function, which makes a *new* `GET` request to the `/cart` endpoint.
      * This fetches the complete, updated cart state from the server.
      * Finally, the JavaScript dynamically clears and rebuilds the cart table in the HTML to reflect the new state, including the new total price.

-----

#### 5\. Key Design Choices & Challenges

  * **Hybrid NLP Approach:** I used a simple but effective hybrid NLP strategy. Regular expressions are fast and reliable for identifying clear commands (intents), while a more sophisticated tool like spaCy is used for the nuanced task of extracting product names (entities). This avoids over-engineering while delivering accurate results for the defined scope.
  * **Server-Side State Management:** The choice to keep the cart in-memory on the server was a deliberate trade-off. It simplifies the logic significantly for a prototype. The main challenge is that the state is ephemeral, which leads to the next point.
  * **Client-Side Persistence:** To provide a sense of continuity, the checkout history is saved in `localStorage`. This demonstrates an understanding of different state-management techniques and their appropriate use cases. The checkout amount is carefully captured from the UI *before* the cart is cleared to prevent data loss.

-----

#### 6\. Future Improvements & Scalability

This prototype serves as a strong foundation, and if I were to continue developing it, I would focus on the following areas:

1.  **Persistent User Carts:** Replace the in-memory list with a proper database (like PostgreSQL or MongoDB) and implement user authentication (e.g., JWT tokens). This would allow users to have their own carts that persist across sessions.
2.  **Advanced NLP Model:** Train a custom intent classification and entity recognition model (using tools like Rasa or scikit-learn) to handle more complex and varied user commands, improving accuracy and flexibility.
3.  **Frontend Framework:** Migrate the frontend to a modern framework like **React or Vue.js**. This would enable more robust state management, create reusable components, and make the UI more dynamic and easier to maintain.
4.  **Comprehensive Testing:** Implement a testing suite with `pytest` for the backend API and a framework like Jest for the frontend to ensure code quality and prevent regressions.
5.  **Deployment & Containerization:** Containerize the application using **Docker** and deploy it to a cloud service (like AWS or Google Cloud) for public access and scalability.

## How to Use

- Click on "Something Want to buy" Button
- Tell the product name then multiple products matching to same name display on suggestion list if products available.
- Tell add [product name] [quatity] for adding the product to the cart.
- Tell remove [product name] [quatity if needed] for remove the product from the cart.
- Tell checkout to checkout or place the order.
- Thank You
