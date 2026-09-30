"""El dataset de entrenamiento: reseñas cortas en español, etiquetadas a mano.

Pequeño a propósito — cabe en un archivo que puedes leer completo y entender
exactamente de qué aprendió el modelo.

Un detalle que importa más de lo que parece: el vocabulario se REPITE. Palabras
como "excelente", "recomiendo", "pésimo" o "porquería" aparecen en varias
frases distintas. Con datasets chicos eso es lo que hace la diferencia entre un
modelo que aprende y uno que adivina: si cada frase usara palabras únicas, una
frase nueva no tendría nada en común con lo que el modelo vio, y quedaría en
50% — igual que lanzar una moneda.
"""

POSITIVOS = [
    # excelente / buenísimo / bueno
    "Excelente servicio, muy recomendado",
    "Excelente calidad, quedé muy contento",
    "Excelente atención de todo el personal",
    "Un producto excelente por muy buen precio",
    "El curso es excelente, muy bien explicado",
    "Buenísimo, superó todas mis expectativas",
    "Buenísimo el servicio, muy rápido",
    "Muy bueno, lo recomiendo sin dudar",
    "Muy buena calidad y muy buen precio",
    "Buena atención y buen producto",
    "Qué buena experiencia, volveré pronto",
    "Todo muy bueno, cero quejas",
    # encantó / encanta / amo
    "Me encantó este curso",
    "Me encantó el producto, llegó perfecto",
    "Me encantó la atención, muy amables",
    "Me encanta, es justo lo que buscaba",
    "Me encanta la calidad de los materiales",
    "Lo amo, mejor de lo que esperaba",
    "Amo este lugar, siempre vuelvo",
    "Me fascinó, quedé encantada",
    "Quedé encantado con el resultado",
    # perfecto / impecable
    "Funciona perfecto, justo lo que necesitaba",
    "Todo perfecto, llegó antes de lo previsto",
    "Perfecto, no tengo ninguna queja",
    "El producto llegó en perfecto estado",
    "Perfecto para lo que lo necesitaba",
    "Un servicio impecable de principio a fin",
    "La app funciona de forma impecable",
    "Impecable la presentación del producto",
    # recomiendo
    "Lo recomiendo totalmente, muy bueno",
    "Recomiendo este lugar, excelente atención",
    "Recomiendo el curso, aprendí muchísimo",
    "Totalmente recomendado, muy buena calidad",
    "Muy recomendado, vale cada peso",
    "Se lo recomiendo a todo el mundo",
    # increíble / maravilloso / genial / espectacular / fantástico
    "Increíble atención al cliente",
    "Increíble calidad por ese precio",
    "Una experiencia increíble, muy feliz",
    "Maravilloso, mejor de lo que imaginaba",
    "Una experiencia maravillosa de principio a fin",
    "Genial todo, muy contento con la compra",
    "Qué genial servicio, muy rápidos",
    "Espectacular, superó mis expectativas",
    "El lugar es espectacular y muy limpio",
    "Fantástico, sin una sola queja",
    "Fantástica la atención, muy amables",
    # rápido / puntual / eficiente
    "Servicio rápido y muy eficiente",
    "Llegó rápido y muy bien empacado",
    "Muy rápido, resolvieron todo al instante",
    "Envío puntual y producto perfecto",
    "Rápido, sencillo y muy efectivo",
    "Atención inmediata, muy eficientes",
    # amable / atento / servicial
    "Personal muy amable y atento",
    "Muy amables todos, excelente trato",
    "El personal es muy atento y servicial",
    "Nos trataron muy bien, muy amables",
    "Atención muy amable y profesional",
    # limpio / cómodo / bonito / hermoso
    "El hotel estaba muy limpio y cómodo",
    "Todo muy limpio y muy bien cuidado",
    "Súper cómodo y muy bonito",
    "La habitación era cómoda y limpia",
    "Diseño hermoso y muy fácil de usar",
    "Un lugar hermoso, muy agradable",
    "Muy agradable el ambiente, volveré",
    # delicioso / rico
    "La comida estaba deliciosa",
    "Delicioso todo, volveré pronto",
    "Comida muy rica y buena atención",
    "Qué rico, el mejor restaurante de la ciudad",
    # útil / claro / práctico / completo
    "Muy útil y muy bien explicado",
    "Me ayudó bastante, muy útil el material",
    "Explicaciones muy claras y útiles",
    "Todo muy claro y bien organizado",
    "Curso completo y muy práctico",
    "Contenido práctico y de mucha calidad",
    "Material muy completo y muy claro",
    # feliz / contento / satisfecho
    "Estoy muy feliz con mi compra",
    "Feliz con el resultado, todo perfecto",
    "Muy contento, cumplieron con todo",
    "Quedé muy satisfecho con el servicio",
    "Muy satisfecha, lo volvería a comprar",
    # mejor / superó / vale la pena
    "El mejor servicio que he recibido",
    "La mejor decisión que tomé, muy bueno",
    "Simplemente lo mejor, muy recomendado",
    "Superó mis expectativas por completo",
    "Vale totalmente la pena, muy buena calidad",
    "Vale cada peso, excelente producto",
    # barato / buen precio
    "Muy barato y de muy buena calidad",
    "Buen precio para tan buena calidad",
    "Excelente precio, muy contento",
    # cumplió / resolvió
    "Cumplió con todo lo prometido",
    "Cumplieron perfecto, muy buen servicio",
    "Resolvieron mi problema al instante",
    "Resolvieron todo muy rápido y muy amables",
    # varios
    "Producto original y muy bien presentado",
    "Un trabajo excelente, felicitaciones",
    "Muy profesional todo el equipo",
    "Aprendí muchísimo, muy buen curso",
    "Gran experiencia, la repetiría",
    "Me sorprendió gratamente, muy bueno",
    "Sin quejas, todo salió genial",
    "Volvería a comprar sin dudarlo",
    "Buen producto, buena atención, todo bien",
    "Todo bien, muy conforme con la compra",
    "Increíblemente bueno, muy recomendado",
    "Muy bien, gracias por todo",
]

