🚀 Key Features of Trade Opportunities API

AI Market Analysis: Generates deep-dive Markdown reports on trends, regulations, and trade news.
JWT Authentication: Secure access using JSON Web Tokens (Bearer Scheme).
Input Validation: Uses Pydantic Enums to restrict inputs to specific valid sectors.
Rate Limiting: IP-based sliding window protection (5 requests per minute). 
Markdown Output: Returns raw .md content for easy saving and documentation.


🛠️ Tech Stack

Language: Python (3.12+)
Framework: FastAPI
AI SDK: google-generativeai
Security: PyJWT for token handling
Server: Uvicorn


⚙️ Setup and Installation

1. Clone the Repository
git clone https://github.com/ThomasBaby27/Trade-Opportunities-API.git
cd appscrip
2. Create Virtual Environment
python -m venv env
Windows: env\Scripts\activate
Mac/Linux: source env/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Environment Variables
GEMINI_API_KEY=enter your api key
SECRET_KEY=appscrip_task_2026


🚦 How to Run

1. Start the Server
uvicorn app.main:app --reload
The API will be available at: http://127.0.0.1:8000
2. Access Documentation
Open your browser to: http://127.0.0.1:8000/docs (Swagger UI)


🔐 How to Test

1. Get Token: Use the /token endpoint. Input your SECRET_KEY as the api_key.
2. Authorize: Copy the access_token from the response. Click the "Authorize" button at the top of Swagger and paste the token.
3. Analyze: Call the GET /analyze/{sector} endpoint. Choose a sector from the dropdown (Technology, Pharmaceuticals, or Agriculture).
4. Download: The response will be a structured Markdown report ready for use.