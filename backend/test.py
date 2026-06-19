from utils.resume_parser import extract_text_from_pdf

text = extract_text_from_pdf("uploads/Mishita_Soni_Resume(4).pdf")

print("Length:", len(text))
print(text[:1000])