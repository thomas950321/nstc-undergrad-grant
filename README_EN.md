<div align="center">

# AI-Assisted Proposal Writing Toolkit for NSTC Undergraduate Research Grants

**Automated topic selection, real literature citation audit, 10-page C802 proposal writing, and reviewer self-evaluation**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

[繁體中文](README.md) | [English](README_EN.md)

</div>

---

## Project Overview

This toolkit is an AI Agent Skill tailored specifically for the **NSTC Undergraduate Student Research Grant** (National Science and Technology Council, Taiwan). By loading this skill into AI assistants supporting Agent Skills (such as Claude Code, Gemini CLI, Cursor, Codex, etc.) and entering your research domain or initial concept, the AI will guide you step-by-step according to the latest NSTC guidelines and review criteria—from topic refinement, literature review, writing a full 10-page C802 proposal body, to pre-submission compliance checklist and final report writing.

## Pain Points Solved

Reviewers in recent years have grown increasingly vigilant against "AI-generated generic boilerplate" and "hallucinated/fabricated literature citations":

- **Strict Prevention of Fabricated Citations & Academic Integrity Red Lines**: Under NSTC and university regulations, all AI-generated data and references must be verified by the applicant. Fabricated papers or non-existent DOIs will be classified as forged research and result in immediate rejection.
- **Elimination of Generic AI Boilerplate**: Fluffy text filled with clichés like "significantly enhance" and "deeply explore", lacking concrete data and technical architecture diagrams, signals a lack of independent critical thinking.
- **Strict Format and Page Count Constraints**: The main body of the C802 proposal must strictly adhere to the 10-page limit. Exceeding page caps or omitting key diagrams (e.g., Gantt charts, workflow charts) frequently leads to direct point deductions.

This toolkit introduces an authentic reviewer evaluation perspective, featuring built-in literature authenticity audits (`citation-audit`), research gap validation, precise page-budget allocation, and Mermaid Gantt chart generation to build compelling, high-scoring proposals.

## Core Advantages

- **Dual-Verification for Real Literature**: Built-in citation integrity module that filters out hallucinated papers and ensures every reference is authentic and verifiable.
- **7-Dimension Reviewer Self-Evaluation**: Aligned with the 4 major NSTC review criteria to simulate reviewer scoring across originality, argumentation, literature, methodology, clarity, impact, and technical soundness.
- **Structured 10-Page C802 Layout**: Precise page allocation across Abstract (0.5 page), Motivation (1–1.5 pages), Literature Review (2.5–3 pages), Methodology (3–4 pages), and Expected Results (1 page), complete with an 8-month Mermaid Gantt chart.

## Quick Start

Get started in under a minute—no programming background required.

### Method A: Use GitHub Repository URL (Recommended)

If using Codex, Cursor, or Claude Code, enter the following directly into your chat interface:

```text
Please load this Skill repo: https://github.com/thomas950321/nstc-undergrad-grant.git
```

Once loaded, initiate your request:

```text
I want to apply for this year's NSTC Undergraduate Research Grant. My major is Information Management, and my advisor suggested working on "Generative AI Applications in Customer Service". Please guide me starting from Step 0.
```

### Method B: Copy Skill Folder Manually

Copy the downloaded `nstc-undergrad-grant` directory into your AI tool's skill folder:

- **Claude Code**: `~/.claude/skills/nstc-undergrad-grant/`
- **Gemini CLI**: `~/.gemini/skills/nstc-undergrad-grant/`
- **Cursor / Other Tools**: Place into your project root at `.agents/skills/`

## How It Works: 7 Core Steps

1. **Step 0 - Pre-check**: Verify sophomore+ eligibility, submission deadlines, 6-hour research ethics certificate, and budget rules (NT$48,000 stipend + up to NT$20,000 consumables).
2. **Step 1 - Topic & Research Gap Validation**: Narrow down to 2–3 candidate topics, analyze pros/cons of existing approaches, and establish a valid research gap.
3. **Step 2 - Literature Review & Citation Audit**: Construct a matrix of key literature from the past 3 years and verify citations to prevent AI hallucinations.
4. **Step 3 - C802 Proposal Drafting**: Write a full proposal adhering to the 300-word abstract formula, motivation data charts, technical architecture diagrams, and 8-month Mermaid Gantt chart.
5. **Step 4 - 7-Dimension Reviewer Self-Evaluation**: Simulate reviewer scoring (target score ≥ 28/35) and iterate on weak areas.
6. **Step 5 - Pre-submission Formatting & Compliance**: Verify 12pt PMingLiU/Times New Roman, 1.5 line spacing, PDF layout stability, and completeness of forms C801–C804.
7. **Step 6 - Final Report Writing**: Assist in writing the project final report within 1 month after project completion to maintain eligibility for the Research Creativity Award.

## Project Structure

```
nstc-undergrad-grant/
├── SKILL.md                        # Main skill workflow (Steps 0–6)
├── references/
│   ├── nstc_format_rules.md        # NSTC regulations, form IDs, formatting rules, and 10 common pitfalls
│   ├── section_template.md         # Abstract golden formula and detailed section templates
│   └── reviewer_checklist.md       # 7-dimension self-evaluation checklist aligned with NSTC criteria
└── prompts/
    ├── abstract.md                 # 300-word abstract generation and 30-second reviewer stress test prompt
    ├── gap_analysis.md             # Research gap matrix and citation audit prompt
    └── gantt.md                    # 8-month timeline Mermaid Gantt chart prompt
```

## License

This project is licensed under the [MIT License](./LICENSE).

## Important Disclaimers

- All deadlines, regulations, and funding amounts must be verified against the official announcements on the NSTC website ([nstc.gov.tw](https://www.nstc.gov.tw/)).
- Generative AI serves as an auxiliary tool for research and writing. Do not fabricate data or plagiarize, and ensure compliance with disclosure guidelines established by your institution and field.
- This toolkit is a community open-source template and is not an official publication of the NSTC.

## Contributing

Contributions of any kind are welcome! Whether updating regulations, refining prompts, fixing typos, or providing discipline-specific proposal examples, feel free to open a Pull Request or Issue.

## Sources & References

- NSTC Official Undergraduate Student Research Grant Portal & FAQ
- NSTC Operating Guidelines for Undergraduate Student Research Grants (Nov 1, 2024 revision)
- Executive Yuan and NSTC Generative AI Utilization Guidelines & Academic Ethics Guidelines
- wiki.interaction.tw Grant Writing Guide
