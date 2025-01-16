from pathlib import Path

from src.extract import extract_all2markdown
from memory_profiler import profile


@profile
def test_extract_all2markdown_pdf():
    extract_all2markdown(
        file=(
            "../data/source/"
            "[CIO Brief] CIO Old sGINII - Documentation.pdf"
        ),
        target='../data/target/cio_old_sginii.md',
    )


def test_extract_all2markdown_pptx():
    extract_all2markdown(
        file=(
            "../data/source/"
            "[BD Requirement] GINII 2.0 V.1.pptx"
        ),
        target='../data/target/bd_requirement_ginii_2_v1.md',
    )


def test_extract_all2markdown_xlsx():
    extract_all2markdown(
        file=(
            "../data/source/"
            "Home Online - Project Management.xlsx"
        ),
        target='../data/target/home_online_project_management.md',
    )


def test_extract_all2markdown_docx():
    extract_all2markdown(
        file=(
            "../data/source/"
            "Business Objectives of Revamping Data Management Platform.docx"
        ),
        target='../data/target/business_obj_of_revamping_dmp.md',
    )


def test_extract_all2markdown_docx_with_image():
    extract_all2markdown(
        file="../data/source/DURA ONE V.2_230404.docx",
        target='../data/target/dura_one_v2_230404.md',
    )


def test_extract_all2markdown_png():
    extract_all2markdown(
        file="../data/source/ginii_image.png",
        target='../data/target/ginii_image.md',
    )
