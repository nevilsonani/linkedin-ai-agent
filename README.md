# LinkedIn AI Content Creator 🤖

Automate and optimize your LinkedIn content creation process by analyzing trends, generating AI-powered posts, and improving based on user feedback.

---

## Features

- 🕵️‍♂️ Scrapes LinkedIn profiles for posts and engagement data  
- 📈 Analyzes content trends and optimal posting times  
- 🤖 Generates 3 AI-powered post variations with hashtags and CTAs  
- 🔄 Records user feedback to improve future suggestions  
- 🖥️ Simple Streamlit UI for interaction  
- ⏰ (Bonus) Schedule posts at optimal times based on engagement trends  

---

## Folder Structure

```plaintext
linkedin-ai-agent/
├── config/
│ ├── init.py
│ └── settings.py
├── data/
│ ├── scraped_posts.db
│ └── user_feedback.db
├── modules/
│ ├── init.py
│ ├── scraper.py
│ ├── analyzer.py
│ ├── generator.py
│ ├── database.py
│ └── scheduler.py
├── ui/
│ ├── init.py
│ └── app.py
├── requirements.txt
├── .env.example
└── README.md
```


---

## Prerequisites

- Python 3.9 or higher  
- Google Chrome browser  
- ChromeDriver (matching your Chrome version) installed and added to PATH  
- Git (optional, for cloning repo)  
- OpenAI API key ([Get API key](https://platform.openai.com/))  
- (Optional) LinkedIn credentials for scraping  

---

## Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/linkedin-ai-agent.git
cd linkedin-ai-agent
```


2. **Create virtual environment (recommended)**

```bash
python -m venv venv
.\venv\Scripts\activate
```


3. **Install dependencies**

```bash
pip install -r requirements.txt
```


4. **Configure environment variables**

-  `.env`:

```bash
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
OPENAI_API_KEY=sk-your-openai-api-key
```


---

## Usage

1. **Run the Streamlit app**

Make sure you are in the project root folder:

```bash
streamlit run ui/app.py
```


2. **Interact with the UI**

- Enter your post topic, select tone and call-to-action from the sidebar.  
- Click **Generate Posts** to get AI-generated LinkedIn post suggestions.  
- Review generated posts and click **Use Post** to provide feedback.  
- View trend insights and optimal posting times in the sidebar.

---

## Database

- SQLite databases are stored in the `data/` folder:  
  - `scraped_posts.db` — stores scraped LinkedIn posts and engagement data  
  - `user_feedback.db` — stores user feedback on generated posts  

---

## ChromeDriver Setup

- Download ChromeDriver that matches your installed Chrome version from:  
  https://chromedriver.chromium.org/downloads  
- Add the folder containing `chromedriver.exe` to your system PATH environment variable.  
- Verify installation by running `chromedriver --version` in your terminal.

---

## Notes

- LinkedIn scraping requires your LinkedIn credentials and may be subject to LinkedIn's terms of service. Use responsibly.  
- The AI post generation uses OpenAI GPT-4 model; API usage costs may apply.  
- Feedback on generated posts improves future suggestions by updating the feedback database.  
- Scheduler module can be extended to automatically post at optimal times.

---

## Troubleshooting

- **ModuleNotFoundError:**  
  Run Streamlit from the project root folder, not inside `ui/`:

```bash
cd linkedin-ai-agent
streamlit run ui/app.py
```



- **ChromeDriver errors:**  
Ensure ChromeDriver version matches Chrome browser and is in PATH.

- **OpenAI API errors:**  
Check your API key and internet connection.


