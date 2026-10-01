# Aesen A. Chavez — Portfolio

Personal portfolio site: aviation maintenance background + self-hosted systems automation.

**Live:** https://Aeseeen.github.io

---

## What's here

| Path | What it is |
|---|---|
| `index.html` | The portfolio site. Single file, zero dependencies, no build step. |
| `cv/CV_Aesen_Chavez_Hybrid.pdf` | One-page hybrid CV (aviation IT / MRO systems) |
| `cv/CV_Aesen_Chavez_Hybrid.docx` | Same CV, editable |
| `build_cv.py` | Python generator that produces both CV files from one content block |
| `assets/` | Screenshots of the automation work |

The CV is **generated, not hand-formatted**. Edit the `CONTENT` block in `build_cv.py`,
run `python3 build_cv.py`, and both the `.docx` and `.pdf` rebuild from a single source.
That keeps the two files from ever drifting apart.

```bash
pip install python-docx reportlab
python3 build_cv.py
```

---

## The work behind it

**Automation pipeline for a service business** *(live, in production)*
Google Forms → Google Sheets → n8n → self-hosted Baserow CRM, running in Docker on Debian.
Replaced manual booking records with a single source of truth and automated follow-up tracking.

**Aircraft Maintenance Log & Compliance Tracker** *(in development)*
Self-hosted inspection logging with due-date alerting across both calendar days and flight hours,
plus an immutable edit history. Built on Baserow + n8n + Docker.
Inspired by paper-based record-keeping observed during a 420-hour maintenance rotation
at the Philippine Air Force 207th Tactical Helicopter Squadron.

---

## Aviation background

- **Aircraft Maintenance Trainee (OJT)** — 207th Tactical Helicopter Squadron,
  Philippine Air Force, Col. Jesus Villamor Air Base, Pasay City (Jun–Aug 2026)
- 420 supervised hours on **Bell 412EP** and **UH-1H** helicopters
- 600-hour inspections, preventive maintenance, component installation,
  engine ground runs, towing and tie-down, refuelling
- Tool control, FOD prevention, technical manual reading, maintenance documentation

---

## Contact

- Email: aesenchavez18@gmail.com
- Mobile: +63 947 245 0023
- Location: Muntinlupa City, Metro Manila, Philippines
- LinkedIn: [linkedin.com/in/YOUR-HANDLE](https://linkedin.com/in/YOUR-HANDLE)

---

<sub>Built and hosted by me — on Debian Linux, with Docker.</sub>
