"""Build the submission PDF from SS1.png ... SS4.png; --draft uses run logs."""

import argparse
from pathlib import Path
from textwrap import wrap

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Image, PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer,
)


ROOT = Path(__file__).resolve().parent
STEM = "PES1UG24CS666_Harsha_K_LAB7"
SECTIONS = [
    ("SS1", "Original application", "SS1_buggy_application.txt",
     "The input cs is missing its course number. The original function raises "
     "ValueError when it tries to unpack one word into two variables."),
    ("SS2", "Failing Hypothesis tests", "SS2_summary.txt",
     "All three no-crash properties fail against the original module. The "
     "complete tracebacks and minimized inputs are in evidence/SS2_buggy_tests.txt."),
    ("SS3", "Fixed application", "SS3_fixed_application.txt",
     "Malformed inputs produce Invalid input, and execution continues. A second "
     "run verifies CS301, a credit total of 11, and a normalized student record."),
    ("SS4", "Passing test suite", "SS4_fixed_tests.txt",
     "All 31 tests pass: three Hypothesis properties and 28 regression cases "
     "covering valid results, malformed strings, and incorrect input types."),
]


def build(draft=False):
    missing = [key for key, *_ in SECTIONS
               if not (ROOT / "screenshots" / f"{key}.png").is_file()]
    if missing and not draft:
        raise SystemExit(
            "Missing screenshots: " + ", ".join(missing)
            + ". Save them in LAB7/screenshots, or use --draft for a transcript preview."
        )
    output = ROOT / f"{STEM}{'_DRAFT' if missing else ''}.pdf"
    styles = getSampleStyleSheet()
    styles["Title"].textColor = colors.HexColor("#193b56")
    styles["Heading1"].textColor = colors.HexColor("#193b56")
    styles["BodyText"].fontSize = 10
    styles["BodyText"].leading = 15
    styles.add(ParagraphStyle(
        "RunOutput", fontName="Courier", fontSize=8, leading=11,
        backColor=colors.HexColor("#f1f4f6"), borderPadding=8,
    ))
    story = []

    def paragraph(text, style="BodyText"):
        story.append(Paragraph(text, styles[style]))
        story.append(Spacer(1, 9))

    paragraph("Lab 7: Fuzzing for Input Validation Bugs", "Title")
    paragraph("Harsha K | PES1UG24CS666<br/>Course Registration | 13 November 2026")
    if missing:
        paragraph(
            "<b>DRAFT - screenshots pending.</b> The following pages show genuine "
            "captured run transcripts, not screenshots. Capture SS1-SS4 using the "
            "README commands and rebuild this report before submission."
        )
    paragraph("Objective", "Heading1")
    paragraph(
        "Use Hypothesis to find failures caused by unexpected input, harden all "
        "three parser functions, and verify both crash resistance and correct "
        "results for valid inputs."
    )
    paragraph("Implementation and validation", "Heading1")
    paragraph(
        "format_course_code validates an alphabetic ASCII department and a "
        "digit-only course number. total_credits validates the input type and "
        "handles integer conversion errors without returning a partial sum. "
        "parse_student_record requires exactly three non-empty fields. All three "
        "return None on invalid input; the command-line application displays "
        "Invalid input. Signed integer credits retain the starter's behavior."
    )
    paragraph(
        "The three property tests generate Unicode text, None, integers, floats, "
        "bytes, lists, and dictionaries. They report any exception as a test "
        "failure. The 28 regression cases also check expected results so a "
        "function that always returns None cannot pass the whole suite."
    )
    paragraph(
        "Observed result: three fuzz properties failed on the original code; "
        "all 31 tests passed on the fixed code. The original parser is preserved "
        "from repository commit 71e1df4 for reproducible before/after evidence."
    )
    for key, title, log_name, caption in SECTIONS:
        story.append(PageBreak())
        paragraph(f"{key} - {title}", "Heading1")
        paragraph(caption)
        screenshot = ROOT / "screenshots" / f"{key}.png"
        if screenshot.is_file():
            picture = Image(str(screenshot))
            scale = min(480 / picture.imageWidth, 565 / picture.imageHeight)
            picture.drawWidth = picture.imageWidth * scale
            picture.drawHeight = picture.imageHeight * scale
            story.append(picture)
        else:
            paragraph("<b>Screenshot pending - captured output transcript below.</b>")
            content = (ROOT / "evidence" / log_name).read_text()
            lines = []
            for line in content.splitlines():
                lines.extend(wrap(line, 91, replace_whitespace=False,
                                  drop_whitespace=False) or [""])
            story.append(Preformatted("\n".join(lines), styles["RunOutput"]))

    story.append(PageBreak())
    paragraph("Reflections", "Heading1")
    paragraph(
        "The repository README requests three reflections, but the supplied "
        "handout does not list questions. These reflections address the observed "
        "bugs, the fixes, and the testing approach."
    )
    paragraph("1. What failures did fuzz testing reveal?", "Heading2")
    paragraph(
        "Hypothesis reduced failing inputs to small examples. An empty string "
        "caused ValueError in course-code unpacking and credit conversion, and "
        "IndexError in student-record parsing. None caused AttributeError when "
        "the functions called split. Byte strings also exposed TypeError where "
        "a string separator was used. A record containing only | still lacked "
        "the third field. These failures show that the parser relied on input "
        "shape and type without checking them."
    )
    paragraph("2. How were the functions hardened?", "Heading2")
    paragraph(
        "Each function first rejects non-string inputs. Course codes must match "
        "the documented department/number format. Credit conversion catches "
        "ValueError and rejects the whole list, including empty tokens. Student "
        "records must contain exactly three non-empty fields before indexing. "
        "Invalid data returns None, which is distinct from a valid zero-credit "
        "total. Existing case normalization and valid credit sums are preserved."
    )
    paragraph("3. What does fuzz testing add, and what are its limits?", "Heading2")
    paragraph(
        "Property-based tests explore many values beyond hand-picked examples "
        "and shrink failures into inputs that are easier to explain and replay. "
        "Regression tests complement this by checking exact valid outputs and "
        "known malformed cases. Passing a finite fuzz run does not prove that "
        "every possible object or arbitrarily large input is safe, nor does a "
        "no-crash property alone prove correctness. Domain rules such as credit "
        "limits or a list of allowed statuses need their own specification and tests."
    )

    def footer(canvas, doc):
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#526372"))
        canvas.drawString(48, 28, "PES1UG24CS666 | Harsha K | Lab 7")
        canvas.drawRightString(A4[0] - 48, 28, str(doc.page))

    SimpleDocTemplate(
        str(output), pagesize=A4, rightMargin=48, leftMargin=48,
        topMargin=45, bottomMargin=45, title="Lab 7 - Fuzz Testing",
        author="Harsha K",
    ).build(story, onFirstPage=footer, onLaterPages=footer)
    print(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", action="store_true")
    build(parser.parse_args().draft)
