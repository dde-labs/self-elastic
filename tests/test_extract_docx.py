from src.extract_docx import (
    extract_docx2xlm, extract_docx2images, extract_docx2txt
)


def test_extract_docx2xlm():
    rs = extract_docx2xlm('../data/source/DURA ONE V.2_230404.docx')
    print(rs)


def test_extract_docx2images():
    rs = extract_docx2images(
        '../data/source/DURA ONE V.2_230404.docx',
        '../data/target/dura_one_images'
    )
    print(rs)


def test_extract_docx2txt():
    rs = extract_docx2txt(
        '../data/source/DURA ONE V.2_230404.docx',
        img_dir='../data/target/dura_one_images',
    )
    print(rs)
