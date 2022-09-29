decoded_jwt_stub = {
    "created_at": 1656425421.60926,
    "exp": 1687961421,
    "scope": {
        "features": ["default", "realtime"],
        "user_level": "client",
        "view_type": "default",
    },
    "user": {
        "client_has_br_trade_allowed": True,
        "client_has_us_trade_allowed": True,
        "client_profile": "investor",
        "nick_name": "RAST3",
        "portfolios": {
            "br": {"bmf_account": "14", "bovespa_account": "000000014-6"},
            "us": {
                "dw_account": "89c69304-018a-40b7-be5b-2121c16e109e.1651525277006",
                "dw_display_account": "LX01000001",
            },
        },
        "unique_id": "40db7fee-6d60-4d73-824f-1bf87edc4491",
    },
}

request_body_stub = {"w8_form_confirmation": "true"}

response_bytes_stub = (
    b'{"result": true, "message": "The W8 Form Was Updated Successfully", "success'
    b'": true, "code": 0}'
)
