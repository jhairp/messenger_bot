# =============================================
# RESPUESTAS FIJAS DEL BOT DE STREAMING
# Edita este archivo para personalizar el bot
# =============================================

RESPUESTAS = {
    # --- SALUDOS ---
    ("hola", "hello", "buenas", "buenos dias", "buenas tardes", "buenas noches", "ey", "hey"): 
        "Hola! Bienvenido a Streaming Free. Vendemos cuentas compartidas de Netflix, Disney+, Max y mas a precios increibles. Como te puedo ayudar?",

    # --- CATALOGO / SERVICIOS ---
    ("catalogo", "servicios", "que venden", "que tienen", "plataformas", "que ofrecen"):
        "Tenemos estas plataformas disponibles:\n\nNetflix - desde \$3/mes\nDisney+ - desde \$2/mes\nMax (HBO) - desde \$2.50/mes\nPrime Video - desde \$2/mes\nCrunchyroll - desde \$1.50/mes\n\nEscribe el nombre de la plataforma para mas detalles!",

    # --- NETFLIX ---
    ("netflix",):
        "Netflix compartido:\nPantalla 1: \$3/mes\nPantalla 2: \$5/mes\nAcceso inmediato, sin cortes. Escribe COMPRAR NETFLIX para adquirirlo.",

    # --- DISNEY ---
    ("disney", "disney+"):
        "Disney+ compartido:\nPantalla 1: \$2/mes\nInclye Disney, Marvel, Star Wars y mas. Escribe COMPRAR DISNEY para adquirirlo.",

    # --- MAX / HBO ---
    ("max", "hbo", "hbo max"):
        "Max (HBO) compartido:\nPantalla 1: \$2.50/mes\nSeries, peliculas y contenido HBO exclusivo. Escribe COMPRAR MAX para adquirirlo.",

    # --- PRECIOS ---
    ("precio", "precios", "cuanto cuesta", "cuanto vale", "costo", "tarifas"):
        "Nuestros precios:\nNetflix: desde \$3/mes\nDisney+: desde \$2/mes\nMax: desde \$2.50/mes\nPrime Video: desde \$2/mes\nCrunchyroll: desde \$1.50/mes\n\nTodos con garantia! Escribe GARANTIA para saber mas.",

    # --- COMPRAR ---
    ("comprar", "quiero comprar", "me interesa", "adquirir", "pedir"):
        "Para comprar sigue estos pasos:\n1. Dime que plataforma quieres\n2. Te damos los datos de pago\n3. Envias el comprobante\n4. Recibes tu cuenta en minutos!\n\nQue plataforma te interesa?",

    # --- PAGO ---
    ("pago", "como pago", "metodos de pago", "transferencia", "paypal", "binance"):
        "Aceptamos estos metodos de pago:\nPayPal\nBinance Pay\nTransferencia bancaria\nNequi / Daviplata (Colombia)\n\nEscribe COMPRAR para iniciar tu pedido!",

    # --- GARANTIA ---
    ("garantia", "garantias", "es seguro", "confiable"):
        "Si! Ofrecemos garantia completa:\nReposicion en menos de 24h si la cuenta falla\nSoporte todos los dias\nClientes satisfechos desde 2022\n\nEscribe COMPRAR para adquirir tu cuenta!",

    # --- TIEMPO DE ENTREGA ---
    ("cuando", "tiempo", "entrega", "rapido", "cuanto tarda"):
        "La entrega es INMEDIATA! En minutos recibes tus datos de acceso por este chat despues de confirmar tu pago.",

    # --- CONTACTO / HUMANO ---
    ("humano", "persona", "asesor", "agente", "hablar con alguien"):
        "Te comunico con un asesor humano ahora mismo. Por favor espera un momento o escribenos directamente a nuestro WhatsApp.",

    # --- DESPEDIDA ---
    ("adios", "bye", "hasta luego", "chao", "gracias"):
        "Gracias por contactarnos! Si necesitas algo mas, aqui estamos. Que disfrutes tu streaming!",
}

# Respuesta cuando no se entiende el mensaje (antes de usar IA)
RESPUESTA_DEFAULT = "No entendi bien tu pregunta. Puedes preguntarme sobre:\nPrecios, Catalogo, Como comprar, Garantia, o el nombre de una plataforma (Netflix, Disney+, etc.)"
