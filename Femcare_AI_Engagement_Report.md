# Femcare AI · Engagement Report · June 2025

**SilverTrust AI Consulting**  
Responsible AI Solution Design for Women's Menopause Health

| | |
|---|---|
| **Prepared by** | Lucas Barrios, Mira Raab, Ellen Sea |
| **Client** | Femcare AI |
| **Date** | June 2025 |
| **Industry** | Women's Healthcare — Menopause |

---

## Executive Summary

Femcare AI is a pre-GTM women's health startup with a clear mission — to become the number one trusted health companion for women navigating the menopause lifecycle — but with three critical blockers standing between their vision and a safe, scalable product launch.

> **Core Problem Statement**  
> Femcare AI struggles to move from vision to product because it lacks a data compliance framework, a scalable AI architecture, and a defined niche strategy. Without these, any new product built risks legal exposure under GDPR, unsustainable operational costs, and zero market differentiation. The client has confirmed that the product focus is the full menopause lifecycle: premenopause, menopause, and postmenopause as three clinically distinct phases.

This engagement report delivers:

- A discovery summary from stakeholder interviews with Sam Johnson (Product), Max Carter (Operations), and Ady (Business Development)
- A compliant-by-design AI solution — a Personalised Menopause Health Navigation Assistant built on RAG architecture
- A full EU AI Act risk classification and GDPR data map
- LangSmith observability setup for client trust and regulatory auditability
- Three distinct business model options for client consideration
- A recommended go-forward architecture and implementation roadmap
- A pricing strategy with concrete token cost mitigation options addressing the review board's change requests

---

## 1. Discovery Findings

Findings gathered through blind stakeholder interviews using indirect questioning — no pain points were volunteered; all were uncovered through process and time-based questions.

### 1.1 Discovery Questions

**Q1.** *"Walk me through what a typical week looks like for you — where does most of your time go?"*  
Target: All personas — opens the workflow conversation without directing it

**Q2.** *"What's the last project or initiative that didn't go as planned — what happened?"*  
Target: Sam — surfaced the failed agent build and unclear AI strategy

**Q3.** *"If you imagine the business 12 months from now running smoothly — what does that look like, and what had to change to get there?"*  
Target: Max — surfaced the cost, restructuring, and lean process concerns

**Q4.** *"When you think about bringing a new product to market, what's the step that always takes longer than it should?"*  
Target: Ady — surfaced the missing value proposition, compliance gap, and absent marketing owner

**Q5.** *"How do you currently decide which ideas are worth pursuing — and where does that process break down?"*  
Target: Sam — surfaced the 'thousands of ideas, no filter' problem and the failed agent attempt

### 1.2 Stakeholder Pain Point Summary

| Persona | Role | Implied Pain | Signal | Severity |
|---|---|---|---|---|
| Sam Johnson | Product Manager | No clear AI strategy; failed agent build; thousands of ideas with no filter | "Tried to build our own agent — it failed" | **HIGH** |
| Max Carter | Operations / Finance | Over budget; token costs unsustainable at scale; restructuring creating team uncertainty | "We ran over budget — cost sensitivity is real" | **HIGH** |
| Ady | BD Manager | No value proposition defined; no niche strategy; no in-house marketing; compliance gaps blocking GTM | "Data and compliance not yet in place" | **HIGH** |

### 1.3 The Three Critical Blockers

> **Blocker 1 — No Compliance Foundation**  
> Only a cookie policy exists. No GDPR consent framework, no legal owner, no data processing agreements. The company is about to build a personalised health application collecting sensitive health data (Article 9 special category) with zero legal coverage.

> **Blocker 2 — Unsustainable AI Architecture**  
> Currently burning €1,000–2,000/month on tokens using GPT-4 and Claude Opus for research tasks alone. No architecture decision has been made. An internal agent build failed. At current usage patterns, scaling to thousands of users makes the model financially unviable.

> **Blocker 3 — No Niche Strategy**  
> Targeting 'all women' broadly means the product cannot be specifically designed, positioned, or marketed. Without a defined niche, compliance scope is undefined, the AI cannot be optimised for specific conditions, and differentiation from general-purpose AI tools is impossible.

---

## 2. AI Solution Design

### 2.1 Solution Overview

