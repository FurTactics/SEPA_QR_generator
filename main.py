import qrcode


def throw(message):
    raise ValueError(message)


def get_default_data_elements():
    return {
        "ServiceTag": "BCD",
        "Version": "002",
        "CharacterType": "1",
        "IdentificationCode": "SCT",
    }


def full_data_elements(bic, beneficiary_name, beneficiary_iban, amount_in_eur="", purpose="",
                       remittance_information=""):

    beneficiary_iban = beneficiary_iban.replace(" ", "")

    data_elements = get_default_data_elements()

    data_elements["BIC"] = bic if len(bic) <= 11 else throw(f"BIC must be 11 characters or less but was {len(bic)}")
    data_elements["BeneficiaryName"] = beneficiary_name if len(beneficiary_name) <= 70 else throw(f"Beneficiary name must be 70 characters or less but was {len(beneficiary_name)}")
    data_elements["BeneficiaryIBAN"] = beneficiary_iban if len(beneficiary_iban) <= 34 else throw(f"IBAN must be 34 characters or less but was {len(beneficiary_iban)}")
    data_elements["AmountInEUR"] = amount_in_eur if len(amount_in_eur) <= 12 and amount_in_eur.startswith("EUR") else throw(f"Amount must be 12 characters or less and start with EUR but was {amount_in_eur} with length {len(amount_in_eur)}")
    data_elements["Purpose"] = purpose if len(purpose) <= 4 else throw(f"Purpose must be 4 characters or less but was {len(purpose)}")
    data_elements["RemittanceInformationReference"] = remittance_information[:35] if remittance_information.startswith("RF") else ""
    data_elements["RemittanceInformationUnstructured"] = remittance_information[:140] if not remittance_information.startswith("RF") else ""
    return data_elements


def construct_message(data_elements):
    return "\n".join(data_elements.values()).strip()


def generate_qr(message):
    qr = qrcode.QRCode(
        version=6,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(message)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


if __name__ == "__main__":

    data_elements = full_data_elements(
        "COBADEFF850", "TU Dresden", "DE25 8504 0000 0800 4004 01",
        "EUR100.12", "", "1234567 Familienname Vorname"
    )

    data_elements = full_data_elements(
        "COBADEFF850", "TU Dresden", "DE25 8504 0000 0800 4004080 0800 4004 01",
        "EUR100.12", "", "RF1234567 Familienname Vorname"
    )

    message = construct_message(data_elements)
    print("__")
    print(message)
    print("__")
    img = generate_qr(message)
    img.save("qr.png")
