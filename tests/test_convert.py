from src.convert import convert_simple
from memory_profiler import profile


@profile
def test_convert_simple_pdf():
    convert_simple(
        file=(
            "../data/source/"
            "[CIO Brief] CIO Old sGINII - Documentation.pdf"
        ),
        target='../data/target/cio_old_sginii.md',
    )


def test_convert_simple_pptx():
    convert_simple(
        file=(
            "../data/source/"
            "[BD Requirement] GINII 2.0 V.1.pptx"
        ),
        target='../data/target/bd_requirement_ginii_2_v1.md',
    )


def test_convert_simple_xlsx():
    convert_simple(
        file=(
            "../data/source/"
            "Home Online - Project Management.xlsx"
        ),
        target='../data/target/home_online_project_management.md',
    )


def test_convert_simple_docx():
    convert_simple(
        file=(
            "../data/source/"
            "Business Objectives of Revamping Data Management Platform.docx"
        ),
        target='../data/target/business_obj_of_revamping_dmp.md',
    )


def test_convert_simple_png():
    convert_simple(
        file="../data/source/ginii_image.png",
        target='../data/target/ginii_image.md',
    )
