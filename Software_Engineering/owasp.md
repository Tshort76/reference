<div align="center">**OWASP Top 10**</div>
===

# Injection
An application is built to accept user input, presumably data, and execute some process using that data.  This can serve as an attack vector if the user can provide 'code as data', in which case the application will execute unintended code.

## Examples
An app retrieves invoices records for a certain date, which the user provides (e.g. date = X).  The app then plugs that value into a SQL Select statement:
`SELECT * from dbo.invoices WHERE user.hasAccess and date = X`.  An attacker can insert `2020-10-10 or 'a' = 'a'` and the WHERE clause becomes meaningless, allowing the attacker unauthorized access.  A user could also insert a DROP statement to wipe the data.

## Prevention
<dl>
  <dt>Input Validation</dt>
  <dd>Check that the input matches an expected form (e.g. use a regex)</dd>
  <dt>Prepared statements and stored procedures</dt>
  <dd>Limits the control that the user has to setting certain parameters</dd>
  <dt>Least Privilege</dt>
  <dd>Prefer access to views over tables, read-only over everything</dd>
</dl>

# Broken Authentication
<dl>
<dt>Brute force</dt>
<dd>Enumerate all permutations of possible characters, or use a heuristic (e.g. terms from dictionary)</dd>
<dt>Credential Stuffing</dt>
<dd>Use credentials from a data breach to attempt access to other sites (e.g. users repeat passwords)</dd>
<dt>Broken 'forgot password' logic</dt>
<dd>Enumerate all permutations of characters</dd>
</dl>

## Prevention
- Use complex passwords
- Store passwords with good encryption
- Multi-factor authentication

# Sensitive Data Exposure
Sensitive data is exposed to unauthorized persons.
## Prevention
- Categorize your data and set access controls accordingly
  - public, internal, confidential, restricted
- Limit the storage and flow of sensitive data to only what is necessary
- Use transport layer security and encryption

# XML External Entities (XXE)
A variant of an injection attack, an XXE attack can occur when a user is able to submit an XML entity to an XML parser.  A recursively defined entity could lead to an exponential growth in the entity's size, effectively rendering the server useless (Denial of service attack).

## Prevention 
- Input validation and White/black lists
- Disable XXE processing
- Upgrade to XML processors that do not have this vulnerability

# Broken Access Control
Authorization is not setup in a way that accurately enforces the desired access control scheme.

## Prevention
- Correctly setup access controls
  - Use roles and groups
- Log and alert
- Manual penetration testing

# Security Misconfiguration
Hardware often ships with simple default settings/values for security (e.g. admin/admin).  These values should be updated to more secure values.

## Prevention
- Correctly setup access controls
  - Use roles and groups
- Patch and update software
- Test your configurations

# Cross Site Scripting (XSS)
<dl>
<dt>Reflected Cross Site Scripting</dt>
<dd>A user clicks on a hyperlink that executes JS scripts within the browser</dd>
<dt>Stored Cross-Site Scripting</dt>
<dd>A user views a site, which stores cookies in their browser</dd>
</dl>

Cross-site script execution can result in the stealing of credentials (fake login page), the installation of keyloggers, and the defacement of websites.

## Prevention
<dl>
<dt>Content Secure Policy (CSP)</dt>
<dd>allows admins to whitelist content by domains</dd>
<dd>restricts media types</dd>
<dd>admins can whitelist domains that can run scripts</dd>
<dt>Context sensitive encoding</dt>
<dd>URL or HTML encode data to force that text is treated as data and not commands </dd>
<dt>Escape Untrusted HTTP</dt>
<dd>If you are putting the entity into a script tag, beware of injection attacks</dd>
</dl>

# Insecure Deserialization
Information can be injected into serialized object streams such that deserializing the stream produces a different object than what was originally serialized.

## Prevention
- Integrity checks
- Encrypt the serialized object
- Isolate deserialization code

# Using Components with Known Vulnerabilities
## Prevention
- Continuously perform:
  - Inventory checks on software components that are used
  - Monitor vulnerabilities sites for information on used components
- Virtual patch with a Web Application Firewall (WAF)

# Insufficient Logging and Monitoring
- Mean time between a breach and its detection is 197 days

## Prevention
- Log and monitor those logs

<div align="center">Sources</div>
===
- [Linked In Learning Path: Master the OWASP Top 10](https://www.linkedin.com/learning/learning-the-owasp-top-10?u=2095860)