We propose the **Femcare Menopause Navigator** — a RAG-based personalised health companion mobile application focused exclusively on the menopause lifecycle. This is not a general AI chatbot. It is a medically grounded, menopause-specific health navigation assistant that knows when to answer and when to refer.

> **Core Value Proposition**  
> Femcare Menopause Navigator gives women access to medically verified, menopause-specific health guidance across all three phases — premenopause, menopause, and postmenopause — grounded in peer-reviewed research, not generic AI hallucination, with every answer cited, every response traceable, and every data interaction legally sound.

### 2.2 System Architecture

| # | Layer | Function |
|---|---|---|
| 1 | User Input Layer | Mobile app (iOS/Android). Accepts text, voice, and symptom body-map input. Collects explicit consent at onboarding before any data is stored. |
| 2 | Query Processing | Rewrites vague symptom descriptions into structured medical queries specific to menopause phase. Handles ambiguity before retrieval begins. |
| 3 | RAG Retrieval Engine | Searches a curated knowledge base of menopause-specific medical literature (PubMed, WHO, EMA, NICE, proprietary advisor-validated content). Returns the most relevant document chunks. |
| 4 | Generation & Citation Layer | Smaller, cost-efficient model (GPT-4o mini or Claude Haiku) generates the answer with inline citations. Every response shows its source. |
| 5 | Confidence Threshold & Referral | If confidence falls below threshold, the system does not answer — it generates a structured GP or specialist referral summary instead. This eliminates medical advice liability. |

### 2.3 Knowledge Base Sources

| Tier | Sources | Why It Matters |
|---|---|---|
| Tier 1 — Core | PubMed/MEDLINE, WHO Guidelines, EMA, NICE | Credibility foundation. Publicly available, citable, covering EU clinical standards. |
| Tier 2 — Differentiation | WHI studies, Femcare advisor-validated proprietary content, phase-specific deep dives | **Product moat.** No other app has Femcare's proprietary, advisor-approved menopause knowledge layer. |
| Tier 3 — User-Generated | Anonymised symptom patterns from existing journal users (post-consent only) | High value for menopause phase pattern detection. Only activated after the full GDPR framework is in place. |

### 2.4 Full Feature Set

#### Layer 1 — Core RAG Menopause Navigation
- Conversational symptom input with voice support
- Menopause phase detection: premenopause, menopause, postmenopause
- Female-specific medical literature retrieval, scoped to menopause and hormonal health
- Cited answers — every response shows its source
- Confidence threshold: low confidence triggers a structured GP or specialist referral, not a guess
- Phase-specific condition depth: hot flushes, sleep disturbance, mood changes, brain fog, HRT guidance, bone health, cardiovascular risk, sexual health

#### Layer 2 — Agentic Workflows (LangChain)
- **Research Agent**: monitors PubMed and clinical databases for new menopause studies, summarises weekly, updates RAG knowledge base automatically
- **Doctor Prep Agent**: converts symptom journal entries into a structured GP or gynaecologist visit summary before each appointment
- **Follow-up Agent**: after a clinical visit, creates a personalised follow-up plan with reminders
- **Idea Filter Agent**: surfaces emerging menopause health topics from research to Sam's product pipeline — resolves the 'thousands of ideas, no filter' problem

#### Layer 3 — Workflow Automation (n8n)
- User onboarding flow: form input triggers consent confirmation, phase profile creation, and personalisation setup
- Consent management: every data collection event auto-logs a timestamped consent record — GDPR compliance by default
- Referral workflow: low-confidence responses trigger automatic GP or specialist referral summary generation
- Content pipeline: new research paper detected → summarised → medical advisor review queue → approved → injected into RAG

#### Layer 4 — Engagement and Retention Features
- Menopause phase tracking with insight streaks and personalised pattern summaries
- Symptom journal: conversational input, auto-structured for GP visits
- Body map input: tap to record where symptoms occur; AI tracks patterns over time
- Weekly health digest: personalised summary with one new relevant clinical finding
- Pattern detection alert: *'Based on 6 weeks of data, there is a pattern worth discussing with your doctor'*
- Anonymous community layer: shared experiences without medical claims

#### Layer 5 — Data and Backend Infrastructure
- Supabase backend with row-level security for health profiles
- Consent records with timestamps and full audit trail
- Anonymised aggregate data layer for research partnerships (post-consent only)
- LangSmith tracing on every AI query — full observability for regulators and medical advisors

### 2.5 Cost Architecture — Resolving the Token Burn Problem

