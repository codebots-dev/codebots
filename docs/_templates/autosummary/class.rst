{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :exclude-members:
..    :members:
..    :inherited-members:

   {% block methods %}
   {% if methods %}
   .. rubric:: Methods

   .. autosummary::
      :toctree: methods/

   {% for item in methods %}
   {%- if not item.startswith('_') or item in ['__call__'] %}   {{ name }}.{{ item }}
   {% endif %}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: Properties

   .. autosummary::
      :toctree: attributes/

   {% for item in attributes %}
   {%- if not item.startswith('_') or item in ['__call__'] %}   {{ name }}.{{ item }}
   {% endif %}
   {%- endfor %}
   {% endif %}
   {% endblock %}
