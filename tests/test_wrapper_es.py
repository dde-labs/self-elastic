from src.wrapper import Es


def test_cat_health(es: Es):
    rs = es.cat_health(verbose=False)
    print(type(rs))
    print(rs.body)

    rs = es.cat_health(verbose=True)
    print(type(rs))
    print(rs.body)


def test_indices(es: Es):
    rs = es.indices('*', verbose=True)
    # rs = es.indices('home-*', verbose=True)
    print(type(rs))
    for r in rs.body:
        print(r)


def test_list_synonyms(es: Es):
    rs = es.list_synonyms()
    print(type(rs))
    print(rs)
