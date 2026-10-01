#!/usr/bin/env python3
"""
Aesen A. Chavez - HYBRID CV (Aviation IT / MRO Systems positioning)
ONE PAGE. ATS-safe (single column, no tables, no graphics, no headers/footers).

Outputs:
  CV_Aesen_Chavez_Hybrid.docx  -- editable + ATS upload
  CV_Aesen_Chavez_Hybrid.pdf   -- email / portfolio download

Edit CONTENT only, then re-run:  python3 build_cv.py
"""
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = "/home/user/portfolio/cv"

# ============================================================================
#  CONTENT  --  replace every [BRACKETED] placeholder before sending out.
# ============================================================================
NAME = "AESEN A. CHAVEZ"
TAGLINE = "Aviation Maintenance Trainee  |  Maintenance Data & Compliance Automation"
CONTACT = "Muntinlupa City, Metro Manila  |  +63 947 245 0023  |  aesenchavez18@gmail.com"
LINKS = "linkedin.com/in/aesen-chavez-870b26343  |  aeseeen.github.io"

SUMMARY = (
    "BS Aviation Engineering Technology student with 420 supervised helicopter maintenance hours under "
    "the Philippine Air Force 207th Tactical Helicopter Squadron. Self-taught in Linux, Docker, and n8n "
    "automation, with a live booking and CRM pipeline running on self-hosted infrastructure. Targeting MRO "
    "systems, technical records, and maintenance compliance automation."
)

SECTIONS = [
    ("TECHNICAL PROJECTS", [
        ("role", "Independent Operations & Automation Project",
                 "Britt's Zen Home Service Massage  |  Jun 2026 - Present"),
        ("bullet", "Designed, deployed, and now operate an end-to-end booking and lead-capture workflow using Google Forms, Google Sheets, n8n automation, and a self-hosted Baserow CRM."),
        ("bullet", "Replaced manual record-keeping with a single source of truth; automated lead routing and follow-up tracking."),
        ("bullet", "Administer the self-hosted stack on a Debian Linux host with Docker, covering deployment, backups, and troubleshooting."),

        ("role", "Aircraft Maintenance Log & Compliance Tracker - Capstone, in development",
                 "Self-hosted  |  Baserow + n8n + Docker on Debian  |  2026 - Present"),
        ("bullet", "Building a self-hosted inspection logging system with due-date alerting across both calendar days and flight hours, plus an immutable edit history."),
        ("bullet", "Scoped from paper-based record-keeping observed during a 420-hour live airbase rotation; covers aircraft and component records, inspection scheduling, findings, and audit trail."),
    ]),

    ("AVIATION MAINTENANCE EXPERIENCE", [
        ("role", "Aircraft Maintenance Trainee (On-the-Job Training)",
                 "207th Tactical Helicopter Squadron, Philippine Air Force  |  Col. Jesus Villamor Air Base, Pasay City  |  Jun 2026 - Aug 2026"),
        ("bullet", "Completed 420 supervised maintenance hours on Bell 412EP and UH-1H helicopters in a live military airbase environment."),
        ("bullet", "Assisted in 600-hour inspections, preventive maintenance, component installation, engine ground runs, towing and tie-down, and refueling."),
        ("bullet", "Applied aviation safety standards daily: tool control, FOD prevention, technical manual reading, and maintenance documentation."),
        ("bullet", "Coordinated with officers and technicians on daily work assignments, tool crib inventory, and hangar upkeep."),
    ]),

    ("ADDITIONAL EXPERIENCE & LEADERSHIP", [
        ("role", "Customer Service Representative (in training)",
                 "Alorica Philippines - foodpanda voice account  |  [MONTH] 2026 - Present"),
        ("bullet", "High-volume voice account training; daily practice in strict script compliance and per-transaction documentation."),

        ("role", "Office Assistant Intern - Guidance Department",
                 "Mano Amiga Academy  |  Paranaque City  |  Feb 2023 - Mar 2023"),
        ("bullet", "Front-desk point of contact for students, staff, and visitors; maintained records, filing systems, and reports."),
    ]),

    ("EDUCATION", [
        ("role", "BS Aviation Engineering Technology - 4th Year Level",
                 "Sapphire International Aviation Academy  |  Paranaque City  |  2023 - Present"),
        ("bullet", "Coursework: aircraft maintenance practices, aviation safety and regulations, aircraft systems."),
    ]),

    ("CERTIFICATIONS & LICENSES - IN PROGRESS", [
        ("li", "Linux Essentials (Cisco NetAcad) - Nov 2026  |  Azure Fundamentals AZ-900 - Dec 2026"),
        ("li", "CompTIA Network+ - Mar 2027  |  CompTIA Security+ - Jul 2027  |  CAAP AMT License - Sep 2027"),
    ]),

    ("TECHNICAL SKILLS", [
        ("kv", "Systems", "Linux (Debian) administration and CLI troubleshooting; Docker and self-hosted service deployment; backups"),
        ("kv", "Automation", "n8n workflow automation; HTTP webhooks; REST API integration; Baserow CRM (self-hosted)"),
        ("kv", "Aviation & Safety", "Maintenance support (Bell 412EP, UH-1H); tool control and inventory; FOD prevention; technical manual reading; ground handling assist"),
        ("kv", "Documentation", "Google Workspace (Forms, Sheets, Drive); Microsoft Word and Excel; technical and compliance documentation"),
        ("kv", "Languages", "English (fluent); Filipino (native)"),
    ]),
]

