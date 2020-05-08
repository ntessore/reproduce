function link_field(name, link) {
    return Array.prototype.slice.call(document.querySelectorAll('dt'))
    .filter(function (dt) {
        return dt.textContent === name
    })
    .map(function (dt) {
        var dd = dt.nextElementSibling;
        var id = dd.textContent;
        var a = document.createElement('a');
        a.setAttribute('href', link(id))
        a.innerHTML = dd.innerHTML;
        dd.innerHTML = a.outerHTML;
        return dd;
    });
}

function link_doi(doi) {
    return 'https://dx.doi.org/' + doi;
}

function link_arXiv(id) {
    return 'https://arxiv.org/abs/' + id;
}

function link_bibcode(bibcode) {
    return 'https://ui.adsabs.harvard.edu/abs/' + bibcode + '/abstract';
}

document.addEventListener('DOMContentLoaded', function () {
    link_field('DOI', link_doi);
    link_field('arXiv', link_arXiv);
    link_field('Bibcode', link_bibcode);
});
