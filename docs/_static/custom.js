// Load jQuery from a CDN
var script = document.createElement('script');
script.src = 'https://code.jquery.com/jquery-3.6.0.min.js';
script.integrity = 'sha256-KyZXEAg3QhqLMpG8r+Knujsl5/6b2W3v0ZWkFqJ2V1w=';
script.crossOrigin = 'anonymous';
script.onload = function() {
    console.log('jQuery loaded');
    loadSphinxRtdTheme();
};
document.head.appendChild(script);

function loadSphinxRtdTheme() {
    var sphinxScript = document.createElement('script');
    sphinxScript.src = '_static/js/theme.js';
    sphinxScript.onload = function() {
        console.log('SphinxRtdTheme loaded');
    };
    document.head.appendChild(sphinxScript);
}
