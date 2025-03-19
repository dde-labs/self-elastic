from pathlib import Path

from src.wrapper import Es, Synonym


def test_synonym_get(es: Es, test_path: Path):
    synonym_name: str = "tmp-home-product-synonym-set"
    synonym: Synonym = es.synonym(name=synonym_name)
    rs = synonym.get()
    print(type(rs))
    print(rs)
    print(rs.body)

