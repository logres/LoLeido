from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_key_pair():
    # 生成私钥
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # 生成公钥
    public_key = private_key.public_key()

    # 将私钥和公钥以字节串形式返回
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return private_key_bytes, public_key_bytes


from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes


def generate_csr(
    private_key_bytes,
    common_name,
    country_name,
    state_name,
    locality_name,
    organization_name,
):
    # 加载私钥
    private_key = serialization.load_pem_private_key(private_key_bytes, password=None)

    # 生成证书请求
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization_name),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ]
    )

    builder = x509.CertificateSigningRequestBuilder().subject_name(subject)
    csr = builder.sign(private_key, hashes.SHA256())

    # 将CSR以字节串形式返回
    csr_bytes = csr.public_bytes(serialization.Encoding.PEM)

    return csr_bytes


from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime


def generate_self_signed_certificate(private_key_bytes, csr_bytes):
    # 加载私钥
    private_key = serialization.load_pem_private_key(private_key_bytes, password=None)

    # 加载CSR
    csr = x509.load_pem_x509_csr(csr_bytes)

    # 生成自签证书
    issuer = csr.subject
    cert = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(issuer)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        .sign(private_key, hashes.SHA256())
    )

    # 将证书以字节串形式返回
    cert_bytes = cert.public_bytes(serialization.Encoding.PEM)

    return cert_bytes

