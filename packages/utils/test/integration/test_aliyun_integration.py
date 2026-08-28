import httpx
from dotenv import load_dotenv
from pathlib import Path
import os


from utils.aliyun import AliyunOSSConfig, AliyunOssUpload


class TestAliyunUpload:
    async def test_upload(self):
        ENV_FILE = Path(__file__).parent.parent.parent.parent.parent / ".env.test"
        load_dotenv(ENV_FILE)
        config = AliyunOSSConfig(
            OSS_ENDPOINT=os.environ.get("OSS_ENDPOINT"),
            OSS_REGION_ID=os.environ.get("OSS_REGION_ID"),
            OSS_ACCESS_KEY_ID=os.environ.get("OSS_ACCESS_KEY_ID"),
            OSS_ACCESS_KEY_SECRET=os.environ.get("OSS_ACCESS_KEY_SECRET"),
            OSS_BUCKET_NAME=os.environ.get("OSS_BUCKET_NAME"),
            OSS_STS_ROLE_ARN=os.environ.get("OSS_STS_ROLE_ARN"),
        )

        uploader = AliyunOssUpload(config=config, filename="1.png")

        cred = await uploader.generate_upload_params()

        IMAGE = Path(__file__).parent / "tiny.png"
        image_bytes = IMAGE.read_bytes()
        res = httpx.post(
            cred["host"],
            data={
                "success_action_status": "200",
                "policy": cred["policy"],
                "x-oss-signature-version": cred["x_oss_signature_version"],
                "x-oss-signature": cred["signature"],
                "x-oss-credential": cred["x_oss_credential"],
                "x-oss-date": cred["x_oss_date"],
                "key": cred["key"],
                "x-oss-security-token": cred["security_token"],
                "content-type": cred["content_type"],
            },
            files={"file": ("1.png", image_bytes, cred["content_type"])},
        )
        assert res.status_code == 200