> **Current vs. Proposed**  
> Current: €1,000–2,000/month using GPT-4/Opus for research queries directly.  
> Proposed: RAG retrieval handles the heavy lifting. Generation model drops to GPT-4o mini or Claude Haiku. Only edge cases escalate to larger models.  
> **Estimated result: 80–90% reduction in token cost at equivalent or higher output quality.**

---

## 3. Compliance Package

### 3.1 EU AI Act Classification

> **Risk Classification: LIMITED RISK (with High-Risk monitoring obligations)**  
> The system provides health information and guidance but explicitly does not provide medical diagnoses or treatment decisions. It operates as a 'health guide' rather than a 'medical device.' This keeps it outside the High-Risk category (Annex III, Medical Devices) provided the confidence threshold and referral mechanism are strictly implemented.  
>  
> **CRITICAL:** If the product ever generates diagnoses, treatment plans, or triage decisions autonomously, reclassification to High-Risk is mandatory. This boundary must be technically enforced, not only stated in the terms of service.

**Role Identification**

| Role | Obligations |
|---|---|
| Femcare AI — Deployer | Transparency obligations: users must know they are interacting with AI. Must not impersonate human health professionals. Must maintain interaction logs. |
| SilverTrust — Consultant / Implementation Partner | Responsible for ensuring the system designed and deployed meets the classification requirements identified in this report. Compliance documentation is a SilverTrust deliverable. |

### 3.2 GDPR Data Map

Femcare AI collects and processes special-category health data under Article 9 GDPR. This requires explicit consent and heightened protection measures.

| Data Type | Category | Purpose | Lawful Basis | Retention |
|---|---|---|---|---|
| Menopause symptom data | Special Category (Art. 9) | Personalised health navigation | Explicit consent | Duration of account + 30 days |
| Phase tracking & body map data | Special Category (Art. 9) | Pattern detection, personalisation | Explicit consent | Duration of account |
| Doctor visit summaries | Special Category (Art. 9) | Agent-generated prep documents | Explicit consent | User-controlled deletion |
| Name, email, device ID | Personal Data (Art. 6) | Account management | Contract performance | Duration of account + 90 days |
| Usage analytics (anonymised) | Non-personal (post-anonymisation) | Product improvement | Legitimate interest | 24 months rolling |
| Research aggregate data | Non-personal (post-anonymisation) | Research partnerships | Legitimate interest (strict anonymisation required) | Per research agreement |

### 3.3 Key GDPR Requirements

**Consent Framework (Priority: Launch Blocker)**
- Granular, explicit consent at onboarding — separate consent for each data purpose
- Freely given, specific, informed, and unambiguous — pre-ticked boxes are invalid
- Users must be able to withdraw consent at any time with immediate effect
- Consent records must be timestamped and stored — n8n automation handles this
- A Data Protection Officer (DPO) or equivalent legal owner must be assigned before any data collection begins

**Data Subject Rights**
- Right of access: users can request all data held about them
- Right to erasure: full account and data deletion within 30 days
- Right to portability: health data must be exportable in a machine-readable format
- Right to rectification: users can correct inaccurate health data

**Data Minimisation**
- Only collect data explicitly required for the stated purpose
- Menopause symptom data is not shared with third parties without separate consent
- Research data is anonymised before any use — re-identification must be technically impossible

> **Data Protection Impact Assessment — Mandatory**  
> Because Femcare AI processes special-category health data (Article 9) at scale and uses automated personalisation, a full DPIA is mandatory before launch under Article 35 GDPR. This is not optional. SilverTrust recommends commissioning this immediately.

### 3.4 Sector-Specific Regulation

| Regulation | How We Address It |
|---|---|
| EU MDR (Medical Device Regulation) | Not triggered provided the system does not diagnose, treat, or triage. The confidence threshold and referral mechanism are the technical safeguard. Legal review required if any diagnostic language appears in the UX. |
| EHDS (European Health Data Space) | Emerging regulation for secondary use of health data. The research data layer must be designed with EHDS compliance in mind from day one. |
| German Digital Healthcare Act (DVG/DiGA) | If marketed in Germany as a health application, the DiGA fast-track pathway applies. DiGA-certified apps are reimbursable by statutory health insurers (GKV) — a significant distribution opportunity. |
| ePrivacy Directive | Cookie consent and communication tracking must comply beyond standard GDPR. No tracking pixels or analytics tools without active consent. |

