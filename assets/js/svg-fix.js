function getSvgMap() {
    const out = {};
    const sprite = document.getElementById("svg-map");
    const symbols = sprite.querySelectorAll('symbol[id]');
    const serializer = new XMLSerializer();

    symbols.forEach(sym => {
        const id = sym.getAttribute('id');
        const viewBox = sym.getAttribute('viewBox') || '';
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');

        Array.from(sym.attributes).forEach(attr => {
        if (attr.name !== 'id' && attr.name !== 'viewBox') {
            g.setAttribute(attr.name, attr.value);
        }
        });
        sym.childNodes.forEach(node => {
        g.appendChild(node.cloneNode(true));
        });

        const content = serializer.serializeToString(g);

        out[id] = {
        viewbox: viewBox,
        content: content.trim()
        };
    });

  return out;
}

// SVG map fix
(function() {
        const svgMap = getSvgMap();
        var allItems = document.querySelectorAll('use');

        for (var i = 0; i < allItems.length; i++) {
            var item = allItems[i];
            var anchor = item.getAttribute('xlink:href').split('#')[1];
            var itemData = svgMap[anchor];

            if(!itemData) {
                console.log('ANCHOR', anchor, i);
                continue;
            }

            var svgItem = item.parentNode;
            svgItem.innerHTML = itemData.content;
            svgItem.setAttribute('viewBox', itemData.viewbox);
        }
})();