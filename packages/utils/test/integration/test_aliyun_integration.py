import httpx
from dotenv import load_dotenv
from pathlib import Path
import base64

ENV_FILE = Path(__file__).parent.parent.parent.parent.parent / ".env.test"
load_dotenv(ENV_FILE)

from utils.aliyun import generate_upload_params


class TestAliyunUpload:
    async def test_upload(self):
        cred = await generate_upload_params("1.png")

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
