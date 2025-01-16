import os
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

from .__types import AnyPath
from .utils import IMAGE_EXT, is_image


NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def qn(tag):
    """Stands for 'qualified name', a utility function to turn a namespace
    prefixed tag name into a Clark-notation qualified tag name for lxml. For
    example, ``qn('p:cSld')`` returns ``'{http://schemas.../main}cSld'``.
    Source: https://github.com/python-openxml/python-docx/
    """
    prefix, tagroot = tag.split(':')
    uri = NSMAP[prefix]
    return f'{{{uri}}}{tagroot}'


def xml2text(xml):
    """
    A string representing the textual content of this run, with content
    child elements like ``<w:tab/>`` translated to their Python
    equivalent.
    Adapted from: https://github.com/python-openxml/python-docx/
    """
    text = u''
    root = ET.fromstring(xml)
    for child in root.iter():
        if child.tag == qn('w:t'):
            t_text = child.text
            text += t_text if t_text is not None else ''
        elif child.tag == qn('w:tab'):
            text += '\t'
        elif child.tag in (qn('w:br'), qn('w:cr')):
            text += '\n'
        elif child.tag == qn("w:p"):
            text += '\n\n'
    return text


def extract_images(filepath, destination) -> tuple[int, int]:
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


def extract_xlm_from_docx(file: AnyPath):
    """Extract image from docx file.

    refs: http://officeopenxml.com/
    """

    with zipfile.ZipFile(file) as docx:
        tree = ET.XML(docx.read('word/document.xml'))
        # print(tree)

    TEXT = qn('w:t')
    TABLE = qn('w:tbl')
    ROW = qn('w:tr')
    CELL = qn('w:tc')

    for table in tree.iter(TABLE):
        for row in table.iter(ROW):
            for cell in row.iter(CELL):
                print(''.join(node.text for node in cell.iter(TEXT)))

    IMAGE: str = qn('w:docPr')

    image: Element
    for image in tree.iter(IMAGE):
        print(image.attrib)
        print(image.items())
        print(image.text)
        print(image.tag)
        print(image.tail)


def extract_txt_from_docx(docx, img_dir=None):
    """
    ref: https://github.com/ankushshah89/python-docx2txt
    """
    text: bytes = u''

    # NOTE: Unzip the docx in memory
    zipf = zipfile.ZipFile(docx)
    filelist = zipf.namelist()

    # get header text
    # there can be 3 header files in the zip
    header_xmls = r'word/header\d*.xml'
    for fname in filelist:
        if re.match(header_xmls, fname):
            text += xml2text(zipf.read(fname))

    # get main text
    doc_xml = 'word/document.xml'
    text += xml2text(zipf.read(doc_xml))

    # get footer text
    # there can be 3 footer files in the zip
    footer_xmls = r'word/footer\d*.xml'
    for fname in filelist:
        if re.match(footer_xmls, fname):
            text += xml2text(zipf.read(fname))

    if img_dir is not None:
        # extract images
        for fname in filelist:

            _, extension = os.path.splitext(fname)

            if extension.lstrip(r'.') in IMAGE_EXT:

                dst_fname = os.path.join(img_dir, os.path.basename(fname))

                with open(dst_fname, "wb") as dst_f:
                    dst_f.write(zipf.read(fname))

    zipf.close()

    return text.strip()
