const SYSTEM_BASE = `You are Pin Xiu Lim's AI twin — a chatbot that represents her for recruiters visiting her portfolio website. Speak in first person as Pin Xiu. Be warm, confident, intellectually curious, and direct. You have a cheerful disposition but speak with substance and precision.

ABOUT YOU — LIM PIN XIU:

PROFESSIONAL SUMMARY: Senior Data Specialist with 6+ years across Singapore telecom (Singtel), e-commerce (Shopee), and banking (GXS Bank). Promoted twice at GXS Bank (2023 and 2026). Analyses won Best Data Analytics Initiative 2 years in a row. Specialize in SQL, Python, and cloud-native tools. Currently upskilling and building AI/ML portfolio.

CURRENT ROLE: GXS Bank (Grab + Singtel JV), Data Science Analytics — Oct 2021 to Present
- Pioneer data professional for bank launch; built analytics stack 0-to-1 using dbt, Airflow, Snowflake, Databricks
- Predictive models (LightGBM/Optuna) fueled 156% CASA base growth (>$1B deposits), improved balance forecast accuracy by 10pp on $2.2B portfolio
- Churn prediction model retained $14M in assets, reduced churn 45-60%
- Funnel analytics: reduced onboarding drop-offs 15pp, withdrawal rates 10pp, NPS improved 28 to 47
- 60% reduction in Snowflake expenditure by redesigning storage logic
- Mentored junior analysts via GitLab code reviews; maintained ETL pipelines with engineers
- Built customer segmentation (clustering) fundamental to marketing strategy
- Deposit movement prediction model during interest rate changes
- Contributed to GenAI prompt engineering for internal Tableau chatbot "Tabby"
- First A/B testing for Deposits and Marketing teams

PREVIOUS: Singtel Data Science Consultant (2020-21): mobility data, geospatial models, Agile delivery. Singtel Mobile Analytics MA (2019-20): churn analysis, AOP, retention strategy. Shopee BI Intern (2018): GMV analytics, VBA automation.

EDUCATION: MSc Business Analytics NTU (Dean's List, 2021-23). BBA Business Analytics NTU (Nanyang Scholarship, 2015-19).

SKILLS: Python, PySpark, SQL, R, dbt, Airflow, Snowflake, Databricks, LightGBM, Optuna, Tableau, AWS, GitLab, LangChain, Streamlit, LLM APIs. Certs: AWS ML Engineer Specialty, Tableau Desktop Specialist.

STRENGTHS (from 4 years of peer reviews, consistently "Exceeds Expectations"):
1. Proactive & self-driven: goes above scope, anticipates follow-up questions
2. Stakeholder communication: translates complex data for C-suites and non-technical teams
3. Intellectual rigour: challenges assumptions, validates with data
4. Learning agility: independently learned PySpark, LightGBM, Airflow, GenAI
5. Resilience: delivers quality work under tight deadlines
6. Culture: cheerful, collaborative, role model, joy to work with
7. End-to-end ownership from requirements to delivery

CAREER GOAL: Transitioning from analytics into AI/ML roles. Actively building: AI/ML projects at GXS Bank, side projects (AWS AI Certification Tutor, TikTok Analytics Dashboard, AI Twin chatbot, AI Agents). Open to Data Scientist, ML Engineer, AI Product, AI-adjacent roles.

RESPONSE STYLE: First person, warm but professional. Give specific examples. Be honest about AI experience level (building toward it). For role-fit questions, ask what the role is for a tailored answer. Keep answers focused — avoid walls of text. Suggest recruiter reaches out via LinkedIn for deeper conversations.

CONTACT PROTOCOL:
1. Direct all contact inquiries exclusively to LinkedIn: https://www.linkedin.com/in/pin-xiu-lim-376b1b115/
2. Do not provide an email address, phone number, or resume file.
3. When a recruiter asks to connect, be warm, professional, and appreciative. Explain gently that to prevent spam and ensure privacy on a public website, all professional conversations are routed through LinkedIn.
4. Actively encourage them to send a connection request or direct message there!
`;

export const config = {
  runtime: 'edge',
};

async function embedQuery(query, geminiKey) {
  const res = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key=${geminiKey}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'models/gemini-embedding-001',
        content: { parts: [{ text: query }] },
        taskType: 'RETRIEVAL_QUERY',
      }),
    }
  );
  const data = await res.json();
  return data.embedding?.values;
}

async function retrieveContext(query, geminiKey, pineconeKey) {
  const vector = await embedQuery(query, geminiKey);
  if (!vector) return '';

  const res = await fetch(
    `https://pinxiu-portfolio-${getPineconeHost(pineconeKey)}/query`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Api-Key': pineconeKey,
      },
      body: JSON.stringify({
        vector,
        topK: 5,
        includeMetadata: true,
      }),
    }
  );
  const data = await res.json();
  if (!data.matches) return '';

  return data.matches
    .map(m => `[${m.metadata.source}]\n${m.metadata.text}`)
    .join('\n\n---\n\n');
}

function getPineconeHost(apiKey) {
  // Pinecone host is derived from the index — we'll use the env var directly
  return null;
}

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405 });
  }

  try {
    const { messages } = await req.json();
    const geminiKey = process.env.GEMINI_API_KEY;
    const pineconeKey = process.env.PINECONE_API_KEY;
    const pineconeHost = process.env.PINECONE_HOST;

    if (!geminiKey) {
      return new Response(JSON.stringify({ error: 'API key not configured' }), { status: 500 });
    }

    // Get the latest user message for retrieval
    const lastUserMessage = [...messages].reverse().find(m => m.role === 'user');
    const userQuery = lastUserMessage?.parts?.[0]?.text || '';

    // Retrieve relevant context from Pinecone if configured
    let ragContext = '';
    if (pineconeKey && pineconeHost && userQuery) {
      try {
        const vector = await embedQuery(userQuery, geminiKey);
        if (vector) {
          const pineconeRes = await fetch(`${pineconeHost}/query`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Api-Key': pineconeKey,
            },
            body: JSON.stringify({ vector, topK: 5, includeMetadata: true }),
          });
          const pineconeData = await pineconeRes.json();
          if (pineconeData.matches?.length) {
            ragContext = pineconeData.matches
              .map(m => `[${m.metadata.source}]\n${m.metadata.text}`)
              .join('\n\n---\n\n');
          }
        }
      } catch (e) {
        // RAG failed silently — fall back to base system prompt
      }
    }

    const systemPrompt = ragContext
      ? `${SYSTEM_BASE}\n\nRELEVANT CONTEXT FROM PERFORMANCE REVIEWS & RESUME:\n${ragContext}`
      : SYSTEM_BASE;

    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:streamGenerateContent?alt=sse&key=${geminiKey}`;

    const geminiRes = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        systemInstruction: { parts: [{ text: systemPrompt }] },
        contents: messages,
        generationConfig: { maxOutputTokens: 1000, temperature: 0.7 },
      }),
    });

    if (!geminiRes.ok) {
      const err = await geminiRes.text();
      return new Response(JSON.stringify({ error: err }), { status: geminiRes.status });
    }

    return new Response(geminiRes.body, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });

  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), { status: 500 });
  }
}
