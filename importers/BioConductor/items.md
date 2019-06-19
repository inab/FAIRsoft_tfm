## DOI
By title:
<a title="DOI for use in publications, etc., will always redirect to current release version (or devel if package is not in release yet)." href="https://doi.org/doi:10.18129/B9.bioc.edge">10.18129/B9.bioc.edge</a>

<a> with title="DOI four use..."

## Extended name
<h2>

## Description
Second <p>

## Author
Third <p>
<p>Author: John D. Storey, Jeffrey T. Leek and Andrew J. Bass </p>

## Maintainer
Fourth <p>
<p>Maintainer: John D. Storey &lt;jstorey at princeton.edu&gt;, Andrew J. Bass &lt;ajbass at princeton.edu&gt; </p>

## Citation
In:
<div id="bioc_citation" class="bioc_citation">
<p>Storey JD, Leek JT, Bass AJ (2018).
<em>edge: Extraction of Differential Gene Expression</em>.
R package version 2.14.0, <a href="https://github.com/jdstorey/edge">https://github.com/jdstorey/edge</a>.
</p>
</div>
Title of papaer inside <em>
Notice that still inside this div, there might be a link

## Installation instructions

Below
<h3>Installation</h3>

<p>To install this package, start R (version
"3.5") and enter:
</p>
....



## Extract html between two tags:

This is the clear BeautifulSoup way, when the second h1 tag is a sibling of the first:

```
html = u""
for tag in soup.find("h1").next_siblings:
    if tag.name == "h1":
        break
    else:
        html += unicode(tag)
```
