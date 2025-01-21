import os
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from typing import Optional

from .__types import AnyPath
from .utils import IMAGE_EXT, is_image


NAMESPACE_MAP: dict[str, str] = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
}


def qn(tag) -> str:
    """Stands for 'qualified name', a utility function to turn a namespace
    prefixed tag name into a Clark-notation qualified tag name for lxml.

    Examples:

        >>> qn('m:cSld')
        '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}cSld'

    Source: https://github.com/python-openxml/python-docx/

    :rtype: str
    """
    prefix, tag_root = tag.split(':')
    uri: str = NAMESPACE_MAP[prefix]
    return f'{{{uri}}}{tag_root}'


def xml2text(xml) -> str:
    """A string representing the textual content of this run, with content
    child elements like ``<w:tab/>`` translated to their Python
    equivalent.

    Adapted from: https://github.com/python-openxml/python-docx/

    :rtype: str
    """
    text: str = ''
    root = ET.fromstring(xml)
    for child in root.iter():

        # NOTE: Text
        if child.tag == qn('w:t'):
            t_text = child.text
            text += t_text if t_text is not None else ''

        # NOTE: Tab
        elif child.tag == qn('w:tab'):
            text += '\t'

        # NOTE: Newline
        elif child.tag in (qn('w:br'), qn('w:cr')):
            text += '\n'

        # NOTE: Page
        elif child.tag == qn("w:p"):
            text += '\n\n'

    return text


def extract_docx2images(filepath, destination) -> tuple[int, int]:
    """Extract images from a docx file format."""

    overall_size: int = 0

    with tempfile.TemporaryDirectory() as working_dir:
        print(
            'Created temporal working directory {}'.format(working_dir))

        # Unzips the images
        with ZipFile(filepath) as working_zip:
            image_list = [
                name for name in working_zip.namelist() if is_image(name)
            ]
            for x in image_list:
                overall_size: int = (
                    overall_size + working_zip.getinfo(x).file_size
                )

            file_count = len(image_list)
            working_zip.extractall(working_dir, image_list)

        print('Extracted {} images'.format(file_count))

        # Copies the extracted images to destination directory
        for x in image_list:
            if not Path(destination).exists():
                Path(destination).mkdir(parents=True)

            shutil.copy(Path(working_dir).resolve() / x, destination)
            print(f'Copied {x}')
        print(f'Copied all image files to {Path(destination).resolve()}')

    return file_count, overall_size


def extract_docx2xlm(file: AnyPath):
    """Extract image from docx file.

    refs: http://officeopenxml.com/
    """

    with zipfile.ZipFile(file) as docx:
        tree = ET.XML(docx.read('word/document.xml'))
        # print(tree)

    text = qn('w:t')
    table = qn('w:tbl')
    row = qn('w:tr')
    cell = qn('w:tc')

    for table in tree.iter(table):
        for row in table.iter(row):
            for cell in row.iter(cell):
                print(''.join(node.text for node in cell.iter(text)))

    image: str = qn('w:docPr')

    img: Element
    for img in tree.iter(image):
        print(img.attrib)
        print(img.items())
        print(img.text)
        print(img.tag)
        print(img.tail)


def extract_docx2txt(docx, img_dir: Optional[str] = None) -> str:
    """Extract text from docx

    ref: https://github.com/ankushshah89/python-docx2txt
    """
    text: str = ''

    # NOTE: Unzip the docx in memory
    zip_file: ZipFile = zipfile.ZipFile(docx)
    filelist: list = zip_file.namelist()

    # NOTE: Get header text there can be 3 header files in the zip
    for filename in filelist:
        if re.match(r'word/header\d*.xml', filename):
            text += xml2text(zip_file.read(filename))

    # NOTE: Fet main text
    text += xml2text(zip_file.read('word/document.xml'))

    # NOTE: Get footer text there can be 3 footer files in the zip
    for filename in filelist:
        if re.match(r'word/footer\d*.xml', filename):
            text += xml2text(zip_file.read(filename))

    if img_dir is not None:

        for filename in filelist:

            _, extension = os.path.splitext(filename)

            if extension.lstrip(r'.') in IMAGE_EXT:

                dst_filename = os.path.join(img_dir, os.path.basename(filename))

                with open(dst_filename, "wb") as dst_f:
                    dst_f.write(zip_file.read(filename))

    zip_file.close()

    return text.strip()
