"""File-type reference tables and detection helpers for the malware scanner."""

DANGEROUS_EXTENSIONS = {
    "exe", "scr", "bat", "cmd", "com", "pif", "vbs", "vbe", "js", "jse",
    "wsf", "wsh", "ps1", "psm1", "jar", "msi", "dll", "hta", "reg",
}

CAUTION_EXTENSIONS = {"zip", "rar", "7z", "docm", "xlsm", "pptm", "iso", "lnk"}

# (magic bytes, description, extensions it's expected to appear under)
SIGNATURES = [
    (b"MZ", "Windows PE executable", {"exe", "dll", "scr", "com", "sys"}),
    (b"\x7fELF", "Linux ELF executable", {"elf", "bin", "out", ""}),
    (b"PK\x03\x04", "ZIP-based archive (zip/docx/jar/apk...)",
     {"zip", "docx", "xlsx", "pptx", "jar", "apk", "docm", "xlsm", "pptm"}),
    (b"%PDF", "PDF document", {"pdf"}),
    (b"\x89PNG", "PNG image", {"png"}),
    (b"\xff\xd8\xff", "JPEG image", {"jpg", "jpeg"}),
    (b"GIF8", "GIF image", {"gif"}),
    (b"Rar!", "RAR archive", {"rar"}),
]


def get_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def detect_signature(data: bytes):
    """Return (description, expected_extensions) for the first matching signature, or (None, None)."""
    for magic, desc, exts in SIGNATURES:
        if data.startswith(magic):
            return desc, exts
    return None, None


def format_bytes(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 ** 2:
        return f"{n / 1024:.1f} KB"
    return f"{n / 1024 ** 2:.2f} MB"
