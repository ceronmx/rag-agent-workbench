import shutil
import subprocess
import sys


def check_command(cmd):
    return shutil.which(cmd) is not None


def check_python_magic():
    try:
        import magic

        magic.from_buffer("test")
        return True
    except ImportError:
        return False
    except Exception:
        return False


def main():
    print("--- Unstructured.io System Dependency Check ---")

    deps = {
        "tesseract": "Tesseract OCR (Required for images/scanned PDFs)",
        "pdftotext": "Poppler (Required for PDF processing)",
        "pandoc": "Pandoc (Required for various document conversions)",
    }

    missing = []

    for cmd, desc in deps.items():
        status = "INSTALLED" if check_command(cmd) else "MISSING"
        print(f"{cmd:12}: {status} ({desc})")
        if status == "MISSING":
            missing.append(cmd)

    # Special check for libmagic
    magic_status = "INSTALLED" if check_python_magic() else "MISSING"
    print(f"{'libmagic':12}: {magic_status} (File type detection)")
    if magic_status == "MISSING":
        missing.append("libmagic")

    if not missing:
        print("\n✅ All core system dependencies are installed!")
    else:
        print("\n❌ Some dependencies are missing. Please run:")
        brew_cmds = []
        if "libmagic" in missing:
            brew_cmds.append("libmagic")
        if "pdftotext" in missing:
            brew_cmds.append("poppler")
        if "tesseract" in missing:
            brew_cmds.append("tesseract")
        if "pandoc" in missing:
            brew_cmds.append("pandoc")

        print(f"brew install {' '.join(brew_cmds)}")
        print(
            "\nNote: You might also need 'libreoffice' for converting older .doc files."
        )


if __name__ == "__main__":
    main()