---

## 4. LangSmith Monitoring

### 4.1 Why Monitoring Matters for Femcare AI

Women using this application are making health decisions about a significant life transition based on AI outputs. A wrong answer is not a UX failure — it is a patient safety event. LangSmith gives Femcare AI, its medical advisors, and regulators full visibility into every decision the system makes.

### 4.2 What We Monitor

| Signal | Why We Watch It | Action if Triggered |
|---|---|---|
| Low confidence responses | Catches cases where the model is guessing rather than retrieving from verified sources | Auto-escalate to referral; flag for medical advisor review |
| Retrieval quality score | Ensures RAG is returning relevant menopause-specific content, not hallucinating | Re-index knowledge base; review chunking strategy |
| Response latency | User experience and cost indicator | Alert if average exceeds 3 seconds; investigate retrieval bottleneck |
| Flagged outputs | User feedback: 'this answer was wrong or unhelpful' | Human review queue; update RAG if knowledge gap is identified |
| Sensitive topic detection | Crisis signals — suicide, self-harm, eating disorders | Hard override: block AI response; display crisis resources immediately |
| Data access patterns | Unusual query volumes may indicate misuse or potential data breach | Security alert; DPO notification if threshold is exceeded |

### 4.3 The Client-Facing Monitoring Commitment

> Every question a user asks, every answer the AI provides, and every time it chooses to refer rather than respond — all of it is logged, traceable, and reviewable. Medical advisors can audit outputs. If a regulator asks what the AI communicated to a specific user on a specific date, Femcare AI can demonstrate it. **This is not a black box. It has full visibility — and we built that in by design.**

---

## 5. Business Model Options

Three distinct business model options for Femcare AI's consideration. Not mutually exclusive — a hybrid approach is viable in later stages. All three are scoped to the menopause lifecycle focus confirmed by the review board.

### Option A — Consumer Freemium (B2C)

> **Strategic Priority: User growth and brand trust at scale**  
> Best for: becoming the most recognised app for menopause health in Europe.  
> Requires: strong product-led growth, viral mechanics, and a clear free-to-paid conversion funnel.

**Tiers**
- **Free:** symptom journal, basic menopause health search, phase tracking
- **Essential (€9.99/month or €79/year):** full AI navigation, phase-specific depth, doctor prep agent, weekly digest
- **Premium (€16.99/month or €129/year):** all Essential features plus HRT guidance, pattern detection alerts, and priority knowledge base updates
- **Phase-specific bundles:** Premenopause Plan, Menopause Plan, Postmenopause Plan

**Assessment**

| Dimension | Detail |
|---|---|
| Advantages | Highest brand visibility; fastest user acquisition; strong long-term data asset; viral potential |
| Risks | Highest customer acquisition cost; slowest path to profitability; requires marketing investment Ady's team is not yet resourced for; GDPR consent management at scale is complex |

### Option B — B2B2C via Employer Health Benefits

> **Strategic Priority: Revenue efficiency and a fast path to profitability**  
> Best for: solving the cost problem quickly while building the user base indirectly.  
> Requires: a targeted sales motion directed at HR departments and employee benefits platforms.

**How It Works**
- Sell to employers as a menopause health benefit (similar to Calm for Work, Headspace for Work)
- Pricing: €8–15/employee/month for companies with 200+ female employees
- One enterprise contract at 500 employees = €4,000–7,500/month recurring
- 10 contracts = €40,000–75,000/month — profitable at relatively low volume
- Partnership with employee benefits platforms: Benefitsy, Circula, Nilo Health

**Assessment**

| Dimension | Detail |
|---|---|
| Advantages | Fastest path to sustainable revenue; Germany actively mandating better menopause health benefits; longer contracts with lower churn |
| Risks | Longer sales cycles; requires enterprise sales capability Femcare does not yet have; GDPR complexity increases with employer as data processor |

### Option C — Clinical and Research Partnerships (B2B)

> **Strategic Priority: Credibility, defensibility, and long-term data moat**  
> Best for: building the most defensible and differentiated market position.  
> Requires: strong medical advisor relationships, DiGA certification pathway, and a longer investment horizon.

**Revenue Drivers**
- DiGA reimbursement: GKV pays €200–600 per prescription — scalable with no direct CAC per user
- Clinical licensing: €5,000–20,000/month per clinic partner
- Research data licensing: €50,000–200,000 per dataset per research partner (subject to strict GDPR anonymisation)

