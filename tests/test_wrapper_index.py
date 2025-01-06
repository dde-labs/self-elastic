from src.wrapper import Es, Index


def test_get_mapping(es: Es):
    index: Index = es.index(name='home-product')
    rs = index.get_mapping()
    print(type(rs))
    print(rs)
    print(rs.body)


def test_get_setting(es: Es):
    index: Index = es.index(name='home-product')
    rs = index.get_setting()
    print(type(rs))
    print(rs)
    print(rs.body)


def test_count(es: Es):
    index: Index = es.index(name='home-product')
    rs: int = index.count()
    assert rs >= 0
    assert isinstance(rs, int)
