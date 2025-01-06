from src.wrapper import Es


def test_cat_health(es: Es):
    rs = es.cat_health(verbose=False)
    print(type(rs))
    print(rs)
    print(rs.body)

    rs = es.cat_health(verbose=True)
    print(type(rs))
    print(rs)
    print(rs.body)


def test_indices(es: Es):
    rs = es.indices('home-*', verbose=True)
    print(type(rs))
    print(rs)
    print(rs.body)
