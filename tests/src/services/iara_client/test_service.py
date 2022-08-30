# STANDARD IMPORTS
from unittest.mock import Mock, patch
import pytest
from iara_client import Iara

# PROJECT IMPORTS
from heimdall_client import Heimdall, HeimdallStatusResponses
from func.src.domain.exceptions.exceptions import ErrorLoggingOnIara
from func.src.services.iara_client.service import SendToIara

# STUBS
from tests.main_stub import decoded_jwt_stub
from tests.src.services.iara_client.stub_file import get_unique_id_from_jwt_payload


@pytest.mark.asyncio
@patch.object(Iara, "send_to_iara", return_value=[True, True])
@patch.object(Heimdall, "decode_payload", return_value=(decoded_jwt_stub, HeimdallStatusResponses.SUCCESS))
async def test_when_sending_right_params_then_return_none_which_is_the_expected(
        mock_send_to_iara,
        mock_decode_payload
):
    response = await SendToIara.register_user_w8_signature_log_on_persephone(
        jwt_data=Mock(return_value=get_unique_id_from_jwt_payload)
    )

    assert response is None


@pytest.mark.asyncio
@patch.object(Iara, "send_to_iara", return_value=[False, False])
@patch.object(Heimdall, "decode_payload", return_value=(decoded_jwt_stub, HeimdallStatusResponses.SUCCESS))
async def test_when_sending_right_params_then_return_but_not_sent_to_iara_then_raise_error_logging(
        mock_decode_payload,
        mock_send_to_iara
):
    with pytest.raises(Exception):
        await SendToIara.register_user_w8_signature_log_on_persephone(
            jwt_data=Mock(return_value=get_unique_id_from_jwt_payload)
        )
