
import os

from collections import defaultdict

from rfam_db import get_rfam_families



html_header = """
<html>
<head>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
<title>Rfam {rna_type} Secondary Structures</title>
</head>
<body>
<div class="container">
"""

html_footer = """
</div>
</body>
</html>
"""

html_index = """
<div class="row">
    <div class="col-md-12">
        <h1><a href="http://rfam.org">Rfam</a> {rna_type} secondary structures generated using <a href="http://eddylab.org/R-scape">R-scape</a></h1>

        <h2>Browse by RNA type</h2>
        <ul>
            <li><a href="HACA-box.html">HACA-box</a></li>
            <li><a href="antisense.html">antisense</a></li>
            <li><a href="antitoxin.html">antitoxin</a></li>
            <li><a href="CD-box.html">CD-box</a></li>
            <li><a href="Cis-reg.html">Cis-reg</a></li>
            <li><a href="CRISPR.html">CRISPR</a></li>
            <li><a href="frameshift_element.html">frameshift_element</a></li>
            <li><a href="Gene.html">Gene</a></li>
            <li><a href="Intron.html">Intron</a></li>
            <li><a href="IRES.html">IRES</a></li>
            <li><a href="leader.html">leader</a></li>
            <li><a href="lncRNA.html">lncRNA</a></li>
            <li><a href="miRNA.html">miRNA</a></li>
            <li><a href="riboswitch.html">riboswitch</a></li>
            <li><a href="ribozyme.html">ribozyme</a></li>
            <li><a href="rRNA.html">rRNA</a></li>
            <li><a href="scaRNA.html">scaRNA</a></li>
            <li><a href="snRNA.html">snRNA</a></li>
            <li><a href="splicing.html">splicing</a></li>
            <li><a href="sRNA.html">sRNA</a></li>
            <li><a href="thermoregulator.html">thermoregulator</a></li>
            <li><a href="tRNA.html">tRNA</a></li>
        </ul>
        <hr>
    </div>
</div>
"""

html_row = """
<div class="row">
    <div class="col-md-12">
        <h3>
            {rfam_acc}
            <small>
                <a href="http://rfam.org/family/{rfam_acc}" target="_blank">{rfam_id}</a>
            </small>
        </h3>
        <p>{description}</p>
        <a href="http://rfam.org/family/{rfam_acc}/image/rscape" target="_blank">
            <img class="img-thumbnail rounded col-md-5" src="http://rfam.org/family/{rfam_acc}/image/rscape" title="Current Rfam secondary structure fromm SEED alignment">
        </a>
        <a href="http://rfam.org/family/{rfam_acc}/image/rscape-cyk" target="_blank">
            <img class="img-thumbnail rounded col-md-5" src="http://rfam.org/family/{rfam_acc}/image/rscape-cyk" title="Predicted by R-scape">
        </a>
    </div>
</div>
"""


def get_rna_type(rna_type):
    rna_type = rna_type.strip()
    parts = rna_type.split('; ')
    output = parts[-1].replace(';', '')
    return output


def main():
    print('Retrieving data from the public Rfam database')
    data = defaultdict(list)
    for family in get_rfam_families():
        data[get_rna_type(family['type'])].append(family)

    for rna_type in data.keys():
        print('Generating {} pages'.format(rna_type))
        with open(os.path.join('docs', rna_type + '.html'), 'w') as f:
            f.write(html_header.format(rna_type=rna_type))
            f.write(html_index.format(rna_type=rna_type))
            for family in data[rna_type]:
                row = html_row.format(
                    rfam_acc=family['rfam_acc'],
                    description=family['description'],
                    rfam_id=family['rfam_id']
                )
                f.write(row)
            f.write(html_footer)

    with open(os.path.join('docs', 'index.html'), 'w') as f:
        f.write(html_header.format(rna_type=''))
        f.write(html_index.format(rna_type=''))
        f.write(html_footer)

    print('Done')


if __name__ == '__main__':
    main()
