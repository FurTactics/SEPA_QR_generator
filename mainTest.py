import unittest

import main


class MyTestCase(unittest.TestCase):
    def test_get_default_data_elements(self):
        self.assertEqual(main.get_default_data_elements(),
                         {
                             "ServiceTag": "BCD",
                             "Version": "002",
                             "CharacterType": "1",
                             "IdentificationCode": "SCT",
                         }
                         )

    def test_construct_message(self):
        self.assertEqual(main.construct_message(main.get_default_data_elements()),
                         "BCD\n002\n1\nSCT"
                         )
        self.assertNotEqual(main.construct_message(main.get_default_data_elements()),
                            "BCD\n002\n1\nSCT\n"
                            )

    def test_throw(self):
        with self.assertRaises(ValueError):
            main.throw("Test")

    def test_full_data_elements(self):
        self.assertEqual(main.full_data_elements("COBADEFF850", "TU Dresden", "DE25 8504 0000 0800 4004 01",
                                                 "EUR100.12", "", "1234567 Familienname Vorname"),
                         {
                             "ServiceTag": "BCD",
                             "Version": "002",
                             "CharacterType": "1",
                             "IdentificationCode": "SCT",
                             "BIC": "COBADEFF850",
                             "BeneficiaryName": "TU Dresden",
                             "BeneficiaryIBAN": "DE25850400000800400401",
                             "AmountInEUR": "EUR100.12",
                             "Purpose": "",
                             "RemittanceInformationReference": "",
                             "RemittanceInformationUnstructured": "1234567 Familienname Vorname"
                         }
                         )


if __name__ == '__main__':
    unittest.main()
