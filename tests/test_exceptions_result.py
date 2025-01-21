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
                    },
                ],
            },
        }
    )
    print(except_rs)


def test_exception_result_400():
    except_rs = ExceptionResult(
        **{
            '_index': 'tmp-korawica-home-product',
            '_id': '1',
            'status': 400,
            'error': {
                'type': 'document_parsing_exception',
                'reason': "[1:56] failed to parse field [height_number] of type [float] in document with id '1'. Preview of field's value: 'very height'",
                'caused_by': {
                    'type': 'number_format_exception',
                    'reason': 'For input string: "very height"'
                },
            },
        },
    )
    print(except_rs)


def test_exception_result_400():
    # [
    #     {
    #         'index': {
    #             'error': "BadRequestError(400, 'action_request_validation_exception', 'Validation Failed: 1: index is missing;')",
    #             'status': 400,
    #             'exception': BadRequestError(
    #                 'action_request_validation_exception',
    #                 meta=ApiResponseMeta(
    #                 status=400,
    #                 http_version='1.1',
    #                 headers={
    #                     'Content-Encoding': 'gzip',
    #                     'Content-Length': '144',
    #                     'Content-Type': 'application/vnd.elasticsearch+json;compatible-with=8',
    #                     'X-Cloud-Request-Id': 'me-H5pdeQDSHfTMzk-Q_uA',
    #                     'X-Elastic-Product': 'Elasticsearch',
    #                     'X-Found-Handling-Cluster': '17afea6b4e0b41f096fe89e66ff54a1c',
    #                     'X-Found-Handling-Instance': 'instance-0000000002',
    #                     'Date': 'Tue, 21 Jan 2025 11:45:10 GMT'},
    #                 duration=0.03972673416137695,
    #                 node=NodeConfig(
    #                     scheme='https',
    #                     host='17afea6b4e0b41f096fe89e66ff54a1c.ap-southeast-1.aws.found.io',
    #                     port=443,
    #                     path_prefix='',
    #                     headers={
    #                         'user-agent': 'elasticsearch-py/8.15.1 (Python/3.11.9; elastic-transport/8.15.1)'},
    #                     connections_per_node=10,
    #                     request_timeout=10.0,
    #                     http_compress=True,
    #                     verify_certs=True,
    #                     ca_certs=None,
    #                     client_cert=None,
    #                     client_key=None,
    #                     ssl_assert_hostname=None,
    #                     ssl_assert_fingerprint=None,
    #                     ssl_version=None,
    #                     ssl_context=None,
    #                     ssl_show_warn=True,
    #                     _extras={})),
    #                     body={
    #                         'error': {
    #                             'root_cause': [
    #                                 {
    #                                     'type': 'action_request_validation_exception',
    #                                     'reason': 'Validation Failed: 1: index is missing;'
    #                                 }
    #                             ],
    #                                 'type': 'action_request_validation_exception',
    #                                 'reason': 'Validation Failed: 1: index is missing;'
    #                         },
    #                         'status': 400
    #                     }
    #             ),
    #             'data': {
    #                 'index': 'tmp-korawica-home-product',
    #                 'barcode': '10001',
    #                 'cms_id': 'cms10001', 'height_number': 1.12, 'article_id': 1,
    #                 'upload_date': '2025-01-01'
    #             },
    #             '_id': '1'
    #         }
    #     }
    # ]
    ...
