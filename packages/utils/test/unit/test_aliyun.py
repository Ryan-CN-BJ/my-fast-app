from dotenv import load_dotenv
from pathlib import Path

test_env = Path(__file__).resolve().parent.parent.parent.parent.parent / ".env.test"
load_dotenv(test_env)

from utils.aliyun import generate_upload_params


class TestGenerateUploadCredentials:
    async def test_successful_credential_generation(self):

        result = await generate_upload_params("1.png")
        assert result["host"] == "http://test-mrj.oss-cn-beijing.aliyuncs.com"
        assert result["policy"] is not None
        assert result["signature"] is not None
        assert result["key"] is not None
