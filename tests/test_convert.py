from src.convert import convert_simple


def test_convert_simple_pdf():
    convert_simple(
        file=(
            "../data/source/"
            "[CIO Brief] SCG CIO Old sGINII - Documentation.pdf"
        ),
        target='../data/target/scg_cio_old_sginii.md',
    )
