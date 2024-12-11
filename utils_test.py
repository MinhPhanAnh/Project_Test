import pdfplumber

def clean_text(text):
    """Xử lý văn bản, loại bỏ ký tự không cần thiết."""
    text = text.replace("\n", " ")
    text = text.replace("-", " ")
    text = text.replace("\t", " ")
    text = " ".join(text.split(" "))
    return text.strip()

def chunk_by_token(text, max_len=1000):
    """Chia văn bản thành các đoạn nhỏ với số lượng từ tối đa là max_len."""
    words = clean_text(text).split(" ")
    chunks = []
    current_chunk = []
    current_len = 0
    for word in words:
        if current_len + len(word) + 1 > max_len:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_len = 0
        current_chunk.append(word)
        current_len += len(word) + 1
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def extract_text_from_pdf(file_path):
    """Trích xuất văn bản từ file PDF."""
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                # Sử dụng layout tốt hơn để giữ định dạng
                page_text = page.extract_text()
                if page_text:  # Kiểm tra nếu không rỗng
                    text += page_text + "\n"
            return clean_text(text)
    except Exception as e:
        raise ValueError(f"Lỗi khi xử lý file PDF: {e}")