# ============================================================================
#  STYLE CONSTANTS  (points). Tuned so the CV lands on exactly one page.
# ============================================================================
FONT = "Calibri"
S_NAME = 19
S_TAG = 10
S_CONTACT = 8.7
S_HEAD = 10.5
S_ROLE = 9.5
S_ORG = 8.8
S_BODY = 9.1
LEAD = 10.5          # exact line height for body text
NAVY = (0x1F, 0x38, 0x64)
GREY = (0x50, 0x50, 0x50)


# ============================================================================
#  DOCX
# ============================================================================
def build_docx():
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Inches(0.42)
    sec.bottom_margin = Inches(0.42)
    sec.left_margin = Inches(0.58)
    sec.right_margin = Inches(0.58)

    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(S_BODY)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    pf = normal.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)

    def set_exact(p, line_pt, before=0, after=0):
        """Exact line rule makes pagination deterministic across Word/LibreOffice."""
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        if line_pt:
            pPr = p._p.get_or_add_pPr()
            sp = pPr.find(qn("w:spacing"))
            if sp is None:
                sp = OxmlElement("w:spacing")
                pPr.append(sp)
            sp.set(qn("w:line"), str(int(line_pt * 20)))
            sp.set(qn("w:lineRule"), "exact")

    def newp(line_pt=LEAD, before=0, after=0, indent=None, hang=None):
        p = doc.add_paragraph()
        set_exact(p, line_pt, before, after)
        if indent is not None:
            p.paragraph_format.left_indent = Inches(indent)
        if hang is not None:
            p.paragraph_format.first_line_indent = Inches(-hang)
        return p

    def put(p, text, bold=False, italic=False, size=S_BODY, color=None):
        r = p.add_run(text)
        r.bold, r.italic = bold, italic
        r.font.size = Pt(size)
        r.font.name = FONT
        r._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        if color:
            r.font.color.rgb = RGBColor(*color)
        return r

    def rule(p):
        pPr = p._p.get_or_add_pPr()
        pbdr = OxmlElement("w:pBdr")
        b = OxmlElement("w:bottom")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "6")
        b.set(qn("w:space"), "1")
        b.set(qn("w:color"), "1F3864")
        pbdr.append(b)
        pPr.append(pbdr)

    def heading(text):
        p = newp(line_pt=S_HEAD + 2.4, before=5.2, after=1.2)
        put(p, text, bold=True, size=S_HEAD, color=NAVY)
        rule(p)

    # ---- header
    p = newp(line_pt=S_NAME + 3)
    put(p, NAME, bold=True, size=S_NAME, color=NAVY)
    p = newp(line_pt=S_TAG + 2)
    put(p, TAGLINE, size=S_TAG, color=GREY)
    p = newp(line_pt=S_CONTACT + 2)
    put(p, CONTACT, size=S_CONTACT)
    p = newp(line_pt=S_CONTACT + 2.6, after=1)
    put(p, LINKS, size=S_CONTACT, color=NAVY)

    # ---- summary
    heading("PROFESSIONAL SUMMARY")
    p = newp(after=0.5)
    put(p, SUMMARY)

    # ---- body sections
    for title, blocks in SECTIONS:
        heading(title)
        for b in blocks:
            kind = b[0]
            if kind == "role":
                p = newp(line_pt=S_ROLE + 2.4, before=2.6)
                put(p, b[1], bold=True, size=S_ROLE)
                p = newp(line_pt=S_ORG + 2)
                put(p, b[2], italic=True, size=S_ORG, color=GREY)
            elif kind == "bullet":
                p = newp(indent=0.19, hang=0.14)
                put(p, "\u2022  ", color=NAVY)
                put(p, b[1])
            elif kind == "kv":
                p = newp(indent=0.19, hang=0.0)
                put(p, b[1] + ": ", bold=True)
                put(p, b[2])
            elif kind == "li":
                p = newp(indent=0.19, hang=0.14)
                put(p, "\u2022  ", color=NAVY)
                put(p, b[1])

    path = f"{OUT}/CV_Aesen_Chavez_Hybrid.docx"
    doc.save(path)
    return path


