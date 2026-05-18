from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_DIR = BASE_DIR / "sample_data"
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

pdf_content = b"%PDF-1.4\n1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] /Contents 4 0 R >> endobj\n4 0 obj << /Length 44 >> stream\nBT /F1 24 Tf 50 150 Td (Resume Placeholder) Tj ET\nendstream>> endobj\n5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\nxref\n0 6\n0000000000 65535 f \n0000000010 00000 n \n0000000053 00000 n \n0000000102 00000 n \n0000000177 00000 n \n0000000271 00000 n \ntrailer << /Size 6 /Root 1 0 R >>\nstartxref\n332\n%%EOF\n"
for name in ["sample_resume_1.pdf", "sample_resume_2.pdf"]:
    (SAMPLE_DIR / name).write_bytes(pdf_content)

png_path = BASE_DIR / "architecture.png"
png_path.write_bytes(bytes.fromhex(
    "89504E470D0A1A0A0000000D49484452000000010000000108060000001F15C4890000000A49444154789C636000000200010005FE02FEA57A120000000449454E44AE426082"
))
print("Sample assets created.")