**Assessment**

| Dimension | Detail |
|---|---|
| Advantages | Highest credibility and differentiation; DiGA reimbursement removes price sensitivity; research licensing becomes more valuable as user base scales |
| Risks | Slowest to revenue — DiGA certification takes 12–24 months; most complex compliance requirements (MDR, GDPR, EHDS) |

### 5.4 Business Model Comparison

| Dimension | Option A — B2C Freemium | Option B — B2B2C Employer | Option C — Clinical / Research |
|---|---|---|---|
| Time to first revenue | 3–6 months | 6–9 months | 12–24 months |
| Revenue ceiling | Very high (scale) | High (enterprise) | Very high (reimbursement) |
| Compliance complexity | High | Very High | Extreme |
| Sales capability required | Marketing / growth | Enterprise sales | Medical / clinical network |
| Token cost risk | High at scale | Manageable (contracts) | Low (clinical use is bounded) |
| Brand building | Strongest | Moderate | Credibility-focused |
| **SilverTrust recommendation** | **Start here** | **Parallel track from month 6** | **Build toward from day one** |

---

## 6. Pricing Strategy and Token Cost Mitigation

*Addresses Change Request 2 (CR-2) from the review board.*

### 6.1 Competitive Pricing Landscape

| App | Category | Monthly | Annual | AI Features |
|---|---|---|---|---|
| Balance (Dr. Louise Newson) | Menopause tracking | — | ~$98.99/year | Health report generation |
| Caria | Menopause CBT | — | $78/year (~$6.50/month) | CBT sessions, symptom insights |
| Flo Premium | Cycle + menopause | ~$9.99 | ~$50/year | AI Health Assistant |
| Natural Cycles | Cycle/contraception | $12.99 | $99.99/year | Algorithmic fertility prediction |
| Clue Plus | Cycle tracking | — | ~$39.99/year | Limited |
| Omena (EU) | Menopause | — | €60/year (~€5/month) | Personalised wellness programmes |
| Evernow | Menopause telehealth | $35–49/month | — | Clinician-backed, prescriptions |
| Reverse Health | Menopause fitness | ~$20/month | — | Programme-based |

### 6.2 Three Strategic Observations

**1. A Pricing Gap Exists at the Clinical AI Level**  
The market clusters at a low end (€5–8/month: Caria, Omena, Clue) and a high end (€35–49/month: Evernow). There is no credible, AI-native menopause product in the €10–20/month range.

**2. Clinical Credibility Unlocks Higher Revenue Per User**  
Balance by Dr. Louise Newson (first certified by ORCHA for NHS use) charges $98.99/year despite relatively simple symptom tracking. The driver is clinical trust. Femcare's RAG architecture with cited sources is structurally positioned to compete at this tier.

**3. Scale Requires Cost Architecture, Not Just Revenue**  
Flo supported ~70 million monthly active users and ~5 million paid subscribers at $50/year. This model is only viable at significant scale. For Femcare pre-GTM, the priority is ensuring cost per user is structurally covered by revenue at modest volumes.

### 6.3 Recommended Pricing Architecture

| Tier | Price | Included | Benchmark Anchor |
|---|---|---|---|
| Free | €0 | 10 AI queries/month, symptom journal (unlimited) | Balance free tier, Flo free tier |
| Essential | €9.99/month or €79/year | 50 queries, phase tracking, doctor prep agent | Caria $78/yr, Flo $50/yr + premium positioning |
| Premium | €16.99/month or €129/year | Unlimited* queries, research digest, pattern alerts, HRT guidance | Balance $98.99/yr + AI navigation premium |

*'Unlimited' is internally capped via a credit architecture. Users experience it as unlimited; the business controls cost exposure.*

### 6.4 Internal Cost Control — Credit Architecture

| Query Type | Model Used | Estimated Cost | Routing Logic |
|---|---|---|---|
| Simple menopause symptom questions (Tier 1) | Claude Haiku / GPT-4o mini | ~€0.001/query | Always routed here first — 70%+ of all queries |
| Complex phase or HRT queries (Tier 2) | Mid-tier model | ~€0.005/query | Triggered by complexity classification |
| Edge cases + low confidence (Tier 3) | Referral output, not further inference | Minimal | Output is a GP referral summary, not a larger model call |

