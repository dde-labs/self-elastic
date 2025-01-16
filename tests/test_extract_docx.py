from src.extract_docx import (
    extract_xlm_from_docx, extract_images, extract_txt_from_docx
)


def test_extract_xlm_from_docx():
    extract_xlm_from_docx('../data/source/DURA ONE V.2_230404.docx')


def test_extract_images():
    rs = extract_images(
        '../data/source/DURA ONE V.2_230404.docx',
        '../data/target/dura_one_images'
    )
    print(rs)


def test_process():
    rs = extract_txt_from_docx(
        '../data/source/DURA ONE V.2_230404.docx',
        img_dir='../data/target/dura_one_images',
    )
    print(rs)
