# -*- coding: utf-8 -*-

from branca.element import Figure, JavascriptLink

from folium.map import Layer

from jinja2 import Template


class SideBySideLayers(Layer):
    """
    Creates a SideBySideLayers that takes two Layers and adds a sliding
    control with the leaflet-side-by-side plugin.

    Uses the Leaflet leaflet-side-by-side plugin https://github.com/digidem/leaflet-side-by-side

    Parameters
    ----------
    layer_left: Layer.
        The left Layer within the side by side control.
        Must  be created and added to the map before being passed to this class.
    layer_right: Layer.
        The left Layer within the side by side control.
        Must  be created and added to the map before being passed to this class.
    name : string, default None
        The name of the Layer, as it will appear in LayerControls.
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening (only for overlays).
    Examples
    --------
    >>> sidebyside = SideBySideLayers(layer_left, layer_right)
    >>> sidebyside.add_to(m)
    """

    _template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.control.sideBySide(
                {{ this.layer_left.get_name() }}, {{ this.layer_right.get_name() }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
        """)

    def __init__(self, layer_left, layer_right, name=None, overlay=True, control=True, show=True):
        super(SideBySideLayers, self).__init__(name=name,
                                               overlay=overlay,
                                               control=control,
                                               show=show)
        self._name = 'SideBySideLayers'
        self.layer_left = layer_left
        self.layer_right = layer_right

    def render(self, **kwargs):
        super(SideBySideLayers, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://raw.githack.com/digidem/leaflet-side-by-side/gh-pages/leaflet-side-by-side.js'),  # noqa
            name='leaflet.sidebyside')