> **Unit Economics (Illustrative, Medium Confidence)**  
> Average 30 queries/month for an Essential user → approximately €0.10–0.20 in inference cost.  
> ARPU at €9.99/month → margin remains structurally sound even at a 3× vendor price increase with Tier-1 routing in place.  
> *This assumption requires validation against actual usage data. Establishing average queries per user per month is the single most important analytical step before finalising the cost model.*

### 6.5 Concrete Token Risk Mitigation (CR-2 Response)

**Option 1 — Model Switching Layer (Immediate, Low Effort)**  
An abstraction layer (LiteLLM or LangChain Router) decouples application code from any single AI vendor. If OpenAI prices increase, Femcare can switch to Anthropic, Mistral, or Gemini in a single day without rebuilding the application. **Implement in Phase 0, not deferred to Phase 2.**

**Option 2 — Open-Source Fallback (Medium-Term)**  
Tier-1 queries can run on a self-hosted model such as Llama 3 or Mistral 7B (estimated infrastructure cost: €80–120/month on Hetzner Germany). Estimated 70% of all queries are Tier-1 eligible — a material cost reduction. *This assumption requires testing before commitment.*

**Option 3 — Internal Token Budget per Subscription Tier**  
Each subscription tier carries a monthly internal token budget. Free tier: hard cap. Premium tier: soft cap with graceful throttling, not hard blocking. The user-facing message — *'You've received three in-depth answers this week'* — creates perceived value while controlling cost exposure.

> **Usage-Based Pricing: Not Recommended for This Product**  
> Usage-based pricing creates a mental cost barrier at every symptom question — the opposite of building clinical trust. Women navigating menopause have high, episodic information needs; usage-based pricing punishes the most valuable users. Health decisions should feel safe to ask, not metered.

---

## 7. Implementation Roadmap

| Phase | Timeline | Key Actions | Blocker Resolved |
|---|---|---|---|
| Phase 0 — Foundation | Weeks 1–4 | Assign DPO/legal owner. Commission DPIA. Build consent framework. Confirm menopause lifecycle as product scope. Finalise AI architecture decision. Implement LiteLLM abstraction layer. | Blockers 1 & 3 |
| Phase 1 — Core Build | Months 2–4 | Build RAG pipeline scoped to menopause phases. Integrate PubMed, WHI studies, and advisor-validated content. Implement LangSmith monitoring. Build n8n onboarding and consent automation. Internal testing with medical advisors. | Blocker 2 |
| Phase 2 — Beta | Months 4–6 | Closed beta with 200–500 users from the existing journal community. Tune RAG quality. Validate confidence threshold. Test doctor prep agent. Collect consent records. Measure average queries per user. | Validation |
| Phase 3 — GTM | Months 6–9 | Launch B2C freemium. Begin employer sales conversations in parallel. Publish first research insights from aggregate anonymised data (with consent). Begin DiGA assessment. | Revenue |

---

## 8. Risk Register

| Risk | Severity | Status | Mitigation |
|---|---|---|---|
| Medical advice liability | **HIGH** | Unresolved | Confidence threshold + referral mechanism. Legal framing as 'health guide', not 'medical device'. MDR legal review required. |
| GDPR / data compliance gap | **HIGH** | Not in place | Assign DPO immediately. Commission DPIA. Build consent framework in Phase 0 before any data collection begins. |
| No defined value proposition | **HIGH** | Resolved (CR-1) | Menopause lifecycle confirmed as product scope in Phase 0. |
| Token cost unsustainable | **MEDIUM** | Active | RAG + smaller model routing reduces cost by 80–90%. LiteLLM abstraction layer prevents vendor lock-in. Implement in Phase 0–1. |
| AI vendor pricing dependency | **MEDIUM** | Active (CR-2) | Model-switching layer (LiteLLM). Open-source fallback (Llama 3) for Tier-1 queries. Internal token budget per subscription tier. |
| Team morale / restructuring | **MEDIUM** | Active | Transparent process visibility. AI augments roles, not replaces them. |
| No in-house marketing | **MEDIUM** | External only | Phase 0–1: external partner sufficient. Hire in-house growth lead before Phase 3 GTM. |

---

## 9. Recommended Next Steps

Five decisions and actions that unlock everything else. None require significant budget — they require commitment and clear ownership.

