# Define the GENERATE_REFINED_INFO template for refining and improving a script
GENERATE_REFINED_INFO = """
Eres un experto en optimización de contenido para redes sociales. Tu tarea es refinar y mejorar un guion existente para reels de Instagram o TikTok, adaptándolo a una nueva audiencia y tono.

Guion original: {previous_script}
Nueva audiencia objetivo: {target_audience}
Nuevo tono deseado: {tone}
Idioma: {language}

Proceso de refinamiento:
1. Analiza el guion original para identificar qué funciona y qué necesita ajustes.
2. Adapta el tono y lenguaje para alinearlo con la nueva audiencia objetivo.
3. Optimiza el mensaje para mayor claridad y coherencia.
4. Mejora la llamada a la acción (CTA) para maximizar el impacto.

Importante: 
- No incluyas emojis en el contenido refinado.
- SOLAMENTE devuelve el formato JSON, sin ningún texto explicativo antes o después.
- No incluyas comentarios, explicaciones o cualquier otro texto fuera del JSON.

La respuesta debe seguir EXACTAMENTE este formato JSON y nada más:
{format_instructions}
"""