---
title: SSL Certificates
---

## \*.api.gov.bc.ca

| Issue Date  | Expires     | Deployed    | SHA1 Fingerprint (abbrev.)                      | Serial No.   |
| ----------- | ----------- | ----------- | ----------------------------------------------- | ------------ |
| Oct 6 2020  | Oct 16 2021 | Oct 6 2020  | 20:7D:15:9D:42:BE:CC:BC:FD:EF:DF:13:77:C7:25:A3 | 7876EB597E14 |
| Feb 16 2021 | Oct 16 2021 | Feb 25 2021 | 4D:EA:CE:C4:0A:73:67:D3:B4:03:F6:63:C4:E1:67:2C | 3B5849D8A670 |
| Sep 27 2021 | Oct 16 2022 | Oct 6 2021  | E3:DF:EC:89:BC:03:9B:E9:7D:57:91:EB:52:18:59:46 | 1B588948FBB2 |
| Sep 28 2022 | Oct 16 2023 | Oct 2022    | 2D:E5:32:16:C6:0A:0D:F4:0C:1F:39:DD:BD:DD:A8:1A | 34A6625E5ECF |
| Oct 4 2023  | Oct 16 2024 | Oct 13 2023 | 52:78:CD:99:3C:00:4E:4F:57:CD:EF:71:B9:E2:53:08 | 74BC58EEA87E |
| Oct 1 2024  | Oct 16 2025 | Oct 04 2024 | CF:52:11:01:AF:97:6C:A4:B8:31:CD:1C:A6:C2:8C:53 | 00A9EEDE0318 |
| Sep 28 2025 | Oct 16 2026 | Oct 01 2025 | 20:4C:D5:79:D8:D3:75:42:26:54:09:F2:92:52:21:2D | B06689CC407B |

## Verification

If you would like to verify the SSL endpoint for `*.api.gov.bc.ca`, you can run the following two commands and compare the fingerprint and serial no.

```
export A_HOST=httpbin-regression.api.gov.bc.ca
openssl s_client -showcerts -verify 5 -connect 142.34.194.118:443 \
  -servername ${A_HOST} < /dev/null | awk '/BEGIN/,/END/{ if(/BEGIN/){a++}; print}' > gw.crt

openssl x509 -in gw.crt -fingerprint -serial -dates -noout

```

You can run the above as one line:

```
A_HOST=httpbin-regression.api.gov.bc.ca; openssl s_client -showcerts -verify 5 -connect ${A_HOST}:443 -servername ${A_HOST} < /dev/null | awk '/BEGIN/,/END/{ if(/BEGIN/){a++}; print}' | openssl x509 -fingerprint -serial -dates -noout
```

## Internal Notes

**Individual File Verification**

```
openssl x509 -in data-api-wildcard-2020.crt -fingerprint -serial -dates -noout
openssl x509 -in data-api-wildcard-2021.crt -fingerprint -serial -dates -noout
```

**Cert/Key Verification**

```
openssl x509 -noout -modulus -in data-api-wildcard.crt | openssl md5
openssl rsa -noout -modulus -in data-api-wildcard.key | openssl md5
```
