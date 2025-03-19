from src.wrapper import Es, Synonym


def test_synonym_get(es: Es):
    # synonym_name: str = "home-product-synonym"
    synonym_name: str = "tmp-home-product-synonym-set"
    synonym: Synonym = es.synonym(name=synonym_name)
    rs = synonym.get()
    print(type(rs))
    assert isinstance(rs.count, int)
    print(rs.synonyms_set)


def test_synonym_put(es: Es):
    synonym_name: str = "tmp-home-product-synonym-set"
    synonym: Synonym = es.synonym(name=synonym_name)
    rs = synonym.put(synonyms_set=[
        {"id": "1", "synonyms": "หลังคาไฟเบอร์ซีเมนต์, หลังคาลอนคู่"},
        {"id": "2", "synonyms": "กระเบื้องหลังคาคอนกรีต, หลัังคาโมเนีย"}
    ])
    print(type(rs))
    print(rs)


def test_synonym_rule_get(es: Es):
    synonym_name: str = "tmp-home-product-synonym-set"
    synonym: Synonym = es.synonym(name=synonym_name)
    rs = synonym.get_rule(rule_id='1')
    print(type(rs))
    print(rs)


def test_synonym_rule_put(es: Es):
    synonym_name: str = "tmp-home-product-synonym-set"
    synonym: Synonym = es.synonym(name=synonym_name)
    rs = synonym.put_rule(rule_id='1', synonyms="หลังคาไฟเบอร์ซีเมนต์, หลังคาลอนคี่")
    print(type(rs))
    print(rs)


def test_synonym_rule_delete(es: Es):
    synonym_name: str = "tmp-home-product-synonym-set"
    synonym: Synonym = es.synonym(name=synonym_name)
    rs = synonym.delete_rule(rule_id='1')
    print(type(rs))
    print(rs)


def test_synonym_delete(es: Es):
    synonym_name: str = "tmp-home-product-synonym-set"
    synonym: Synonym = es.synonym(name=synonym_name)
    rs = synonym.delete()
    assert rs.acknowledged


