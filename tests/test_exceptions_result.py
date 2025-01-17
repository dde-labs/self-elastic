from src.exceptions import ExceptionResult


def test_exception_result_500():
    except_rs = ExceptionResult(
        **{
            '_index': 'home-content-article',
            '_id': '1ff8a7b5dc7a7d1f0ed65aaa29c04b1e',
            'status': 500,
            'error': {
              'type': 'exception',
              'reason': 'Exception when running inference id [home-text-embedding-3-small-chunk100] on field [content]',
              'caused_by': {
                  'type': 'status_exception',
                  'reason': (
                      'Received a rate limit status code. Remaining tokens [unknown]. Remaining requests [272]. '
                      'for request from inference entity id [home-text-embedding-3-small-chunk100] status [429]. '
                      'Error message: [Requests to the Embeddings_Create Operation under Azure OpenAI API '
                      'version 2024-02-01 have exceeded call rate limit of your current OpenAI S0 pricing tier. '
                      'Please retry after 53 seconds. Please go here: https://aka.ms/oai/quotaincrease if you would '
                      'like to further increase the default rate limit.]'
                  )
              }
            }
        }
    )
    print(except_rs)


def test_exception_result_404():
    except_rs = ExceptionResult(
        **{
            "_index": "cap-product",
            "_id": "9bf5661ed2f646fae726a4dea06dfcda",
            "status": 404,
            "error": {
                "type": "resource_not_found_exception",
                "reason": "Inference id [cap-text-embedding-3-small-chunk50] not found for field [concat_display_name]",
                "suppressed": [
                    {
                        "type": "resource_not_found_exception",
                        "reason": (
                            "Inference id [cap-text-embedding-3-small-chunk50] not found for field [short_description]"
                        ),
                    }
                ],
            },
        }
    )
    print(except_rs)
