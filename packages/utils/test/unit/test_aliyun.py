from dotenv import load_dotenv
from pathlib import Path
import os

test_env = Path(__file__).resolve().parent.parent.parent.parent.parent / ".env.test"
load_dotenv(test_env)

from utils.aliyun import AliyunOSSConfig, AliyunOssUpload


class TestGenerateUploadCredentials:
    async def test_successful_credential_generation(self):

        config = AliyunOSSConfig(
            OSS_ENDPOINT=os.environ.get("OSS_ENDPOINT"),
            OSS_REGION_ID=os.environ.get("OSS_REGION_ID"),
            OSS_ACCESS_KEY_ID=os.environ.get("OSS_ACCESS_KEY_ID"),
            OSS_ACCESS_KEY_SECRET=os.environ.get("OSS_ACCESS_KEY_SECRET"),
            OSS_BUCKET_NAME=os.environ.get("OSS_BUCKET_NAME"),
            OSS_STS_ROLE_ARN=os.environ.get("OSS_STS_ROLE_ARN"),
        )

        uploader = AliyunOssUpload(config=config, filename="1.png")

        result = await uploader.generate_upload_params()
        assert result["host"] == "http://test-mrj.oss-cn-beijing.aliyuncs.com"
        assert result["policy"] is not None
        assert result["signature"] is not None
        assert result["key"] is not None
