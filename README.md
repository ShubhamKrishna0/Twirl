# Twirl: Copilot for the IRL — Turn Thoughts into Things


![Twirl.png](https://i.ibb.co/fqZYrYn/Twirl-train.png)

What if you could describe something, like a chair or a cup, and have it physically created?

Think **Copilot, but for the IRL**. 

Twirl, or Text-to-World IRL, is an AI agent for turning thoughts into reality via 3D printing.

Inspired by the theme of *Perspectives*, we set out to bridge the gap between imagination and reality. Twirl empowers anyone to create real-world objects without requiring technical expertise. By reimagining how we design and build, Twirl expands perspectives on creation, making the complex world of 3D modelling accessible for all.

Give any prompt, like "rocking chair with three back supports" and attach an image if you'd like.

Twirl will extract and infer features (ex. dimensions, object spatial relationships) and create a parameterized 3D CAD model instantly.

It'll allow you to continuously iterate on model generation until you have the perfect creation, making modifications with more prompts or images.

You can even adjust sliders and fields that change model variables like dimensions, colour, translations, and rotations. The entire generated CAD model is parameterized, allowing full customization within the web UI.

We render the 3D model live on the UI as it is created, allowing you to examine every pixel instantly.

Twirl doesn't just stop at visualization. It turns perspectives into physical reality. Models can be exported for 3D printing, making it possible to create functional objects directly from ideas. During the hackathon, we tested this end-to-end pipeline by designing and printing a chair model generated entirely by Twirl, with 0 human assistance.

With Twirl, we redefine the creative process, allowing everyone to see their ideas from a new perspective—one where imagination is the only limit.

Technologies used: 
![image](https://github.com/user-attachments/assets/ac63649c-f9ce-4efc-a95b-ddebeb0c9d46)


Created by: 
Martin, Marcus, William, and Jeff

## Getting Started

To get this project up and running on your local machine, follow these steps:

### Prerequisites
Make sure you have the following installed:
- [Node.js](https://nodejs.org/) (version 14 or higher)
- [Python](https://www.python.org/) (version 3.8 or higher)
- [Pip](https://pip.pypa.io/en/stable/) (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ShubhamKrishna0/Twirl.git
   cd Twirl
   ```
   
2. Navigate to the backend directory and install the required Python packages:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Navigate to the frontend directory and install the required Node.js packages:
   ```bash
   cd frontend
   npm install
   ```

### Configuration
1. Create a `.env` file in the `backend` directory and add your environment variables:
   ```plaintext
   SUPABASE_URL=your_supabase_url # https://your-supabase-url.supabase.co
   SUPABASE_KEY=your_supabase_key # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVzZXItYXR0YWNob3MtY29wZW90Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYwMzIwMjgsImV4cCI6MjA0MTYwODAyOH0.6-sHnS03OaQ4L0Gm5C-L5AmtZksvR8hQctY4QbQ4IU
   ANTHROPIC_API_KEY=your_anthropic_api_key # sk-ant-api03-1234567890abcdef1234567890abcdef
   AZURE_STORAGE_CONNECTION_STRING=your_azure_storage_connection_string # DefaultEndpointsProtocol=https;AccountName=youraccount;AccountKey=yourkey;EndpointSuffix=core.windows.net
   ```
2. Run the database migrations on Supabase dashboard:

```sql
-- Migration to create the artifacts, messages, and projects tables

-- Create artifacts table
CREATE TABLE IF NOT EXISTS artifacts (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    openscad_code TEXT,
    message_id BIGINT,
    parameters JSONB
);

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    is_user BOOLEAN,
    content TEXT,
    project_id BIGINT,
    image_url TEXT
);

-- Create projects table
CREATE TABLE IF NOT EXISTS projects (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    title TEXT
);
```

### Running the Application
1. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:3000` to view the application.
