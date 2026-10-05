# Council of Architecture (CoA) Directory Investigation

## 1. Target Website

Council of Architecture (CoA) public architect directory:

https://coa.gov.in/search_arch.php?lang=1&level=1&linkid=&lid=289&lang=1

The purpose of the investigation was to understand how the public architect directory works and identify the legitimate data-access mechanism before building the extraction pipeline.

---

## 2. Search Form Investigation

The directory provides a search form for finding architects.

The search can be performed using architect-related information such as the architect name.

During investigation, a manual search was performed using:

**Search term:** Amol

The website generated a result page containing architect records.

---

## 3. Network Request Investigation

The website was investigated using browser network requests.

A request was identified for retrieving architect search results.

### Result endpoint

`https://coa.gov.in/search_architectResult.php?lang=1&level=1&linkid=&lid=289`

The request method observed was:

**POST**

Example parameters observed during the investigation:

```text
val_sub=1
searCat=1
arc_name=Amol
m_name=
l_name=
cap_code=ycEz74
T3=ycEz74
submit=Search
```

The CAPTCHA-related values were observed as part of the normal website request.

The pipeline does not attempt to bypass or defeat the CAPTCHA.

---

## 4. Response Investigation

The architect search request returned a normal HTML document.

The result was not observed as a JSON API response.

The final result page was saved locally as:

```text
data/coa_search_results.html
```

The saved HTML was then parsed using BeautifulSoup.

---

## 5. Data Fields Identified

The publicly displayed result table contained the following fields:

* S.No
* Architect Name
* Registration Number
* Disciplinary Action
* Address
* Mobile
* Email ID

Example result:

```text
Architect Name:
Mr. Amol Arvind Chaphalkar

Registration Number:
CA/1990/13290

Disciplinary Action:
No

Mobile:
9422457875

Email:
a.chaphalkar@rediffmail.com
```

---

## 6. Registration Number Structure

The observed registration numbers follow a pattern similar to:

```text
CA/YYYY/NUMBER
```

Examples observed:

```text
CA/1990/13290
CA/2005/36698
CA/2014/64140
```

The year portion appears to represent the registration year.

However, the investigation does not assume that the complete registration number sequence is predictable or that every possible registration number is valid.

Further investigation is required before using registration numbers for record discovery.

---

## 7. Current Extraction Result

For the test search term `Amol`, 3 publicly displayed architect records were extracted.

The extracted data was saved to:

```text
data/architect_results.csv
```

Current records:

```text
3
```

The CSV contains:

* Architect Name
* Registration Number
* Disciplinary Action
* Address
* Mobile
* Email ID

---

## 8. Access Restrictions

The result page indicates that further records require login and purchase of an online directory.

The website also uses CAPTCHA/security verification during the search process.

The extraction system will not attempt to bypass:

* CAPTCHA
* Login requirements
* Subscription restrictions
* Purchase restrictions
* Other security controls

Only data that can be legitimately accessed through the public interface will be processed.

---

## 9. Current Extraction Approach

The current proof-of-concept pipeline is:

```text
COA Website
     |
     v
Manual Search
     |
     v
Search Result HTML
     |
     v
coa_search_results.html
     |
     v
BeautifulSoup Extraction
     |
     v
architect_results.csv
     |
     v
SQLite Database
     |
     v
coa_architects.db
```

---

## 10. Database

A SQLite database has been created:

```text
data/coa_architects.db
```

The database currently contains 3 architect records.

Duplicate registration numbers are protected using a unique database constraint.

The pipeline uses `INSERT OR IGNORE` so that an already stored registration number is not inserted again.

---

## 11. Current Limitations

The current implementation is a proof of concept.

The following features still need to be implemented:

* Registration/architect ID investigation
* Additional field extraction
* Address normalization
* City extraction
* State extraction
* Pincode extraction
* Registration status extraction where available
* CAPTCHA detection and manual-verification pause
* Processing status tracking
* Failed-record tracking
* Resume capability
* Extraction speed measurement
* Progress dashboard
* Data quality validation
* Final dataset statistics
* Technical documentation
* Demonstration workflow

---

## 12. Compliance Approach

The extraction system is designed to respect the access restrictions of the website.

The system will:

1. Use the public website interface.
2. Record the legitimate requests observed during investigation.
3. Detect security verification requirements.
4. Pause when manual verification is required.
5. Allow the operator to complete permitted verification manually.
6. Continue only when access is available.
7. Avoid excessive request rates.
8. Store successful records immediately.
9. Track failures so that they can be retried later.
10. Preserve source values for traceability.

The system will not attempt to defeat CAPTCHA, authentication, subscription controls, or other security mechanisms.