NEGATIVOS = [
    # terrible / horrible / espantoso / fatal
    "Terrible experiencia, no lo recomiendo",
    "Terrible atención, muy groseros",
    "Terrible servicio, me dejaron esperando",
    "Horrible, nunca más compro aquí",
    "Horrible la atención, muy mala",
    "Horrible calidad, no lo compren",
    "Espantoso, cero estrellas",
    "Espantosa la comida, muy fría",
    "Fatal el servicio, pedí un reembolso",
    "Fatal, no funciona nada",
    # pésimo / malo / malísimo / peor
    "Pésima calidad, se dañó al segundo día",
    "Pésimo servicio, no respondieron nunca",
    "Pésima atención, muy malos",
    "Muy mala atención, muy groseros",
    "Muy mala calidad y muy caro",
    "Mala experiencia, no lo recomiendo",
    "Mal servicio y peor producto",
    "Todo muy mal, no lo compren",
    "Malísimo, muy mal hecho",
    "Malísima calidad, llegó roto",
    "Lo peor que he probado",
    "Lo peor, una pérdida de tiempo",
    "Peor imposible, muy decepcionado",
    # porquería / basura / desastre
    "Qué porquería de servicio",
    "Una porquería, no sirve para nada",
    "Es una porquería, pésima calidad",
    "Pura basura, perdí mi dinero",
    "Es basura, muy mala calidad",
    "Un desastre total, evítenlo",
    "Un desastre, todo salió mal",
    "Fue un desastre la atención",
    # decepción / decepcionado / arrepiento
    "Decepción absoluta, muy malo",
    "Qué decepción, esperaba mucho más",
    "Muy decepcionado con la compra",
    "Muy decepcionada, no lo recomiendo",
    "Me arrepiento de haberlo comprado",
    "Me arrepiento, fue una mala decisión",
    # estafa / falso / no cumplieron
    "Es una estafa, tengan mucho cuidado",
    "Una estafa total, no compren aquí",
    "Producto falso, no es original",
    "Es falso y de muy mala calidad",
    "No cumplieron con nada de lo prometido",
    "Prometen mucho y cumplen muy poco",
    "Cobran y no entregan, una estafa",
    "Cobraron más de lo acordado",
    # roto / defectuoso / incompleto / se dañó
    "El producto llegó roto y sucio",
    "Llegó roto, muy mal empacado",
    "Vino defectuoso, no funciona",
    "Producto defectuoso y mala atención",
    "Llegó incompleto, faltaban piezas",
    "Se me rompió a la semana",
    "Se dañó al poco tiempo, mala calidad",
    "No funciona, llegó dañado",
    # sucio / viejo / incómodo
    "La habitación estaba muy sucia",
    "Todo sucio y en muy mal estado",
    "Sucio, viejo y descuidado",
    "Muy incómodo y de mal gusto",
    "Incómoda la habitación y sucia",
    # lento / tardísimo / demoraron
    "El servicio fue lentísimo",
    "Muy lento todo, perdí la mañana",
    "Frustrante de usar, muy lento",
    "Llegó tardísimo y mal empacado",
    "Tardísimo el envío, muy mal",
    "Se demoraron un mes en responder",
    "Demasiado lento, no lo recomiendo",
    # caro / no vale
    "Muy caro para lo poco que ofrece",
    "Demasiado caro y mala calidad",
    "No vale lo que cuesta, muy malo",
    "Carísimo y pésimo servicio",
    # grosero / antipático / mal trato
    "Personal antipático y desatento",
    "Muy groseros, muy mala atención",
    "Me trataron muy mal, muy groseros",
    "Atención grosera y muy lenta",
    # no respondieron / inexistente
    "Nunca respondieron mis mensajes",
    "Atención al cliente inexistente",
    "No responden, muy mal servicio",
    "Escribí mil veces y nadie responde",
    # confuso / aburrido / desactualizado
    "Confuso y muy mal explicado",
    "Explicaciones pobres y desordenadas",
    "Muy confuso, no se entiende nada",
    "Aburrido y sin contenido real",
    "El curso está desactualizado y flojo",
    "Muy flojo el contenido, no lo recomiendo",
    # inservible / errores / deficiente
    "Demasiados errores, inservible",
    "Inservible, no funciona nada bien",
    "Calidad deficiente y muy frágil",
    "Funciona mal, se cierra todo el tiempo",
    "Muy mal hecho, deficiente en todo",
    # frío / sin sabor
    "La comida estaba fría y sin sabor",
    "Comida fría y muy mala atención",
    "Sin sabor, muy mala la comida",
    # varios
    "Perdí mi dinero, no sirve para nada",
    "No sirve, no lo compren",
    "Una pérdida de tiempo total",
    "No recomiendo este lugar a nadie",
    "No lo recomiendo, muy mala experiencia",
    "El envío nunca llegó",
    "Nada que ver con las fotos",
    "Insoportable el ruido y el desorden",
    "Sinceramente lamentable, muy malo",
    "Lamentable la atención, nunca más",
    "Un fracaso, no lo compren",
    "Muy mala experiencia en general",
    "Todo mal, muy decepcionado",
    "Nunca más vuelvo, pésimo",
]


def cargar():
    """Devuelve (textos, etiquetas) listos para entrenar."""
    textos = POSITIVOS + NEGATIVOS
    etiquetas = ["POSITIVO"] * len(POSITIVOS) + ["NEGATIVO"] * len(NEGATIVOS)
    return textos, etiquetas