# ============================================================================
#  PDF  (reportlab, same content + metrics)
# ============================================================================
def build_pdf():
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    ListFlowable, ListItem, HRFlowable)

    NAVY_C = colors.HexColor("#1F3864")
    GREY_C = colors.HexColor("#505050")
    DARK = colors.HexColor("#1A1A1A")

    def esc(t):
        return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    name_st = ParagraphStyle("n", fontName="Helvetica-Bold", fontSize=S_NAME + 1,
                             textColor=NAVY_C, leading=S_NAME + 3, spaceAfter=2)
    tag_st = ParagraphStyle("t", fontName="Helvetica", fontSize=S_TAG,
                            textColor=GREY_C, leading=S_TAG + 2, spaceAfter=2)
    con_st = ParagraphStyle("c", fontName="Helvetica", fontSize=S_CONTACT,
                            textColor=DARK, leading=S_CONTACT + 2)
    h_st = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=S_HEAD,
                          textColor=NAVY_C, leading=S_HEAD + 2.4,
                          spaceBefore=5.2, spaceAfter=1.2)
    body = ParagraphStyle("b", fontName="Helvetica", fontSize=S_BODY,
                          textColor=DARK, leading=LEAD, spaceAfter=1.2)
    role_ = ParagraphStyle("r", fontName="Helvetica-Bold", fontSize=S_ROLE,
                           textColor=DARK, leading=S_ROLE + 2.2,
                           spaceBefore=2.6, spaceAfter=0)
    org_ = ParagraphStyle("o", fontName="Helvetica-Oblique", fontSize=S_ORG,
                          textColor=GREY_C, leading=S_ORG + 2, spaceAfter=0.5)
    bul = ParagraphStyle("bl", fontName="Helvetica", fontSize=S_BODY,
                         textColor=DARK, leading=LEAD)

    def rule():
        return HRFlowable(width="100%", thickness=0.7, color=NAVY_C,
                          spaceBefore=1, spaceAfter=2.4)

    def bullet_list(items):
        return ListFlowable(
            [ListItem(Paragraph(esc(t), bul), leftIndent=8) for t in items],
            bulletType="bullet", bulletFontName="Helvetica", bulletFontSize=7,
            bulletOffsetY=-1.2, start="\u2022",
            leftIndent=9, spaceBefore=0.6, spaceAfter=0)

    story = [
        Paragraph(esc(NAME), name_st),
        Paragraph(esc(TAGLINE), tag_st),
        Paragraph(esc(CONTACT), con_st),
        Paragraph(f'<font color="#1F3864">{esc(LINKS)}</font>', con_st),
        Spacer(1, 5),
        Paragraph("PROFESSIONAL SUMMARY", h_st),
        rule(),
        Paragraph(esc(SUMMARY), body),
    ]

    for title, blocks in SECTIONS:
        story.append(Paragraph(esc(title), h_st))
        story.append(rule())
        pending = []
        for b in blocks:
            if b[0] in ("bullet", "li"):
                pending.append(b[1])
                continue
            if pending:
                story.append(bullet_list(pending))
                pending = []
            if b[0] == "role":
                story.append(Paragraph(esc(b[1]), role_))
                story.append(Paragraph(esc(b[2]), org_))
            elif b[0] == "kv":
                story.append(Paragraph(f"<b>{esc(b[1])}:</b> {esc(b[2])}", body))
        if pending:
            story.append(bullet_list(pending))

    path = f"{OUT}/CV_Aesen_Chavez_Hybrid.pdf"
    doc = SimpleDocTemplate(
        path, pagesize=LETTER,
        leftMargin=0.58 * inch, rightMargin=0.58 * inch,
        topMargin=0.40 * inch, bottomMargin=0.40 * inch,
        title="Aesen A. Chavez - Curriculum Vitae",
        author="Aesen A. Chavez",
        subject="Aviation Maintenance Trainee | Maintenance Data & Compliance Automation",
    )
    doc.build(story)
    return path


if __name__ == "__main__":
    print(build_docx())
    print(build_pdf())
