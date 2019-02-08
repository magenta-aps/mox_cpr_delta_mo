import unittest

import mox_cpr_delta_mo.cpr_interface as cpr


GAF_response = """\
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
   <soap:Body>
      <ns3:GetAllFiltersResponse
        xmlns="http://serviceplatformen.dk/xml/schemas/InvocationContext/1/"
        xmlns:ns2="http://serviceplatformen.dk/xml/schemas/cpr/PNR/1/"
        xmlns:ns3="http://serviceplatformen.dk/xml/wsdl/soap11/CprSubscriptionService/1/">
         <ns3:MunicipalityCode>706</ns3:MunicipalityCode>
         <ns2:PNR>0123456789</ns2:PNR>
         <ns2:PNR>0123456788</ns2:PNR>
         <ns3:noFilter>false</ns3:noFilter>
      </ns3:GetAllFiltersResponse>
   </soap:Body>
</soap:Envelope>"""

GAF_response_empty = """\
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
   <soap:Body>
      <ns3:GetAllFiltersResponse
        xmlns="http://serviceplatformen.dk/xml/schemas/InvocationContext/1/"
        xmlns:ns2="http://serviceplatformen.dk/xml/schemas/cpr/PNR/1/"
        xmlns:ns3="http://serviceplatformen.dk/xml/wsdl/soap11/CprSubscriptionService/1/">
         <ns3:MunicipalityCode>706</ns3:MunicipalityCode>
         <ns3:noFilter>false</ns3:noFilter>
      </ns3:GetAllFiltersResponse>
   </soap:Body>
</soap:Envelope>"""


class TestCprInterface(unittest.TestCase):
    def test_cpr_get_all_subscribed(self):
        cpr.pnr_all_subscribed = (
            lambda dependencies_dict, operation: GAF_response
        )
        self.assertEqual(
            cpr.cpr_get_all_subscribed(),
            ["0123456789", "0123456788"]
        )

    def test_empty_cpr_get_all_subscribed(self):
        cpr.pnr_all_subscribed = (
            lambda dependencies_dict, operation: GAF_response_empty
        )
        self.assertEqual(cpr.cpr_get_all_subscribed(), [])
