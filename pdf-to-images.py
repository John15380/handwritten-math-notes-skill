"""Convert PDF pages to high-resolution PNG images."""
import sys
import os
import fitz  # pymupdf

def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf-to-images.py <pdf_path> [output_dir] [dpi]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "/tmp/pdf_pages"
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 400

    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    print(f"Pages: {doc.page_count}")

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        out_path = os.path.join(out_dir, f"page_{i+1}.png")
        pix.save(out_path)
        print(f"  -> {out_path} ({pix.width}x{pix.height})")

    num_pages = doc.page_count
    doc.close()
    print(f"Done. {num_pages} pages saved to {out_dir}")

if __name__ == "__main__":
    main()
