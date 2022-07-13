jwt_decoded_stub = {
  "user": {
    "unique_id": "40db7fee-6d60-4d73-824f-1bf87edc4491",
    "nick_name": "RAST3",
    "portfolios": {
      "br": {
        "bovespa_account": "000000014-6",
        "bmf_account": "14"
      },
      "us": {
        "dw_account": "89c69304-018a-40b7-be5b-2121c16e109e.1651525277006",
        "dw_display_account": "LX01000001"}
    }}}

find_one_stub = {
  "portfolios": {
    "default": {
      "us": {
        "dw_id": "89c69304-018a-40b7-be5b-2121c16e109e.1651525277006"
      }}}}

jwt_data_stub = {'is_payload_decoded': True, 'decoded_jwt': {'exp': 1687961421, 'created_at': 1656425421.60926, 'scope': {'view_type': 'default', 'user_level': 'client', 'features': ['default', 'realtime']}, 'user': {'unique_id': '40db7fee-6d60-4d73-824f-1bf87edc4491', 'nick_name': 'RAST3', 'portfolios': {'br': {'bovespa_account': '000000014-6', 'bmf_account': '14'}, 'us': {'dw_account': '89c69304-018a-40b7-be5b-2121c16e109e.1651525277006', 'dw_display_account': 'LX01000001'}}, 'client_has_br_trade_allowed': True, 'client_has_us_trade_allowed': True, 'client_profile': 'investor'}}, 'message': 'Jwt decoded'}
jwt_invalid = {'is_payload_decoded': False, 'decoded_jwt': {}}

jwt_to_decode_stub = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOiAxNjc2Njc0MTIwLCAiY3JlYX"


decoded_jwt_stub = {'created_at': 1656425421.60926,
 'exp': 1687961421,
 'scope': {'features': ['default', 'realtime'],
           'user_level': 'client',
           'view_type': 'default'},
 'user': {'client_has_br_trade_allowed': True,
          'client_has_us_trade_allowed': True,
          'client_profile': 'investor',
          'nick_name': 'RAST3',
          'portfolios': {'br': {'bmf_account': '14',
                                'bovespa_account': '000000014-6'},
                         'us': {'dw_account': '89c69304-018a-40b7-be5b-2121c16e109e.1651525277006',
                                'dw_display_account': 'LX01000001'}},
          'unique_id': '40db7fee-6d60-4d73-824f-1bf87edc4491'}}
