<h1 align="center">
  <br>
  <a href="https://github.com/s0md3v/Parth"><img src="https://i.ibb.co/n1m7fR2/parth.png" alt="Parth"></a>
  <br>
  Parth
  <br>
</h1>

<h4 align="center">Heuristic Vulnerable Parameter Scanner</h4>

<p align="center">
  <a href="https://github.com/s0md3v/Parth/releases">
    <img src="https://img.shields.io/github/release/s0md3v/Parth.svg">
  </a>
  <a href="https://github.com/s0md3v/Parth/issues?q=is%3Aissue+is%3Aclosed">
      <img src="https://img.shields.io/github/issues-closed-raw/s0md3v/Parth.svg">
  </a>
</p>

![demo](https://i.ibb.co/6wbY7fT/Screenshot-2020-08-19-22-17-19.png)

## Introduction
Some HTTP parameter names are more commonly associated with one functionality than the others. For example, the parameter `?url=` usually contains URLs as the value and hence often falls victim to file inclusion, open redirect and SSRF attacks. Parth can go through your burp history, a list of URLs or it's own disocovered URLs to find such parameter names and the risks commonly associated with them. Parth is designed to aid web security testing by helping in prioritization of components for testing.

## Usage
### Import targets from a file
This option works for all 3 supported import types: Burp Suite history, newline delimited text file or a HTTP request text file.
```
python3 parth.py -i example.history
```
### Find URLs for a domain
This option will make use of CommonCrawl, Open Threat Exchange and Waybackmachine to find URLs of the target domain.
```
python3 parth.py -t example.com
```
### Ignore duplicate parameter names
Same parameter names across all URLs are ignored.
```
python3 parth.py -ut example.com
```
### Save parameter names
This option will write all the parameter names found in a file with name `params-{target}.txt` for later use.
```
python3 parth.py -pt example.com
```
### JSON Output
The following command will save the result as a JSON object in the specified file.
```
python3 parth.py -t example.com -o example.json
```

## Credits
The database of parameter names and the risks associated with them is mainly created from the public work of various people of the community.
