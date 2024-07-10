from jwcrypto import jwk


def generate_rsa_keys():
    key = jwk.JWK.generate(kty='RSA', size=2048)

    priv_pem = key.export_to_pem(private_key=True, password=None)
    pub_pem = key.export_to_pem()

    with open('private_key.pem', 'wb') as f:
        f.write(priv_pem)
    print("Chave privada salva em 'private_key.pem'")

    with open('public_key.pem', 'wb') as f:
        f.write(pub_pem)
    print("Chave pública salva em 'public_key.pem'")


if __name__ == '__main__':
    generate_rsa_keys()