| # | Action | Why It Unblocks Everything | Owner |
|---|---|---|---|
| 1 | Assign a legal / compliance owner | Without this, nothing that touches data can move forward. Single highest-leverage appointment Femcare can make right now. | Max Carter |
| 2 | Confirm menopause lifecycle as product scope | Confirmed by the review board as CR-1. Drives product design, AI optimisation, marketing, compliance scope, and market differentiation simultaneously. | Sam + Ady |
| 3 | Choose a business model | Options A, B, and C are presented in Section 5. The choice determines the sales motion, GTM timeline, and team capability required. | Full leadership team |
| 4 | Commission the DPIA | Mandatory before any data collection at scale. Can proceed in parallel with other actions once the legal owner is appointed. | Max Carter + Legal |
| 5 | Follow-up session with SilverTrust | To cover internal processes, user acquisition lifecycle, and cross-team communication flows. The initial discovery session was cut short; this session is required to complete the engagement. | Full team |

---

## Appendix: Peer Approval Record & Change Log

### A.1 Proposal Pitched

| | |
|---|---|
| **Problem** | Women navigating menopause lack medically grounded, female-specific health information. Generic AI is too broad and not clinically trustworthy. Femcare AI's current web journal is outdated and does not scale. |
| **Solution** | RAG-based mobile health companion — answers symptom questions with cited sources, prepares users for doctor visits, refers to a physician when uncertain. Never guesses. |
| **Architecture** | Layered model routing: cheap models for simple queries, escalation for complex. Projected 80–90% cost reduction vs. current setup. |
| **EU AI Act** | Limited-risk (health information, not diagnosis). Transparency obligations apply. |
| **GDPR** | Explicit consent at onboarding · Right to erasure · Anonymised research data. |
| **Safety gate** | Model refers to doctor when confidence is low — never guesses. |
| **Monitoring** | LangSmith traces every interaction. Medical advisors review outputs. Flagged answers trigger human review. |
| **Business model** | Consumer app first (Option A), then layer corporate benefits (Option B) once validated. |

### A.2 Review Board Decision

> **CHANGES REQUESTED**  
> The review board acknowledged the strength of the architecture and compliance framing but raised two substantive concerns before sign-off. The proposal is not approved in its current form.

### A.3 Change Requests

**CR-1 — Narrow product scope to the full menopause lifecycle**

> *"The product scope is too broad. Rather than targeting all women across all health topics, the focus must be narrowed to the full menopause lifecycle — premenopause, menopause, and postmenopause — as three clinically distinct phases, each with different symptom profiles, information needs, and user journeys."*

**CR-2 — Address third-party AI dependency and pricing risk**

> *"The current proposal is too reliant on third-party AI providers. Rising token costs and vendor pricing changes are a real business risk — especially given Femcare AI is already burning €1,000–2,000/month before scaling. The revised proposal must present concrete pricing mitigation options and reduce single-vendor dependency. A hybrid consumption model or model-switching strategy must be specified, not left as a monitoring note."*

### A.4 Open Action Items

| # | Action | Owner | Priority |
|---|---|---|---|
| 1 | Redesign scope to cover premenopause / menopause / postmenopause as three distinct phases | Consulting team | **HIGH** |
| 2 | Specify concrete AI pricing mitigation strategy (hybrid, model-switching, open-source) | Consulting team | **HIGH** |
| 3 | Appoint legal/compliance owner | Max Carter | **BLOCKER** |
| 4 | Commission data protection review | Max + Legal | **BLOCKER** |
| 5 | Confirm business model choice | Sam, Ady, Max | **HIGH** |

### A.5 Change Log

| CR | Change Requested | Before | After | Decision |
|---|---|---|---|---|
| CR-1 | Narrow product scope | Generic women's health — all topics, no niche, no defined condition | Full menopause lifecycle: premenopause, menopause, postmenopause as three distinct clinical phases | **Accepted** |
| CR-2 | Address AI pricing dependency | Pricing risk noted as monitoring item only | Concrete options: hybrid model, model-switching strategy, open-source fallback | **Accepted** |

*Captured at the conclusion of the Tuesday peer-review session · Revisions to be presented Wednesday.*

---

*SilverTrust AI Consulting · Responsible AI. By design.*  
*Lucas Barrios · Mira · Ellen — June 2025*  
*Confidential · SilverTrust AI Consulting*
